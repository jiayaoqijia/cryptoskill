---
name: assess-stablecoin-depeg-from-pool-balances
description: Use when checking whether a stablecoin has depegged, using AMM pool imbalances and cross-venue prices rather than a single ticker. Quantifies deviation and flags thin-liquidity false positives.
---

# Assess stablecoin depeg from pool balances

A stablecoin depegs when it trades persistently below peg across deep venues; a momentary AMM imbalance is noise, and the real test is whether the imbalance survives arbitrage against deep pools.

## Procedure

1. Read a canonical pool's balances (Curve 3pool: index 0 = DAI, 1 = USDC, 2 = USDT):

   cast call $CURVE_POOL "balances(uint256)(uint256)" 0 --rpc-url $RPC

2. Compare each balance to the ideal `total/3`. Worked example — 3pool ideal 33.33M each: DAI 30.5M, USDC 34.0M, USDT 35.5M. DAI is the odd one out, so it is the candidate depeg.

3. Do not use the raw balance ratio: stableswap amplification understates small deviations. Read the marginal rate instead:

   cast call $CURVE_POOL "get_dy(int128,int128,uint256)(uint256)" 0 1 1000000000000000000 --rpc-url $RPC

   The returned value is DAI-in-USDC for 1e18 DAI; divide by 1e18 for the implied rate.

4. Thresholds: deviation < 0.3% = noise; 0.3–1% = watch, re-check in 15 min; 1–3% = active depeg, cross-check a second venue; > 3% sustained 30 min = treat as broken and price collateral at market.

5. Cross-venue: query at least two of Curve, a Uniswap v3 stable pool, and a CEX mid. A single DEX divergence the CEXs do not echo is a liquidity event, not a peg break.

6. Check contagion: if the depegged coin is borrowable collateral with e-mode LT = 0.93, a depeg triggers cross-asset liquidations. Read the reserve's liquidation threshold.

## Pitfalls

- Reading one pool's spot as "the price" — a $2M pool can be moved 1% by a $20k trade.
- Using raw balance ratios in a stableswap pool, which overstates small deviations often by 10x versus `get_dy`.
- Treating a depeg that only exists on one chain as global; bridged wrappers depeg independently of the canonical asset.

## Verification

    cast call $CURVE_POOL "get_dy(int128,int128,uint256)(uint256)" 0 1 1000000000000000000 --rpc-url $RPC

Divide the result by 1e18; a value below 0.99 confirms > 1% deviation on that venue.

Report deviation, venues checked, and the `get_dy` output with the block number.
