---
name: index-for-the-predicate-not-the-column
description: Use when a query still scans after an index was added — match the index to the predicate shape (equality, range, sort order) and confirm with the plan.
---

# Index for the predicate, not the column

An index on the column named in the `WHERE` clause is not automatically the index the query can use. Column order, operator type, and `ORDER BY` decide whether the planner takes it; a badly ordered composite index is ignored outright.

## Procedure

1. List the predicate shapes you must serve, in operator order: equality columns first, then the range or sort column.
2. Build the composite index in exactly that order:
```sql
CREATE INDEX CONCURRENTLY idx_orders_cust_status_created
  ON orders (customer_id, status, created_at DESC);
```
   Equality columns (`customer_id`, `status`) precede range/sort (`created_at`); reversing them makes the range column unusable for the equality lookup.
3. Use `CONCURRENTLY` in production — a plain `CREATE INDEX` takes an `ACCESS EXCLUSIVE` lock and blocks writes for the whole build.
4. Match operator to index type: `jsonb` containment needs `GIN`; text prefix `LIKE 'foo%'` needs `text_pattern_ops`; full-text needs `GIN (to_tsvector(...))`; geospatial needs `GiST`.
5. Cover the query when it avoids a heap fetch: add `INCLUDE (total)` so an index-only scan can return the projected column.
6. Use a partial index for a skewed predicate — when 99% of rows are `closed`, index only the hot slice:
```sql
CREATE INDEX idx_orders_open ON orders (customer_id) WHERE status = 'open';
```
7. `ANALYZE` the table, then `EXPLAIN` to confirm `Index Scan` / `Index Only Scan` with no `Sort` node and estimate close to actual.

## Pitfalls

- An index on `(status, customer_id)` cannot serve a query filtered by `customer_id` alone — the leading-column rule.
- A function on the column (`WHERE lower(email) = ...`) needs an expression index `ON users (lower(email))`, not the plain column.
- A `CONCURRENTLY` build that fails leaves an `INVALID` index; check `pg_index.indisvalid` and drop/recreate it.
- Adding a single-column index for every query bloats writes — every `INSERT` maintains all of them.
- A `DESC` index does not serve an `ASC` sort as an index-only scan unless backward scan applies.
- Indexing a low-cardinality boolean column on its own; the planner usually ignores it.

## Verification

    psql -c "EXPLAIN (ANALYZE, BUFFERS) SELECT ..." | grep -E "Scan|Sort"
    psql -c "SELECT indexrelid::regclass, indisvalid, pg_size_pretty(pg_relation_size(indexrelid))
             FROM pg_index WHERE indrelid='orders'::regclass;"
    # pass: Index Scan, no Sort node, indisvalid = t

Report the predicate shape, the index column order chosen, the plan node before/after, and the index size.
