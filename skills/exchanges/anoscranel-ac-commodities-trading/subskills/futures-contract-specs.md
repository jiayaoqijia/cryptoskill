---
name: futures-contract-specs
domain: investing/futures-contract-specs
trigger: "Reading a commodity futures contract specification before trading it."
anti_trigger: "Not for predicting prices, and not for asset allocation."
scope: "Grade, location, size, tick value, and the expiry that defines the contract."
status: seedling
---

# Futures contract specs

## Standard

A futures contract is defined by five attributes that together determine what the position is: the underlying grade, the delivery location, the contract size, the tick size and value, and the expiry and last trading day. Two contracts with the same name can differ on any of them, and the differences decide the money at risk per point of price movement.

The delivery terms deserve reading even for a trader who never intends to deliver. The first notice day, the last trading day, and the delivery period are different dates, and a position held past the first can be assigned delivery obligations. The exchange publishes the calendar, and the broker's cut-off for closing a position is often earlier than the exchange's, which is the date that actually binds.

Primary sources: <https://www.cmegroup.com/> and <https://www.cftc.gov/>.

## Decision rules

- Record the contract code, the exchange, and the contract month.
- Record the size, the tick size, and the tick value in currency.
- Record the deliverable grade and the delivery location, including any alternatives and their differentials.
- Record the first notice day, the last trading day, and the broker's close-out cut-off.
- Record the daily price limit and what happens when it is hit.
- Where the contract is cash-settled, record the settlement index and its source.

## Procedure

1. Obtain the exchange's contract specification for the exact contract month.
2. Record size, tick, and value.
3. Record grade, location, and deliverable alternatives.
4. Record notice and trading dates alongside the broker's cut-off.
5. Note price limits and settlement method.
6. Write the specification summary the trade will reference.

## Anti-patterns

- Trading from the chart without the specification.
- Assuming the last trading day is the broker's cut-off.
- Ignoring grade and location when comparing two contracts.
- Treating a cash-settled contract as if it had delivery risk, or the reverse.
- Forgetting that tick value scales with contract size.

## Done checklist

- [ ] Contract code, exchange, month recorded.
- [ ] Size, tick, and value recorded.
- [ ] Grade and location recorded.
- [ ] Notice and trading dates recorded with the broker cut-off.
- [ ] Price limits and settlement recorded.
- [ ] Specification summary written.

Reading the specification also settles a question that decides the size of every later calculation: whether the quoted price is per unit or per contract, and whether the tick value already reflects the contract multiplier. A trader who assumes the wrong convention is out by a factor equal to the contract size, which is the kind of error that looks like a risk-management failure and is really a reading failure.

## Sources

- Exchange contract specifications and calendars: <https://www.cmegroup.com/>
- Regulatory background on futures markets: <https://www.cftc.gov/>
- Investor education on futures: <https://www.investor.gov/introduction-investing>
