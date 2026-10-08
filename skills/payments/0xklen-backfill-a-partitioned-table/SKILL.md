---
name: backfill-a-partitioned-table
description: Use when reprocessing historical partitions after a bug, a logic change, or new data. Runs the backfill in bounded idempotent chunks with a concurrency cap and verifies each partition before moving on.
---

# Backfill a Partitioned Table

A backfill re-derives history with fixed logic. Done carelessly it locks the table, blows the budget, or overwrites good data with half-computed results. Run it in idempotent chunks through the same code path as the daily job.

## Procedure

1. Reuse the production job code with only the partition range changed. Never a one-off script that drifts from the daily logic.
2. Compute the affected range precisely: the first and last partition the bug touched. Do not backfill everything for a narrow fix.
3. Write to a shadow partition and swap, or merge on the natural key, so a failed chunk leaves the original intact.
4. Chunk by partition and cap concurrency at 2-4 partitions at once, to bound source load and keep each chunk cheaply retryable.
5. Make each chunk idempotent (upsert) so a retried chunk converges.
6. Verify each chunk before moving on: row count and checksum for the partition, compared to a recompute from the source.
7. Order: oldest-to-newest when later partitions depend on earlier ones (cumulative snapshots), newest-to-oldest when only freshness matters and time is short.
8. Rate-limit against the source: a backfill on the same replica as production can starve it; add a query tag and a per-query budget.
9. Record progress in a table so the backfill is resumable after a stop.
10. Pin the code revision in the progress record, so a mid-flight deploy does not produce partitions computed by two different versions.

## Pitfalls

- Overwriting the target partition in place means a crash mid-write leaves it empty or partial.
- Backfilling new logic into partitions downstream already consumed creates a silent inconsistency with cached results.
- Running all partitions in parallel exhausts the source connection pool.
- Backfilling from a source table that was itself already corrected changes nothing; check the raw history still exists.
- Forgetting the trailing late-data horizon re-introduces the gap the backfill was meant to fix.
- No progress table means a restart redoes the whole range.
- A deploy that changes the transform while a backfill is running mixes two logic versions across the range.
- Verifying only the first and last partition misses a bad middle chunk.

## Verification

```sh
psql -c "SELECT dt, count(*), sum(amount) FROM sales WHERE dt BETWEEN '2026-09-01' AND '2026-09-30' GROUP BY dt ORDER BY dt"
```

Every partition's count and sum match the source; run the query twice to confirm idempotency (no growth). Report the range backfilled, partitions verified, rows written, and any partition left failing.