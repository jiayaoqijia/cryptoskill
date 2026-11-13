---
name: scenario-construction
domain: investing/scenario-construction
trigger: "Building a scenario that is coherent across asset classes."
anti_trigger: "Not for predicting the scenario, and not for portfolio construction."
scope: "Building a scenario that is coherent across asset classes."
status: seedling
---

# Scenario construction

## Standard

A scenario is coherent when its moves are consistent with a single mechanism. A rise in rates that is accompanied by a fall in the currency and a widening of credit spreads describes a specific state of the world; a set of moves assembled from different episodes does not describe anything, and the portfolio's response to it is not informative because no such combination has a cause.

Coherence is what makes the result interpretable. If the scenario has a mechanism, the portfolio's response can be traced to the exposures that mechanism touches, and the finding is about those exposures rather than about an arbitrary set of numbers. The record should state the mechanism in one sentence before the moves are listed.

Primary sources: <https://www.bis.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the mechanism the scenario describes, in one sentence.
- Record the moves per asset class and show how each follows from the mechanism.
- Record the time horizon over which the moves occur.
- Record which variables are held fixed and why.
- Record any move that is included for prudence rather than for coherence, and label it.
- Record the scenario's severity against the historical distribution.

## Procedure

1. State the mechanism.
2. Derive the moves from it per asset class.
3. Set the horizon.
4. Record the fixed variables.
5. Label any prudence adjustments.
6. Record severity placement.

## Anti-patterns

- Assembling moves from different historical episodes.
- Including a shock in one asset class with no transmission path to the others.
- Ignoring the horizon, which changes the effect on a portfolio with duration.
- Hiding a prudence adjustment inside the scenario rather than labelling it.
- Building a scenario around a single position rather than a market state.

## Done checklist

- [ ] Mechanism stated.
- [ ] Moves derived and recorded.
- [ ] Horizon recorded.
- [ ] Fixed variables recorded.
- [ ] Prudence adjustments labelled.
- [ ] Severity placed.

A scenario also needs a stated starting point: the moves should be applied to current positions and current valuations, not to a portfolio as it stood at the start of the historical episode, because the transmission from a market move to a portfolio loss runs through the exposures that exist now.


The horizon also interacts with the mechanism: a rate shock transmitted through duration takes effect immediately while the same shock transmitted through refinancing takes quarters, and a scenario that applies both on the same timeline will misattribute which exposure drove the loss.


## Sources

- Scenario design and stress testing practice: <https://www.bis.org/>
- Historical data for mechanism evidence: <https://fred.stlouisfed.org/>
- Investor education on scenario analysis: <https://www.investor.gov/introduction-investing>
