---
name: match-logs-to-transactions-by-hash
description: Use when joining decoded events to their parent transaction. Groups logs by block_hash and tx_hash, never by block position, so a reorg that re-mines the same transaction keeps the join correct.
---

# Match logs to transactions by hash

A log's parent is its transaction, identified by hash within a block. Joining on position or ordering breaks the moment a reorg re-mines the same transaction in a new block.

## Procedure

1. Key both tables on the same identity: transactions on `(block_hash, tx_hash)`, logs on `(block_hash, tx_hash, log_index)`.
2. Fetch transactions for a block with `eth_getBlockByNumber(full=true)` and index them by `hash`; assign logs to their tx by `txHash`, not by array order:
   ```python
   txs = {t["hash"]: t for t in block["transactions"]}
   for lg in block["logs"]:
       parent = txs[lg["transactionHash"]]        # exact match, not positional
   ```
3. Because the same `tx_hash` can appear under two block hashes across a reorg, always include `block_hash` in the join; otherwise logs from the orphaned copy attach to the canonical tx.
4. Verify the ordering invariant: for each tx, its logs' `log_index` ascending reconstructs execution order.
5. When a tx is re-mined unchanged, re-key its logs to the new block hash and drop the orphaned copies.
6. Use a composite reference `(block_hash, tx_hash)` so the store enforces the correct parentage.
7. Fetch a block's logs and transactions where the provider allows, so both come from the same head.
8. Materialise the `(block_hash, tx_hash)` parent key on the log table as a generated column so the join is an index lookup.

## Pitfalls

- Joining logs to txs only on `tx_hash` attaches orphaned-fork logs to the canonical transaction after a reorg.
- Relying on `transactionIndex` alone is unsafe under reorgs, where a tx keeps its hash but changes block and index.
- A tx with zero logs is legitimately absent from the log join; a plain `JOIN` drops it, so use `LEFT JOIN` when you need all txs.
- Block-level `full=true` responses are large and can hit provider limits; fetch per block, not per range.
- A tx hash shared between an uncle block and the canonical chain appears twice if `block_hash` is dropped from the join key.
- Recomputing the join on every query is wasteful; store the parent key at ingest time.

## Verification

    psql -c "SELECT count(*) FROM logs l LEFT JOIN txs t USING (block_hash, tx_hash) WHERE l.tx_hash IS NOT NULL AND t.tx_hash IS NULL;"
    # expect 0 logs without a same-block parent transaction

Report the log-to-tx match rate per block and confirmation that every log's `(block_hash, tx_hash)` resolves to a stored transaction.
