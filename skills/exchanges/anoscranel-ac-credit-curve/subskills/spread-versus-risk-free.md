---
name: spread-versus-risk-free
domain: investing/spread-versus-risk-free
trigger: "Separating credit spread from the risk-free curve that underlies it."
anti_trigger: "Not for predicting rates, and not for default modelling."
scope: "The credit curve as a spread over a curve that also moves."
status: seedling
---

# Spread versus risk-free

## Standard

A credit spread is measured over a benchmark risk-free curve at the same maturity, and both components move. When the risk-free curve shifts, the spread can stay unchanged while the all-in yield moves, and a position that appears to have gained or lost on credit may have moved entirely because of rates.

Separating the two requires recording the spread and the underlying at each observation. A trade that expresses a credit view should be structured so that the rate exposure is neutralised, typically by matching duration or by trading spread rather than yield. A trade that leaves the rate exposure in place is a combined view, and recording it as a credit view misattributes the result.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the spread and the risk-free level at each observation, with dates.
- Record the benchmark curve used and its maturity convention.
- Record whether the position is duration-neutral or carries rate exposure.
- Record the result decomposition: rate move versus spread move.
- Record any change in the benchmark, which changes the spread series.
- Where the benchmark is unavailable at a maturity, record the interpolation.

## Procedure

1. Record spreads alongside the benchmark at each point.
2. Note the benchmark and its convention.
3. Determine whether the position carries rate exposure.
4. Decompose the result into rate and spread components.
5. Record benchmark changes.
6. Write the separation summary.

## Anti-patterns

- Reading an all-in yield change as a credit move.
- Comparing spreads computed over different benchmarks.
- Leaving rate exposure in a trade described as a credit view.
- Ignoring a benchmark change that shifts the whole spread series.
- Assuming duration neutrality from matching notionals.

## Done checklist

- [ ] Spreads and benchmarks recorded.
- [ ] Convention noted.
- [ ] Rate exposure determined.
- [ ] Decomposition made.
- [ ] Benchmark changes recorded.
- [ ] Summary written.

A practical check is to revalue the position holding spreads constant and letting the benchmark move: if the result changes materially, the position carries rate exposure that a credit view did not intend, and that finding is more useful than the attribution afterwards.


The distinction also determines which benchmark a review should use: a position evaluated against a stale benchmark can show a spread gain that is entirely a rate move on a curve that has shifted since the position was opened.


## Sources

- Credit and rate market conventions: <https://www.isda.org/>
- Benchmark rates and yields: <https://www.federalreserve.gov/>
- Rate series: <https://fred.stlouisfed.org/>
