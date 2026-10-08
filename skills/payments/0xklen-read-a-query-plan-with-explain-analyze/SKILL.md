---
name: read-a-query-plan-with-explain-analyze
description: Use when a query is slow and guessing at the cause wastes time — read the planner's plan, compare estimated against actual rows, and fix the node that diverges.
---

# Read a query plan with EXPLAIN ANALYZE

The planner tells you why a query is slow if you read the plan instead of guessing at indexes. The number that matters most is the gap between estimated and actual rows: a bad estimate drives every bad decision downstream.

## Procedure

1. Run with `ANALYZE`, `BUFFERS`, and `VERBOSE` — never plain `EXPLAIN`, which shows only the estimate and may not be the plan that ran:
```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT TEXT)
SELECT o.id, o.total FROM orders o WHERE o.customer_id = 42 AND o.status = 'open';
```
2. Read the plan bottom-up: leaf scans feed the nodes above. Find the node with the highest `actual time` and the largest `rows removed by filter`.
3. Compare `rows=` (estimate) to `actual rows=` at each node. A 100x underestimate means the planner picked a nested loop where a hash join was needed.
4. Check the access method: `Seq Scan` on a large table with a selective predicate is the classic missing-index signal; an `Index Scan` with a `Filter` that discards most rows means the index does not match the predicate.
5. Read `Buffers: shared read=` vs `hit=`. High `read` means the working set exceeds `shared_buffers`; high `hit` on a sequential scan of a big table is wasted memory.
6. After `VACUUM ANALYZE orders`, rerun. Stale statistics are the most common cause of a wrong estimate — more common than a missing index.
7. To confirm a suspected planner error, test a plan choice in one session only:
```sql
SET LOCAL enable_nestloop = off;
```

## Pitfalls

- `EXPLAIN` without `ANALYZE` shows estimates only; the plan it prints is not necessarily the plan that executed.
- A fast-looking plan with a huge `rows removed` is a scan masquerading as a lookup.
- `actual time` is per loop; multiply by `loops` before comparing nodes.
- Reading only the top node; the cost lives at the leaf feeding the expensive join.
- Running `EXPLAIN ANALYZE` on a write outside a transaction, so the mutation commits.
- Ignoring `Planning Time` vs `Execution Time`; high plan time means too many partitions or a plan-cache miss.

## Verification

    psql -c "EXPLAIN (ANALYZE, BUFFERS) SELECT ..." | grep -E "Seq Scan|rows=|actual"
    # pass: no Seq Scan on a table > 1M rows with a selective predicate,
    # and every node's actual rows within 10x of its estimate

Report the node whose estimate diverges worst, the access method changed, and the before/after `Execution Time` from the ANALYZE header.
