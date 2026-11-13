---
name: bond-futures-basics
domain: investing/bond-futures-basics
trigger: "Reading a bond futures contract and how delivery is priced."
anti_trigger: "Not for bond portfolio mechanics, and not for predicting yields."
scope: "Notional coupon, conversion factors, eligible baskets, and invoice price."
status: seedling
---

# Bond futures basics

## Standard

A bond future is written on a notional bond with a stated coupon and maturity, and delivery is made by handing over one of several eligible real bonds. Because those bonds have different coupons and maturities, each carries a conversion factor that adjusts the invoice price so that the basket is roughly comparable. The short chooses which bond to deliver, and that choice is the source of most of the contract's behaviour.

The invoice price is the futures price multiplied by the conversion factor plus accrued interest. That formula is the arithmetic that connects the futures market to the cash market, and it is why two traders can disagree about the contract's value while both being right about the bond: they are pricing different deliverables, or the same deliverable at different financing costs.

Primary sources: <https://www.cmegroup.com/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the contract, its notional coupon, and its notional maturity.
- Record the eligible basket and each bond's conversion factor.
- Record the invoice price calculation and verify it against the exchange's example.
- Record which bonds in the basket are currently cheapest to deliver.
- Record the delivery months and the last delivery day.
- Where the basket changes with a new contract cycle, record the change.

## Procedure

1. Obtain the contract specification and the deliverable basket.
2. Record the conversion factor for each eligible bond.
3. Compute the invoice price at the current futures price for one bond.
4. Verify the formula against the exchange's published example.
5. Identify the current cheapest-to-deliver.
6. Record the specification summary with its date.

## Anti-patterns

- Treating the future as a claim on one specific bond.
- Ignoring conversion factors when comparing the future with a cash bond.
- Assuming the cheapest-to-deliver is stable.
- Using an old basket after the contract cycle rolled.
- Computing accrued interest on the wrong day count.

## Done checklist

- [ ] Contract and notional terms recorded.
- [ ] Basket and conversion factors recorded.
- [ ] Invoice price computed and verified.
- [ ] Cheapest-to-deliver identified.
- [ ] Delivery dates recorded.
- [ ] Summary dated.

The practical consequence is that the contract's price is not a bond price and not a yield: it is the market's price for the delivery obligation, and it moves when the identity of the cheapest deliverable moves. A trader who reads the future as a proxy for one bond will be surprised at exactly the moments when the basket matters most.

## Sources

- Exchange bond futures specifications: <https://www.cmegroup.com/>
- Treasury market data and auction information: <https://www.federalreserve.gov/>
- Yield and rate series: <https://fred.stlouisfed.org/>
