---
name: pre-registration
domain: crypto-trading/pre-registration
trigger: "How to pre-register trading strategy hypotheses, testing windows, parameter grids, and decision rules before data inspection."
anti_trigger: "Not for executing ad-hoc exploratory data analysis or un-registered parameter tuning."
scope: "Fixing the analysis before the data: hypothesis, window, cells, test statistic, decision rule; the 42-cell/Bonferroni example; versioning the pre-registration."
status: seedling
---

## Standard

Pre-registration is the formal practice of locking and timestamping a research hypothesis, analytical pipeline, parameter grid, test statistic, and decision rule prior to observing, analyzing, or backtesting against the target dataset. In quantitative finance, unconstrained exploratory data analysis inevitably produces false discoveries that fail out-of-sample. Pre-registration serves as an epistemological firewall, cleanly separating exploratory data mining from confirmatory hypothesis testing. By committing to an immutable analytical plan in advance, researchers prevent p-hacking, selective reporting of optimal parameter combinations, and post-hoc hypothesis generation.

A robust pre-registration document must specify the exact asset universe, historical testing windows, parameter grids, evaluation metrics, and decision rules. For instance, in a multi-cell parameter sweep—such as a 42-cell grid evaluated across rolling windows—the pre-registration must explicitly declare the familywise error rate correction method (e.g., Bonferroni adjustment with $\alpha_{corr} = 0.05 / 42 \approx 0.00119$) and the precise threshold required to claim statistical significance. Any deviation from the pre-registered protocol during execution invalidates confirmatory status, requiring the iteration to be classified strictly as exploratory. Platforms such as the Open Science Framework (OSF) provide standardized registries for locking research protocols prior to empirical execution.

Primary sources for the claims in this section: <https://doi.org/10.1177/09567976611421272> and <https://doi.org/10.1073/pnas.1708276115>.

## Decision rules

1. No quantitative strategy may be submitted for live deployment consideration unless its complete testing protocol, parameter grid, and decision rules were pre-registered prior to data inspection.
2. The pre-registration document must explicitly define the exact asset universe, start and end dates, test statistics, and multiple-testing correction methods (such as Bonferroni thresholds for $N$-cell sweeps).
3. Any post-hoc modification to the parameter grid, feature set, or decision rules after observing backtest results requires re-registration and demotion of the experiment from confirmatory to exploratory status.
4. Version control and immutable timestamping (via git commit hashes or archival registries like OSF) are mandatory for all pre-registration documents.

## Procedure

1. Draft the strategy specification including economic rationale, formal mathematical hypothesis, asset universe, and historical timeframe.
2. Define the exhaustive parameter search space (e.g., exact 42-cell grid) and pre-calculate required multiple-testing significance thresholds (e.g., Bonferroni $\alpha_{corr}$).
3. Specify performance metrics (Sharpe ratio, max drawdown, DSR threshold) and definitive binary decision rules (proceed vs. kill).
4. Deposit the immutable protocol into an archiving system (OSF pre-registration or cryptographically hashed repository) prior to executing code against historical data.
5. Execute the backtest strictly adhering to the pre-registered script without manual parameter tweaking.
6. Compare final results against pre-registered criteria in the audit report.

## Anti-patterns

- Leaving parameter ranges open-ended or undefined in the protocol (e.g., "optimizing moving average lengths as appropriate").
- Changing the evaluation metric or sliding-window boundaries mid-backtest because initial results were subpar.
- Omitting multiple-testing corrections for multi-cell sweeps within the pre-registered protocol.

## Done checklist

- [ ] Pre-registration document created, hashed, and archived prior to data execution.
- [ ] Asset universe, timeframes, and parameter grids exhaustively defined.
- [ ] Multiple-testing correction thresholds (Bonferroni $\alpha_{corr}$) specified.
- [ ] Definitive binary decision rules established.
- [ ] Strict protocol adherence verified during audit.

## Sources

- Open Science Framework (OSF). Pre-Registration Protocols and Registration Standards. https://osf.io/prereg/
- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The Preregistration Revolution. Proceedings of the National Academy of Sciences, 115(11), 2600-2606. https://doi.org/10.1073/pnas.1708276115
- Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-Positive Psychology: Undisclosed Flexibility in Data Collection and Analysis Allows Presenting Anything as Significant. Psychological Science, 22(11), 1359-1366. https://doi.org/10.1177/09567976611421272
- National Institute of Standards and Technology (NIST). Scientific Integrity and Research Protocols. https://www.nist.gov/
