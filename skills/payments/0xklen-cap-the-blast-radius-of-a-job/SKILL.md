---
name: cap-the-blast-radius-of-a-job
description: Use when an unattended job writes or deletes in bulk and a bad predicate could run away. Bounds what one run can change so a bug cannot touch everything at once.
---

# Cap the blast radius of a job

An unattended job with an unbounded write is one typo away from a mass delete. Bound every run by count, scope, and reversibility, so a bug produces a bounded, recoverable incident instead of a catastrophe.

## Procedure

1. Put a hard row cap on every bulk write and check it before acting. If the predicate can match more than the cap, the job exits with a distinct code and alerts, rather than quietly capping:
       UPDATE ... WHERE ... LIMIT 10000;   -- refuse, don't truncate, if more match
2. Scope by tenant, shard, or partition so no single run touches the whole estate; process one shard per run and advance.
3. Default to reversible operations: soft-delete (set `deleted_at`) before hard-delete, and let a separate, slower job purge later.
4. Never `DELETE FROM` or `UPDATE` without a `WHERE` derived from data, not from a variable that could be empty. Guard against the empty predicate:
       [ -z "$CUTOFF" ] && exit 1     # refuse to run with a blank cutoff
5. Run the write in a transaction with a statement timeout so a runaway lock cannot pin the table.
6. Preview the affected count first (`SELECT count(*)` with the same predicate) and abort if it exceeds the cap — the same predicate, same transaction, no drift.
7. Make the write idempotent and keyed so a re-run after a partial failure is safe.
8. Take a snapshot or record the pre-image of affected rows when the operation is destructive and the store supports it.
9. Dry-run first and compare the proposed count to the cap.
10. Alert when a run hits or approaches the cap; hitting the ceiling means either data growth or a wrong predicate.

## Pitfalls

- A `DELETE` whose cutoff variable expanded empty, deleting everything.
- Capping silently (`LIMIT 10000`) so the remaining rows are never processed and nobody knows.
- One run touching all tenants, so a bug affects every customer at once.
- Hard deletes with no pre-image, making recovery impossible.
- No transaction, so a mid-run failure leaves a half-applied change.
- A cap set so high it is decorative, or so low the job never finishes.

## Verification

    # the proposed count must be under the cap before the write runs
    psql -tc "select count(*) from events where created_at < '$CUTOFF'"   # < cap, else abort
    ./purge --as-of "$CUTOFF" --max-rows 10000; echo "exit=$?"
    # pass: over-cap runs exit non-zero and alert; under-cap runs write and log the count

Report the row cap, the scope (tenant/shard/partition), the reversibility (soft vs hard), and the empty-predicate guard.
