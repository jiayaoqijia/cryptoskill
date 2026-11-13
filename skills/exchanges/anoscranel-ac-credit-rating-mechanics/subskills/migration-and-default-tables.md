---
name: migration-and-default-tables
domain: investing/migration-and-default-tables
trigger: "Reading a transition matrix or a default study without over-reading it."
anti_trigger: "Not for predicting a specific default, and not for pricing a credit."
scope: "Transition matrices, default rates, and how to read them honestly."
status: seedling
---

# Migration and default tables

## Standard

A transition matrix reports the historical frequency with which issuers moved from one rating to another over a stated horizon, and a default study reports the frequency of default by rating and horizon. Both are useful and both are easy to misread: the frequencies are sample averages over a period, they are dominated by a small number of stressed years, and the sample thins quickly at the highest ratings where defaults are rare.

The honest reading states the period, the population, and the sample size. A default rate of zero for the top category over ten years is not a probability of zero; it is the absence of an observation in a sample too small to distinguish zero from a fraction of a percent. The same discipline applies to migration: a rating that has historically been stable may simply not have been tested in the conditions that would move it.

Primary sources: <https://www.sec.gov/investor> and <https://www.nber.org/>.

## Decision rules

- Record the study period, the population, and the sample size.
- Record the horizon over which the rates are stated.
- Record the number of observations in the cell being used.
- Record whether the period includes a stress episode.
- Record the difference between issuer-weighted and volume-weighted rates.
- Where a cell has few observations, record the confidence as low.

## Procedure

1. Record the source, period, and population.
2. Record the horizon and the cell being used.
3. Record the observation count for that cell.
4. Record whether stress years are included.
5. Compare issuer-weighted with volume-weighted where both exist.
6. Write the reading with its confidence.

## Anti-patterns

- Treating a historical frequency as a probability for a specific issuer.
- Using a cell with almost no observations as an estimate.
- Ignoring the period's composition.
- Mixing issuer-weighted and volume-weighted figures.
- Assuming stability observed is stability possible.

## Done checklist

- [ ] Source and period recorded.
- [ ] Horizon recorded.
- [ ] Observation count recorded.
- [ ] Stress inclusion recorded.
- [ ] Weighting method recorded.
- [ ] Confidence stated.

A further caution is that transition matrices are built from rated issuers only: the population excludes everything that was never rated, which is a large and systematically different set, so a matrix describes the behaviour of the rated universe rather than of credit in general, and a portfolio holding unrated debt is not described by it at all.

## Sources

- Rating agency default and transition studies: <https://www.sec.gov/investor>
- Research on credit risk: <https://www.nber.org/>
- Regulatory capital data on ratings: <https://www.bis.org/>
