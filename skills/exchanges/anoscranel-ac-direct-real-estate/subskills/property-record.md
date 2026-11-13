---
name: property-record
domain: investing/property-record
trigger: "Writing the record of a direct property analysis."
anti_trigger: "Not for recommending a property, and not for the appraisal itself."
scope: "The written record: NOI, leases, valuation, debt, and capital plan."
status: seedling
---

# Property record

## Standard

The property record states the net operating income rebuilt from the rent roll rather than reported, the lease profile with its concentration and rollover, the valuation with its capitalisation rate and implied growth, the capital plan including deferred items, and the debt with its covenants and refinancing assumptions. Each of those is a judgement with a number attached, and the record's purpose is to keep the judgement visible beside the number.

Its second purpose is comparability across a portfolio of properties. Two assets with the same reported yield can differ in lease concentration, capital need, and refinancing exposure, and a portfolio view that compares only yields will allocate to the one with the hidden liability. Stating the same fields for every property is what makes the comparison possible.

Primary sources: <https://www.sec.gov/investor> and <https://osf.io/prereg/>.

## Decision rules

- Record NOI as rebuilt, alongside the reported figure and the gap.
- Record lease concentration, expiry profile, and recovery structure.
- Record the capitalisation rate, comparables, and implied growth.
- Record the capital plan and the deferred maintenance total.
- Record the debt, covenants, and refinancing assumptions.
- Record the review triggers: lease expiry, loan maturity, and appraisal dates.

## Procedure

1. Record the rebuilt and reported NOI with the gap.
2. Record the lease profile and concentration.
3. Record the valuation and its assumptions.
4. Record the capital plan and deferred items.
5. Record the debt and refinancing scenario.
6. Set review triggers and file the record.

## Anti-patterns

- Recording the reported NOI without the rebuild.
- Omitting the deferred maintenance total from the value.
- Leaving the implied growth inside the cap rate unexplained.
- Recording debt without the refinancing assumption.
- Setting no trigger at lease expiry or loan maturity.

## Done checklist

- [ ] Rebuilt NOI recorded with the gap.
- [ ] Lease profile and concentration recorded.
- [ ] Valuation and assumptions recorded.
- [ ] Capital plan and deferred total recorded.
- [ ] Debt and refinancing recorded.
- [ ] Review triggers set.

Storing the appraisal date beside the capital plan is what makes the record a control: an appraisal older than the last major capital item is a valuation that predates a change in the asset, and a review that compares them can see that the value being carried no longer reflects the building.

## Sources

- Property and valuation disclosure: <https://www.sec.gov/investor>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Rate and market data: <https://www.federalreserve.gov/>
