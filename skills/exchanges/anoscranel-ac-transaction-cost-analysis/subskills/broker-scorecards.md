---
name: broker-scorecards
domain: investing/broker-scorecards
trigger: "Scoring brokers on evidence rather than on relationship."
anti_trigger: "Not for choosing a broker for custody, and not for predicting performance."
scope: "Scoring brokers and venues on evidence, and the sample size problem."
status: seedling
---

# Broker scorecards

## Standard

A scorecard converts execution data into a comparison across brokers, and the first problem is sample size. A strategy trading a few times a week produces, per broker, a handful of observations per quarter, and the difference between two brokers is frequently smaller than the dispersion of costs within each. A scorecard that ranks them anyway is reporting noise as a finding.

The second problem is selection. Brokers receive different orders: the difficult ones, the illiquid names, the urgent ones, are not distributed evenly, and a broker that receives only easy flow will score well without being better. A scorecard that does not normalise for order difficulty is a measure of what the broker was given rather than of what it did.

Primary sources: <https://www.cfainstitute.org/> and <https://www.finra.org/>.

## Decision rules

- Record the number of observations per broker and per category.
- Record the normalisation applied for order size, liquidity, and urgency.
- Record the metric used and its benchmark.
- Record the confidence interval or dispersion around each broker's figure.
- Record the period and whether it includes unusual market conditions.
- Where the sample is too small, record the ranking as indicative rather than conclusive.

## Procedure

1. Collect execution data by broker and order characteristics.
2. Group orders into comparable categories.
3. Compute the metric per broker within each category.
4. Record the dispersion and the count.
5. Normalise or stratify before ranking.
6. Write the scorecard with its confidence stated.

## Anti-patterns

- Ranking brokers on raw averages across unmatched order types.
- Ignoring the number of observations behind each figure.
- Normalising only for size and not for urgency.
- Treating a one-quarter ranking as a durable judgement.
- Scoring on relationship or on research received rather than on execution.

## Done checklist

- [ ] Observations counted per broker.
- [ ] Normalisation recorded.
- [ ] Metric and benchmark recorded.
- [ ] Dispersion recorded.
- [ ] Period recorded.
- [ ] Confidence stated.

A further refinement is to score on the relationship between cost and the difficulty the broker faced, rather than on cost alone: a broker that pays eight basis points on easy flow and twelve on hard flow may be better than one that pays ten on both, because the second is either mispricing the easy orders or being given only the hard ones. Plotting cost against difficulty for each broker turns a ranking into a diagnosis.

## Sources

- Trading and performance standards: <https://www.cfainstitute.org/>
- Execution quality and market practice: <https://www.finra.org/>
- Market structure context: <https://www.sec.gov/investor>
