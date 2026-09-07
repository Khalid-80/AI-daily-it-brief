#!/usr/bin/env python3
"""
AI Daily IT Intelligence Brief — free / open-source pipeline
=============================================================

Stages (mirrors the original Power Automate design 1:1):
  1. COLLECT   -> pull trusted public RSS feeds
  2. PREPARE   -> filter to the lookback window, dedupe, clean text
  3. ANALYZE   -> ask an open-source LLM (served via Groq's free API) to
                  classify/prioritize/explain each item as strict JSON
  4. FORMAT    -> build a Teams-ready message
  5. PUBLISH   -> POST to a Teams "Workflows" incoming webhook

Steps 1-4 run in the "build" GitHub Actions job (no secrets needed except
the Groq key). Step 5 runs in a separate "publish" job gated behind a
GitHub Environment that requires manual approval — that manual approval
*is* the human-review-before-publish control from the original design.

Nothing here talks to company systems, changes configuration, or takes
any remediation action. It only reads public RSS and posts a text
summary. Advisory only.
"""

from __future__ import annotations

import html
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "feeds.json"
BRIEF_JSON_PATH = ROOT / "brief.json"
BRIEF_TEXT_PATH = ROOT / "brief.md"

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# Any current free/open-weight model Groq hosts works here (Llama, Qwen, etc).
# Kept as an env var so you can swap models without touching code.
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")

ALLOWED_PRIORITIES = {"Critical", "High", "Medium", "Information"}
ALLOWED_CATEGORIES = {"Security", "Microsoft 365", "Windows", "Vendor"}

SYSTEM_PROMPT = """You are an IT intelligence analyst. You will be given a JSON array of
recent public IT/security news items (title, summary, publishedAt, source, url).

For EACH item, produce one object with exactly these fields:
  headline, category, priority, summary, whyItMatters, recommendedAction, sourceUrl

Rules:
- category must be one of: Security, Microsoft 365, Windows, Vendor
- priority must be one of: Critical, High, Medium, Information
- Use ONLY the information supplied. Never invent facts, numbers, or details
  not present in the input.
- If an item's input is too thin to summarize responsibly, still return it with
  priority "Information" and note in whyItMatters that it needs human review.
- sourceUrl must be copied exactly from the input url field, unchanged.
- summary: 1-2 sentences. whyItMatters: 1 sentence. recommendedAction: 1 short sentence.

Respond with ONLY a JSON array of these objects — no prose, no markdown fences,
no commentary before or after.
"""


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_text(raw: str) -> str:
    """Strip HTML tags/entities and collapse whitespace."""
    text = html.unescape(raw or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def collect_items(config: dict) -> list[dict]:
    """Stage 1 + 2: COLLECT & PREPARE."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=config["lookback_hours"])
    max_chars = config["max_summary_chars"]

    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    items: list[dict] = []

    for feed in config["feeds"]:
        url = feed["url"]
        if "REPLACE_WITH" in url:
            print(f"[skip] placeholder feed not configured: {feed['name']}", file=sys.stderr)
            continue
        try:
            parsed = feedparser.parse(url)
        except Exception as e:  # noqa: BLE001 - log and keep going, one bad feed shouldn't kill the run
            print(f"[error] failed to fetch {feed['name']}: {e}", file=sys.stderr)
            continue

        for entry in parsed.entries:
            link = getattr(entry, "link", "").strip()
            title = clean_text(getattr(entry, "title", ""))
            if not link or not title:
                continue  # quality check: require title + source link

            # time window check
            published_struct = getattr(entry, "published_parsed", None) or getattr(
                entry, "updated_parsed", None
            )
            if published_struct:
                published_dt = datetime(*published_struct[:6], tzinfo=timezone.utc)
                if published_dt < cutoff:
                    continue
                published_iso = published_dt.isoformat()
            else:
                # no date available; keep it but flag "now" so it isn't silently dropped
                published_iso = datetime.now(timezone.utc).isoformat()

            # duplicate check: URL first, then title, keep newest (feeds are newest-first)
            dedupe_key = link if link not in seen_urls else None
            if link in seen_urls or title.lower() in seen_titles:
                continue
            seen_urls.add(link)
            seen_titles.add(title.lower())

            summary = clean_text(getattr(entry, "summary", "") or getattr(entry, "description", ""))
            if len(summary) > max_chars:
                summary = summary[:max_chars].rsplit(" ", 1)[0] + "…"

            items.append(
                {
                    "title": title,
                    "summary": summary,
                    "publishedAt": published_iso,
                    "source": feed["name"],
                    "url": link,
                }
            )

    # newest first, capped
    items.sort(key=lambda x: x["publishedAt"], reverse=True)
    return items[: config["max_items"]]


def analyze_items(items: list[dict], api_key: str) -> list[dict]:
    """Stage 3: ANALYZE via an open-source model hosted on Groq's free tier."""
    if not items:
        return []

    payload = {
        "model": GROQ_MODEL,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Return a JSON object with a single key \"items\" whose value is "
                    "the array described in your instructions. Input items:\n\n"
                    + json.dumps(items, ensure_ascii=False)
                ),
            },
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]

    parsed = json.loads(content)
    analyzed = parsed["items"] if isinstance(parsed, dict) else parsed

    # Guardrail: validate the model didn't invent a sourceUrl or drift outside
    # the allowed enums. Anything invalid gets flagged for human review instead
    # of silently trusting the model.
    valid_urls = {i["url"] for i in items}
    cleaned = []
    for entry in analyzed:
        if entry.get("sourceUrl") not in valid_urls:
            entry["priority"] = "Information"
            entry["whyItMatters"] = (entry.get("whyItMatters", "") + " [Flagged: source URL mismatch — needs human review]").strip()
        if entry.get("category") not in ALLOWED_CATEGORIES:
            entry["category"] = "Vendor"
        if entry.get("priority") not in ALLOWED_PRIORITIES:
            entry["priority"] = "Information"
        cleaned.append(entry)
    return cleaned


PRIORITY_EMOJI = {
    "Critical": "🔴",
    "High": "🟠",
    "Medium": "🟡",
    "Information": "🔵",
}


def format_brief(analyzed: list[dict]) -> str:
    """Stage 4: FORMAT — build the Teams-ready text."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if not analyzed:
        return f"**AI Daily IT Intelligence Brief — {today}**\n\nNo new items in the review window."

    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Information": 3}
    analyzed.sort(key=lambda x: priority_order.get(x.get("priority"), 9))

    lines = [f"**AI Daily IT Intelligence Brief — {today}**", ""]
    for item in analyzed:
        emoji = PRIORITY_EMOJI.get(item.get("priority"), "⚪")
        lines.append(f"{emoji} **[{item.get('category')} / {item.get('priority')}] {item.get('headline')}**")
        lines.append(item.get("summary", ""))
        lines.append(f"_Why it matters:_ {item.get('whyItMatters', '')}")
        lines.append(f"_Suggested action:_ {item.get('recommendedAction', '')}")
        lines.append(f"[Source]({item.get('sourceUrl')})")
        lines.append("")

    lines.append("_Advisory only — no automatic changes were made to any system._")
    return "\n".join(lines)


def main() -> None:
    config = load_config()
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("GROQ_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)

    items = collect_items(config)
    print(f"[info] collected {len(items)} item(s) after filtering/dedup", file=sys.stderr)

    if items:
        analyzed = analyze_items(items, api_key)
    else:
        analyzed = []

    brief_text = format_brief(analyzed)

    BRIEF_JSON_PATH.write_text(json.dumps(analyzed, ensure_ascii=False, indent=2), encoding="utf-8")
    BRIEF_TEXT_PATH.write_text(brief_text, encoding="utf-8")
    print(f"[info] wrote {BRIEF_JSON_PATH.name} and {BRIEF_TEXT_PATH.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
