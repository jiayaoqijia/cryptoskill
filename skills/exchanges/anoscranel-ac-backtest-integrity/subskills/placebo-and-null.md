---
name: placebo-and-null
domain: crypto-trading/placebo-and-null
trigger: "How to construct shifted placebos, permutation tests, bootstrap nulls, and avoid collider bias in backtesting."
anti_trigger: "Not for analyzing live exchange order books or executing manual discretionary trades."
scope: "Shifted placebos, permutation and bootstrap nulls, the collider problem (sample conditioned on its own outcome), and what a null must be able to reject."
status: seedling
---

## Standard

A rigorous backtest proves that observed performance cannot be replicated by random noise, data artifacts, or flawed experimental design. To establish this, quantitative researchers must test strategies against rigorous placebo models and empirical null distributions. Shifted-placebo tests—where entry signals are offset in time by arbitrary intervals while preserving return series properties—serve as a baseline test. If a shifted or randomized placebo strategy achieves comparable performance to the primary model, the original edge is spurious.

Furthermore, collider bias represents a severe threat to backtest validity. The collider problem occurs when a sample is conditioned on its own outcome—such as evaluating strategies only on assets that survived a specific exchange listing or filtering data based on post-hoc volatility thresholds. Conditioning on a collider induces spurious correlations between independent variables and target outcomes, creating phantom alpha. To prevent this, null models must be constructed via block bootstrap re-sampling, circular block permutation, and strict out-of-sample null generation, ensuring that the null hypothesis of zero true predictive power is thoroughly tested.

Primary sources for the claims in this section: <https://doi.org/10.1080/01621459.1994.10476870> and <https://doi.org/10.1017/CBO9780511803161>.

## Decision rules

1. Every quantitative strategy must be evaluated against at least two distinct null models: a shifted-placebo test and a block-bootstrap permutation test.
2. If a shifted-placebo or randomized null strategy yields a Sharpe ratio or cumulative return statistically indistinguishable from the primary strategy (p > 0.05), the strategy fails audit and must be rejected.
3. The evaluation sample must never be filtered using post-hoc criteria that condition the dataset on future outcomes, thereby avoiding collider bias.
4. The null model must be capable of rejecting false positives under conditions of heavy-tailed return distributions and volatility clustering typical of digital asset markets.

## Procedure

1. Generate a shifted-placebo series by lagging or leading strategy trading signals by a fixed non-zero offset (e.g., 24-hour shift).
2. Execute a circular block bootstrap on the underlying asset return series to create 1,000 synthetic price paths preserving autocorrelation and volatility clustering.
3. Run the complete strategy pipeline across all bootstrap paths to construct the empirical null distribution of Sharpe ratios.
4. Compare the actual strategy performance metric against the 95th and 99th percentiles of the empirical null distribution.
5. Check data ingestion filters to ensure no conditioning on colliders (such as selecting assets based on end-of-period outperformance).
6. Document placebo comparison results in the audit report.

## Anti-patterns

- Declaring a strategy successful without testing whether time-shifted or randomly scrambled signals achieve identical profitability.
- Conditioning dataset inclusion on assets that exhibited high liquidity or positive returns across the entire backtest window (collider bias).
- Using simple independent and identically distributed (IID) bootstrap re-sampling that destroys volatility clustering and temporal autocorrelation.
- Failing to establish an explicit null distribution prior to evaluating strategy optimization results.

## Done checklist

- [ ] Shifted-placebo test executed (signals offset in time).
- [ ] Circular block bootstrap null distribution generated (1,000+ paths).
- [ ] Actual strategy performance compared against 95th/99th null percentiles.
- [ ] Collider bias audited and eliminated from dataset filters.
- [ ] Strategy rejected if null hypothesis cannot be rejected.

## Sources

- Efron, B., & Tibshirani, R. J. (1993). An Introduction to the Bootstrap. Chapman and Hall/CRC. https://doi.org/10.1201/97804290246cb
- Pearl, J. (2009). Causality: Models, Reasoning, and Inference. Cambridge University Press. https://doi.org/10.1017/CBO9780511803161
- Politis, D. N., & Romano, J. P. (1994). The Stationary Bootstrap. Journal of the American Statistical Association, 89(428), 1303-1313. https://doi.org/10.1080/01621459.1994.10476870
- Open Science Framework (OSF). Statistical Validation and Null Hypothesis Testing. https://osf.io/prereg/
