---
name: benchmark-selection
domain: investing/benchmark-selection
trigger: "Choosing or questioning the benchmark a result is measured against."
anti_trigger: "Not for predicting performance, and not for fund selection."
scope: "The policy benchmark, investable alternatives, and benchmark drift."
status: seedling
---

# Benchmark selection

## Standard

A benchmark answers the question "compared with what". The right one is determined by the policy the portfolio is meant to follow, not by whichever index the result happens to beat: a portfolio with a stated allocation should be measured against that allocation, weighted the same way, rebalanced the same way. A benchmark chosen after the fact is a description of the portfolio rather than a test of it.

Benchmark drift is the failure mode. Over time a portfolio's actual exposure can move away from the policy, and a benchmark that tracks the actual exposure will always look achievable; the comparison then measures nothing. The discipline is to hold the benchmark fixed to the policy and let the difference show as the result, rather than to redefine the benchmark until the difference disappears.

Primary sources: <https://www.cfainstitute.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the portfolio's stated policy and the benchmark that represents it.
- Record the benchmark's construction and whether it is investable.
- Record the rebalancing assumption built into the benchmark.
- Record any change to the benchmark and the reason, with a date.
- Record the tracking difference between the benchmark and the policy weights.
- Where no investable benchmark exists, record the gap and use a stated proxy.

## Procedure

1. State the policy the portfolio follows.
2. Select the benchmark that represents that policy.
3. Record its construction, weights, and rebalancing rule.
4. Compare current policy weights with benchmark weights.
5. Record any past changes to the benchmark and why.
6. Write the benchmark definition into the record with its date.

## Anti-patterns

- Choosing a benchmark after seeing the result.
- Using an index the portfolio could not actually hold.
- Changing the benchmark when performance disappoints.
- Ignoring the benchmark's rebalancing assumption.
- Measuring a multi-asset portfolio against a single equity index.

## Done checklist

- [ ] Policy stated.
- [ ] Benchmark selected and defined.
- [ ] Construction and rebalancing recorded.
- [ ] Weight differences recorded.
- [ ] Changes dated with reasons.
- [ ] Proxy recorded where no investable benchmark exists.

The other test is the benchmark's own behaviour: a benchmark whose volatility and drawdown differ materially from the portfolio's will produce tracking error that reflects the mismatch rather than the decisions, and a portfolio measured against it will appear to have taken risk it did not take.


## Sources

- Investment performance and benchmark standards: <https://www.cfainstitute.org/>
- Investor education on benchmarks: <https://www.investor.gov/introduction-investing>
- Index and market data: <https://fred.stlouisfed.org/>
