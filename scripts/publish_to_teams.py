#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
BRIEF_TEXT_PATH = ROOT / "brief.md"

TEXT_FIELD_NAME = "text"


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
