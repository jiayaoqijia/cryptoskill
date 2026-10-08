---
name: backrun-a-pending-swap-safely
description: Use when building a backrun that extracts the price move a large pending swap creates: computing the residual edge, sizing to the pool, and setting the bundle that cannot revert.
---

# Backrun a pending swap safely

A backrun profits from the price dislocation a known swap leaves behind, but the edge is thin and vanishes if the swap reverts or someone else lands first, so the bundle must be conditional on the swap actually executing.

## Procedure

1. Decode the pending swap: pool, direction, exact input amount, and the sender. A buy moves the price up; the backrun is the reverse trade at the new price.

2. Simulate the post-swap reserves. For a constant-product pool, `x' = x + dx`, `y' = y - y*dx*997/(x*997 + dx*997)`. Do this in integer arithmetic, never float.

3. Compute the edge: the amount out of the reverse trade minus the amount you would pay at the pre-swap price, minus fees, minus gas. If it is below your gas cost, do nothing.

4. Size to the pool, not to your balance. Passing a size that returns the pool to a mid further than the profit point pushes the price past equilibrium and the trade loses. The optimum is where `dy/dx` equals the marginal cost; solve numerically, not by sweeping large sizes.

5. Make the bundle atomic with the target swap: `[swap, backrun]` in that order, so the backrun reverts (and the bundle is dropped) if the swap never lands. A backrun alone can execute against a pool that did not move, at a loss.

6. Set the bundle tip near the full edge. On a competitive pair, a backrun that bids less than the edge is displaced by one that bids more; keep only a small margin.

7. Submit to a builder relay with the target block pinned, and re-derive on every new head. A backrun computed against the last head is stale by the next block.

8. Cap concurrent exposure: if you have several pending backruns on the same pool, they can land in one block and partially cancel. Track in-flight state per pool.

## Pitfalls

- Assuming the pending swap lands unchanged. Its slippage guard may revert it, leaving your lone backrun to execute at a loss.
- Sizing by balance instead of by pool depth; an oversized backrun over-corrects the price and locks in a loss.
- Using the quoted price after the swap rather than the exact reserve math; fees and integer rounding on large trades differ by basis points that erase the edge.
- Competing on the same opportunity with two of your own bundles, which raises your effective bid and lowers net profit.
- Ignoring a second large swap in the same block that moves price against you between your two legs.
- Running on a public mempool where another searcher backruns you before you land.

## Verification

    cast call $POOL "getReserves()(uint112,uint112,uint32)" --rpc-url $RPC --block $((N-1))

Recompute the edge from the actual pre-block reserves after inclusion and confirm the backrun was profitable net of tip. Report edge before tip, tip paid, and realized net delta.
