---
name: credit-option-record
domain: investing/credit-option-record
trigger: "Writing the record of a credit option position."
anti_trigger: "Not for recommending a position, and not for the confirmation itself."
scope: "The written record: reference, expiry, spread, recovery, and settlement."
status: seedling
---

# Credit option record

## Standard

The credit option record states the reference entity and seniority, the option expiry and the underlying swap's maturity, the strike spread and standard coupon, the volatility convention and recovery assumption, and the settlement mechanism. Those fields define the instrument; most disagreements about a credit option trace back to one of them being unstated.

The record also carries the event exposure, because a credit event during the option's life changes the position in a way an equity option has no analogue for. A default can trigger settlement of the underlying before the option is exercised, and the documentation decides what happens to the option. That clause belongs in the record, not in a file consulted after the event.

Primary sources: <https://www.isda.org/> and <https://osf.io/prereg/>.

## Decision rules

- Record the reference entity, seniority, and documentation version.
- Record the option expiry and the underlying swap maturity.
- Record the strike spread, the standard coupon, and the upfront.
- Record the volatility convention and the recovery assumption.
- Record the settlement mechanism and the deliverable.
- Record the credit event treatment during the option's life.

## Procedure

1. Record the reference and documentation.
2. Record both dates and the strike.
3. Record volatility, recovery, and model.
4. Record settlement and deliverable.
5. Record the event clause.
6. Review at each expiry and at any event.

## Anti-patterns

- Recording the option expiry without the swap maturity.
- Omitting the recovery assumption.
- Leaving the settlement mechanism implicit.
- Ignoring the event clause.
- Recording the notional without the spread DV01.

## Done checklist

- [ ] Reference and documentation recorded.
- [ ] Both dates recorded.
- [ ] Strike and coupon recorded.
- [ ] Volatility, recovery, model recorded.
- [ ] Settlement and deliverable recorded.
- [ ] Event clause recorded.

The record's second purpose is comparability across a book: two positions with the same reference and different underlying tenors are not the same trade, and two with the same tenor and different recovery assumptions are priced off different worlds. Storing those fields consistently is what allows a portfolio-level view to add up to something rather than to a sum of unlike quantities. A record that can be aggregated is worth more than one that merely describes.

One field more than any other prevents a review from misreading the position: the direction of the option relative to protection, since a payer option and a receiver option on the same reference with the same expiry lose money in opposite states of the world.


## Sources

- Credit derivatives documentation: <https://www.isda.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Market and credit data: <https://www.federalreserve.gov/>
