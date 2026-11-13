---
name: earnings-and-event-risk
domain: investing/earnings-and-event-risk
trigger: "Handling a stock position into an earnings date or a scheduled event."
anti_trigger: "Not for forecasting results, and not for the investment case."
scope: "Earnings dates, implied move, and sizing a position into a binary event."
status: seedling
---

# Earnings and event risk

## Standard

An earnings release replaces information with a new distribution in a single moment, and the market re-prices before most participants can react. The implied move — the option market's estimate of the event's effect — is observable before the event and is the honest starting point for sizing, because it prices the uncertainty the position carries.

The decision has three branches, and each should be chosen deliberately. Reduce the position before the event; hold it and accept the gap risk; or hedge it with options, which costs the premium. What is not a plan is holding at full size because the thesis is strong, since the event can be right on the business and wrong on the price. The record states which branch was chosen, the implied move at the time, and the resulting exposure in currency.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the confirmed event date and time, and whether it is before or after the session.
- Record the implied move from the option market, with its source and date.
- Record the position's exposure at that move, in currency.
- Choose the branch: reduce, hold, or hedge, and record the reason.
- Record the post-event plan for each outcome, including the exit if the thesis breaks.
- Where the event date is unconfirmed, record the assumed date and the risk of being wrong.

## Procedure

1. Confirm the date and time of the event from the company's own disclosure.
2. Collect the implied move from the options market.
3. Compute the position's gain or loss at that move.
4. Choose and record the branch.
5. Write the post-event plan for the up, flat, and down cases.
6. Review the position against the plan after the event.

## Anti-patterns

- Holding full size into an event because the thesis is strong.
- Using a historical average move instead of the implied move.
- Forgetting that a release after the close gaps the next open.
- Hedging without computing the cost against the exposure.
- Having no post-event plan for the case where the thesis breaks.

## Done checklist

- [ ] Event date and time confirmed.
- [ ] Implied move recorded with source.
- [ ] Exposure at that move computed.
- [ ] Branch chosen and justified.
- [ ] Post-event plan written for three cases.
- [ ] Review recorded after the event.

## Sources

- Company disclosure and event filings: <https://www.sec.gov/investor>
- Trading and options guidance: <https://www.finra.org/>
- Investor education on event risk: <https://www.investor.gov/introduction-investing>
