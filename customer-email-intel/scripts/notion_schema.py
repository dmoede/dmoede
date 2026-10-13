"""Notion database schema and record -> page-properties mapping.

Shared by create_notion_database.py and import_to_notion.py so the database
and the importer can never drift apart.
"""

NOTION_VERSION = "2022-06-28"
NOTION_API = "https://api.notion.com/v1"
RICH_TEXT_LIMIT = 2000  # Notion rejects rich_text items longer than this

CATEGORIES = [
    ("Support Issue", "red"),
    ("Feature Request", "purple"),
    ("Implementation / Onboarding", "blue"),
    ("Data / Integration", "orange"),
    ("Billing / Commercial", "yellow"),
    ("Renewal / Expansion", "green"),
    ("Escalation", "red"),
    ("Relationship / General", "gray"),
    ("Praise", "green"),
]
SENTIMENTS = [("Positive", "green"), ("Neutral", "gray"), ("Negative", "orange"), ("At Risk", "red")]
URGENCIES = [("P1 - Critical", "red"), ("P2 - High", "orange"), ("P3 - Normal", "blue"), ("P4 - Low", "gray")]
DIRECTIONS = [("Inbound", "blue"), ("Outbound", "gray")]
STATUSES = [("New", "blue"), ("Reviewed", "yellow"), ("Actioned", "green"), ("No Action Needed", "gray")]


def _select(options):
    return {"select": {"options": [{"name": n, "color": c} for n, c in options]}}


DATABASE_PROPERTIES = {
    "Subject": {"title": {}},
    "Customer": {"select": {"options": []}},
    "Contact": {"rich_text": {}},
    "Contact Email": {"email": {}},
    "Received": {"date": {}},
    "Direction": _select(DIRECTIONS),
    "Category": _select(CATEGORIES),
    "Sentiment": _select(SENTIMENTS),
    "Urgency": _select(URGENCIES),
    "Needs Response": {"checkbox": {}},
    "Status": _select(STATUSES),
    "Summary": {"rich_text": {}},
    "Customer Asks": {"rich_text": {}},
    "Action Items": {"rich_text": {}},
    "Commitments Made": {"rich_text": {}},
    "Risk Signals": {"rich_text": {}},
    "Products Mentioned": {"multi_select": {"options": []}},
    "Suggested Next Step": {"rich_text": {}},
    "Outlook Link": {"url": {}},
    "Conversation ID": {"rich_text": {}},
    "Message ID": {"rich_text": {}},
}


def _text(value):
    value = (value or "").strip()
    return {"rich_text": [{"text": {"content": value[:RICH_TEXT_LIMIT]}}] if value else []}


def _bullets(items):
    return _text("\n".join(f"• {i}" for i in items or [] if i))


def _action_items(items):
    lines = []
    for item in items or []:
        if isinstance(item, str):
            lines.append(item)
            continue
        line = item.get("task", "")
        extras = [x for x in (item.get("owner"), item.get("due_date") and f"due {item['due_date']}") if x]
        if extras:
            line += f" ({', '.join(extras)})"
        lines.append(line)
    return _bullets(lines)


def _choice(value, options):
    """Select value, or None if Copilot returned something off-list."""
    names = {n for n, _ in options}
    return {"select": {"name": value}} if value in names else {"select": None}


def record_to_properties(record):
    """Map one export record (see samples/sample-export.json) to Notion properties."""
    a = record.get("analysis", {})
    # Notion multi-select option names cannot contain commas.
    products = [p.replace(",", " ")[:100] for p in a.get("products_mentioned") or [] if p]
    props = {
        "Subject": {"title": [{"text": {"content": (record.get("subject") or "(no subject)")[:RICH_TEXT_LIMIT]}}]},
        "Customer": {"select": {"name": a["customer_account"].replace(",", " ")[:100]}}
        if a.get("customer_account")
        else {"select": None},
        "Contact": _text(a.get("contact_name")),
        "Contact Email": {"email": a.get("contact_email") or None},
        "Received": {"date": {"start": record["received_at"]}} if record.get("received_at") else {"date": None},
        "Direction": _choice(a.get("direction"), DIRECTIONS),
        "Category": _choice(a.get("category"), CATEGORIES),
        "Sentiment": _choice(a.get("sentiment"), SENTIMENTS),
        "Urgency": _choice(a.get("urgency"), URGENCIES),
        "Needs Response": {"checkbox": bool(a.get("needs_response"))},
        "Status": {"select": {"name": "New"}},
        "Summary": _text(a.get("summary")),
        "Customer Asks": _bullets(a.get("customer_asks")),
        "Action Items": _action_items(a.get("action_items")),
        "Commitments Made": _bullets(a.get("commitments_made")),
        "Risk Signals": _bullets(a.get("risk_signals")),
        "Products Mentioned": {"multi_select": [{"name": p} for p in dict.fromkeys(products)]},
        "Suggested Next Step": _text(a.get("suggested_next_step")),
        "Outlook Link": {"url": record.get("outlook_link") or None},
        "Conversation ID": _text(record.get("conversation_id")),
        "Message ID": _text(record.get("message_id")),
    }
    return props
