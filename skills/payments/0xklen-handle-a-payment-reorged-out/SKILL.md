---
name: handle-a-payment-reorged-out
description: Use when a credited crypto payment disappears from the canonical chain. Detects the reorg, halts fulfilment, and re-clears the payment only when it reappears with the right confirmations.
---

# Handle a payment that reorgs out

A tx seen in a block is not a tx in the canonical chain. When the source tx vanishes from the head, any fulfilment already triggered is unbacked; detect it, freeze downstream actions, and re-clear on canonical evidence.

## Procedure

1. Watch the head each block: re-check that each credited tx hash is still in its block and that the block is still canonical.
   `cast tx $TXHASH --rpc-url $RPC | grep -E "blockNumber|blockHash"`
   Compare that `blockHash` with the block you credited against.
2. On a mismatch, mark the payment `reorged` and stop any fulfilment that can still be stopped (shipping, further sends, entitlement grants).
3. Re-derive the canonical chain and look for the tx in the new blocks:
   `cast receipt $TXHASH --rpc-url $RPC` — a different `blockNumber` means the tx was re-included later; a null result means it is not on the canonical chain.
4. Distinguish a re-inclusion (tx re-mined elsewhere) from a drop (tx gone, possibly replaced by a higher-fee tx or never valid).
5. Re-clear the payment only when the tx is canonical and accumulated confirmations exceed the value-tiered threshold.
6. If the tx never returns, void the credit and notify the counterparty with the hash and the block-hash mismatch as evidence.
7. Log the head block hashes around the incident so the depth and cause are reconstructable.

## Pitfalls

- Crediting at first inclusion on a probabilistic chain with no reorg watch; the policy, not the incident, is the failure.
- Assuming a disappeared tx is a double-spend attack when a natural 2-block reorg explains it.
- Fulfilling instantly on soft-confirm and being unable to claw back a shipped good.
- Re-crediting twice when the tx reappears: match on tx hash and suppress the duplicate.
- Watching only your own tx and missing that the whole block was reorged, invalidating sibling payments too.
- A tx can be re-included with a different effect if it was one of several in the block; re-check the whole batch, not one hash.
- Re-clear logic that keys on amount can double-credit when two identical payments exist; key on tx hash.

## Verification

    cast tx $TXHASH --rpc-url $RPC | grep blockHash
    # must equal the blockHash of the current canonical block at that height

Report the tx hash, the block hash at credit time versus now, the reorg depth, and the payment's final status.
