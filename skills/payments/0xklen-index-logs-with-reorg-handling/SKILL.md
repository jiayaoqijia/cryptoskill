---
name: index-logs-with-reorg-handling
description: Use when building or reviewing a log indexer that must survive chain reorgs without serving orphaned rows or double-counting events.
---

# Index logs with reorg handling

An indexer that stores a block number but not the block hash will serve data from a chain
that no longer exists after a reorg. Key every row by `blockHash` and roll back on mismatch.

## Procedure

1. Persist the cursor as `(block_number, block_hash)`, never block number alone. Use
   `block_hash` as the primary key component for log rows:

       CREATE TABLE logs (
         block_number INTEGER, block_hash TEXT, log_index INTEGER,
         address TEXT, topic0 TEXT, data TEXT,
         PRIMARY KEY (block_hash, log_index)
       );

2. Before appending a new block, verify it still extends the stored head.

       python3 - <<'PY'
       import json, subprocess
       def head(n, rpc):
           out = subprocess.check_output(["cast","block",str(n),"--json","--rpc-url",rpc])
           b = json.loads(out); return b["hash"], b["parentHash"]
       last_n, last_h = db.head()               # stored (number, hash)
       now_h, parent = head(last_n, RPC)
       if now_h != last_h:
           rewind(last_n)                       # hash changed -> orphaned
       PY

3. On mismatch, walk back until the stored hash matches the canonical chain. Delete rows with
   the orphaned hashes, set the cursor to the last common ancestor, and re-fetch forward.

       cast block $((N)) --json --rpc-url $RPC | jq -r '.hash, .parentHash'
       cast block $((N-1)) --json --rpc-url $RPC | jq -r .hash   # must equal .parentHash above

4. Only index blocks at `confirmed_depth` behind the head. Mainnet: 12 blocks. Arbitrum: wait
   for the L1-`finalized` batch. Optimism/Base: use the `safe` head returned by
   `eth_getBlockByNumber("safe", false)`.
5. Store the log's `removed` flag from `eth_getLogs`; a subsequent poll can return the same
   log with `removed: true` instead of re-fetching ranges.

## Pitfalls

- Treating `latest` as final. A reorg of depth 2 is routine on mainnet and common on testnets;
  anything indexed off `latest` will be rolled back eventually.
- Cursor stored as only a block number: after a reorg you cannot tell which hash you processed,
  so you either re-index duplicates or skip blocks.
- `logIndex` is unique only within a block and can be reused after a reorg reorders logs, so
  `(blockNumber, logIndex)` is not a stable key — include the hash.
- Long polling gaps widen the reorg window; if you resume after downtime, re-verify the last
  `confirmed_depth + slack` blocks, not just the head.
- Providers can serve a cached, slightly stale head; a hash mismatch that "flips back" on the
  next poll usually means the RPC is behind, not that the chain reorged. Re-query a second
  provider before rewinding.

## Verification

    cast block $N --json --rpc-url $RPC | jq -r .hash          # canonical head hash
    # indexer's stored hash for block N must equal that value

After indexing, re-run the same block range and diff the row counts; they must be identical,
and the indexer's head hash must match `cast block <head> --json | jq -r .hash`.
