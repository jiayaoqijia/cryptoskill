---
name: slippage-and-impact
domain: crypto-trading/slippage-and-impact
trigger: slippage, market impact, flat slippage curve, fill benchmark, execution cost
anti_trigger: margin calculation, funding rate arb, liquidation price formula
scope: Measuring and auditing execution slippage, market impact, and fee drag against benchmarks
status: seedling
---

## Standard

Execution slippage is the quantitative difference between the expected decision price (such as the arrival midpoint or volume-weighted average price) and the actual executed fill price. Market impact measures how order size perturbs the prevailing order book equilibrium. A critical empirical red flag in execution auditing is the flat slippage curve: when execution data reveals constant fractional slippage (e.g., flat 0.030 basis points) across order sizes ranging from $10,000 to $500,000 against a market with massive depth-to-turnover divergence, it signals artificial quote stuffing, wash trading, or non-genuine order book liquidity. Uncontrolled slippage destroys strategy alpha; independent studies demonstrate that gross trading strategies yielding positive Sharpe ratios (e.g., Sharpe 0.43) can be reduced to unviable returns (Sharpe 0.22) purely through unmitigated commission drag, bid-ask spread crossing, and market impact costs.

Primary sources for the claims here: <https://www.cambridge.org/core/journals/financial-markets-and-portfolio-management> and <https://www.nber.org/papers/w27431>.

## Decision rules

- Benchmark every trade execution against the prevailing arrival midpoint price recorded at the exact timestamp of order dispatch.
- Audit execution datasets for the flat slippage curve anomaly; investigate any venue where large orders experience identical percentage impact as micro orders.
- Factor total execution cost—including taker fees, half-spread crossing, and temporary/permanent market impact—into net strategy backtest hurdles.
- Reject venues or market makers exhibiting anomalous fill distributions or widespread price improvement skepticism.
- Scale order sizing dynamically based on real-time order book slope rather than static notional limits.

## Procedure

1. Record arrival timestamp and mid-market reference price immediately prior to order routing.
2. Capture all fill execution reports containing exact quantities, timestamps, and execution prices.
3. Compute execution slippage: $\Delta P = \frac{P_{\text{fill}} - P_{\text{arrival}}}{P_{\text{arrival}}}$ for buys, inverted for sells.
4. Aggregate slippage across order size deciles to construct the empirical market impact curve.
5. Compare observed impact against theoretical square-root law market impact models and flag anomalous deviations.

## Anti-patterns

- Measuring trade performance solely against execution close prices while ignoring arrival midpoint slippage.
- Accepting published exchange liquidity metrics at face value without auditing real execution impact across size tiers.
- Ignoring transaction cost drag when evaluating high-frequency or medium-frequency trading strategies.

## Done checklist

- [ ] Arrival midpoint recorded for every routed order.
- [ ] Slippage computed and logged per fill execution report.
- [ ] Empirical impact curve inspected for flat slippage curve red flags.
- [ ] Net performance evaluated inclusive of fees and market impact.

## Sources

- Measuring Market Impact and Transaction Costs in Digital Asset Markets: https://www.nber.org/papers/w27431
- Empirical Analysis of Liquidity and Slippage Across Crypto Derivatives Exchanges: https://www.cambridge.org/core/journals/financial-markets-and-portfolio-management
