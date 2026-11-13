---
name: partitioning-strategy
domain: software-engineering/partitioning-strategy
trigger: "Choosing the partition layout for pipeline tables."
anti_trigger: "Not for analytical sort order, and not for shard placement in distributed stores."
scope: "Partition keys as the pipeline's physical index for pruning and reruns."
status: seedling
---

# Partitioning strategy

## Standard

A partition layout is the physical index of a pipeline: it decides which bytes a query or a rerun must touch. Partitioned by ingestion date, every historical question and every backfill touches everything. Partitioned by a business date or event period aligned with the pipeline's idempotency key, both pruning and rerun become proportional to the window of interest. The layout choice and the idempotency choice are the same choice.

The standard alignments: batch pipelines partition by the processing period (day, hour) because tasks run per period; event-sourced datasets partition by event date; entities with overlapping valid periods partition by the effective period. The wrong-but-common layout is partitioning by arrival time, which makes every historical correction a full rewrite.

Primary sources: <https://www.postgresql.org/docs/current/ddl-partitioning.html> and <https://spark.apache.org/docs/latest/sql-programming-guide.html>.

## Decision rules

- Choose partition columns from the idempotency key and the dominant query window, not from the ingestion timestamp.
- Align partition granularity with rerun granularity: what a rerun rewrites should be one or a few partitions.
- Keep the partition column inside the data: derived partition columns drift from their source.
- Record the expected partition size range and alert on outliers: tiny partitions multiply metadata, huge ones defeat pruning.
- State the retention policy per partition: dropping a partition is the cheap deletion path.
- Treat re-partitioning as a migration, not a tweak: it rewrites every partition.

## Procedure

1. List the dominant access patterns: query windows, rerun units, retention drops.
2. Choose columns and granularity that make each pattern proportional to the data it needs.
3. Verify alignment with the idempotency key of the writing task.
4. Estimate partition sizes at current and target volumes.
5. Write the retention policy against partition boundaries.
6. Record the layout and its reasons; treat any change as a migration with a backfill.

## Anti-patterns

- Partitioning by ingestion time and paying full scans for every historical read.
- Partitions misaligned with rerun granularity, so a rerun rewrites ten partitions.
- A partition column not present in the underlying rows, maintained by convention.
- Thousands of tiny partitions whose metadata costs exceed their data.
- Re-partitioning casually in a release because "the layout felt wrong".

## Done checklist

- [ ] Partition columns derive from idempotency and query windows.
- [ ] Granularity aligned with rerun units.
- [ ] Sizes estimated at current and target volumes.
- [ ] Retention bound to partition drops.
- [ ] Layout recorded with reasons.
- [ ] Changes treated as migrations.

## Sources

- PostgreSQL declarative partitioning: <https://www.postgresql.org/docs/current/ddl-partitioning.html>
- Spark partition handling: <https://spark.apache.org/docs/latest/sql-programming-guide.html>
- Delta Lake table layout: <https://delta.io/>
