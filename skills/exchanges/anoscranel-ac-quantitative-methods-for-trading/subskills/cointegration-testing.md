---
name: cointegration-testing
domain: crypto-trading/cointegration-testing
trigger: "Testing whether two series can underpin a spread trade."
anti_trigger: "Not for predicting convergence timing, and not for backtest validation."
scope: "Tests, in-sample traps, and what a passing test does and does not license."
status: seedling
---

# Cointegration testing

## Standard

Cointegration is the statistical property that makes a pairs spread legal to trade: two non-stationary prices whose *combination* is stationary. A test asks whether the residual of one series regressed on the other wanders like a random walk or reverts toward zero. Only the second licenses a mean-reversion trade on the spread; correlation, which measures co-movement, licenses nothing about reversion.

The traps are mostly statistical honesty. The test has a null of no cointegration, so a failure to reject is not evidence of its presence; a regression-based hedge ratio introduces bias that the basic test does not correct (an enhanced test does); and searching many pairs for a passing test guarantees false positives, because a five-percent significance level repeated over a hundred pairs produces five lucky ones. Out-of-sample confirmation is the only honest answer to search bias.

Primary sources: <https://quant.stackexchange.com/> and <https://www.quantconnect.com/docs/>.

## Decision rules

- Record the test used, its null, and its p-value, not just pass or fail.
- Use the enhanced test when the hedge ratio is estimated from the same data.
- Record how many pairs were tested before this one was chosen.
- Require an out-of-sample window to confirm, and record its result.
- Record the test's assumptions about constants and trends, which change the answer.
- State the staleness of the relationship: when was it last confirmed?

## Procedure

1. Run the chosen test and record the statistic and p-value.
2. Record the hedge-ratio estimation method and the bias correction used.
3. Record the search: how many candidates were examined in total.
4. Hold out a window and re-test; record the result.
5. Note the specification choices (constant, trend, lag length).
6. Date the confirmation and set a re-test trigger.

## Anti-patterns

- Reading correlation as cointegration.
- Reporting pass or fail without the p-value and specification.
- Skipping the enhanced correction when the ratio is estimated from the same sample.
- Selecting the best pair from a large search and treating it as independently significant.
- Never re-testing after months of live trading.

## Done checklist

- [ ] Test, statistic, and p-value recorded.
- [ ] Bias correction applied and recorded.
- [ ] Search breadth recorded.
- [ ] Out-of-sample confirmation recorded.
- [ ] Specification choices recorded.
- [ ] Re-test trigger dated.

A further discipline is the direction of the test: because the null is no-cointegration, a small sample can fail to reject simply because it lacks power, and a large sample rejects trivially. The record should state the sample size beside the p-value, since the same statistic means different things at sixty observations than at six hundred.

## Sources

- Cointegration methods discussion: <https://quant.stackexchange.com/>
- Implementation references and examples: <https://www.quantconnect.com/docs/>
- Statistical background: <https://en.wikipedia.org/wiki/Cointegration>
