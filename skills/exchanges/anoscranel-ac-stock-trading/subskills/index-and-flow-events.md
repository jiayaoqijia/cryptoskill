---
name: index-and-flow-events
domain: investing/index-and-flow-events
trigger: "Anticipating the flows created by index changes and corporate events."
anti_trigger: "Not for predicting index decisions, and not for the investment case."
scope: "Rebalances, lockups, offerings, and buybacks, and the flow they create."
status: seedling
---

# Index and flow events

## Standard

Some of the largest and most predictable flows in a single stock come from events that have nothing to do with its business: an index addition or deletion, the expiry of a lockup, a secondary offering, or a buyback programme. These events are scheduled and disclosed, and the flow they create arrives in a narrow window, which is why they are among the few calendar items a trader can plan around rather than react to.

The direction is not always obvious. An index addition brings buying from tracking funds, but the effect is often anticipated and partly priced before the effective date. A lockup expiry releases supply that may or may not be sold. A buyback provides a bid whose size and timing are disclosed but whose execution is discretionary. The record states the event, the estimated flow, and the uncertainty around it.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the event, its announced and effective dates, and the mechanism that creates the flow.
- Estimate the flow from published index weights or disclosed share counts, and state the method.
- Record how much of the flow is likely to be anticipated in the price.
- Record the uncertainty: index decisions can change, and lockup holders need not sell.
- Record the position's exposure to the event date, and size it deliberately.
- Record the post-event behaviour observed, for later comparison.

## Procedure

1. List the scheduled events for the name over the holding period.
2. Estimate the flow for each with a stated method.
3. Assess how much is likely priced.
4. Decide the position treatment for each event.
5. Record the uncertainty and the alternative outcome.
6. Compare the observed flow with the estimate afterwards.

## Anti-patterns

- Treating an index addition as guaranteed buying at the effective date.
- Assuming every lockup holder sells.
- Ignoring the announcement date in favour of the effective date.
- Sizing on the estimated flow without its uncertainty.
- Forgetting that a buyback is discretionary and can be paused.

## Done checklist

- [ ] Events listed with dates.
- [ ] Flow estimated with method stated.
- [ ] Anticipation assessed.
- [ ] Position treatment decided per event.
- [ ] Uncertainty recorded.
- [ ] Observed outcome compared afterwards.

## Sources

- Corporate event disclosure: <https://www.sec.gov/investor>
- Trading and market practice guidance: <https://www.finra.org/>
- Investor education on corporate actions: <https://www.investor.gov/introduction-investing>
