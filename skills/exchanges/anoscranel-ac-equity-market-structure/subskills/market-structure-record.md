---
name: market-structure-record
domain: investing/market-structure-record
trigger: "Writing the record of the market-structure facts a decision relies on."
anti_trigger: "Not for the trade decision, and not for the trading journal."
scope: "The written record: venue, timing, mechanics relied on, and what could invalidate them."
status: seedling
---

# Market structure record

## Standard

Every equity decision rests on assumptions about mechanics: that the order will route to a venue with depth, that the auction will price it, that settlement will free the cash on a known date, that the borrow will still exist tomorrow. The record states those assumptions so that when one fails, the failure is attributable rather than mysterious.

The record is short by design: one page per decision, naming the mechanics relied on and the rule or disclosure that supports each. It is updated when a rule changes, and it is the first document read when an execution surprises.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/rules-guidance>.

## Decision rules

- Each mechanic relied on is named with its supporting rule or disclosure.
- Assumptions about timing are dated and marked as assumptions.
- Rule changes are recorded as amendments with their effective date.
- The record names the failure that would show the assumption wrong.
- It is written before the order, not after the fill.
- It is stored with the trade record so the two can be read together.

## Procedure

1. List the mechanics the decision relies on.
2. For each, record the rule or disclosure and its date.
3. Mark the assumptions about timing and availability.
4. Write the failure mode for each assumption.
5. Store the record with the trade record.
6. Amend on any rule change.

## Anti-patterns

- Relying on a mechanic without naming it.
- Assuming a settlement date without checking the cycle.
- Recording the assumptions after the execution.
- Leaving out the failure mode.
- Never updating the record after a rule change.

## Done checklist

- [ ] Mechanics listed.
- [ ] Rule or disclosure recorded per mechanic with date.
- [ ] Timing assumptions marked.
- [ ] Failure modes written.
- [ ] Record stored with the trade record.
- [ ] Amendments on rule changes.

## Sources

- Regulatory context for market structure: <https://www.sec.gov/investor>
- Rule context for trading mechanics: <https://www.finra.org/rules-guidance>
- Investor education on market mechanics: <https://www.investor.gov/introduction-investing>

The record also makes the post-mortem cheap: when an execution surprises, the first question is which assumption failed, and the record answers it without a reconstruction from memory. That is the entire return on keeping it.

Keep the record with the trade record rather than in a separate folder, because the value comes from reading them together: the decision, the mechanics it assumed, and the fill that resulted. Separated, each is a fragment; together they are an audit trail.

