---
name: partition-events-table-by-block-range
description: Use when an events table outgrows a single Postgres relation. Partitions by block range so queries prune to a few partitions and old ranges detach for archival instead of slow row deletes.
---

# Partition events by block range

At hundreds of millions of rows a monolithic events table makes every range query scan too much and every vacuum too slow. Range partitioning by block bounds the work.

## Procedure

1. Partition by `RANGE (block_number)` with bounds sized to a stable chunk (e.g. 1,000,000 blocks) chosen so each partition stays manageable:
   ```sql
   CREATE TABLE events (
     block_number bigint NOT NULL, block_hash bytea NOT NULL,
     tx_hash bytea NOT NULL, log_index int NOT NULL
   ) PARTITION BY RANGE (block_number);
   CREATE TABLE events_p19000000 PARTITION OF events
     FOR VALUES FROM (19000000) TO (20000000);
   ```
2. Every range query now prunes: `WHERE block_number BETWEEN a AND b` scans only overlapping partitions. Confirm in `EXPLAIN` that only the intended ones appear.
3. The partition key must be part of the primary key of every partitioned table: `(block_number, block_hash, tx_hash, log_index)`.
4. Pre-create the next partition ahead of the cursor so inserts never fail with "no partition found".
5. Archive by detaching old partitions to cheaper storage rather than `DELETE`:
   `ALTER TABLE events DETACH PARTITION events_p10000000;`
6. Keep a default partition only briefly; a partitioning mistake routes everything there.

## Pitfalls

- Partition pruning only fires for literals or parameterised constants; a wrapped expression like `block_number::int` disables it.
- Overlapping bounds fail at creation and gaps fail at insert; a generation script must produce correct ranges.
- Too many small partitions slow planning; a partition should hold hundreds of thousands of rows, not hundreds.
- A row `DELETE` over an old partition is far slower than detaching it; archive by detach.

## Verification

    EXPLAIN SELECT count(*) FROM events WHERE block_number BETWEEN 19100000 AND 19110000;
    # expect only events_p19000000 in the scan (an Append with one child)

Report the partition size chosen, the partitions pruned by a sample range query, and the archive-by-detach plan.
