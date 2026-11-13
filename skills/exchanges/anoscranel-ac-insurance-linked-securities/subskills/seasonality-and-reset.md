---
name: seasonality-and-reset
domain: investing/seasonality-and-reset
trigger: "Reading the season window and reset terms of a catastrophe bond."
anti_trigger: "Not for predicting events, and not for pricing a new issue."
scope: "Season windows, reset dates, and the pricing around them."
status: seedling
---

# Seasonality and reset

## Standard

Most catastrophe perils have a season, and a bond's risk is concentrated in it: a US hurricane bond carries most of its expected loss between June and November, and a bond covering a winter storm peril carries it in the opposite months. The spread does not vary through the year, so the compensation per unit of risk changes as the season approaches, which is why secondary pricing moves ahead of the season rather than during it.

Reset provisions add a second dynamic. A bond may reset its terms — the attachment point, the price, or both — on an anniversary, and a reset can extend exposure rather than terminate it. The record should state the season window, the reset dates, and whether the investor has any option to exit at reset, because a position held through a reset is a decision rather than an oversight.

Primary sources: <https://www.artemis.bm/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the season window for the peril and the share of expected loss inside it.
- Record the reset dates and what resets.
- Record whether the investor may exit at reset and at what price.
- Record the spread relative to the remaining season's expected loss.
- Record the historical frequency of events outside the stated season.
- Record any extension provision and its trigger.

## Procedure

1. Record the season window and the expected loss distribution across it.
2. Record the reset dates and terms.
3. Record the exit option at reset.
4. Compute spread per unit of remaining expected loss.
5. Record out-of-season events.
6. Write the season summary with the reset decision.

## Anti-patterns

- Holding a bond through a season without noting the concentration.
- Assuming a reset terminates the position.
- Treating the spread as constant compensation through the year.
- Ignoring events outside the stated season.
- Missing an extension provision.

## Done checklist

- [ ] Season window recorded.
- [ ] Expected loss share inside it recorded.
- [ ] Reset dates and terms recorded.
- [ ] Exit option recorded.
- [ ] Out-of-season events recorded.
- [ ] Season decision written.

The reset decision is also a liquidity event: a reset date is one of the few moments at which an investor can exit without finding a buyer in the secondary market, which is thin for most deals, so the calendar should be recorded as an opportunity rather than only as a risk.

## Sources

- Catastrophe bond terms and market data: <https://www.artemis.bm/>
- Securities disclosure context: <https://www.sec.gov/investor>
- Investor education on structured risk: <https://www.investor.gov/introduction-investing>
