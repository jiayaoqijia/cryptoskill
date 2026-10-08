---
name: detect-sandwich-risk-before-swapping
description: Use when a swap might be sandwiched, to estimate the extractable value, and to choose mitigations. Checks trade size versus pool depth, slippage tolerance, and transaction visibility.
---

# Detect sandwich risk before swapping

A sandwich is a front-run that pushes price against your swap plus a back-run that unwinds the attacker into the move your fill created; the attacker's ceiling is exactly the slippage you allowed.

## Procedure

1. Compute your price impact (see the slippage skill). The attacker's max profit ≈ `impact% * notional - fees - gas`. A $50,000 swap at 1% impact is worth up to $500 minus costs.

2. Risk score: sandwichable if `notional / pool_depth > 0.001` AND `slippage_tolerance > 0.005`. Below either threshold, extraction is usually unprofitable after gas (~$5–50 on mainnet, ~$0.01 on L2).

3. Check visibility. A transaction broadcast to a public mempool is observable immediately:

   cast tx $TXHASH --rpc-url $RPC | grep '"to"'

   If it went to a public RPC, assume a searcher scanned it.

4. Detect a sandwich after the fact by pulling the block and finding same-pair swaps adjacent to yours:

   cast logs --from-block $B --to-block $B --address $POOL "Swap(address,uint256,uint256,uint256,uint256,address)" --rpc-url $RPC

   Three consecutive swaps of the same pair, the middle one yours with the outer two from the same address, is a sandwich.

5. Mitigate in order of strength: (a) submit via a private/MEV-protected RPC; (b) set tolerance <= 0.5%; (c) split into pieces under the impact threshold; (d) use a batch auction or commit-reveal DEX.

6. Weigh the mitigation cost: near zero on L2 and free via Flashbots Protect. Leaving `amountOutMin` loose to "avoid a revert" trades a guaranteed loss for a rare retry.

## Pitfalls

- Tight slippage without a protected RPC just makes you revert — reverts still burn gas and are a loss.
- Assuming low impact alone is safe: repeated small swaps in one block are sandwichable if they net to a large move.
- Assuming L2s are sandwich-proof: sequencers can reorder, and priority-order-flow auctions still exist.

## Verification

    cast logs --from-block $B --to-block $B --address $POOL "Swap(address,uint256,uint256,uint256,uint256,address)" --rpc-url $RPC

Count swaps before and after yours in the same block; same-funder outer swaps confirm the sandwich.

Report impact, tolerance, the RPC submitted to, and whether adjacent swaps match your pool.
