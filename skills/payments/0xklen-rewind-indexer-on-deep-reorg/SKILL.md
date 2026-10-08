---
name: rewind-indexer-on-deep-reorg
description: Use when a reorg deeper than one block invalidates indexed rows. Uses stored block hashes to find the common ancestor, then deletes and reprocesses exactly the orphaned range.
---

# Rewind the indexer on a deep reorg

When the canonical chain replaces blocks you already indexed, the derivative state is wrong. Rewind by hash, not by a fixed depth, and delete only the rows the orphaned blocks produced.

## Procedure

1. Detect the reorg: compare the parent hash of the newly fetched block N against the hash you stored for N-1.
   ```python
   prev = db.block_hash(n - 1)
   if block["parentHash"] != prev:
       reorg = True
   ```
2. Walk back block by block until `parentHash` equals the hash you stored at that height. That height is the common ancestor (fork point).
3. Delete derived rows whose `block_number > ancestor` in every affected table, in one transaction, child-first to satisfy foreign keys:
   `DELETE FROM transfers WHERE block_number > $ANCESTOR;`
4. Reset the cursor to the ancestor's number and hash together.
5. Reprocess from ancestor + 1 against the new canonical blocks; the writes must be idempotent (upsert on `(block_hash, log_index)`).
6. Record the reorg: fork point, depth, and how many rows were replaced.
7. Snapshot the pre-rewind row counts so you can prove the rewind deleted exactly the orphaned block's rows, no more.
8. Emit the fork depth and ancestor height as metrics; a rising deep-reorg count is a chain-health signal.

## Pitfalls

- Assuming a fixed reorg depth either truncates too little (stale rows) or too much (wasted refetch). Derive it from hashes.
- Deleting by `block_number` alone leaves rows keyed on an orphaned `block_hash`; key every derived row on the hash.
- A backfill running concurrently with the rewind re-inserts orphaned data; pause writers during the rewind.
- A missed reorg compounds; verify `parentHash` linkage after every block rather than trusting a periodic sweep.
- Deleting derived rows without recording the fork point makes it impossible later to tell a rewind from a gap.
- A rewind that runs while the live tail writes leaves half-orphaned state; take the writer lock first.

## Verification

    python -c "import db; print(db.min_unlinked_block_number())"
    # expect None: every block_hash chain links to its parent up to the cursor

Report fork depth, the ancestor height, rows deleted, and confirmation that the block-hash chain is unbroken after reprocessing.
