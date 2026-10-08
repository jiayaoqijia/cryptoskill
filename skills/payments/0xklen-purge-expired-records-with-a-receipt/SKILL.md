---
name: purge-expired-records-with-a-receipt
description: Use when data must be deleted on a schedule for privacy or cost. Deletes expired records from every replica, index and backup, and leaves a count as proof the deletion happened.
---

# Purge Expired Records with a Receipt

A deletion that runs on one table but not the search index, cache, or backups is not a deletion — it is a partial one that a privacy request or audit will expose. Purge every copy and record a receipt.

## Procedure

1. Enumerate every place the record lives: primary table, read replicas, search index, cache, analytics warehouse, object store, and backup sets.
2. Pick the sweep cadence: nightly for cost, or per-request for privacy erasure where the request must complete promptly.
3. Delete in bounded batches to avoid a long lock: `DELETE FROM events WHERE created_at < now() - interval '90 days' LIMIT 10000;` in a loop until `rowcount` is 0.
4. Delete from dependent stores: `curl -X POST 'search/_delete_by_query?conflicts=proceed'`, `redis-cli --scan --pattern 'sess:*' | xargs redis-cli del`, or an idempotent index rebuild.
5. Handle backups explicitly. You usually cannot rewrite every backup; document the maximum backup retention as the outer bound on how long a deleted record could reappear, and expire past it.
6. For a legal erasure request, delete live now, tag the subject id, and let backups age out within the stated window — record the request id.
7. Emit a receipt: rows deleted per store, timestamp, and the cutoff. `SELECT count(*) ... ` before and after, logged immutably.
8. Alert if a scheduled sweep deletes 0 for two cycles or if counts diverge from the expected expiry volume.

## Pitfalls

- Deleting from the primary but not the read replica, so the record reappears on the next replica read.
- Purging the search index but not the underlying table, or the reverse; a stale copy survives in whichever store was forgotten.
- A `DELETE` of millions of rows in one transaction that bloats the table and locks it, causing an availability incident.
- Forgetting the analytics warehouse and data lake, where a copy persists indefinitely because loaders keep re-adding it.
- Claiming a GDPR erasure is complete while backups still hold the record beyond the disclosed window.
- Sweeping without a receipt, so the only evidence of deletion is a cron exit code and an operator's memory.
- Using a soft-delete flag that no downstream reader honours, so the "deleted" record still appears in reports.

## Verification

    psql -c "SELECT count(*) FROM events WHERE created_at < now() - interval '90 days';"  # expect 0
    curl -s 'search/_count?q=created_at:[* TO now-90d]' | jq .count                      # expect 0

Every enumerated store returns zero for the expired predicate, and the receipt file records the per-store counts and cutoff.

Report: "Swept cutoff <date>: primary <n>, index <m>, cache <k>, object <j> rows deleted; backups bounded to <d>d; receipt at ops/purge/<date>.json."
