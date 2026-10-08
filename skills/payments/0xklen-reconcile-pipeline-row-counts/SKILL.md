---
name: reconcile-pipeline-row-counts
description: Use when a pipeline may have silently dropped or duplicated rows. Reconciles counts and control totals at each hop so a divergence is localised to one stage instead of a report next quarter.
---

# Reconcile Pipeline Row Counts

A pipeline that "ran green" can still have lost rows. Reconcile counts and control totals at every hop so a divergence is localised to one stage instead of discovered in a report next quarter.

## Procedure

1. Define a control total per hop: row count plus a checksum of a business column (`sum(amount)`, `count(distinct order_id)`).
2. Capture the source count in the same window the extract reads: `SELECT count(*) FROM src WHERE updated_at > :last AND updated_at <= :run_start`.
3. Capture the staging count after the parse/transform and the target count after the load.
4. Compare hop by hop: extract equals parsed plus quarantined; parsed equals loaded plus deduped plus filtered.
5. Investigate the first hop where the numbers diverge; that is the bug's location.
6. Account for expected differences explicitly: filters (`WHERE status='paid'`), dedupe, join fan-out. Fan-out that inflates counts is itself a bug.
7. Store control totals per run so drift is visible as a trend, not a one-off.
8. Alarm on a hard mismatch: `(extract - loaded - quarantined) != 0`.
9. Validate sums, not just counts: 100 rows with the wrong amounts passes a count check.
10. Time-box the source count and the extract together, so a writer changing rows between the two does not create a phantom gap.

## Pitfalls

- Comparing counts only after the load, with no per-hop capture, cannot localise the loss.
- `count(*)` on a join fans out and inflates; use `count(distinct key)`.
- A filter that should be a no-op (`status IS NOT NULL` on a non-null column) silently dropping rows is found only by a per-hop count.
- Reconciliation that ignores the dedupe step flags expected dedupe as a failure.
- Reading the source count at a different time than the extract creates a phantom mismatch.
- Summing a float column and comparing for equality fails on rounding; use a tolerance.
- A checksum over an unordered set of values changes when row order changes; aggregate with an ORDER BY.
- Reconciling only the happy-path partition misses the first run after a schema change.

## Verification

```sh
psql -c "SELECT 'extract', count(*), sum(amount) FROM src WHERE dt='2026-10-01'
         UNION ALL
         SELECT 'loaded', count(*), sum(amount) FROM tgt WHERE dt='2026-10-01'"
```

Extract minus loaded minus quarantined is zero and the sums match within tolerance. Report each hop's count and sum and the first divergence, if any.