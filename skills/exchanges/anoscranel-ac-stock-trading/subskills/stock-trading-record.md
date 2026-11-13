---
name: stock-trading-record
domain: investing/stock-trading-record
trigger: "Writing the record of a single-name trade and the mechanics it depends on."
anti_trigger: "Not for recommending a stock, and not for the broker statement."
scope: "The written record: name, size, event plan, borrow, and review."
status: seedling
---

# Stock trading record

## Standard

The single-name record captures what the statement cannot: the reason the position exists, the liquidity that permitted its size, the events it will pass through, and the plan for each. It is shorter than a research note and more specific than a journal entry, because its job is to make the trade reviewable against the conditions it was opened under.

The mechanics section is what distinguishes it from an investment record. Days to liquidate, overnight gap exposure, earnings treatment, borrow fee, and halt contingency are all facts that change and all facts that determine whether the idea could be expressed at all. Recording them at entry means a later review can ask whether the trade failed on the idea or on the plumbing, which are different lessons.

Primary sources: <https://www.finra.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the name, direction, size, entry, venue, and timestamp.
- The permitted size from liquidity and the risk-budget size are both recorded, with the smaller chosen.
- The event calendar for the holding period is listed with the treatment of each event.
- Overnight gap exposure and halt contingency are recorded in currency and in plan.
- For shorts, the borrow fee and recall plan are recorded.
- Review entries are dated and state whether the mechanics or the thesis changed.

## Procedure

1. Record the trade, the size, and the two size constraints.
2. Record the liquidity measurement and the days to liquidate.
3. List the events and the treatment chosen for each.
4. Record the gap and halt contingencies.
5. Record the borrow terms for a short.
6. Review on the stated cadence and record which assumption changed.

## Anti-patterns

- Recording the thesis and leaving out the liquidity.
- Omitting the event calendar.
- Reporting the result without the costs that came from the mechanics.
- Recording a short without the borrow fee.
- Reviewing only the outcome.

## Done checklist

- [ ] Trade, size, and constraints recorded.
- [ ] Liquidity and days to liquidate recorded.
- [ ] Event calendar with treatments recorded.
- [ ] Gap and halt contingencies recorded.
- [ ] Borrow terms recorded for shorts.
- [ ] Reviews dated with the assumption that changed.

The record's final test is whether a reviewer could reconstruct the trade's constraints without asking: the size the book allowed, the events it passed through, the gap it accepted, and the borrow it paid. A record that contains those can say afterwards whether the loss came from the idea or from the plumbing.

## Sources

- Trading practice and investor guidance: <https://www.finra.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Corporate event disclosure: <https://www.sec.gov/investor>
