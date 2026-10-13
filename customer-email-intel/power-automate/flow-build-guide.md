# Power Automate build guide: "Customer Email Intel – Daily"

This is one scheduled cloud flow. Once a day it:

1. pulls the last day of Outlook email from customer domains,
2. runs each email through the Copilot prompt (`../prompt/`),
3. saves the day's results as a JSON export in OneDrive, and
4. creates one row per email in the Notion database (Option A).

Build it at **make.powerautomate.com → Create → Scheduled cloud flow**.
Action names in quotes below must match exactly, because later expressions refer to them.
If you rename an action, update the expressions too.

> **Before you start:** create the Copilot prompt (`../prompt/copilot-email-analysis-prompt.md`)
> and the Notion database (see the main README, step 2).

---

## 1. Trigger: "Recurrence"
- Interval: `1`, Frequency: `Day`
- Time zone: your time zone. At times: `6` (runs at 6:00 AM, so the summary is ready before the day starts)

## 2. "Initialize CustomerDomains" (Initialize variable)
- Name: `CustomerDomains` · Type: **Array**
- Value: your customer email domains, lower case, for example:
  ```json
  ["examplelaw.com", "samplepartners.com"]
  ```
  An allowlist keeps vendor, newsletter, and internal email out of the database.
  Keep it in sync with your customer list. You can move it to a SharePoint list later.

## 3. "Initialize Results" (Initialize variable)
- Name: `Results` · Type: **Array** · Value: `[]`

## 4. "Get emails (V3)" (Office 365 Outlook)
- Folder: `Inbox` · Top: `250` · Include Attachments: `No` · Fetch Only Unread: `No`
- To also capture outbound email, add a second "Get emails (V3)" on `Sent Items` and `union()` the two `value` arrays in step 5.

## 5. "Filter customer emails" (Data Operation → Filter array)
- From: `@body('Get_emails_(V3)')?['value']`
- Click **Edit in advanced mode** and paste:
  ```
  @and(
    greaterOrEquals(item()?['receivedDateTime'], addHours(utcNow(), -25)),
    contains(variables('CustomerDomains'), toLower(last(split(item()?['from'], '@'))))
  )
  ```
  The 25-hour window overlaps the previous run by an hour, so nothing slips through
  if the flow starts late. The Notion duplicate check in step 6g ignores the overlap.

## 6. "Apply to each email" (Control → Apply to each)
- Select an output: `@body('Filter_customer_emails')`
- **Settings → Concurrency control: On, Degree of parallelism: 1** (needed for "Append to array variable")

Inside the loop:

### 6a. "Html to text" (Content Conversion)
- Content: `@items('Apply_to_each_email')?['body']`

### 6b. "Run a prompt" (AI Builder)
- Prompt: **Customer Email Analysis**
- Set the inputs:
  - EmailSubject: `@items('Apply_to_each_email')?['subject']`
  - EmailFrom: `@items('Apply_to_each_email')?['from']`
  - EmailTo: `@items('Apply_to_each_email')?['toRecipients']`
  - ReceivedDate: `@items('Apply_to_each_email')?['receivedDateTime']`
  - EmailBody (expression; caps very long threads at 12,000 characters):
    ```
    substring(body('Html_to_text'), 0, min(length(body('Html_to_text')), 12000))
    ```

### 6c. "Parse analysis" (Data Operation → Parse JSON)
- Content: the prompt's **Text** output from the dynamic content picker.
  If the picker only shows the full response, use the expression
  `outputs('Run_a_prompt')?['body/responsev2/predictionOutput/text']`.
- Schema: **Generate from sample** and paste `../prompt/output-schema.json`.
  Then, in the generated schema, remove the `"required"` arrays, so one missing field doesn't fail the run.

### 6d. "Build record" (Data Operation → Compose)
Switch the input to code view and paste:
```json
{
  "message_id": "@{items('Apply_to_each_email')?['id']}",
  "conversation_id": "@{items('Apply_to_each_email')?['conversationId']}",
  "subject": "@{items('Apply_to_each_email')?['subject']}",
  "received_at": "@{items('Apply_to_each_email')?['receivedDateTime']}",
  "outlook_link": "https://outlook.office365.com/owa/?ItemID=@{encodeUriComponent(items('Apply_to_each_email')?['id'])}&exvsurl=1&viewmodel=ReadMessageItem",
  "analysis": "@body('Parse_analysis')"
}
```
(`"@body(...)"` with no braces inserts the parsed object itself, not a string.)

### 6e. "Append to Results" (Variables → Append to array variable)
- Name: `Results` · Value: `@outputs('Build_record')`

> **Stop here for Option B.** If you will import into Notion with the Python script,
> skip 6f–6i and go to step 7.

### 6f. Notion helper "Select" actions (Data Operation → Select)
"Select products":
- From: `@body('Parse_analysis')?['products_mentioned']`
- Map (key/value mode): key `name`, value `@item()`

"Select action items":
- From: `@body('Parse_analysis')?['action_items']`
- Map (switch to text mode):
  `@concat(item()?['task'], if(empty(item()?['due_date']), '', concat(' (due ', item()?['due_date'], ')')))`

### 6g. "Check Notion for duplicate" (HTTP, premium)
- Method: `POST`
- URI: `https://api.notion.com/v1/databases/<NOTION_DATABASE_ID>/query`
- Headers:
  - `Authorization`: `Bearer <NOTION_TOKEN>`
  - `Notion-Version`: `2022-06-28`
  - `Content-Type`: `application/json`
- Body:
  ```json
  {
    "filter": { "property": "Message ID", "rich_text": { "equals": "@{items('Apply_to_each_email')?['id']}" } },
    "page_size": 1
  }
  ```
- In **Settings**, turn on **Secure inputs** so the token is hidden in run history.

### 6h. "Is new email?" (Condition)
- `@length(body('Check_Notion_for_duplicate')?['results'])` **is equal to** `0`

### 6i. If yes → "Create Notion page" (HTTP)
Same URI host, headers, and Secure inputs as 6g, but:
- Method: `POST` · URI: `https://api.notion.com/v1/pages`
- Body (code view):

```json
{
  "parent": { "database_id": "<NOTION_DATABASE_ID>" },
  "properties": {
    "Subject": { "title": [ { "text": { "content": "@{items('Apply_to_each_email')?['subject']}" } } ] },
    "Customer": { "select": "@if(empty(body('Parse_analysis')?['customer_account']), null, setProperty(json('{}'), 'name', replace(body('Parse_analysis')?['customer_account'], ',', ' ')))" },
    "Contact": { "rich_text": [ { "text": { "content": "@{body('Parse_analysis')?['contact_name']}" } } ] },
    "Contact Email": { "email": "@if(empty(body('Parse_analysis')?['contact_email']), null, body('Parse_analysis')?['contact_email'])" },
    "Received": { "date": { "start": "@{items('Apply_to_each_email')?['receivedDateTime']}" } },
    "Direction": { "select": { "name": "@{body('Parse_analysis')?['direction']}" } },
    "Category": { "select": { "name": "@{body('Parse_analysis')?['category']}" } },
    "Sentiment": { "select": { "name": "@{body('Parse_analysis')?['sentiment']}" } },
    "Urgency": { "select": { "name": "@{body('Parse_analysis')?['urgency']}" } },
    "Needs Response": { "checkbox": "@equals(body('Parse_analysis')?['needs_response'], true)" },
    "Status": { "select": { "name": "New" } },
    "Summary": { "rich_text": [ { "text": { "content": "@{body('Parse_analysis')?['summary']}" } } ] },
    "Customer Asks": { "rich_text": [ { "text": { "content": "@{join(body('Parse_analysis')?['customer_asks'], decodeUriComponent('%0A'))}" } } ] },
    "Action Items": { "rich_text": [ { "text": { "content": "@{join(body('Select_action_items'), decodeUriComponent('%0A'))}" } } ] },
    "Commitments Made": { "rich_text": [ { "text": { "content": "@{join(body('Parse_analysis')?['commitments_made'], decodeUriComponent('%0A'))}" } } ] },
    "Risk Signals": { "rich_text": [ { "text": { "content": "@{join(body('Parse_analysis')?['risk_signals'], decodeUriComponent('%0A'))}" } } ] },
    "Products Mentioned": { "multi_select": "@body('Select_products')" },
    "Suggested Next Step": { "rich_text": [ { "text": { "content": "@{body('Parse_analysis')?['suggested_next_step']}" } } ] },
    "Outlook Link": { "url": "https://outlook.office365.com/owa/?ItemID=@{encodeUriComponent(items('Apply_to_each_email')?['id'])}&exvsurl=1&viewmodel=ReadMessageItem" },
    "Conversation ID": { "rich_text": [ { "text": { "content": "@{items('Apply_to_each_email')?['conversationId']}" } } ] },
    "Message ID": { "rich_text": [ { "text": { "content": "@{items('Apply_to_each_email')?['id']}" } } ] }
  }
}
```

If no is the result, leave the branch empty (the email is already in Notion).

If one email fails (for example, a bad Notion value), the loop still processes
the rest and the run is marked Failed, so you'll see it in run history.
Turn on failure alerts in the flow's details page to get an email when that happens.

## 7. "Save daily export" (OneDrive for Business → Create file)
Add this **after** the loop, not inside it.
- Folder Path: `/Customer Email Intel/exports`
- File Name: `@{formatDateTime(utcNow(), 'yyyy-MM-dd')}.json`
- File Content: `@{variables('Results')}`
- *Settings → Run after:* tick **is successful** and **has failed**, so the export is saved even if one Notion write failed.

This file is your daily export and audit trail. Option B imports it into Notion.
It also lets you backfill: re-run `import_to_notion.py` on old exports at any time.

---

## Test it
1. Put one or two of your own customer domains in `CustomerDomains`.
2. **Test → Manually** and watch the run.
3. Check the JSON file in OneDrive and the new rows in Notion.
4. Run it a second time. No duplicate rows should appear.

## Troubleshooting
| Symptom | Fix |
|---|---|
| Parse JSON fails | The prompt returned extra text. Make sure the prompt's output is set to **JSON**. |
| Notion `400 validation_error` on a select | Copilot returned a value that isn't one of the options. Check the prompt's category, sentiment, and urgency lists. |
| Notion `404 object_not_found` | The Notion integration isn't connected to the database (database ••• → Connections). |
| Notion `400` on Products Mentioned | A product name contains a comma. Add `replace(item(), ',', ' ')` in "Select products". |
| Some emails missing | Raise **Top** in "Get emails (V3)", or check the sender's domain is in `CustomerDomains`. |
