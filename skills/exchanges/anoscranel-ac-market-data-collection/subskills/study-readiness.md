---
name: study-readiness
domain: crypto-trading/study-readiness
trigger: "The checklist before a study runs: window arithmetic (e.g. 31 days of print history -> earliest valid date), the pre-registered test (42 cells, Bonferroni, placebo), and the rule that a collector is finished when the study can run without you."
anti_trigger: "Not for the analysis itself, not for the trade record or risk budget."
scope: "The checklist before a study runs: window arithmetic (e.g. 31 days of print history -> earliest valid date), the pre-registered test (42 cells, Bonferroni, placebo), and the rule that a collector is finished when the study can run without you."
status: seedling
---

# Study Readiness

## Standard
Before launching an empirical study or statistical test on collected market data, researchers must complete a formal study-readiness audit. This audit verifies window arithmetic (e.g., ensuring a 31-day study window has fully accumulated 31 days of historical print history before execution), confirms zero temporal gaps, validates point-in-time universe coverage, and ensures the data collector operates autonomously without human intervention.

Primary sources for the claims in this step: <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api> and <https://binance-docs.github.io/apidocs/futures/en/>.

## Decision rules
- **Window arithmetic verification:** The earliest valid analysis date must equal `collection_start_date + required_lookback_window`, ensuring no boundary truncation artifacts.
- **Pre-registered testing protocol:** Statistical parameters, including significance thresholds (e.g., Bonferroni corrected $\alpha = 0.00119$), hypothesis definitions, and placebo tests, must be locked before running queries against the corpus.
- **Collector autonomy gate:** A data collection pipeline is officially ready for study consumption only when it runs unattended via automated daemon schedulers without manual intervention.
- **Completeness sign-off:** Empirical studies cannot commence if data completeness falls below 99.9% across the target temporal window.

## Procedure
1. Review study pre-registration documents and extract required lookback windows, sample sizes, and venue inclusions.
2. Execute automated readiness verification scripts against the storage corpus to confirm date range coverage and boundary arithmetic.
3. Verify that watermark logs confirm continuous ingestion up to the current operational time minus maximum allowable latency.
4. Run gap-detection and survivorship-bias audits across the selected sample subset, documenting any identified anomalies.
5. Confirm that statistical testing scripts reference pre-registered alpha levels and correction methods without exploratory p-hacking.
6. Generate a signed Study Readiness Report certifying that the dataset and pipeline meet all operational standards.

## Anti-patterns
- **Premature analysis:** Commencing statistical studies before data collection windows have fully matured, leading to truncated sample bias.
- **Unverified lookbacks:** Assuming historical depth is sufficient without inspecting earliest available partition timestamps.
- **Moving goalposts:** Adjusting statistical significance thresholds or Bonferroni corrections after observing initial analytical outputs.
- **Manual dependency:** Relying on human operators to manually trigger data collection scripts daily rather than deploying robust automated daemons.

## Done checklist
- [ ] Window arithmetic confirms complete historical lookback depth without boundary truncation.
- [ ] Automated readiness scripts verify zero temporal gaps and 99.9% minimum data completeness.
- [ ] Statistical testing parameters and Bonferroni thresholds are pre-registered prior to query execution.
- [ ] Collector daemon operates fully autonomously under scheduled automation.

## Sources
- Stanford University. (2026). Pre-registration principles in empirical research and statistical analysis. Retrieved from https://osf.io/prereg/
- Python Software Foundation. (2026). Date and time arithmetic in Python (`datetime`). Retrieved from https://docs.python.org/3/library/datetime.html
- Binance API Documentation. (2026). Historical data completeness and API retrieval validation. Retrieved from https://binance-docs.github.io/apidocs/futures/en/
- Hyperliquid API Documentation. (2026). Managing historical API endpoints for empirical backtesting. Retrieved from https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api
