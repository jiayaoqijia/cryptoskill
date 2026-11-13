---
name: sample-and-regime
domain: crypto-trading/sample-and-regime
trigger: "How to evaluate sample size adequacy, regime heterogeneity, and subcritical cascade limits in backtesting."
anti_trigger: "Not for executing trades or managing live operational risk limits."
scope: "Regime heterogeneity (herd vs arbitrage regimes with identical distributions), sample size vs effect size, the one-year/five-ticker limits, and subcriticality's implication."
status: seedling
---

## Standard

Backtest validity depends on sample size adequacy and regime stationarity. A model evaluated across a homogeneous market regime will fail catastrophically when deployed into a distinct structural regime (e.g., liquidity contraction, high-stress liquidation cascade, or panic-driven herd behavior), even if return distributions appear statistically identical on aggregate. Regime heterogeneity introduces hidden parameter instability where alpha decays rapidly as market microstructure shifts. Furthermore, insufficient sample sizes relative to effect sizes lead to extreme estimation error and false confidence.

Empirical studies, such as arXiv 2605.16895 ("Alpha Illusion"), demonstrate that published strategies collapse when subjected to broader sample windows, shrinking from apparent high Sharpe ratios to levels below buy-and-hold benchmarks once transaction costs and regime shifts are accounted for. In crypto derivatives markets, forensic analyses reveal that liquidation branching ratios ($\hat{\lambda}$) hover between 0.1 and 0.2—indicating a deeply subcritical process where self-sustaining avalanches do not exist. Consequently, backtests attempting to simulate endogenous liquidity cascades using stationary stochastic processes fail because the underlying physical phenomenon is transient, subcritical, and non-stationary.

Primary sources for the claims in this section: <https://arxiv.org/abs/2605.16895> and <https://doi.org/10.2307/1912559>.

## Decision rules

1. Every backtest must explicitly define and test performance across at least three distinct historical market regimes (e.g., high volatility/liquidation, consolidation, and directional trend). If performance is driven by a single regime, the strategy is regime-dependent.
2. Sample sizes must satisfy statistical power requirements; backtests spanning less than three full market cycles or restricted to narrow asset baskets (such as the one-year, five-ticker limitation identified in Alpha Illusion studies) must be rejected as inconclusive.
3. Strategies purporting to capture liquidity cascades must incorporate empirically validated subcritical branching ratios ($\hat{\lambda} \in [0.1, 0.2]$); models assuming supercritical cascade propagation ($\lambda \ge 1$) are physically invalid and must be rejected.
4. Stationarity tests (e.g., Augmented Dickey-Fuller, Chow tests) must be performed on strategy return streams across rolling sub-samples to detect structural decay.

## Procedure

1. Segment historical data into distinct volatility and liquidity regimes using Hidden Markov Models or volatility clustering thresholds.
2. Calculate strategy Sharpe ratios, drawdowns, and win rates independently within each regime segment.
3. Test for structural breaks in return generation across regime boundaries using Chow tests or rolling parameter stability metrics.
4. Evaluate sample size against minimum detectable effect size formulas to confirm adequate statistical power.
5. Cross-reference derivative market findings regarding subcritical branching ratios to ensure cascade simulation models do not rely on impossible self-reinforcing dynamics.

## Anti-patterns

- Assuming return distributions are stationary across major structural shifts in market structure, exchange rules, or macroeconomic interest rates.
- Simulating liquidation cascades as self-sustaining chain reactions with branching ratios $\ge 1.0$ in contradiction of empirical market forensics.
- Generalizing performance from a narrow sample of five tickers across a single year to an entire digital asset universe.

## Done checklist

- [ ] Regime segmentation performed across historical testing window.
- [ ] Strategy performance verified across multiple distinct market regimes.
- [ ] Sample size confirmed adequate for statistical power.
- [ ] Subcritical branching ratio constraints ($\hat{\lambda} \in [0.1, 0.2]$) applied to cascade simulations.
- [ ] Stationarity and structural break tests documented.

## Sources

- arXiv:2605.16895. Alpha Illusion: Evaluating the Limits of Quantitative Trading Strategies Across Limited Samples and Tickers. https://arxiv.org/abs/2605.16895
- Chow, G. C. (1960). Tests of Equality Between Sets of Coefficients in Two Linear Regressions. Econometrica, 28(3), 591-605. https://doi.org/10.2307/1910133
- Hamilton, J. D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle. Econometrica, 57(2), 357-384. https://doi.org/10.2307/1912559
- Open Science Framework (OSF). Research Design and Sample Adequacy Standards. https://osf.io/prereg/
