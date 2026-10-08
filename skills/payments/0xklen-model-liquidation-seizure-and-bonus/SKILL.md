---
name: model-liquidation-seizure-and-bonus
description: Use when sizing a liquidation, checking close-factor limits, or estimating liquidator profit. Computes repay amount, seized collateral, bonus, and the bad debt left behind from reserve parameters.
---

# Model liquidation seizure and bonus

A liquidation repays part of the debt and seizes collateral plus a bonus; the position only recovers if the seizure restores HF >= 1, and any shortfall becomes protocol bad debt.

## Procedure

1. Read the reserve parameters: liquidation threshold, liquidation bonus (e.g. 1.05 = 5%), close factor (Aave 0.5).

   cast call $POOL "getConfiguration(address)(uint256)" $ASSET --rpc-url $RPC

2. Max repayable = `closeFactor * debt`. Collateral seized in value = `repay * liquidationBonus`.

3. Repay to reach a target HF: solve `collateral_weighted / (debt - R) = HF_target`. For `HF_target = 1`, `R = debt - collateral_weighted`.

4. Worked example — weighted collateral $11,760, debt $12,000 (HF 0.98):
   - R = `12,000 - 11,760 = 240`.
   - close factor caps repay at `0.5 * 12,000 = 6,000`, but only 240 is needed.
   - seized collateral value = `240 * 1.05 = 252`, taken in the collateral asset.
   - if instead weighted collateral were 8,000 with 12,000 debt, even the full 50% repay leaves debt 6,000 against 8,000 weighted, and full seizure to zero still leaves `12,000 - 8,000 = 4,000` bad debt.

5. Liquidator profit = `seized_value - repay_value - gas - unwind_slippage`. On thin collateral pools the bonus is eaten by DEX slippage when converting to stables.

6. Flag any position where `debt > Σ weighted_collateral`: it cannot be healed at HF = 1 and belongs in the bad-debt waterfall.

## Pitfalls

- Ignoring the close factor: it caps repay at 50% on Aave (higher on isolated markets) and changes the recovery math.
- The bonus is denominated in the collateral asset; when that asset is illiquid the nominal bonus is not realizable.
- Bad debt is only visible after collateral reaches zero, so a healthy-looking HF at the moment of liquidation can still leave a deficit.

## Verification

    python3 -c "d=12000; w=11760; print(min(d-w, 0.5*d), (d-w)*1.05)"
    240.0 252.0

Matches the `LiquidationCall` event (debtToCover and liquidatedCollateralAmount) for the same position.

Report repay, seized collateral, bonus, and any residual bad debt, each with the reserve param call behind it.
