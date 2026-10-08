---
name: run-a-right-to-erasure-drill
description: Use when a deletion request must be honoured across systems that do not share a key. Execute end to end, then re-search every store to prove the subject is gone.
---

# Run a right to erasure drill

Deletion is a distributed transaction across systems that rarely share a key. This skill runs an end-to-end erasure and proves it by re-searching every store.

## Procedure

1. Build the checklist from the PII inventory: DB tables, replicas, warehouse, search index, caches, logs, queues, backups, exports, and third parties.

2. Choose a test subject that has data in the maximum number of systems; a subject with one row proves almost nothing.

3. Delete children first to satisfy foreign keys, or use cascades you have already tested on a copy:
   `delete from sessions where uid=$1; delete from orders where uid=$1; delete from users where id=$1;`

4. For immutable stores (event logs, Kafka, append-only tables) use crypto-shredding: delete the per-subject key so the ciphertext becomes unreadable, or tombstone with a compaction window.

5. For the warehouse and search index, issue the backend delete and force a merge or refresh; a soft-deleted document still sits on disk:
   `curl -XPOST "es:9200/idx/_delete_by_query?refresh=true" -d '{"query":{"term":{"uid":X}}}'`

6. For backups do not rewrite history; document that the subject's data expires with the backup's own retention and will never be restored into active use.

7. Send the deletion request to third parties and store the vendor's acknowledgement.

8. Re-run the full search from the access workflow after 24h, because pipelines lag, and record hits per system. Any non-zero result is a failure.

9. Write the erasure record: subject, date, systems, evidence, and residual copies with their expiry dates.

## Pitfalls

- Search indexes and caches are the usual survivors; a deleted DB row still shows in autocomplete for days.
- Aggregate tables keyed on an unsalted hash of the id stay linkable when the id space is small.
- Restoring a backup after erasure reintroduces the data; the restore runbook must re-apply pending deletions.
- Deleting a user can cascade into records you must legally keep; separate the legal hold before deleting.
- Analytics SDKs and CDPs keep their own copy on their own schedule and must be on the checklist.

## Verification

    for s in db warehouse index cache; do printf "%s: " "$s"; search_all_systems.sh "$SUBJECT" "$s"; done

All systems must report zero hits; report any store still holding data and its expected expiry date.
