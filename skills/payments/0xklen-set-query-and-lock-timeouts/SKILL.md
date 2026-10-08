---
name: set-query-and-lock-timeouts
description: Use when one slow or blocked query pins connections and cascades — set statement, lock, and idle-transaction timeouts so nothing runs unbounded.
---

# Set query and lock timeouts

A query with no timeout runs until it finishes or the client gives up. Meanwhile it holds a connection, possibly a lock, and the pileup grows. Bound every statement, every lock wait, and every idle transaction.

## Procedure

1. Set a server-side default at the database level so nothing is unbounded:
```sql
ALTER DATABASE app SET statement_timeout = '5s';
ALTER DATABASE app SET lock_timeout = '2s';
ALTER DATABASE app SET idle_in_transaction_session_timeout = '30s';
```
2. `statement_timeout` bounds total execution; `lock_timeout` bounds the wait for a lock and stops a queue of blocked queries forming behind one held lock; `idle_in_transaction_session_timeout` reclaims a session that opened a transaction and hung.
3. Override per query when one legitimately needs longer, instead of raising the global default:
```sql
SET LOCAL statement_timeout = '60s';   -- inside the reporting transaction only
```
4. Distinguish timeout failures by SQLSTATE (`57014` query_canceled) and return `503`/`408` rather than a generic 500, so callers retry knowingly.
5. Set a client-side timeout too, shorter than the server's, so a client that gives up does not leave an orphaned query running:
```python
conn = psycopg.connect(dsn, connect_timeout=3)
cur.execute("SET statement_timeout = 5000")
```
6. For queued work, add a per-job deadline and cancel the query when the job is abandoned, so retries do not stack on still-running originals.
7. Look for the two signatures: many `active` sessions in the same `wait_event` (lock contention) and `idle in transaction` sessions (leaked transaction). Both are fixed by timeouts.

## Pitfalls

- `statement_timeout = 0`, the default, means unlimited; the untouched default is the bug.
- A `lock_timeout` longer than `statement_timeout` can never fire because the statement times out first.
- A client timeout longer than the server's, so the client hangs while the server still works.
- A global timeout low enough that a legitimate batch or reporting job always fails; scope overrides to the session.
- Retrying a timed-out write without idempotency — the original may have committed.
- Timeout values set in an ORM connection string that the pooler strips on the way through.

## Verification

    psql -c "SHOW statement_timeout; SHOW lock_timeout; SHOW idle_in_transaction_session_timeout;"
    psql -c "SELECT state, wait_event_type, count(*) FROM pg_stat_activity GROUP BY 1,2;"
    # pass: all three non-zero, and no 'idle in transaction' accumulation under load

Report the three timeout values, whether they are server defaults or session overrides, and the oldest `state_change` age in `pg_stat_activity`.
