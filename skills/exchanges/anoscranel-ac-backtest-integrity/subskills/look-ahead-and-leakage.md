---
name: look-ahead-and-leakage
domain: crypto-trading/look-ahead-and-leakage
trigger: "How to audit backtests for look-ahead bias, information leakage, survivorship bias, and point-in-time violations."
anti_trigger: "Not for implementing live execution algorithms or database querying scripts."
scope: "Point-in-time discipline (universe, restatements, feature availability), survivorship, and how a single leaked feature invalidates a backtest."
status: seedling
---

## Standard

Look-ahead bias and information leakage occur when a backtest utilizes data, parameters, or structural knowledge from the future that would not have been available in real time. In quantitative finance, such leakage destroys backtest validity, turning random trading rules into seemingly infallible strategies. Leakage manifests through global normalization procedures, incorrect timestamp alignment, corporate action restatements, or survivorship bias where failed or bankrupt entities are omitted from historical asset universes.

Point-in-time discipline requires that every feature and universe constituent be reconstructed strictly as it existed at the exact clock time of decision execution. Survivorship bias distorts historical samples by censoring failed entities, artificially inflating historical returns. Furthermore, information leakage from machine learning target encoding or cross-validation temporal boundary breaches invalidates performance metrics instantly. A single leaked feature corrupts the entire analytical pipeline, rendering performance metrics completely void.

Primary sources for the claims in this section: <https://doi.org/10.1111/j.1540-6261.1995.tb05171.x> and <https://doi.org/10.1016/0304-405X(81>.

## Decision rules

1. Every feature and signal used in a backtest must be timestamped with explicit verification that underlying data was published and accessible prior to signal generation.
2. The trading universe must be point-in-time accurate, including all delisted, bankrupt, or inactive assets that existed historically during each testing window, preventing survivorship bias.
3. Global transformations (such as min-max scaling, Z-score standardization, or PCA fitting) must be computed strictly on expanding historical windows, never using full-sample statistics.
4. If a single instance of look-ahead bias or information leakage is discovered in a feature pipeline, the entire backtest must be invalidated and all results discarded pending refactoring.

## Procedure

1. Audit every feature extraction script and query to verify timestamp alignment, ensuring bar completion times precede execution timestamps.
2. Inspect normalization and feature engineering functions to confirm parameters are derived exclusively from historical data available up to time $t-1$.
3. Verify asset universe inclusion lists against historical exchange directories to ensure delisted instruments are present in past windows.
4. Conduct a label-leakage test by shuffling future targets and verifying that model performance collapses to zero; any non-zero performance indicates leakage.
5. Review transaction logging to ensure order placement uses prevailing order book state at time $t$, rather than post-facto averages.

## Anti-patterns

- Standardizing an entire multi-year price series using standard deviation computed across the entire dataset prior to train-test splitting.
- Using survivorship-biased asset lists downloaded from current exchange APIs without incorporating historical constituent changes.
- Aligning daily closing prices with trading signals generated using closing data without verifying time zones and exact settlement timestamps.
- Permitting machine learning pipelines to perform feature selection using cross-validation splits that interleave future data into past folds.

## Done checklist

- [ ] Feature timestamps verified for real-time availability.
- [ ] Asset universe includes historical delisted entities (survivorship audit passed).
- [ ] Global scaling replaced with rolling or expanding window transformations.
- [ ] Label leakage test executed with performance collapsing to zero.
- [ ] Zero future data dependencies confirmed across all ingestion scripts.

## Sources

- Banz, R. W. (1981). The Relationship Between Return and Market Value of Common Stocks. Journal of Financial Economics, 9(3), 3-18. https://doi.org/10.1016/0304-405X(81)90018-0
- Kothari, S. P., Shanken, J., & Sloan, R. G. (1995). Another Look at the Cross-Section of Expected Stock Returns. Journal of Finance, 50(1), 185-224. https://doi.org/10.1111/j.1540-6261.1995.tb05171.x
- Open Science Framework (OSF). Transparent Research Documentation and Data Integrity. https://osf.io/prereg/
- National Institute of Standards and Technology (NIST). Software Verification and Validation Guidance. https://www.nist.gov/
