---
name: compute-collateral-health-factor
description: Use when checking borrowing capacity, liquidation distance, or the safety of a lending position. Computes weighted collateral, health factor, and the price move that triggers liquidation from live reserve data.
---

# Compute collateral health factor

Health factor is the ratio of risk-adjusted collateral to debt; below 1 anyone may liquidate, so the number and the price distance to it must come from on-chain thresholds rather than a dashboard.

## Procedure

1. Read the account snapshot in one call:

   cast call $AAVE_POOL "getUserAccountData(address)(uint256,uint256,uint256,uint256,uint256,uint256)" $USER --rpc-url $RPC

   Returns `(totalCollateralBase, totalDebtBase, availableBorrowsBase, currentLiquidationThreshold, ltv, healthFactor)` in 8-decimal base units.

2. If reading reserves individually: `HF = Σ(c_i * p_i * LT_i) / Σ(d_j * p_j)`, prices in one numeraire, `LT_i` the reserve liquidation threshold (not the LTV).

3. Worked example — 10 ETH at $2,000, ETH LT = 0.825 (Aave v3), borrow 12,000 USDC:
   - collateral = 20,000; weighted = `20,000 * 0.825 = 16,500`.
   - HF = `16,500 / 12,000 = 1.375`.

4. The price at which HF = 1: `10 * P * 0.825 = 12,000 → P = 1,454.5`. So a 27.3% ETH drop liquidates; report distance-to-liquidation as `(spot - P_liq)/spot`.

5. Borrow capacity: `maxBorrow = collateral * LTV`. With LTV 0.80 that is 16,000, of which 12,000 used, leaving 4,000 headroom — but never borrow to the LTV limit, because a small drop crosses HF = 1.

6. Re-read after any accrual: variable debt grows every block, so HF drifts down with zero price change.

## Pitfalls

- Using LTV instead of the liquidation threshold: LTV <= LT always, so substituting LTV makes HF look safer than it is.
- Ignoring accrued interest — a static HF from an explorer read goes stale within hours on volatile borrow rates.
- e-Mode and correlated-asset tiers raise LT to ~0.93 for stable pairs; applying the default 0.825 wrongly shows a healthy position as near liquidation.

## Verification

    python3 -c "print(16500/12000, 12000/(10*0.825))"
    1.375 1454.5454...

Matches `healthFactor/1e18` from `getUserAccountData`; a divergence means an isolated or e-mode reserve was mis-weighted.

Report collateral, debt, HF, and the liquidation price, each with the call it came from.
