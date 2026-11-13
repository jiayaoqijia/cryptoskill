---
name: cascade-exposure
domain: crypto-trading/cascade-exposure
trigger: Use when evaluating systemic liquidation cascades, ADL risks, insurance fund depletion, and order-book gap defense.
anti_trigger: Not for single-position leverage calculation, daily margin monitoring, or post-liquidation reporting.
scope: ADL, insurance fund depletion, partial liquidations, order-book gaps; how to hold a position such that a wick cannot take it out.
status: seedling
---

## Standard
Systemic liquidation cascades occur when cascading forced liquidations sweep through thin order books, driving prices past structural support levels and triggering secondary waves of liquidations. During extreme volatility, cascades run subcritical, with measured branching ratios ($\hat{\lambda}$) typically between 0.1 and 0.2 in flight, meaning liquidations propagate but tend to damp out unless fueled by continuous spot selling or leveraged accumulation. Insurance funds are finite pools designed to absorb bankruptcy losses; during severe historical events, insurance funds can be partially or fully depleted, forcing exchanges to resort to Auto-Deleveraging (ADL) or socialized losses. ADL closes profitable counterparty positions automatically based on leverage and profit ranking, cutting winning trades without warning. Holding positions through cascades requires maintaining liquidation buffers wider than maximum expected order-book slippage and structural wicks.

Primary sources for the claims here: <https://www.binance.com/en/support/faq/futures-insurance-fund-and-adl-360033532452> and <https://www.bybit.com/en/help-center/article/Auto-Deleveraging-ADL>.

## Decision rules
1. Monitor exchange insurance fund balances and daily drawdown velocity; reduce exposure immediately on venues experiencing rapid insurance fund depletion.
2. Calculate position leverage such that the liquidation price sits outside historical maximum wick depths and order-book gap boundaries (at least 15% to 20% buffer for major assets).
3. Track account leverage ranking on venues utilizing Auto-Deleveraging (ADL) to avoid being targeted as the highest-leverage profitable counterparty during systemic stress.
4. Prohibit holding high-leverage directional positions through scheduled macroeconomic data releases or thin-liquidity weekend sessions prone to cascading wicks.

## Procedure
1. Review exchange health metrics, including insurance fund size, recent liquidation volumes, and open interest concentration.
2. Stress-test all open position liquidation prices against historical flash crash wick depths (e.g., 20% to 30% sudden price dislocations).
3. Reduce position size or add margin to push liquidation thresholds past the extreme stress boundary.
4. Audit ADL indicator lights on exchange interfaces to ensure the position is not sitting in the top decile of ADL vulnerability.
5. Exit speculative perpetual exposure prior to known high-impact liquidity vacuums.

## Anti-patterns
- Assuming exchange insurance funds are infinite buffers that will protect the market from severe gap down events.
- Ignoring Auto-Deleveraging (ADL) warnings and holding maximum leverage profitable positions during systemic market crashes.
- Believing that a tight stop loss will always execute during a cascade without suffering catastrophic slippage through empty order book gaps.
- Overlooking the risk of partial liquidations where the exchange liquidates only part of a position, leaving the remainder vulnerable to subsequent cascade waves.

## Done checklist
- [ ] Exchange insurance fund balance and health verified.
- [ ] Position liquidation price stress-tested against historical 30% flash crash wicks.
- [ ] ADL vulnerability ranking audited across all active derivative accounts.
- [ ] Exposure reduced prior to known macroeconomic liquidity vacuums.
- [ ] Order book depth and slippage parameters incorporated into sizing models.

## Sources
- Binance Insurance Fund and ADL Mechanics: https://www.binance.com/en/support/faq/futures-insurance-fund-and-adl-360033532452
- Bybit Auto-Deleveraging (ADL) Explanation: https://www.bybit.com/en/help-center/article/Auto-Deleveraging-ADL
