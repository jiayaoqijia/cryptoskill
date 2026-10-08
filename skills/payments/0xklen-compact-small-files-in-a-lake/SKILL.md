---
name: compact-small-files-in-a-lake
description: Use when a data lake or table format accumulates thousands of tiny files from frequent appends. Compacts them into right-sized files without breaking concurrent readers or the partition layout.
---

# Compact Small Files in a Lake

Frequent small appends create millions of tiny files; query planning then spends more time listing files than reading data. Compaction rewrites them into right-sized files while preserving the commit protocol and concurrent reads.

## Procedure

1. Diagnose: list file sizes per partition.
   `hadoop fs -ls -R s3://bucket/table/ | awk '{print $5}' | sort -n | head` or read the table format's file-size stats.
2. Set a target file size (typically 128 MB-1 GB for Parquet in a lake) and a max-files-per-partition threshold.
3. Compact per partition, not the whole table at once:
   - Iceberg: `spark.sql("CALL catalog.system.rewrite_data_files(table => 'db.t', options => map('target-file-size-bytes','134217728'))")`.
   - Delta: `OPTIMIZE db.t WHERE dt='2026-10-01' ZORDER BY (user_id)`.
4. Use the format's commit protocol so concurrent readers see a consistent snapshot: Iceberg rewrites produce new snapshots, Delta `OPTIMIZE` is ACID. Never delete files by hand.
5. Schedule compaction after the ingestion window and cap files touched per run to bound cost.
6. Compact within a partition so files do not straddle partitions and break pruning.
7. Re-measure file count and bytes-scanned after; then let the snapshot-expiry job reclaim the old files.
8. For streaming ingest, run compaction on a timer (every N commits or minutes) rather than per micro-batch.
9. Sort or Z-ORDER on the column queried most, so compaction also reduces scan bytes, not just file count.
10. Alert when files-per-partition crosses the threshold again, so the compaction lag does not quietly return.

## Pitfalls

- Manual `rm` of old Parquet files under a table format corrupts the transaction log and breaks readers.
- Compacting the whole table nightly rewrites terabytes to save seconds; compact only hot or small-file-heavy partitions.
- Ignoring the sort means compaction reduces file count but not scan bytes when the filter column is scattered.
- Compaction during ingestion races the writer; use the format's concurrency control or a quiet window.
- Forgetting snapshot expiry leaves storage cost unchanged (old and new both present).
- A target file size below the block/stripe size wastes headers.
- Running compaction as one giant job holds up the table's metadata and blocks concurrent commits.
- Recompacting the same partition every run because the threshold is set below the achievable size wastes forever.

## Verification

```sh
spark-sql -e "SELECT count(*), avg(file_size_in_bytes) FROM db.t.files WHERE partition.dt='2026-10-01'"
# a point query's bytes-scanned should drop after compaction
```

File count falls within the target, average file size is near the target, and a filtered query scans far fewer bytes. Report partitions compacted, before/after file counts, and storage reclaimed after snapshot expiry.