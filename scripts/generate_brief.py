#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "feeds.json"
BRIEF_JSON_PATH = ROOT / "brief.json"
BRIEF_TEXT_PATH = ROOT / "brief.md"

FEED_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; AI-Daily-IT-Brief/1.0; "
        "+https://github.com/) AI-Daily-IT-Brief-RSS-Reader"
    )
}

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
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
    text = html.unescape(raw or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def collect_items(config: dict) -> list[dict]:
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
            resp = requests.get(url, headers=FEED_REQUEST_HEADERS, timeout=20, allow_redirects=True)
            if resp.status_code != 200:
                print(f"[error] {feed['name']}: HTTP {resp.status_code}", file=sys.stderr)
                continue
            parsed = feedparser.parse(resp.content)
