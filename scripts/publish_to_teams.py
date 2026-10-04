#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
BRIEF_JSON_PATH = ROOT / "brief.json"
HISTORY_PATH = ROOT / "history.json"
HISTORY_RETENTION_DAYS = 14

PRIORITY_EMOJI = {
    "Critical": "🔴",
    "High": "🟠",
    "Medium": "🟡",
    "Information": "🔵",
}


def build_adaptive_card(items):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    body = [
        {
            "type": "TextBlock",
            "text": f"AI Daily IT Intelligence Brief — {today}",
            "wrap": True,
            "size": "Large",
            "weight": "Bolder",
        }
    ]

    if not items:
        body.append(
            {"type": "TextBlock", "text": "No new items in the review window.", "wrap": True}
        )
    else:
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Information": 3}
        items = sorted(items, key=lambda x: priority_order.get(x.get("priority"), 9))
        for item in items:
            emoji = PRIORITY_EMOJI.get(item.get("priority"), "⚪")
            body.append(
                {
                    "type": "TextBlock",
                    "text": f"{emoji} [{item.get('category')} / {item.get('priority')}] {item.get('headline')}",
                    "wrap": True,
                    "weight": "Bolder",
                    "spacing": "Medium",
                }
            )
            body.append({"type": "TextBlock", "text": item.get("summary", ""), "wrap": True})
            body.append(
                {
                    "type": "TextBlock",
                    "text": f"Why it matters: {item.get('whyItMatters', '')}",
                    "wrap": True,
                    "isSubtle": True,
                    "size": "Small",
                }
            )
            body.append(
                {
                    "type": "TextBlock",
                    "text": f"Suggested action: {item.get('recommendedAction', '')}",
                    "wrap": True,
                    "isSubtle": True,
                    "size": "Small",
                }
            )
            body.append(
                {
                    "type": "TextBlock",
                    "text": f"[Source]({item.get('sourceUrl')})",
                    "wrap": True,
                    "size": "Small",
                }
            )

    body.append(
        {
            "type": "TextBlock",
            "text": "Advisory only — no automatic changes were made to any system.",
            "wrap": True,
            "isSubtle": True,
            "size": "Small",
            "spacing": "Medium",
        }
    )

    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": body,
                },
            }
        ],
    }


def update_history(items):
    """Record today's published URLs so tomorrow's run won't repeat them,
    even if they're still inside the RSS lookback window."""
    today = datetime.now(timezone.utc).date().isoformat()

    existing = []
    if HISTORY_PATH.exists():
        try:
            existing = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        except Exception:
            existing = []

    cutoff = datetime.now(timezone.utc) - timedelta(days=HISTORY_RETENTION_DAYS)
    kept = []
    for e in existing:
        try:
            if datetime.fromisoformat(e["published_date"]) >= cutoff:
                kept.append(e)
        except Exception:
            continue

    for item in items:
        url = item.get("sourceUrl")
        if url:
            kept.append({"url": url, "published_date": today})

    HISTORY_PATH.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[info] history.json updated ({len(kept)} entries retained)", file=sys.stderr)


def main():
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        print("TEAMS_WEBHOOK_URL environment variable is required.", file=sys.stderr)
        sys.exit(1)

    if not BRIEF_JSON_PATH.exists():
        print("brief.json not found — run generate_brief.py first.", file=sys.stderr)
        sys.exit(1)

    items = json.loads(BRIEF_JSON_PATH.read_text(encoding="utf-8"))
    payload = build_adaptive_card(items)

    resp = requests.post(webhook_url, json=payload, timeout=30)
    if resp.status_code >= 300:
        print(f"[error] Teams webhook returned {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    print("[info] brief published to Teams", file=sys.stderr)

    update_history(items)


if __name__ == "__main__":
    main()
