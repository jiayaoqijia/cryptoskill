---
name: margin-modes
domain: crypto-trading/margin-modes
trigger: Use when selecting between isolated, cross, or portfolio margin modes and evaluating multi-position risk.
anti_trigger: Not for calculating single-position liquidation geometry, leverage selection, or stop-loss placement.
scope: Isolated vs cross vs portfolio margin; what cross-collateral really puts at risk.
status: seedling
---

## Standard
Margin modes dictate how collateral is pooled and allocated across derivative positions. Isolated margin restricts the risk of a position to the specific margin balance allocated to it, protecting the rest of the trading account from total drawdown if liquidated. Cross margin pools the entire account free balance to back all open positions, preventing premature liquidation of individual losing legs at the cost of risking the entire account equity during a systemic shock. Portfolio margin aggregates risk across spot, options, and futures positions, allowing offsetting risks to reduce margin requirements. Cross-collateral arrangements put all deposited assets at risk of liquidation when correlated market downturns depress collateral values simultaneously.

Primary sources for the claims here: <https://www.okx.com/help/margin-trading-rules> and <https://docs.deribit.com/#portfolio-margin>.

## Decision rules
1. Default all directional, swing, or high-conviction perpetual trades to isolated margin to bound maximum loss to the assigned capital allocation.
2. Reserve cross margin exclusively for delta-neutral basis trading, arbitrage books, or sophisticated multi-leg option-perpetual hedging strategies where position correlation actively reduces portfolio risk.
3. Never use volatile altcoin collateral in cross-margin accounts holding major perpetual positions, as a sharp altcoin depreciation can trigger cascading liquidations across the entire book.
4. Audit total account leverage continuously under cross margin rather than evaluating positions independently.

## Procedure
1. Review the account capital structure and categorize open strategies into directional risk and hedging books.
2. Select isolated margin mode on the exchange terminal for any directional or speculative trade before allocating position margin.
3. Configure cross margin only when running correlated multi-leg strategies, ensuring collateral assets are stable or deeply liquid.
4. Calculate maximum portfolio drawdown under cross margin assuming a 30% instantaneous drop in all non-stablecoin collateral assets.
5. Set hard account-level equity stops that trigger manual deleveraging before cross-margin liquidation thresholds are reached.

## Anti-patterns
- Using cross margin for speculative directional trades under the assumption that you will manually add funds before liquidation occurs.
- Depositing high-beta altcoins into a cross-margin collateral pool and expecting stable margin protection during a market-wide liquidity crunch.
- Failing to account for cross-currency haircut rates when using multi-asset collateral under portfolio margin rules.
- Treating isolated margin positions as completely independent without monitoring total capital exposure across the trading desk.

## Done checklist
- [ ] Margin mode explicitly verified as isolated or cross prior to order entry.
- [ ] Account collateral composition audited for high-beta depreciation risk.
- [ ] Maximum cross-margin drawdown calculated under stress scenarios.
- [ ] Account-level equity stop-loss configured on cross margin books.
- [ ] Position risk isolation confirmed on exchange terminal interface.

## Sources
- OKX Margin Trading and Margin Modes Documentation: https://www.okx.com/help/margin-trading-rules
- Deribit Portfolio Margin and Risk Parameters: https://docs.deribit.com/#portfolio-margin
