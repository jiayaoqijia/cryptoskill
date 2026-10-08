---
name: pick-payment-confirmations-by-value
description: Use when crediting crypto payments and needing a confirmation count. Sets value-tiered thresholds tied to reorg depth and cross-checks against the chain's observed reorg history.
---

# Pick payment confirmations by value

A payment is not final at inclusion; it is final when a reorg deep enough to undo it is economically implausible. Set confirmations as a function of value and the chain's actual reorg depth, not a copied default.

## Procedure

1. Pull the chain's recent reorg depth: scan for `parentHash` mismatches over the last 90 days of blocks.
2. Establish the deepest reorg in that window as a floor: if the chain reorged 3 blocks, no threshold below 3 is honest.
3. Tier by value:
   - under $100: 1 confirmation (accept the risk explicitly);
   - $100-$10k: 6 on a probabilistic L1, more on a chain with 1-second blocks;
   - over $10k: 24+ or wait for an explicit finality signal.
4. On a chain with a finality gadget, replace the count with the checkpoint; once justified and finalised, reverting requires slashing a third of validators.
   `cast block finalized --rpc-url $RPC`
5. On an L2 a sequencer confirmation is soft; the real finality is the L1 batch plus the challenge window. Credit soft-confirms only up to a value cap.
6. Write the policy as a table keyed on value and chain, and re-measure reorg depth quarterly.

## Pitfalls

- Treating 6 confirmations as universal; a chain with sub-second blocks and deep reorgs needs far more by time, not count.
- Crediting an L2 deposit at sequencer inclusion, then discovering the batch was reorged out.
- A single confirmation on a high-value transfer because the UI "feels" instant.
- Ignoring that a reorg can be a feature (probabilistic finality) or a bug once the chain has checkpoints; distinguish the two.
- Reorg depth is not stationary: a chain that changed its block time or node software reorged deeper after the policy was written.
- Counting confirmations by time fails across a chain halt, when blocks stop and the clock keeps running.
- An exchange's credit policy is not your policy; a counterparty may reverse at a threshold you did not set.

## Verification

    cast block finalized --rpc-url $RPC | grep -E "number|hash"
    python3 -c "print(max(reorg_depths_90d))"   # the floor your thresholds must exceed

Report the confirmation table, the measured deepest reorg, and the value tier that maps to a finality checkpoint.
