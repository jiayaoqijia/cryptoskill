---
name: incremental-load-with-watermarks
description: Use when extracting only new or changed rows from a large source table. Tracks a high-watermark so each run reads a bounded window and can resume after failure.
---

# Incremental Load with Watermarks

Full extracts grow linearly with the source and eventually time out. Track a high-watermark, the maximum extraction key already loaded, and read only the window after it. Store the watermark only after the load commits.

## Procedure

1. Pick the watermark column: a monotonic `updated_at` timestamp or a strictly increasing `id`. It must never decrease and never be rewritten after insert.
2. Read the last committed value: `SELECT max(watermark) FROM etl_state WHERE job='orders_inc';`
3. Extract with an exclusive lower bound and an upper bound frozen at run start:
   `WHERE updated_at > :last AND updated_at <= :run_start`
   Freezing `:run_start` keeps late writes out of this run so the next run catches them.
4. Overlap the window deliberately: re-read `:last - 5 minutes` to catch rows committed out of timestamp order, then dedupe on the natural key via upsert.
5. Load into staging, validate, merge into the target.
6. Advance the watermark only after the merge commits, in the same transaction: `UPDATE etl_state SET watermark=:run_start WHERE job='orders_inc';`
7. If the load fails, do not touch the watermark. The next run re-reads the same window and upserts, which is safe because writes are idempotent.
8. Track lag as a metric: `now() - max(loaded_updated_at)`. Alert when it exceeds the freshness SLO.
9. For multi-writer sources, use a composite watermark (partition column plus row id) when `updated_at` alone is not unique, so no row is skipped at a tie.
10. Persist the watermark per source and per partition, not one global value, so an active and a rarely-changing source do not block each other.

## Pitfalls

- Advancing the watermark before the merge commits loses the window forever on a crash, a silent gap.
- `updated_at` set by application code using local time, or not updated on in-place edits, misses changes.
- A row exactly on the boundary is reprocessed or skipped depending on which side is open; pick one open and one closed bound.
- Clock skew between source and pipeline can place a just-committed row past `:run_start`; the overlap window absorbs it.
- A hard DELETE upstream leaves no row to extract, so the watermark never learns the row vanished; reconcile with a periodic full-key diff.
- Backdating a row below the watermark means it is never seen again.
- Using the pipeline's own clock as `:run_start` when the source clock runs ahead skips rows written between the two clocks.
- Storing the watermark in the target table means a failed truncate loses both data and position.

## Verification

```sh
psql -c "SELECT job, watermark, now()-watermark AS lag FROM etl_state WHERE job='orders_inc'"
psql -c "SELECT count(*) FROM orders WHERE updated_at > :last AND updated_at <= :run_start"
```

`lag` is within the SLO and the extracted count equals the rows in the window; a zero count on a busy table means the watermark jumped past real data. Report the window bounds, rows loaded, and current lag.