---
name: size-a-connection-pool-to-the-database-limit
description: Use when many app instances exhaust the database's connection slots — size each pool from the database's real ceiling, not from request concurrency.
---

# Size a connection pool to the database limit

Every app process that opens N connections multiplies against every replica. Ten pods at pool=20 is 200 connections against a database that serves far fewer useful ones. Size the pool from the database's capacity and keep the fleet total under `max_connections`.

## Procedure

1. Read the ceiling and the current usage:
```sql
SHOW max_connections;                    -- e.g. 100
SELECT count(*) FROM pg_stat_activity;
```
   Count the three superuser-reserved slots and admin sessions as unavailable.
2. Budget across all clients: `total_pool = max_connections - reserves`. Divide by the number of app instances to get the per-instance size.
3. Use the classic sizing rule as the useful target, not the maximum: `connections ≈ (cores * 2) + effective_spindle_count`. Past ~4x cores, extra connections thrash and raise latency.
4. Set an application pool with a hard maximum and a bounded wait:
```python
engine = create_engine(url, pool_size=10, max_overflow=5, pool_timeout=5, pool_recycle=1800)
```
   `pool_timeout` must be shorter than the request timeout so a starved request fails fast instead of hanging.
5. Put PgBouncer in `transaction` mode in front when the app opens many more connections than the database serves; the app then holds cheap connections to the pooler.
6. Watch both failure modes: `pg_stat_activity` at `max_connections` (exhaustion) and latency rising with connection count (thrash). Both reduce throughput.
7. Set `statement_timeout` and `idle_in_transaction_session_timeout` so a leaked-in-transaction connection is reclaimed rather than held.

## Pitfalls

- Sizing the pool from peak request concurrency; the database, not the app, is the bottleneck.
- Leaving `pool_timeout` unset so requests queue indefinitely and every client times out together.
- PgBouncer in `session` mode, which pins a server connection per client and defeats the purpose.
- `pool_recycle` longer than the DB or proxy idle timeout, handing out dead sockets.
- A serverless function each opening its own pool; use RDS Proxy or a shared pooler.
- Counting connections only on the primary when read replicas have their own lower limits.

## Verification

    psql -c "SELECT state, count(*) FROM pg_stat_activity GROUP BY state;"
    psql -c "SHOW max_connections;"
    # pass: total connections < max_connections - 3, no 'idle in transaction' pileup

Report per-instance pool size, instance count, the computed fleet total against `max_connections`, and `pg_stat_activity` by state under load.
