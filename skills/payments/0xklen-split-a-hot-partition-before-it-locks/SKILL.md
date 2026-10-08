---
name: split-a-hot-partition-before-it-locks
description: Use when one partition or shard dominates load and slows everything. Detects the hot key, splits or reshards with minimal write pause, and verifies balance afterward.
---

# Split a Hot Partition Before It Locks

A single oversized partition serializes writes, bloats autovacuum, and turns one key's traffic into a global slowdown. Detect the hot key from metrics, split it while it is still small, and confirm the load is spread — not just that the command succeeded.

## Procedure

1. Find the hot partition from real data: `pg_stat_statements` by total time, `citus_tables`/`shard_rebalancer`, Kafka topic-partition metrics, or DynamoDB `ConsumedWriteCapacity` by partition key.
2. Confirm it is size or rate: a partition > dozens of GB or > one device's write throughput is past the healthy point.
3. Choose the split axis that spreads the actual access pattern, not the nominal key — hashing a monotonically increasing id splits poorly.
4. For a range-partitioned table, create the new partition before the boundary arrives so writes never land in the default catch-all:
   `CREATE TABLE events_2026_07 PARTITION OF events FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');`
5. For a sharded store, add a hash suffix to the hot key or reshard the table; `ALTER TABLE ... ATTACH PARTITION` avoids a long rewrite.
6. Detach old partitions instead of deleting rows: `ALTER TABLE events DETACH PARTITION events_2026_01;` then drop the standalone table.
7. Verify after the split: per-partition counts are within ~1.5x of each other and the top query's time dropped.
8. Watch for the vacuum gap — a freshly split table needs an `ANALYZE` before the planner trusts it.

## Pitfalls

- Splitting by a low-cardinality key, so all rows with the common value land in one partition and you have not spread anything.
- A default/catch-all partition silently absorbing unbounded rows because the next partition was never created.
- Resharding online without a backfill dual-write, dropping the tail of writes during the move.
- Detaching without reindexing the now-standalone table, leaving it unqueryable at the speed you expect.
- Autovacuum unable to keep up on the large partition before the split, so bloat persists after the split too.
- Splitting too finely, creating thousands of small partitions that each cost planner overhead and file handles.
- Assuming a successful `ALTER TABLE ATTACH PARTITION` proves balance; only per-partition metrics do.

## Verification

    psql -c "SELECT relname, pg_relation_size(oid) FROM pg_class
             WHERE relname LIKE 'events_%' ORDER BY 2 DESC LIMIT 5;"
    psql -c "SELECT count(*) FROM pg_stat_activity;"   # count in-flight during the split window

Partition sizes are within ~1.5x of each other, the hot partition's size dropped, and no client hit an error while the split ran.

Report: "Split <table> at <boundary> / resharded <table>; per-partition sizes now <a>/<b> (was <c>); top query p99 <x>ms (was <y>ms), 0 errors during the move."
