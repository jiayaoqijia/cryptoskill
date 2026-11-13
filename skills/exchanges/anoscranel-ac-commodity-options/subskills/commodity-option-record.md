---
name: commodity-option-record
domain: investing/commodity-option-record
trigger: "Writing the record of a commodity option position and its delivery chain."
anti_trigger: "Not for recommending a position, and not for the confirmation itself."
scope: "The written record: contract, expiry gap, exercise terms, and delivery avoidance."
status: seedling
---

# Commodity option record

## Standard

The commodity option record has to carry the delivery chain, because the position can turn into a futures contract and then into a physical obligation. The option's expiry, the future's notice day, the exercise decision, and the plan for closing any delivered future belong in one place, written before the position exists.

It also carries the volatility context that justifies the price: the at-the-money level, the wing prices, and the seasonal position of the expiry. Those numbers change, and a review that compares the entry price with the exit price without them cannot say whether the position earned or lost on direction, on volatility, or on the passage of the calendar.

Primary sources: <https://www.cmegroup.com/> and <https://osf.io/prereg/>.

## Decision rules

- Record the contract, month, strike, and expiry.
- Record the underlying future's notice day and last trading day.
- Record the exercise decision rule and the automatic exercise threshold.
- Record the plan for a delivered future: close, roll, or accept.
- Record the volatility context at entry: ATM, wings, and seasonal position.
- Review at expiry and at any notice date.

## Procedure

1. Record the option terms and the underlying.
2. Record the delivery chain dates.
3. Record the exercise rule and the delivered-future plan.
4. Record the volatility context at entry.
5. Set review triggers at expiry and notice dates.
6. Record the outcome at close.

## Anti-patterns

- Recording the option without the underlying future's dates.
- Leaving the delivered-future plan implicit.
- Omitting the volatility context from the entry record.
- Reviewing only at expiry, after the decision has been made.
- Treating a cash-settled contract as if it had a delivery chain.

## Done checklist

- [ ] Option terms recorded.
- [ ] Delivery chain dates recorded.
- [ ] Exercise rule recorded.
- [ ] Delivered-future plan written.
- [ ] Volatility context recorded.
- [ ] Review triggers set.

The record's most useful field is the expiry-to-notice interval, expressed in days: it is the window in which a decision must be made, and writing it down converts an exchange calendar that nobody reads into a date that cannot be missed.


A record that names the delivered-future plan in advance also settles the argument about intent: if the position was opened to avoid delivery, the plan proves it, and if it was opened to take delivery, the same plan shows the funding and the storage that were arranged for it.

## Sources

- Exchange contract and expiry data: <https://www.cmegroup.com/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Regulatory market data: <https://www.cftc.gov/>
