---
name: price-cost-to-manipulate-twap-oracle
description: Use when assessing whether an oracle is manipulation-resistant: computes the capital cost to push a pool price by X% and hold it across a TWAP window, versus the value the oracle secures.
---

# Price cost to manipulate TWAP oracle

A TWAP is expensive to move because an attacker must hold a distorted price across the window; the cost is roughly the round-trip slippage of forcing the pool to the target price, held for the number of blocks the window spans.

## Procedure

1. For a constant-product pool (`x` base, `y` quote, spot `P = y/x`), the swap to move price to `k*P` is `Δy = y*(sqrt(k) - 1)` (buy base) or `Δx = x*(1 - 1/sqrt(k))` (sell base).

2. Worked example — pool 500 ETH / 1,000,000 USDC (P = 2,000), attacker doubles price (k = 2):

   python3 -c "import math; print(1e6*(math.sqrt(2)-1), 500/math.sqrt(2))"
   414213.56 353.553...

   Buying in 414,214 USDC leaves reserves 353.55 ETH / 1,414,214 USDC, i.e. price ~4,000.

3. The attacker must sustain the price; selling back immediately moves it down. A TWAP over N blocks charges roughly `cost_per_block * N`, so instantaneous single-block manipulation costs ~414k of temporary capital, while a 30-minute (150-block) TWAP requires holding the position across all 150 blocks.

4. Compare to value at risk: if the oracle secures $5M of borrowable collateral and a 2x move lets the attacker borrow $5M, spending ~$414k of capital (partly recoverable on unwind, minus fees/slippage) to steal $5M is profitable if the borrowed funds are not repaid.

5. Total real cost = `front-half slippage + unwind slippage + LP fees + gas + the risk the price reverts`, plus financing cost of locked capital for N blocks on multi-block windows.

6. Safety rule: a TWAP window >= 30 minutes (150 blocks) on a pool whose depth is >= the TVL the oracle secures is generally manipulation-resistant. A 1-block window or a spot oracle on a thin pool is not.

## Pitfalls

- Computing only the front-run half; the unwind also pays slippage, and both halves cost.
- Assuming multi-block manipulation is impossible — with enough capital, or a flash loan if the whole attack settles in one block, it is not.
- Ignoring that some oracles use spot or a 1-block TWAP, where a single flash-loaned swap sets the price for that block.

## Verification

    python3 -c "import math; y=1e6; print(y*(math.sqrt(2)-1))"
    414213.562...

That is the minimum mid-moving capital to double a 1M-quote pool; compare it to the value the oracle secures.

Report pool depth, target move, manipulation cost, and the secured value, with the formula used.
