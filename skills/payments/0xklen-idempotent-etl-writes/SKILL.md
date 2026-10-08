---
name: idempotent-etl-writes
description: Use when a pipeline job may be retried or rerun after a partial failure. Makes every write an upsert keyed on a natural key so a replay converges to the same table state.
---

# Idempotent ETL Writes

A rerun of a non-idempotent load duplicates rows or double-counts aggregates. Make each write an upsert keyed on a stable natural key so running the job twice leaves the table identical to running it once.

## Procedure

1. Choose the natural key before writing: `(source_id, event_ts)` or `(account_id, date)`. It must be unique in the source, not a surrogate autoincrement.
2. Prefer merge/upsert over append:
   - Postgres: `INSERT ... ON CONFLICT (source_id, event_ts) DO UPDATE SET ...`
   - BigQuery/Snowflake: `MERGE target USING staging ON target.k = staging.k WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT ...`
   - Delta/Iceberg: `MERGE INTO ... ON ...` then `OPTIMIZE`.
3. Write into a staging table or partition, validate counts, then swap or merge. Never mutate the target row-by-row mid-extract.
4. Derive the target partition deterministically from the event timestamp (`dt = DATE(event_ts)`), never from `CURRENT_DATE()`, so a rerun lands in the same partition.
5. Make aggregates recomputable, not incremental-additive. Recompute `SUM` over the window rather than `target += delta`; the delta approach double-counts on replay.
6. Emit a run marker: `INSERT INTO etl_runs (job, partition, run_id, row_count) VALUES (...) ON CONFLICT DO NOTHING`. A second run with the same `run_id` should touch zero rows.
7. Guard the write with a transaction or a single MERGE so a crash leaves either the old or the new state, never a half-merged one.
8. For file sinks, write to a temp path and commit by rename, and name output deterministically from the input (partition, not a clock timestamp).
9. Record the source batch identity (partition plus a file hash) so a rerun of the same input is recognized and skipped.
10. Test idempotency explicitly: run the job, snapshot the target, run it again, diff.

## Pitfalls

- `INSERT` without a conflict clause is the classic duplicate source; retries double the rows.
- `ON CONFLICT DO NOTHING` drops updates when a row changed upstream; you wanted `DO UPDATE`.
- Keying on a millisecond-truncated timestamp collapses distinct events into one row.
- Using `now()` in the partition expression puts a rerun in a different partition and re-reads nothing.
- MERGE on a key that is not unique in the source raises duplicate-row errors or updates arbitrary matches.
- Incremental counters (`count = count + 1`) are not idempotent and drift on every replay.
- Naming output files with a wall-clock timestamp makes every rerun a new file that downstream reads in addition to the old one.
- A MERGE that reads uncommitted rows from the same table it writes can see its own partial state.

## Verification

```sh
# run twice, compare row counts and a checksum of the partition
psql -c "SELECT count(*), md5(string_agg(id::text, ',' ORDER BY id)) FROM events WHERE dt='2026-10-01'"
```

The count and hash are identical after the second run; if the count grew, a write is appending instead of upserting. Report: "Reran job X for partition 2026-10-01; row count and checksum unchanged, only the run marker's second insert no-op'd."