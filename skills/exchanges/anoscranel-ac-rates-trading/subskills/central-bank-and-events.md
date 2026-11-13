---
name: central-bank-and-events
domain: investing/central-bank-and-events
trigger: "Mapping the scheduled events that move rates and the basis."
anti_trigger: "Not for forecasting policy decisions, and not for macro interpretation."
scope: "Meeting dates, auction calendar, and settlement events that move the basis."
status: seedling
---

# Central bank and events

## Standard

Rates markets run on a calendar. Policy meetings, the publication of projections, auctions of new paper, month-end index rebalancing, and quarter-end balance-sheet dates all produce flows that are scheduled and known in advance. The trader's job is not to predict the outcome but to know which dates carry the risk and which carry the flow.

Two events deserve separate treatment. An auction of new paper changes the supply of the deliverable basket and can move the basis around the settlement date. And a policy meeting compresses the front end of the curve, with the risk concentrated in the statement and the projections rather than distributed across the day. A position held through either needs a plan written before the date, not after.

Primary sources: <https://www.federalreserve.gov/> and <https://www.newyorkfed.org/>.

## Decision rules

- Record the policy meeting dates for the currencies traded.
- Record the auction calendar and the settlement dates of new issues.
- Record month-end and quarter-end dates that create index and balance-sheet flows.
- Record the position's exposure to each event, in DV01 terms.
- Record the treatment: hold, reduce, or hedge, decided in advance.
- Record what happened at the last comparable event, for calibration.

## Procedure

1. Build the calendar for the holding period.
2. Mark the events that affect the instruments held.
3. Compute each position's DV01 exposure through each event.
4. Decide the treatment for each event before it arrives.
5. Record the outcome of the previous comparable event.
6. Review the position against the calendar weekly.

## Anti-patterns

- Trading into a policy meeting without a stated plan.
- Ignoring auction settlement when the basis is the trade.
- Forgetting month-end index flows.
- Treating a scheduled event as a surprise because the outcome was.
- Holding a basis trade through a basket change without re-checking.

## Done checklist

- [ ] Policy dates recorded.
- [ ] Auction and settlement calendar recorded.
- [ ] Month-end and quarter-end dates recorded.
- [ ] Exposure per event computed.
- [ ] Treatment decided in advance.
- [ ] Previous outcomes recorded.

The calendar also has a memory: the market's reaction to the last auction or the last meeting is a useful calibration for how much a position should be reduced, and recording that reaction turns an anecdote into a sizing input rather than a recollection.

## Sources

- Policy meeting calendars and statements: <https://www.federalreserve.gov/>
- Auction and repo operations: <https://www.newyorkfed.org/>
- Rate and inflation series: <https://fred.stlouisfed.org/>
