---
name: multiple-testing
domain: crypto-trading/multiple-testing
trigger: "How to correct for multiple testing, data snooping, and inflated Sharpe ratios in trading strategies."
anti_trigger: "Not for collecting market data or calculating raw descriptive statistics."
scope: "How many trials actually happened; deflated Sharpe; Harvey-Liu haircuts; White's Reality Check; the 42-cell/41-window arithmetic as a worked example."
status: seedling
---

## Standard

Multiple testing and data snooping occur when a researcher evaluates numerous trading rules or parameter combinations over the same historical dataset, selecting only top performers for deployment. Without adjustment, apparent predictive power is an artifact of random noise rather than true structural edge. The probability of discovering a false positive increases monotonically with trial counts. In quantitative finance, this manifests as inflated Sharpe ratios and catastrophic out-of-sample failure. 

To maintain statistical integrity, backtest evaluation must account for familywise error rates across all unrecorded trials. Bailey and López de Prado formalize this via the Deflated Sharpe Ratio (DSR), which adjusts the maximum observed Sharpe ratio for trial counts, skewness, kurtosis, and sample length. Similarly, Harvey and Liu provide haircut p-values, adjusting significance thresholds downward as specification tests multiply. White's Reality Check provides a bootstrap framework to test whether the best model among alternatives genuinely outperforms a benchmark.

Primary sources for the claims in this section: <https://doi.org/10.3905/jpm.2014.40.5.094> and <https://doi.org/10.3905/jpm.2015.42.1.013>.

## Decision rules

1. Any backtest derived from parameter grid searches must report total trials $N$, and Sharpe ratios must be adjusted using the Deflated Sharpe Ratio (DSR) or Harvey-Liu haircuts. If $N$ is unknown, the strategy fails audit immediately.
2. The Bonferroni correction must be applied when evaluating multiple independent cells or windows. For example, in a 42-cell parameter sweep with an unadjusted significance level of $\alpha = 0.05$, a Bonferroni-corrected threshold of $\alpha_{corr} = 0.05 / 42 \approx 0.00119$ is required, lifting correlation ρ across approximately 41 independent rolling windows.
3. If White's Reality Check bootstrap p-value exceeds 0.05 under full trial history, the null hypothesis of no superior predictive ability cannot be rejected, and the strategy must be abandoned.
4. No strategy may be evaluated using only in-sample optimal parameters if alternative parameters were tested without inclusion in trial count $N$.

## Procedure

1. Inventory every parameter combination and feature extraction iteration executed during research to establish exact trial count $N$.
2. Compute unadjusted Sharpe ratio ($SR_0$), sample skewness ($\gamma_3$), and kurtosis ($\gamma_4$) over backtest period length $T$.
3. Apply the Deflated Sharpe Ratio formula incorporating $N$, $T$, $\gamma_3$, and $\gamma_4$ to derive the probability of positive true Sharpe.
4. Execute White's Reality Check or Harvey-Liu multiple-testing adjustment using bootstrap re-sampling of strategy versus benchmark returns across all $N$ trials.
5. Compare adjusted p-value against corrected threshold ($\alpha = 0.00119$ for 42 cells).
6. Document unadjusted versus adjusted metrics in the strategy validation log.

## Anti-patterns

- Assuming cross-validation on a single train-test split exempts research from multiple-testing penalties when hyperparameter tuning occurred over hundreds of iterations.
- Treating backtests as independent experiments when sequential trial-and-error was guided by intermediate evaluation performance.
- Using standard significance thresholds ($\alpha = 0.05$) on strategies selected from large combinatorial search spaces without correction.

## Done checklist

- [ ] Exact trial count $N$ documented and included in evaluation.
- [ ] Deflated Sharpe Ratio (DSR) calculated and recorded.
- [ ] Harvey-Liu haircut or White's Reality Check bootstrap executed.
- [ ] Bonferroni-corrected significance threshold applied to multi-cell sweeps.
- [ ] Strategy rejected if adjusted p-value exceeds significance threshold.

## Sources

- Bailey, D. H., & López de Prado, M. (2014). The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Nper. Journal of Portfolio Management, 40(5), 94-107. https://doi.org/10.3905/jpm.2014.40.5.094
- Harvey, C. R., & Liu, Y. (2015). Backtesting. Journal of Portfolio Management, 42(1), 13-28. https://doi.org/10.3905/jpm.2015.42.1.013
- White, H. (2000). A Reality Check for Data Snooping. Econometrica, 68(5), 1097-1126. https://doi.org/10.1111/1468-0262.00152
- Open Science Framework (OSF). Pre-Registration Standards and Guidelines. https://osf.io/prereg/
