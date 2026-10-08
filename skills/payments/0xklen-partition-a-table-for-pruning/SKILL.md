---
name: partition-a-table-for-pruning
description: Use when queries scan far more data than they read because the table is not partitioned on the filter column. Chooses a partition key and granularity that lets the engine prune, then verifies the scan drops.
---

# Partition a Table for Query Pruning

A table partitioned on the wrong column scans the whole dataset for every query. Partition on the column your filters use most, at a granularity that keeps partition sizes sane, and verify the engine actually prunes.

## Procedure

1. Find the filter columns in the query log (`pg_stat_statements`, BigQuery `INFORMATION_SCHEMA.JOBS`) and rank them by frequency in `WHERE`.
2. Partition on the top filter column, usually a date, because it matches the natural predicate and is monotonic.
3. Choose granularity by target partition size (aim 100 MB-1 GB each): daily for high volume, monthly for small, hourly for very high.
4. Add a second dimension only as a clustering/sort key, not a partition, unless cardinality is tiny (a `region` with fewer than 50 values).
5. Never partition on a high-cardinality column (`user_id`, `uuid`) or one that changes, which yields millions of tiny partitions.
6. Always provide the partition filter in queries; an unfiltered scan defeats partitioning. BigQuery: set `require_partition_filter=true`.
7. Verify pruning with the query plan or bytes-scanned before and after.
8. Migrate by creating the partitioned table, backfilling by partition, and swapping. Do not `ALTER` in place on huge data without a rewrite plan.
9. Match the physical partition type to the predicate: a string date filtered as a string, a timestamp filtered as a timestamp.
10. Monitor partition count and average size so a granularity that is drifting too fine is caught.

## Pitfalls

- Partitioning on `DATE(created_at)` while queries filter on `updated_at` prunes nothing.
- Hourly partitions on a low-volume table create empty partitions and metadata overhead.
- Wrapping the partition column in a function (`WHERE DATE(ts)=...` versus `ts=...`) can disable pruning.
- A high-cardinality key produces a metadata explosion and slow planning.
- Existing queries that omit the partition filter now scan everything and cost the same or more.
- A type mismatch (`WHERE dt_string = CAST(:d AS STRING)`) skips pruning even though the values look equal.
- Forgetting the swap leaves the old unpartitioned table read by half the jobs.
- Choosing a partition key that is almost always filtered with a range rather than equality gives no pruning benefit.

## Verification

```sh
psql -c "EXPLAIN (ANALYZE, BUFFERS) SELECT ... WHERE dt='2026-10-01'"
bq query --dry_run "SELECT ... FROM t WHERE dt='2026-10-01'"
```

The plan shows partitions pruned, or BigQuery `bytes_processed` falls from the full-table size to one partition. Report the partition key, granularity, partition count, and the before/after bytes scanned.