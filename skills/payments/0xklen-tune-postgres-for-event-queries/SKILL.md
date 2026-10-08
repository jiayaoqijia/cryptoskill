---
name: tune-postgres-for-event-queries
description: Use when an indexer's Postgres event tables get slow past hundreds of millions of rows. Uses BRIN on block_number and targeted indexes so log-range scans stay cheap as the table grows.
---

# Tune Postgres for event queries

Event tables grow append-only by block, and queries are almost always a block range for one address or topic. Index for that access pattern, not for the primary key alone.

## Procedure

1. Add a BRIN index on `block_number`; it is cheap to maintain and ideal for append-only, naturally ordered data:
   `CREATE INDEX CONCURRENTLY logs_block_brin ON raw_logs USING brin (block_number);`
2. Add targeted btree indexes for the filters actually used: `(address, block_number)` and an expression index on `(block_number, topic0)`.
3. Confirm the planner uses them and see row estimates against actuals:
   ```
   EXPLAIN (ANALYZE, BUFFERS)
   SELECT block_number, log_index FROM raw_logs
   WHERE block_number BETWEEN 19000000 AND 19000100 AND address = '\xabc';
   ```
   Expect an index scan and buffers read close to rows returned, not a seq scan.
4. Partition by block range so a query touches only relevant partitions and old ranges can be detached.
5. Keep wide `topics`/`data` columns out of the hot scan by selecting only needed columns.
6. `VACUUM (ANALYZE)` after large backfills so statistics drive the planner correctly.

## Pitfalls

- A btree on `block_number` alone is huge and slow for range scans; BRIN is the right tool for ordered append-only data.
- `SELECT *` over raw logs pulls uncalled `data` blobs and blows the buffer cache; select narrow columns.
- Missing statistics after a backfill makes the planner choose a seq scan; analyze after bulk load.
- Indexing a low-cardinality column like `topic0` alone rarely helps; pair it with `block_number`.

## Verification

    EXPLAIN (ANALYZE, BUFFERS) SELECT block_number, log_index FROM raw_logs WHERE block_number BETWEEN 19000000 AND 19000100 AND address = '\xabc';
    # expect an Index Scan / Bitmap Index Scan with "rows removed by filter" small

Report the index used, buffers read, and estimated versus actual rows for the hot range query.
