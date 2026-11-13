---
name: severity-calibration
domain: investing/severity-calibration
trigger: "Choosing how severe a stress scenario should be."
anti_trigger: "Not for predicting severity, and not for risk budgeting."
scope: "Choosing how severe a scenario should be, and defending the choice."
status: seedling
---

# Severity calibration

## Standard

Severity is a choice, and it is the parameter most likely to be set to produce a comfortable result. Too mild and the test confirms what was already believed; too extreme and the result is dismissed as implausible, which is a way of avoiding the question. The defensible approach anchors severity to the historical distribution and then states explicitly where the chosen scenario sits within it.

The anchor can be a percentile, a multiple of the worst observed episode, or a loss corresponding to a stated frequency. Whichever is used, the record should state it so that a later reviewer can tell whether the scenario was severe relative to a fixed standard or relative to the portfolio's current circumstances, and whether the standard has moved.

Primary sources: <https://www.bis.org/> and <https://fred.stlouisfed.org/>.

## Decision rules

- Record the severity metric: loss percentage, currency amount, or a factor move.
- Record the historical distribution and the chosen scenario's position within it.
- Record whether severity is fixed across reviews or recalculated.
- Record the rationale for the chosen level, referencing the distribution.
- Record the result at a milder and a harsher setting.
- Record what severity would be required to fail, from the reverse test.

## Procedure

1. Choose the severity metric.
2. Build the historical distribution.
3. Place the scenario within it.
4. State the rationale.
5. Run at three severities.
6. Record the comparison and the choice.

## Anti-patterns

- Choosing severity after seeing which one produces the preferred outcome.
- Using a scenario that is severe in one asset class and mild in another.
- Changing the severity standard between reviews without noting it.
- Treating the worst historical episode as a bound.
- Reporting a single severity without the distribution context.

## Done checklist

- [ ] Severity metric recorded.
- [ ] Historical distribution recorded.
- [ ] Scenario placed within it.
- [ ] Rationale stated.
- [ ] Three severities run.
- [ ] Comparison recorded.

The distribution itself should be recorded with its limitations: a short sample understates the tail, and a distribution built from a period of falling volatility will place today's scenario at an artificially extreme percentile, which is a reason to record the sample window alongside the percentile rather than the percentile alone.


Running the same scenario at three severities is the cheapest protection against a threshold chosen to produce a preferred answer, because the pattern across the three says more than any single result.


## Sources

- Stress testing principles: <https://www.bis.org/>
- Historical market data: <https://fred.stlouisfed.org/>
- Investor education on risk measurement: <https://www.investor.gov/introduction-investing>
