---
name: replay-failed-records-from-dlq
description: Use when reprocessing records that landed in a dead-letter queue. Re-validates each record, re-runs the fixed code path, and clears the entry only after its load commits.
---

# Replay Failed Records from a DLQ

A replay re-runs quarantined records against the fixed pipeline. It must re-validate (the fix may accept some and reject others), stay idempotent, and clear each entry only after its load commits.

## Procedure

1. Fix the root cause first. A replay without a fix re-queues the same failures and burns the attempt budget.
2. Snapshot the queue before replaying: `SELECT * INTO dlq_backup FROM dead_letters WHERE state='failed';` so a bad replay is reversible.
3. Replay in bounded batches (100-1000 records) through the same validation and load code as production, not a bypass path.
4. Re-run through validation and split the batch into now-valid and still-invalid.
5. Load now-valid records with the idempotent upsert on the same natural key, so replaying a record twice is harmless.
6. Clear the DLQ entry only inside the same transaction that commits its load: `DELETE FROM dead_letters WHERE id=:id` on success. A crash between load and clear must not lose the record.
7. For still-invalid records, increment `attempt_count` and store the new error; move to terminal state past max attempts and alert.
8. Record a replay-run row (batch id, accepted, rejected) for audit.
9. Verify no duplicates: the target's natural key must not gain a second copy of a replayed record.
10. Rate-limit the replay so it does not compete with the live job for source or target capacity.

## Pitfalls

- Clearing the DLQ entry before the load commits loses the record on a crash.
- Replaying with bypassed validation lets the same bad record corrupt the target.
- Replaying without the idempotent path duplicates every record that partially succeeded.
- Replaying the whole queue when the fix covers one error class re-queues the others.
- A replay that ignores `attempt_count` re-fails silently forever.
- No backup means the only copy of the bad records was the queue you just cleared.
- Running the replay at full speed while the live job runs causes lock contention and timeouts.
- Marking a record terminal without alerting hides the ones the fix did not cover.

## Verification

```sh
psql -c "SELECT error_class, count(*) FROM dead_letters GROUP BY 1"
psql -c "SELECT id, count(*) FROM orders GROUP BY id HAVING count(*)>1 LIMIT 5"
```

The replayed class is empty (or only terminal rows remain) and the duplicate check returns no rows. Report records replayed, accepted, still failing, and the batch ids.