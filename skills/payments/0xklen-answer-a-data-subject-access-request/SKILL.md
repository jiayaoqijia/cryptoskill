---
name: answer-a-data-subject-access-request
description: Use when a person asks for a copy of their data and there is a legal deadline. Verify identity, search every system with a key list, and export with a manifest of the search.
---

# Answer a data subject access request

A DSAR is a search problem with a legal clock. This skill finds every copy, exports it in a usable form, and documents the search so the answer is defensible.

## Procedure

1. Verify identity before disclosing anything: match the request to the account with a proportional check, a logged-in confirmation plus one corroborating detail. Never disclose on an email alone.

2. Log the request the day it arrives and stamp the deadline: 30 days is common, extendable for complexity with a written reason.

3. Build a search key set: primary id, every email, phone, username, and legacy ids. Miss one and the export is incomplete.

4. Query each system of record in turn with the exact keys:
   `psql "$DB" -c "select * from users where id=$1 or email = any($2)"`

5. Export in a portable format (CSV or JSON), never screenshots, and include the metadata: what, why, recipients, retention.

6. Redact third-party data inside the export; one user's record may name another user, and those names must come out.

7. Produce two parts: the copy of the data, and the information (purposes, categories, recipients, retention). Both are usually required.

8. Supply search evidence: which systems were searched, with which keys, on what date. Record negative results too; "no data in X" is part of the answer.

9. Package as one archive with a manifest and deliver over an authenticated channel, not plain email.

## Pitfalls

- Searching only the primary database misses logs, analytics, and the support inbox, which are exactly the surprising copies.
- Notes and free text are personal data when they relate to the person; include relevant tickets.
- The export itself can leak; sending it to the wrong address turns an answer into a breach.
- Deadline arithmetic is off by a day when the timezone is ignored; count in the requester's jurisdiction.
- Manifestly unfounded or repeat requests may be refusable, but must be answered with reasons, not silence.

## Verification

    jq '.manifest[] | {system, keys_used, hits}' dsar_export/manifest.json   # every system present, keys non-empty

Report the systems searched, the record counts, any system with no coverage, and the response date.
