"""Import a daily Customer Email Intel export (JSON) into Notion.

Usage:
    export NOTION_TOKEN=secret_...
    export NOTION_DATABASE_ID=...
    python import_to_notion.py <export.json | folder> [--dry-run]

Given a folder, imports every *.json file in it. Safe to re-run: a record is
skipped when a page with the same Message ID already exists.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

import requests

from notion_schema import NOTION_API, NOTION_VERSION, record_to_properties

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)


class Notion:
    def __init__(self, token, database_id):
        self.database_id = database_id
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}", "Notion-Version": NOTION_VERSION})

    def _request(self, method, path, body):
        for attempt in range(5):
            resp = self.session.request(method, f"{NOTION_API}{path}", json=body, timeout=30)
            if resp.status_code == 429 or resp.status_code >= 500:
                time.sleep(float(resp.headers.get("Retry-After", 2 ** attempt)))
                continue
            if not resp.ok:
                raise RuntimeError(f"Notion error {resp.status_code}: {resp.text}")
            return resp.json()
        raise RuntimeError(f"Notion kept failing on {method} {path}")

    def exists(self, message_id):
        result = self._request(
            "POST",
            f"/databases/{self.database_id}/query",
            {"filter": {"property": "Message ID", "rich_text": {"equals": message_id}}, "page_size": 1},
        )
        return bool(result["results"])

    def create(self, properties):
        return self._request("POST", "/pages", {"parent": {"database_id": self.database_id}, "properties": properties})


def load_records(path):
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8-sig"))
        for record in data if isinstance(data, list) else data.get("records", []):
            yield f.name, record


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry_run = "--dry-run" in sys.argv
    if len(args) != 1:
        sys.exit(__doc__)

    notion = None
    if not dry_run:
        token = os.environ.get("NOTION_TOKEN") or sys.exit("Set NOTION_TOKEN first.")
        database_id = os.environ.get("NOTION_DATABASE_ID") or sys.exit("Set NOTION_DATABASE_ID first.")
        notion = Notion(token, database_id)

    created = skipped = failed = 0
    for source, record in load_records(Path(args[0])):
        message_id = record.get("message_id")
        label = f"{source}: {record.get('subject', '(no subject)')}"
        try:
            properties = record_to_properties(record)
            if dry_run:
                print(json.dumps(properties, indent=2))
                created += 1
            elif message_id and notion.exists(message_id):
                skipped += 1
            else:
                notion.create(properties)
                created += 1
                log.info("Imported %s", label)
        except Exception as exc:  # keep going; one bad record shouldn't block the day
            failed += 1
            log.error("Failed %s: %s", label, exc)

    log.info("Done. created=%d skipped_duplicates=%d failed=%d", created, skipped, failed)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
