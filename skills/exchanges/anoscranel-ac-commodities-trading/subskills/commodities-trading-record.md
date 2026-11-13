---
name: commodities-trading-record
domain: investing/commodities-trading-record
trigger: "Writing the record of a commodity position, its curve exposure, and its roll plan."
anti_trigger: "Not for recommending a commodity, and not for the broker statement."
scope: "The written record: contract, curve position, roll plan, margin, and delivery avoidance."
status: seedling
---

# Commodities trading record

## Standard

A commodity position has more moving parts than an equity position, and the record has to hold them: the contract and its specification, the curve position and the roll yield implied at entry, the margin posted and the broker's add-on, the notice dates, and the plan for rolling or closing before delivery. Without those, a position that is profitable on price can still lose money to the roll or to an obligation nobody planned for.

The record is also where the thesis is separated from the vehicle. A view that oil will rise is not the same as a position in a particular contract month at a particular location, and the two can diverge: the curve can move against a correct spot view, or a delivery constraint can force an exit at the wrong time. Writing both makes the divergence visible at review rather than at settlement.

Primary sources: <https://www.cmegroup.com/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the contract, month, exchange, size, and entry price with a timestamp.
- The curve position at entry is recorded, with the implied roll yield.
- The roll plan is dated, including the broker's cut-off and the backup date.
- Margin posted, the broker add-on, and the maintenance level are recorded.
- The delivery-avoidance rule is recorded: close, roll, or accept delivery, and by when.
- Review entries record curve changes, margin changes, and notice proximity.

## Procedure

1. Record the contract and its specification reference.
2. Record the curve and the roll yield at entry.
3. Record margin posted and the maintenance level.
4. Write the roll plan with dates and a buffer.
5. At each review, record curve, margin, and notice status.
6. At exit, record the realized result including roll costs.

## Anti-patterns

- Recording the price but not the contract month.
- Leaving the roll plan to be decided later.
- Reporting profit without the roll cost.
- Ignoring a margin increase until a call arrives.
- Treating delivery avoidance as automatic.

## Done checklist

- [ ] Contract, month, size, price recorded.
- [ ] Curve and roll yield recorded.
- [ ] Roll plan dated with cut-off.
- [ ] Margin and maintenance recorded.
- [ ] Delivery-avoidance rule written.
- [ ] Reviews recorded with curve and notice status.

## Sources

- Exchange contract and delivery calendars: <https://www.cmegroup.com/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Regulatory market data: <https://www.cftc.gov/>
