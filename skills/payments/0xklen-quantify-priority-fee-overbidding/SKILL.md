---
name: quantify-priority-fee-overbidding
description: Use when auditing gas spend after the fact: computing the minimum tip that would have achieved the same inclusion position in the block, and the amount wasted by overbidding on each transaction.
---

# Quantify priority fee overbidding

Replaying a block shows the lowest tip any transaction could have paid and still landed in the same position, so the difference between what you paid and that floor is what overbidding cost you — often more than the MEV you were competing for.

## Procedure

1. Pull the block's transactions with their effective priority fee and gas used:

   ```bash
   cast block $N --rpc-url $RPC --field transactions --json | \
     jq '[.[] | {hash, tip: (.maxPriorityFeePerGas|tonumber), gas: (.gasUsed|tonumber)}]'
   ```

2. For each transaction, the theoretical floor is the next-lowest tip among transactions that were *also included*, ordered the way a fee-maximising builder would order: sort descending by tip and find the first position where block gas would be exceeded.

3. Overbid for transaction t = `tip_paid(t) - floor_tip_at_its_gas_position`. This is the amount that would have been saved by paying exactly the marginal tip.

4. Handle the case where the tip equals the base-fee burn on some paths; distinguish the priority fee (to the builder) from the base fee (burned). Overbidding is about the priority component only.

5. Aggregate: `sum(overbid) / sum(tips_paid)` is the overbid ratio. Anything above 0.3 on a routine arb means your estimator is pricing against the peak of a spike rather than the clearing margin.

6. Cross-check against outcomes. For transactions that landed early in the block because of a strategic position (a backrun that must follow a specific swap), part of the tip is buying ordering, not just inclusion, and should be excluded from the overbid measure.

7. Feed the distribution back into the tip estimator: target the observed 70th-percentile tip, not the maximum you ever paid. Recompute weekly as the mixture shifts.

## Pitfalls

- Comparing your tip to the block's mean; the mean is dragged down by cheap low-gas inclusions and makes every tip look like overbidding.
- Ignoring gas share. A transaction needing a large gas slot legitimately pays a higher marginal tip; the comparison must be per gas position.
- Treating the minimum-tip transaction as the floor when it landed late in the block; a low tip that got in at the end proves nothing about early inclusion.
- Counting the base fee as overbid. Base fee is burned uniformly and is not part of the auction.
- Forgetting that a bundle bid replaces the tip after inclusion, so on a bundle path the tip field is not what you actually paid.
- Assuming a single builder's ordering. Different builders have different tie-breaks, so the floor from one block is approximate.

## Verification

    cast block $N --rpc-url $RPC --field transactions --json | jq '[.[] | .maxPriorityFeePerGas] | sort | reverse | .[0:5]'

Sort included tips descending and recompute the marginal tip at each gas position; the sum of your paid-minus-floor is the overbid. Report total tips paid, total overbid, the ratio, and the largest single overbid.
