---
name: snapshot-indexer-state-for-replay
description: Use when a decoder change requires reprocessing history. Snapshots the raw tables and cursor so a re-decode can be tested against a frozen input and rolled back without refetching.
---

# Snapshot indexer state for reproducible replay

Re-decoding history needs a frozen input. Snapshot the raw tables and cursor, replay the decoder against the snapshot, compare, then promote or discard.

## Procedure

1. Freeze the raw side; raw data never changes under re-decode, so it is the stable input:
   `pg_dump -t raw_logs -t blocks indexerdb > /snap/raw_$(date +%s).sql`
2. Record the cursor and decoder version as of the snapshot in a manifest beside the dump.
3. Replay into shadow tables (`transfers_v2`) from the snapshot; never overwrite the live derived tables in place.
   ```bash
   psql -f schema_v2.sql
   python -m indexer --replay --in /snap/raw_*.sql --out transfers_v2
   ```
4. Diff old against new on the natural key; a decoder fix should change only the rows it targets:
   `psql -c "SELECT count(*) FROM transfers t JOIN transfers_v2 v USING (block_hash,tx_hash,log_index) WHERE t.value <> v.value;"`
5. Promote with a rename inside one transaction, keeping the old table as `_bak` through the rollback window.
6. Store the snapshot so a regression found weeks later reproduces without an archive node.
7. Checksum the dump (`sha256sum`) and store it with the manifest so the replay input is provably the one diffed against.
8. Time the replay against the snapshot so you know whether a full re-decode is minutes or hours before committing.

## Pitfalls

- Replaying against live tables destroys the ability to compare; always write to a shadow table first.
- Snapshotting only derived state is useless; the raw input is what the decoder reads.
- A snapshot without the cursor cannot reconstruct the exact processed height and misses or repeats the boundary block.
- Keeping dumps forever fills the disk; retire snapshots once the decoder version is promoted and stable.
- A snapshot taken mid-write of a backfill captures a torn range; quiesce writers before dumping.
- Replaying into a schema that differs from the snapshot's columns silently fills NULLs; assert column parity first.

## Verification

    psql -c "SELECT count(*) FROM transfers t JOIN transfers_v2 v USING (block_hash,tx_hash,log_index) WHERE t.value <> v.value;"
    # expect only the rows the decoder change was meant to fix, zero surprises

Report the snapshot size, the cursor frozen, and the diff count between the old and new derived tables.
