---
name: verdict-and-kill
domain: crypto-trading/verdict-and-kill
trigger: "How to define strategy kill rules, document audit verdicts, and enforce re-registration barriers for failed strategies."
anti_trigger: "Not for deploying trading algorithms or overriding risk management protocols."
scope: "The decision rule that kills a strategy, documenting the kill, and the conditions under which a killed strategy may be revisited (new data, new pre-registration — never a re-run on the same sample)."
status: seedling
---

## Standard

A disciplined quantitative research desk is defined by its willingness to terminate unviable strategies. Strategy validation must culminate in an objective, binary verdict: PROCEED or KILL. The decision to kill a strategy must be governed by pre-registered, immutable criteria rather than subjective intuition or emotional attachment to a research hypothesis. When a backtest fails to clear multiple-testing thresholds (e.g., Deflated Sharpe Ratio < 0.95, failure against shifted-placebo nulls, or negative net alpha after realistic transaction costs and slippage), the strategy must be immediately and permanently terminated for the given sample and specification.

To prevent confirmation bias and recursive data snooping, a killed strategy may never be re-run, tweaked, or optimized on the same historical sample. Re-visiting a terminated concept is permitted only under strict boundary conditions: either (a) an entirely new out-of-sample temporal period has elapsed (e.g., a subsequent live trading window), or (b) a fundamentally new structural mechanism or data source is introduced, accompanied by a fresh, independent pre-registration. Documenting strategy kills in an immutable audit ledger ensures institutional memory and prevents wasted computational and capital resources on exhausted alpha hypotheses.

Primary sources for the claims in this section: <https://www.press.uchicago.edu/ucp/books/book/chicago/S/bo17937401.html> and <https://doi.org/10.4324/9780203994641>.

## Decision rules

1. Every backtest audit must conclude with an explicit binary verdict: PROCEED or KILL, determined strictly by pre-registered numerical thresholds.
2. Any strategy failing multiple-testing adjustment, cost hurdle, or placebo null comparison must receive an immediate KILL verdict, halting further optimization on that dataset.
3. A killed strategy is permanently barred from being re-optimized or re-run on the same historical sample. Any subsequent test requires a completely new out-of-sample period or a fundamentally new mechanism with a fresh pre-registration.
4. Audit verdicts and underlying metric failures must be logged in the permanent research repository, ensuring complete transparency and accountability.

## Procedure

1. Evaluate final post-cost metrics against pre-registered success criteria (DSR, Sharpe, Max Drawdown, Placebo rejection).
2. If any primary threshold is breached, issue a formal KILL verdict document detailing exact statistical failure points.
3. Archive complete backtest code, execution logs, and audit report in immutable vault storage with status set to deprecated/killed.
4. Enforce repository-level blocks preventing execution scripts from being rerun on the same dataset.
5. If a conceptual revision is proposed later, verify that conditions require a new temporal dataset and a brand-new pre-registration.

## Anti-patterns

- Modifying threshold criteria post-hoc to rescue a failing strategy from a KILL verdict ("let's lower the Sharpe cutoff to 0.8").
- Rerunning a killed strategy with minor parameter tweaks on the same historical sample in hopes of achieving statistical significance.
- Failing to document rationale for strategy termination, leading to repeated research into already-disproven ideas.
- Treating a KILL verdict as a temporary setback rather than a definitive scientific falsification of the trading hypothesis.

## Done checklist

- [ ] Binary audit verdict (PROCEED or KILL) issued based on pre-registered rules.
- [ ] KILL rationale documented with specific metric failures (DSR, costs, placebo).
- [ ] Strategy code and audit report archived in immutable storage.
- [ ] Re-run ban enforced on original historical sample.
- [ ] Permanent research ledger updated.

## Sources

- Popper, K. (1959). The Logic of Scientific Discovery. Routledge. https://doi.org/10.4324/9780203994641
- Kuhn, T. S. (1962). The Structure of Scientific Revolutions. University of Chicago Press. https://www.press.uchicago.edu/ucp/books/book/chicago/S/bo17937401.html
- Open Science Framework (OSF). Research Archiving and Falsification Standards. https://osf.io/prereg/
- National Institute of Standards and Technology (NIST). Quality Assurance and Audit Documentation. https://www.nist.gov/
