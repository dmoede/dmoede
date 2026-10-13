"""One-time setup: create the "Customer Email Intel" database in Notion.

Usage:
    export NOTION_TOKEN=secret_...            # internal integration token
    python create_notion_database.py <parent-page-id-or-url>

The parent page must be shared with the integration (page ... menu ->
Connections -> add your integration). Prints the new database ID; put it in
NOTION_DATABASE_ID for the importer and in the Power Automate flow.
"""

import os
import re
import sys

import requests

from notion_schema import DATABASE_PROPERTIES, NOTION_API, NOTION_VERSION


def page_id_from(arg):
    match = re.search(r"([0-9a-f]{32})", arg.replace("-", ""))
    if not match:
        sys.exit(f"Could not find a Notion page ID in: {arg}")
    return match.group(1)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    token = os.environ.get("NOTION_TOKEN") or sys.exit("Set NOTION_TOKEN first.")
    resp = requests.post(
        f"{NOTION_API}/databases",
        headers={"Authorization": f"Bearer {token}", "Notion-Version": NOTION_VERSION},
        json={
            "parent": {"type": "page_id", "page_id": page_id_from(sys.argv[1])},
            "icon": {"type": "emoji", "emoji": "📬"},
            "title": [{"text": {"content": "Customer Email Intel"}}],
            "properties": DATABASE_PROPERTIES,
        },
        timeout=30,
    )
    if not resp.ok:
        sys.exit(f"Notion error {resp.status_code}: {resp.text}")
    db = resp.json()
    print(f"Created database: {db['url']}")
    print(f"NOTION_DATABASE_ID={db['id']}")


if __name__ == "__main__":
    main()
