---
name: cost-and-execution
domain: crypto-trading/cost-and-execution
trigger: "How to model transaction costs, slippage, market impact, commissions, and execution frictions in backtesting."
anti_trigger: "Not for executing trades on live exchanges or managing real-time order routing."
scope: "Commission, spread, impact, funding, and the Sharpe 0.43→0.22 example; fill assumptions that flatter a backtest."
status: seedling
---

## Standard

Backtest validity is compromised by unrealistic cost and execution assumptions that flatter performance. Strategies profitable under zero-cost assumptions become loss-making once realistic market frictions—including exchange commissions, bid-ask spreads, market impact, latency, and perpetual funding rates—are incorporated. As demonstrated in recent empirical literature (arXiv 2605.16895, "Alpha Illusion"), strategy Sharpe ratios degrade severely when accounting for full execution drag; aggregate portfolio Sharpe ratios routinely drop from an apparent 0.43 down to 0.22 or lower, falling below passive buy-and-hold benchmarks once commission, token cost, borrowing fees, and market impact are fully charged.

Accurate execution modeling requires accounting for the square-root law of market impact, where price displacement scales with the square root of order size relative to market volume. In crypto derivative trading, ignoring funding rate payments on perpetual swaps during directional trend regimes introduces massive distortion. Similarly, assuming instantaneous fills at prevailing mid-prices ignores adverse selection, where orders are filled precisely when liquidity providers are exiting. Cost modeling must reflect tier-based exchange fee schedules and realistic order-book depth constraints.

Primary sources for the claims in this section: <https://doi.org/10.1016/B978-0-444-53068-6.50005-5> and <https://arxiv.org/abs/2605.16895>.

## Decision rules

1. Every backtest must incorporate commission fees, half-spread crossing, market impact, and perpetual funding rates. Zero-cost backtests are strictly invalid.
2. Market impact must be modeled as a non-linear function of order size relative to average daily volume (ADV) or order book depth, adhering to square-root market impact principles.
3. If incorporating realistic transaction costs reduces net Sharpe ratios below buy-and-hold benchmarks (matching Alpha Illusion 0.43 to 0.22 degradation), the strategy fails audit and must be rejected.
4. Fill assumptions must reflect adverse selection: market orders must cross the full spread, and limit orders must not be assumed filled unless subsequent trade ticks demonstrate resting order priority and sufficient depth.

## Procedure

1. Calculate turnover ratio and total round-trip transaction volume for the strategy across the backtest period.
2. Apply exchange-specific maker/taker fee tiers based on historical volume brackets to gross turnover.
3. Model price impact for each trade using order book depth snapshots or volume participation rate scaling formulas.
4. For derivative strategies, compute cumulative funding rate cash flows based on historical funding intervals and open interest positioning.
5. Recompute net returns, net Sharpe ratio, and maximum drawdown after deducting all cumulative execution frictions.
6. Benchmark net performance against passive buy-and-hold to confirm positive alpha after costs.

## Anti-patterns

- Assuming all trades execute cleanly at the exact mid-price without crossing the bid-ask spread.
- Omitting exchange tier fees or assuming zero-fee market maker rebates apply universally across all order sizes.
- Neglecting perpetual swap funding payments during prolonged high-funding-rate regimes.
- Using static slippage estimates that fail to scale when order sizes exceed available top-of-book liquidity.

## Done checklist

- [ ] Exchange commissions and fee tiers integrated into return calculations.
- [ ] Bid-ask spread crossing and market impact modeled non-linearly.
- [ ] Perpetual funding rates included for derivative instruments.
- [ ] Net Sharpe ratio compared against buy-and-hold benchmark (Alpha Illusion threshold check).
- [ ] Adverse selection accounted for in fill assumptions.

## Sources

- Almgren, R., Thum, C., Hauptmann, E., & Li, H. (2005). Direct Estimation of Equity Market Impact. Risk, 18(7), 58-62. https://www.risk.net/
- arXiv:2605.16895. Alpha Illusion: Evaluating the Limits of Quantitative Trading Strategies Across Limited Samples and Tickers. https://arxiv.org/abs/2605.16895
- Bouchaud, J. P., Farmer, J. D., & Lillo, F. (2009). How Markets Slowly Digest Changes in Supply and Demand. Handbook of Financial Markets: Dynamics and Evolution, 57-160. https://doi.org/10.1016/B978-0-444-53068-6.50005-5
- Open Science Framework (OSF). Financial Modeling Standards and Cost Accounting. https://osf.io/prereg/
