---
name: expiry-and-settlement
domain: investing/expiry-and-settlement
trigger: "Working out the price and time an equity option settles against."
anti_trigger: "Not for predicting the settlement price, and not for option theory."
scope: "AM versus PM settlement, weekly expiries, and the price an option settles against."
status: seedling
---

# Expiry and settlement

## Standard

Two options expiring on the same date can settle against different prices. A PM-settled option settles against the closing price of that day; an AM-settled index option settles against a special opening quotation computed from the opening prices of its components. The difference is not cosmetic: an overnight move that reverses during the day inverts the outcome between the two, and a position held through expiry is exposed to whichever convention its contract specifies.

Weekly and daily expiries add a second layer. They shorten the option's life and concentrate gamma near expiry, which is why the last day of a short-dated contract behaves differently from the last day of a monthly one. A trader who plans an exit "at expiry" without checking whether the contract settles at the open or the close is planning against the wrong price.

Primary sources: <https://www.cboe.com/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the expiry date and whether settlement is AM or PM.
- Record the settlement price source for the specific contract.
- Record the last trading day, which may be the day before settlement.
- Record the expiry cycle: monthly, weekly, or daily.
- Record the gamma concentration near expiry for positions held into it.
- Record the plan for closing or exercising before the settlement computation.

## Procedure

1. Read the contract specification for settlement.
2. Record the expiry and the settlement source.
3. Record the last trading day and the exercise cut-off.
4. Record the gamma profile into expiry.
5. Write the exit plan around the settlement time.
6. Verify the settlement price after the event.

## Anti-patterns

- Assuming settlement is at the close.
- Treating the last trading day as the settlement day.
- Holding a short-dated position without accounting for gamma.
- Planning an exit on the settlement date when trading has already stopped.
- Comparing outcomes between AM and PM settled contracts.

## Done checklist

- [ ] Expiry and settlement type recorded.
- [ ] Settlement source recorded.
- [ ] Last trading day recorded.
- [ ] Expiry cycle recorded.
- [ ] Gamma profile recorded.
- [ ] Exit plan written.

A further trap is the exercise-by-exception rule: an in-the-money option is exercised automatically unless the holder instructs otherwise, so an expiring position that is not monitored can convert into shares or cash without any decision having been made, and the record should state who monitors that threshold and how.


## Sources

- Exchange settlement conventions: <https://www.cboe.com/>
- Regulatory information on options: <https://www.sec.gov/investor>
- Investor education on expiry: <https://www.investor.gov/introduction-investing>
