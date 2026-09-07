#!/usr/bin/env python3
"""
Stage 5: PUBLISH — posts brief.md to a Microsoft Teams "Workflows" webhook.

This is deliberately a separate, tiny script so it can run as its own
GitHub Actions job, gated behind an Environment that requires a human
approver. That approval step is the "human review before publish" gate
from the original design — nothing here posts automatically without it.

Note on payload shape: the modern Teams "Workflows" webhook (the
replacement for the retired Office 365 Connector / Incoming Webhook) is
backed by a Power Automate flow you create from the built-in template
"Post to a channel when a webhook request is received". That template's
default schema expects a JSON body shaped like {"text": "..."}. If you
customize the flow's trigger schema, update TEXT_FIELD_NAME below to match.
"""

import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
BRIEF_TEXT_PATH = ROOT / "brief.md"

TEXT_FIELD_NAME = "text"  # match this to your Teams Workflow trigger schema


def main() -> None:
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        print("TEAMS_WEBHOOK_URL environment variable is required.", file=sys.stderr)
        sys.exit(1)

    if not BRIEF_TEXT_PATH.exists():
        print("brief.md not found — run generate_brief.py first.", file=sys.stderr)
        sys.exit(1)

    brief_text = BRIEF_TEXT_PATH.read_text(encoding="utf-8")

    resp = requests.post(webhook_url, json={TEXT_FIELD_NAME: brief_text}, timeout=30)
    if resp.status_code >= 300:
        print(f"[error] Teams webhook returned {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    print("[info] brief published to Teams", file=sys.stderr)


if __name__ == "__main__":
    main()
