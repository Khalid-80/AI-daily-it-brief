#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
BRIEF_JSON_PATH = ROOT / "brief.json"

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


if __name__ == "__main__":
    main()
