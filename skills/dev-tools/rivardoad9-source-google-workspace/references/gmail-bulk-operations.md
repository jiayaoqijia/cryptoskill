# Gmail bulk operations (hundreds to thousands of messages)

For whole-inbox work — sender censuses, mass label/archive, keeping a mailbox clean over time.
Pairs with the triage procedure in `email-inbox-triage`.

## 1. Audit the scopes first — they decide what is possible

```python
from google.oauth2.credentials import Credentials
c = Credentials.from_authorized_user_file(os.path.expanduser("~/.hermes/google_token.json"))
print(c.scopes)
```

| capability | scope needed |
|---|---|
| search / read messages | `gmail.readonly` (`gmail.modify` implies it) |
| create + reuse labels, `messages.modify`, `messages.batchModify` (archive) | `gmail.modify` |
| send / reply | `gmail.send` |
| **filters** (auto-route new mail) | **`gmail.settings.basic`** |

A token with `gmail.modify` but without `gmail.settings.basic` can label and move everything, yet every
`users.settings.filters.*` call returns 403. The fix is re-running the OAuth flow with that scope, not a
code workaround; until then a scheduled script does the same routing for existing mail.

**Filters do not act retroactively.** Even with the scope, `filters().create` only affects new mail —
the existing backlog still needs the `batchModify` pass.

## 2. Batch endpoint

The Gmail batch URI is `https://gmail.googleapis.com/batch/gmail/v1`. The legacy
`https://www.googleapis.com/batch` returns 404 and `BatchHttpRequest` raises `HttpError`. Pass the URI
explicitly (`BatchHttpRequest(callback=cb, batch_uri=BATCH_URI)`) with up to 100 sub-requests per call.

## 3. Quota — the thing that silently truncates a census

Gmail meters *units per minute per user*. A `messages.get` costs 5 units, so roughly 1,000 metadata
fetches in a burst is enough to trip:

```
403 Quota exceeded for quota metric 'Total Query Cost' and limit 'Units per minute per user'
```

Rules that follow from that:

- A `try/except` around each batch that keeps looping converts throttling into a **partial result with
  no error**. Always assert `len(records) == len(ids)` (or count failures) before reporting totals.
- A full-inbox metadata scan of ~20k messages is a **paced background job**, not an interactive call:
  sleep/backoff between batches and tell the user an ETA.
- Once you have the sender list, count with `messages.list?q=from:<addr>` searches — a list is far
  cheaper than per-message gets. Fetch metadata only for the messages actually being classified.
- Do **not** count size from `resultSizeEstimate`; it is a rough guess. Sum `len(messages)` across pages.

## 4. Do not parallelize with a shared client

Threading one `googleapiclient` service object (e.g. `ThreadPoolExecutor` over `messages.get`)
segfaults the interpreter. Use the batch endpoint single-threaded, or build one client per worker.

## 5. Idempotent label + archive

```python
# reuse an existing label id, otherwise re-runs create duplicates
lid = next((l["id"] for l in svc.users().labels().list(userId="me").execute()["labels"]
            if l["name"] == name), None)
if lid is None:
    lid = svc.users().labels().create(userId="me", body={
        "name": name, "labelListVisibility": "labelShow",
        "messageListVisibility": "show"}).execute()["id"]

# archive: label + leave the inbox (chunk ids at 500 per call). Keep-set = same call, no removeLabelIds.
svc.users().messages().batchModify(userId="me", body={
    "ids": chunk, "addLabelIds": [lid], "removeLabelIds": ["INBOX"]}).execute()

# the filter form of the same rule, once the settings scope is granted
svc.users().settings().filters().create(userId="me", body={
    "criteria": {"from": "sender@example.com"},
    "action": {"addLabelIds": [lid], "removeLabelIds": ["INBOX"]}}).execute()
```

Archive this way is reversible (label retained, "move to inbox"), which is what makes a bulk pass
acceptable to run — never trash or delete to clean an inbox.
