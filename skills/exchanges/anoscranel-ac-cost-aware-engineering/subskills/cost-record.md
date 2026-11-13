---
name: cost-record
domain: software-engineering/cost-record
trigger: "Writing the record of unit cost, its drivers, and its trend."
anti_trigger: "Not for financial reporting, and not for pricing decisions."
scope: "The written record: unit cost, drivers, attribution, and trend."
status: seedling
---

# Cost record

## Standard

The cost record states the unit cost, the breakdown by driver, the attribution to owners, and the trend, with the volumes and prices it rests on. Its value is that it makes a cost comparable across time and across designs, which a total never is: a bill that doubled may reflect doubled volume at constant unit cost, and only the record distinguishes that from a regression.

Its second function is to hold the decisions. Every cost intervention — a retention change, a tiering policy, a batch size — was made on an estimate, and the record keeps the estimate beside the measured outcome so that the next intervention can be judged against the accuracy of the last one.

Primary sources: <https://www.finops.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the unit cost, the unit chosen, and the volume it was computed at.
- The breakdown by cost driver is recorded with each driver's volume.
- Attribution is recorded per owner, with untagged cost shown separately.
- Every intervention is recorded with its estimate and its measured effect.
- Prices are recorded with their date and source, since list prices differ from billed.
- Review triggers are dated: pricing change, volume step change, architecture change.

## Procedure

1. Record the unit cost and the volume.
2. Record the breakdown by driver.
3. Record attribution and untagged cost.
4. Record each intervention with estimate and effect.
5. Record prices with date and source.
6. Review at each trigger and record the change.

## Anti-patterns

- Recording the total and calling it the cost.
- An intervention recorded without its estimate, so its success cannot be judged.
- Prices recorded without a date.
- Untagged cost omitted because it is inconvenient.
- No trigger, so the record describes a price list that has changed.

## Done checklist

- [ ] Unit cost and volume recorded.
- [ ] Driver breakdown recorded.
- [ ] Attribution and untagged cost recorded.
- [ ] Interventions with estimates recorded.
- [ ] Prices dated and sourced.
- [ ] Triggers dated.

The record's most valuable section after a year is the interventions, because it shows which estimates were reliable: a team that consistently underestimated operational burden will read its next estimate differently, and that calibration is not recoverable from the bill alone.


## Sources

- FinOps reporting guidance: <https://www.finops.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Cloud native cost practice: <https://www.cncf.io/>
