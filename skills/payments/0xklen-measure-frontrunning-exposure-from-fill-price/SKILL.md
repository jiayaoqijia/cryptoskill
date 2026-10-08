---
name: measure-frontrunning-exposure-from-fill-price
description: Use when comparing an executed price to the mid at submission time, quantifying adverse selection, or attributing a bad fill to front-running versus ordinary price impact.
---

# Measure frontrunning exposure from the fill price

Front-running shows up as an execution worse than the price you saw at broadcast; separating it from normal price impact means comparing your fill against the pool mid in the block before yours, not against the quote you were handed.

## Procedure

1. Record the mid price at broadcast: `mid_t0 = y/x` from reserves at block N-1. Store it with the tx hash and submit timestamp.

2. After inclusion at block N, compute the fill rate from the `Swap` event (`amount1/amount0`) and compare to `mid_t0`.

3. Adverse move for a buy = `(fill_rate - mid_t0)/mid_t0` (positive = worse). Worked example: submitted at mid 2,000 USDC/ETH, filled at 2,005.6:

   python3 -c "print((2005.6-2000)/2000)"
   0.0028

   Adverse 0.28%; the attributable slippage (fee + impact) was 0.3%, so the residual is ~0% — no front-run.

4. Attribute the movement: subtract your own impact (from `dx/(x+dx)`) from the total; whatever remains after fees is the front-run/external component.

5. Confirm by adjacency — if the swap immediately before yours in the block is the same pair and moved price your way, that is the front-run leg:

   cast logs --from-block $B --to-block $B --address $POOL "Swap(address,uint256,uint256,uint256,uint256,address)" --rpc-url $RPC

6. Track a rolling metric: median adverse residual over your last 50 swaps. A median above 0.3% means the flow is being systematically picked off — move to a private route.

## Pitfalls

- Using the wallet's displayed quote as `mid_t0` — wallets often show a stale or pessimistic quote, inflating the measured front-run.
- Ignoring legitimate oracle-versus-pool divergence: use the prior block's reserves, not a live call, as the baseline.
- Confusing builder/priority reordering (builders reorder for MEV) with classic searcher front-running; both cost you but only one is a sandwich.

## Verification

    python3 -c "mid=2000; fill=2005.6; print((fill-mid)/mid)"
    0.0028

Matches the event-derived rate against the prior-block mid; report the residual after subtracting your own impact.

Report mid at broadcast, fill rate, block, and the adjacency result.
