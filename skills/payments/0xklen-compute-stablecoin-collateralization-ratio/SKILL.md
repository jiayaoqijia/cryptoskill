---
name: compute-stablecoin-collateralization-ratio
description: Use when checking whether a crypto-backed stablecoin is actually over-collateralized. Reads collateral locked and debt issued on-chain and computes the ratio and the liquidation trigger price.
---

# Compute a stablecoin collateralization ratio

Over-collateralisation is a live number, not a launch figure: collateral price moves and debt accrues interest. Compute it from chain state and derive the price at which the position liquidates.

## Procedure

1. Read total debt and collateral for the system (MakerDAO-style):
   `cast call $VAT "ilks(bytes32)(uint256 Art,uint256 rate,uint256 spot,uint256 line,uint256 dust)" $ILK --rpc-url $RPC`
   Debt = `Art * rate / 1e27`; collateral = `cast call $GEM "balanceOf(address)(uint256)" $VAT`.
2. Read the oracle price: `cast call $PIP "read()(bytes32)" --rpc-url $RPC` then decode to a number.
3. Compute the ratio, `collateral_value / debt`, where `collateral_value = gem_amount * price / 1e18`:
   `python3 -c "print(round(gem*price/debt,4))"`.
4. Read the liquidation threshold (`spot` is the price divided by the liquidation ratio); the trigger price is `rate / spot`.
5. Stress it: recompute at -20%, -40%, -60% collateral price and find the drawdown that makes the system under-collateralised.
6. For fiat-backed coins the "ratio" is reserves/liabilities from the attestation, not chain state — read both and the gap between them.

## Pitfalls

- Using the market price of the collateral when the oracle reads a delayed price is how a "safe" ratio liquidates early.
- Ignoring accrued stability fees: `Art` is principal, `rate` grows, so a static ratio understates debt over months.
- Summing all ilks hides a single toxic collateral type; compute per-ilk and look at the worst.
- Counting a governance token as collateral double-counts faith, not value.
- A ratio computed with the collateral's own oracle price but the debt at par ignores that the debt is a stablecoin that can be off peg.
- Liquidation penalties and auction slippage mean the realised recovery is below the nominal collateral value.
- Global debt includes surplus and system debt that are not user positions; net them out before quoting a ratio.

## Verification

    python3 -c "print(round(gem*price/debt,4))"
    1.82
    # ratio > 1.5 leaves headroom; < 1.2 is fragile

Report the ratio now, the liquidation trigger price, and the collateral drawdown that breaches it.
