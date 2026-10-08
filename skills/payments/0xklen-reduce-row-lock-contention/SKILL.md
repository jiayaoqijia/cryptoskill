---
name: reduce-row-lock-contention
description: Use when concurrent updates on the same rows queue behind each other — shorten transactions, lock in a consistent order, and use SKIP LOCKED or optimistic updates to break the pileup.
---

# Reduce row-lock contention

Lock contention turns independent writers into a serial queue. Each transaction holds a row lock until commit, so a long transaction on a hot row stalls every writer behind it. Shrink the lock window, order the locks, or avoid the lock entirely.

## Procedure

1. Find the contention:
```sql
SELECT wait_event_type, wait_event, count(*) FROM pg_stat_activity
WHERE wait_event_type = 'Lock' GROUP BY 1,2;
SELECT relation::regclass, mode, granted FROM pg_locks WHERE NOT granted;
```
2. Shorten the transaction: do network calls, sleeps, and I/O before `BEGIN` or outside the transaction, so locks are held for microseconds.
3. Lock rows in a consistent order (e.g. ascending id) everywhere, so two transactions touching the same rows cannot deadlock.
4. For a queue, use `FOR UPDATE SKIP LOCKED` so workers take different rows instead of blocking:
```sql
SELECT id FROM jobs WHERE status = 'queued'
ORDER BY id FOR UPDATE SKIP LOCKED LIMIT 10;
```
5. For counters, drop `SELECT ... FOR UPDATE; UPDATE` in favour of one atomic statement that holds the lock only for the update:
```sql
UPDATE counters SET n = n + 1 WHERE id = $1;
```
6. For low-conflict updates, use optimistic concurrency and retry on zero rows affected:
```sql
UPDATE docs SET body=$2, version=version+1 WHERE id=$1 AND version=$3;
```
7. Use `NOWAIT` when a caller can do something better than wait, converting a block into a fast failure it handles.

## Pitfalls

- A transaction that makes a network call or waits on a user between `BEGIN` and `COMMIT`, holding locks for seconds.
- Inconsistent lock ordering, producing deadlocks the database resolves by killing one transaction.
- `SELECT ... FOR UPDATE` over a wide set, locking rows the transaction then discards.
- `SKIP LOCKED` on anything that needs every row; it silently skips and returns partial results.
- Expecting an index to remove contention when the same hot row is still locked — the contention is logical, not I/O.
- A long analytics query holding `AccessShareLock` and blocking `ALTER TABLE`; run DDL with a short `lock_timeout`.

## Verification

    psql -c "SELECT count(*) FROM pg_locks WHERE NOT granted;"
    psql -c "SELECT wait_event, count(*) FROM pg_stat_activity WHERE wait_event_type='Lock' GROUP BY 1;"
    # pass: ungranted locks near zero under load, no lock-wait pileup

Report the contended relation or row, the lock window before and after, and whether the fix was lock ordering, an atomic update, or SKIP LOCKED.
