---
name: size-concentrated-liquidity-range
description: Use when providing Uniswap v3-style concentrated liquidity: choosing ticks, converting a price range to sqrt-price bounds, and computing capital efficiency and in-range divergence loss of the position.
---

# Size concentrated liquidity range

Concentrated liquidity earns fees only while price is inside the chosen range; a narrower range raises the fee APR but goes out of range faster and enlarges the divergence loss at the edge.

## Procedure

1. Price to tick: `tick = log(price_quote_per_base) / log(1.0001)`, floored to a multiple of the pool's tick spacing (60 = 0.3% pools, 10 = 0.05%, 1 = 0.01%). Inverse: `price = 1.0001^tick`.

2. Convert bounds to sqrt-price X96: `sqrtPriceX96 = sqrt(price) * 2^96`, widening to the nearest usable tick at or outside the target so the range never inverts.

3. Capital efficiency versus full range = `1 / (1 - sqrt(Pa/Pb))`. For ETH at 2,000 with range [1,800, 2,200]:

   python3 -c "import math; Pa,Pb=1800,2200; print(1/(1-math.sqrt(Pa/Pb)))"
   15.62...

   So ~15.6x the fee-earning depth of a full-range position for the same capital.

4. Token split: `amount0 = L*(1/sqrtP - 1/sqrtPb)` (base, active below the range) and `amount1 = L*(sqrtP - sqrtPa)` (quote). Choose `L` so the two amounts equal your deposit.

5. In-range divergence loss is bounded by the range: exiting below `Pa` leaves the position 100% base, and the loss versus holding equals the range width. Recompute the loss at both edges before depositing.

6. Fee APR, not APY: `fee_apr = volume_24h * fee_tier * your_share / your_capital`. Out-of-range time earns zero, so multiply by the expected in-range fraction.

## Pitfalls

- Forgetting the position converts to 100% of the underperforming asset at each edge — a tight range is a leveraged mean-reversion bet.
- Setting bounds on the wrong-side price: Uniswap prices token1/token0, and the base/quote order flips when token0 is the stable.
- Ignoring tick-spacing rounding: a range "set" at 1,999 rounds to 1,980 and widens your risk.

## Verification

    cast call $POOL "slot0()(uint160,int24,uint16,uint16,uint16,uint8,bool)" --rpc-url $RPC

Take return[0] as sqrtPriceX96, compute `price = (sqrtX96/2^96)^2`, and confirm the current tick lies inside [tickLower, tickUpper].

Report the range, capital efficiency, token split, and fee APR with the slot0 read.
