---
name: vwap-and-participation-benchmarks
domain: investing/vwap-and-participation-benchmarks
trigger: "Choosing a benchmark that does not make the execution look better than it was."
anti_trigger: "Not for predicting prices, and not for broker selection."
scope: "VWAP, participation rate, and the benchmarks that flatter a strategy."
status: seedling
---

# VWAP and participation benchmarks

## Standard

VWAP compares the average price achieved against the volume-weighted average price over a window. It is easy to compute and widely reported, and it is the benchmark most likely to flatter: an order that is a small fraction of volume will often beat VWAP simply because it does not move the price, and an order that trades patiently can beat VWAP while still having cost the portfolio money through delay.

Participation rate benchmarking asks a different question: what share of the volume the order represented, and whether that share was consistent with the urgency the strategy required. A high participation rate is not a failure if the signal was decaying; a low one is not a success if the position was not established in time. The record should state which question the benchmark answers before presenting it as a cost.

Primary sources: <https://www.cfainstitute.org/> and <https://www.finra.org/>.

## Decision rules

- Record the benchmark used and the window over which it was computed.
- Record the order's participation rate against the volume in that window.
- Record the strategy's urgency and whether the benchmark reflects it.
- Record the sign and size of the deviation, not only the average.
- Record the sample period and the instrument types included.
- Where VWAP is used, record that it excludes the delay and opportunity cost.

## Procedure

1. Record the benchmark and its window.
2. Compute the achieved price and the benchmark price.
3. Compute the deviation in basis points.
4. Record the participation rate over the same window.
5. Record the strategy's stated urgency.
6. Write the benchmark summary with its limitation.

## Anti-patterns

- Reporting VWAP as total cost.
- Comparing participation rates across strategies with different urgency.
- Ignoring the delay cost that a favourable VWAP conceals.
- Averaging deviations without the distribution.
- Using a benchmark window chosen after the fact.

## Done checklist

- [ ] Benchmark and window recorded.
- [ ] Deviation computed in basis points.
- [ ] Participation rate recorded.
- [ ] Urgency recorded.
- [ ] Sample recorded.
- [ ] Limitation stated.

A further trap is benchmark choice after the fact: a window selected because it flatters the fill is a benchmark that measures the choice rather than the execution, and the window should be fixed by the order's own schedule rather than by what the data shows afterwards.

## Sources

- Trading and performance standards: <https://www.cfainstitute.org/>
- Execution quality and market practice: <https://www.finra.org/>
- Market structure context: <https://www.sec.gov/investor>
