# 04 — Risk, Correlation and Risk Budget

## Purpose

Measure the portfolio’s loss potential, the dependencies that make diversification fail, and whether the risk fits the mandate. VaR is one input, not a verdict.

## Inputs

- Daily or weekly return series for each position; at least 90 observations, preferably 365.
- Portfolio weights; rebalancing history.
- Benchmark (BTC, policy portfolio, or total market).
- Risk limits: max drawdown, position limit, scenario limit, stop-loss policy.

## Method

1. Build the return series from dated marks.
2. Compute volatility and drawdown.
3. Compute historical VaR/CVaR at a stated level.
4. Compute beta and correlation against the benchmark.
5. Compare with the IPS-lite limits.
6. Run stress and reverse stress.
7. Report method, window, and limitations.

## Core measures

### Volatility

Use sample standard deviation of periodic returns, annualized only when the period is known:

`σ_annual = σ_period × √periods_per_year`

For daily data, `√365`; for weekly, `√52`. State the window and whether returns are simple or log.

### Maximum drawdown

`MDD = min_t (V_t / peak_t − 1)`

Report peak date, trough date, and recovery time if recovered.

### Historical VaR and CVaR

At confidence `c` (e.g., 95%):

- `VaR_c` = the loss at the `1−c` quantile of the historical portfolio return distribution.
- `CVaR_c` = the average loss conditional on exceeding VaR.

Report in currency and % of portfolio; state window, confidence, and that history may not repeat.

### Beta and correlation

- Beta vs benchmark: `β = Cov(R_p, R_b) / Var(R_b)`.
- Correlation: Pearson for linear dependence; note that crypto tails can be nonlinear.
- Compute over a stated window and a rolling window; report instability.

## Risk budget and limits

Translate the IPS-lite into:

- **Position limit:** maximum weight per asset/subnet.
- **Cluster limit:** maximum weight per chain, stablecoin, protocol, or validator cluster.
- **Scenario limit:** maximum acceptable loss in a named scenario.
- **Stop-loss policy:** pre-defined review trigger, not an automatic market order.
- **Risk contribution:** each position’s share of portfolio volatility or CVaR; do not assume weight equals risk.

## Stress and reverse stress

Required scenarios:

1. BTC −30%, ETH −40%, alts −50% to −70%.
2. Stablecoin depeg of 5% and 20%; redemption gate.
3. Bridge pause or chain halt for 7 days.
4. Correlation → 1 across the portfolio.
5. Liquidity haircut: exit only 25% of normal volume.
6. Reverse stress: find the combination of shocks that breaches the mandate’s loss floor.

Report portfolio loss, position contribution, first breached limit, and the failure shape.

## VaR limitations

- Underestimates extreme events and regime shifts.
- Ignores liquidity and exit costs.
- Sensitive to window, confidence level, and correlation assumptions.
- Can be gamed by illiquid marks and stale prices.
- Is not a worst-case loss.

Use CVaR, stress, reverse stress, and liquidity stress alongside it. Never present VaR as “the maximum loss.”

## Output

| Measure | Value | Window | Method | Limitation |
|---|---:|---|---|---|
| Annualized volatility | X% | 365d | Historical | Past regime |
| Max drawdown | X% | Since inception | Daily marks | Stale prices |
| VaR 95% 1d | $X / X% | 365d | Historical | Tail underestimation |
| CVaR 95% 1d | $X / X% | 365d | Historical | Sparse tail |
| Beta vs BTC | X | 365d | OLS | Regime-dependent |
| Top risk contribution | X% | 365d | Component CVaR | Model-dependent |

## Failure modes

- Using parametric normal VaR on heavy-tailed crypto returns as the only risk measure.
- Reporting volatility without the window.
- Treating correlation as stable.
- Ignoring liquidity in the loss estimate.
- Using a stop-loss as a substitute for position sizing.

## Sources

- CFA Institute, *Measuring and Managing Market Risk* (2026).
- CFA Institute, *Introduction to Risk Management* (2026).
- arXiv 2507.08915, *Quantifying Crypto Portfolio Risk* (2025).
