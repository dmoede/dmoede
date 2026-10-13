# Customer Email Intel: Outlook → Copilot → Notion

Every morning, the last day of customer email is analyzed by Copilot and lands in a
Notion database as one row per email. Each row has the customer, category, sentiment,
urgency, a summary, the customer's asks, action items, commitments already made,
risk signals, and a suggested next step.

The CX team then works from one Notion view ("Needs Response", "At Risk",
"P1/P2 this week") instead of from individual inboxes.

```
 Outlook inbox ──► Power Automate (daily 6 AM)
                     │  filter to customer domains
                     │  Copilot prompt ("Run a prompt") → structured JSON
                     ├──► OneDrive: exports/YYYY-MM-DD.json   (daily export / audit trail)
                     └──► Notion API → "Customer Email Intel" database
                                         (Option A: in the flow)
                                         (Option B: scripts/import_to_notion.py)
```

## Why this design
Copilot in Outlook (the chat pane) can't run on a schedule or export results.
The automatable form of Copilot is a **prompt** run from Power Automate
(AI Builder "Run a prompt" / Copilot Studio prompt builder). That's what this uses.
It stays inside your Microsoft 365 tenant until the final write to Notion.

## What's in this folder
| Path | Purpose |
|---|---|
| `prompt/copilot-email-analysis-prompt.md` | The Copilot prompt: inputs, instructions, categories |
| `prompt/output-schema.json` | The JSON format Copilot must return (also the Parse JSON sample) |
| `power-automate/flow-build-guide.md` | Step-by-step build of the daily flow, with every expression |
| `scripts/create_notion_database.py` | One-time: creates the Notion database with the right properties |
| `scripts/import_to_notion.py` | Option B importer: loads daily export JSON into Notion, skipping duplicates |
| `scripts/notion_schema.py` | The single source of truth for Notion properties and field mapping |
| `samples/sample-export.json` | Example export for testing |

## Prerequisites (check these first)
1. **Power Automate with AI Builder prompts.** "Run a prompt" uses AI Builder credits.
   Confirm with IT which licenses/credits Entegrata has (M365 Copilot, Copilot Studio, or AI Builder capacity).
2. **Option A only: the premium HTTP connector** (Power Automate Premium license) to call the Notion API.
   No premium? Use Option B.
3. **Notion internal integration:** notion.so/profile/integrations → New integration →
   copy the token. Content capabilities: Read, Insert, Update.
4. **IT/security sign-off.** This copies summaries of customer email into Notion.
   Keep the database in a restricted teamspace, and store no full email bodies (the design already
   stores summaries plus a link back to Outlook).

## Setup
1. **Create the Copilot prompt.** Follow `prompt/copilot-email-analysis-prompt.md`.
   Test it on 3–5 real emails in the prompt builder before wiring up the flow.
2. **Create the Notion database.**
   ```bash
   cd customer-email-intel
   pip install -r requirements.txt
   export NOTION_TOKEN=secret_...
   python scripts/create_notion_database.py "<URL of the Notion page to put it under>"
   ```
   Connect the integration to that parent page first (page ••• → Connections).
   Note the printed `NOTION_DATABASE_ID`.
3. **Build the flow.** Follow `power-automate/flow-build-guide.md`.
4. **Pick how rows get into Notion:**
   - **Option A (recommended):** the flow writes to Notion directly (steps 6f–6i of the guide).
     Nothing else to run.
   - **Option B (no premium connector):** the flow only writes the daily JSON export.
     On a machine that syncs that OneDrive folder, schedule:
     ```bash
     NOTION_TOKEN=... NOTION_DATABASE_ID=... \
       python scripts/import_to_notion.py "~/OneDrive - Entegrata/Customer Email Intel/exports"
     ```
     daily after the flow runs (Windows Task Scheduler or cron). Re-running is safe; duplicates are skipped.
5. **Create the team views in Notion:**
   - *Needs Response*: Needs Response = checked, Status = New, sorted by Urgency
   - *At Risk*: Sentiment = At Risk, or Risk Signals is not empty
   - *By Customer*: Board grouped by Customer
   - *This Week*: Received within the past week, grouped by Category

## Test without touching Notion
```bash
python scripts/import_to_notion.py samples/sample-export.json --dry-run
```
Prints the exact Notion properties each record would produce.

## Tuning
- **Categories, sentiment, urgency:** edit them in **both** `prompt/copilot-email-analysis-prompt.md`
  and `scripts/notion_schema.py` (and the Notion select options) so they stay in sync.
- **Noise:** tighten the `CustomerDomains` allowlist in the flow.
- **Volume:** raise "Top" in "Get emails (V3)" if more than 250 emails arrive in a day.
- **Shared mailboxes** (for example support@): swap "Get emails (V3)" for "Get emails from a shared mailbox (V2)".
