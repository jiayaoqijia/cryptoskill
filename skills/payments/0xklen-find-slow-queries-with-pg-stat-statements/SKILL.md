---
name: find-slow-queries-with-pg-stat-statements
description: Use when you need to know which queries to optimise before touching code — read pg_stat_statements ranked by total time, and pick the top offender, not the one that feels slow.
---

# Find slow queries with pg_stat_statements

Optimise by measured total time, not by the query that feels slow. `pg_stat_statements` aggregates every statement's calls, total time, and rows, so the highest-total-time query — often a fast query called a million times — is the real target.

## Procedure

1. Enable the extension; it needs `shared_preload_libraries = 'pg_stat_statements'` and a restart before `CREATE EXTENSION` will work:
```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```
2. Rank by total time first — that is the aggregate impact, the correct first sort:
```sql
SELECT substr(query,1,80) AS q, calls,
       round(total_exec_time)::bigint AS total_ms,
       round(mean_exec_time,2) AS mean_ms, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```
3. Also rank by mean time to surface single expensive queries that are rare but slow:
```sql
SELECT substr(query,1,80), calls, round(mean_exec_time,2)
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 20;
```
4. Read `rows / calls`: a query returning one row per call but called a million times is an N+1, not a plan problem — route it to the N+1 fix.
5. Separate `total_exec_time` (actual work) from `total_plan_time`; high plan time points to a plan-cache or prepared-statement issue.
6. Reset stats before a controlled measurement window so you measure current traffic, not history:
```sql
SELECT pg_stat_statements_reset();
```
7. Take the top statement, run `EXPLAIN (ANALYZE)` on it, fix it, re-rank, and keep the before/after totals.

## Pitfalls

- Normalisation collapses constants to `$1`, so distinct queries can share a row; substitute real values when testing.
- Ranking by mean and missing a 5ms query called two million times that dominates total time.
- `mean_exec_time` alone hides a query that mostly waits on a lock; check `blk_read_time`/`blk_write_time` (needs `track_io_timing`).
- Forgetting the restart; `CREATE EXTENSION` alone fails without `shared_preload_libraries`.
- Not resetting after a one-off batch job, so its single run dominates the ranking.
- Querying stats only on the primary when a replica serving reads has its own counters.

## Verification

    psql -c "SELECT calls, round(total_exec_time) FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;"
    psql -c "SELECT pg_stat_statements_reset();"   # before a measurement window
    # pass: top total-time query identified, fixed, and its total drops on re-measure

Report the top statement by total time, its calls and mean, whether the fix was a plan or a loop, and the before/after total.
