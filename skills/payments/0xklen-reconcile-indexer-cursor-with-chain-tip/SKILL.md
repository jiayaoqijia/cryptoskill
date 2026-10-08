---
name: reconcile-indexer-cursor-with-chain-tip
description: Use when an indexer's stored cursor may have drifted from the chain head. Compares the persisted last-processed block against the provider's tip and resolves any mismatch before new work begins.
---

# Reconcile the indexer cursor with the chain tip

A cursor that is ahead of the chain, or behind a reorg, silently skips or double-counts events. Before processing, prove the stored cursor is an ancestor of the current head on the same fork.

## Procedure

1. Read the persisted cursor and its block hash. Storing only the number cannot detect a fork:
   `SELECT block_number, block_hash, chain_id FROM indexer_cursor WHERE stream='transfers';`
2. Fetch the head and confirm the chain id, so an RPC pointed at a fork never reconciles cleanly:
   `cast chain-id --rpc-url $RPC && cast block-number --rpc-url $RPC`
3. Confirm the cursor block still exists on the canonical chain and shares the stored hash:
   `cast block $CURSOR_NUM --rpc-url $RPC --json | jq -r .hash`
4. If the hash differs, walk back to the last common ancestor by re-reading each height and comparing hashes, then rewind to that height.
5. If the cursor number exceeds the head (provider lag or a rolled-back chain), do not process forward; poll until head >= cursor.
6. Only after number and hash agree, resume from cursor + 1.
7. Record the reconcile outcome (cursor number, hash, rewind height) as a metric so a repeat rewind from the same height shows up as a provider fault, not an indexer bug.
8. Cache the verified head hash in the cursor row so the next start compares against the last proven ancestor instead of re-deriving it.

## Pitfalls

- Comparing block numbers alone misses reorgs where the height is valid but the hash is from an orphaned fork.
- A load-balanced RPC pool can return two different heads inside one loop; pin one provider for the reconcile step.
- A testnet reset lowers the head below the cursor permanently; detect and reset rather than looping forever.
- `latest` is not final; reconciling against it re-derives state from a block that may be reorged seconds later.
- An RPC that silently serves a stale cached head looks current; compare the head block's timestamp against wall time to catch it.
- Reconciling on every block is wasted work; do it once at startup and after any detected reorg.

## Verification

    cast block $CURSOR_NUM --rpc-url $RPC --json | jq -r .hash
    # expect it to equal the stored block_hash; if not, rewind before resuming

Report the cursor number, stored hash, canonical hash, and the action taken (resume from cursor + 1, or rewind to ancestor N).
