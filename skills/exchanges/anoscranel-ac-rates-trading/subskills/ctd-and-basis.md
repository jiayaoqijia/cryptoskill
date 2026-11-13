---
name: ctd-and-basis
domain: investing/ctd-and-basis
trigger: "Working out which bond is cheapest to deliver and what the basis pays."
anti_trigger: "Not for predicting yields, and not for bond portfolio construction."
scope: "Cheapest-to-deliver, net basis, and the delivery option the short owns."
status: seedling
---

# Cheapest to deliver and basis

## Standard

The short in a bond future chooses which eligible bond to deliver, and will choose the one that costs least, which is the cheapest-to-deliver. Its identity depends on yields relative to the notional coupon: at low yields the shorter-duration bonds tend to be cheapest, at high yields the longer ones, and the switch is why the contract's behaviour changes with the level of rates.

The basis is the difference between the cash bond's price and the future's invoice price, net of carry. Gross basis ignores the coupon income and financing; net basis accounts for them and is the number that should be compared across bonds. A positive net basis is the cost of the delivery option the short holds, and it is what a long pays for the flexibility the contract gives the other side.

Primary sources: <https://www.cmegroup.com/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the gross basis and the net basis for every bond in the basket.
- Record the carry components: coupon accrual, financing cost, and time to delivery.
- Identify the CTD and record the margin by which it is cheapest.
- Record the delivery option's value as the net basis of the CTD.
- Record how the CTD changes across a range of yields.
- Record the switch yield at which the CTD would change.

## Procedure

1. Collect cash prices, accrued interest, and conversion factors for the basket.
2. Compute the invoice price for each bond.
3. Compute gross and net basis for each.
4. Rank by net basis to identify the CTD.
5. Compute the switch yield for the nearest alternative.
6. Record the basis structure with its date.

## Anti-patterns

- Comparing gross basis across bonds without carry.
- Assuming the CTD is the bond with the lowest coupon.
- Ignoring the switch yield when sizing a hedge.
- Treating a negative net basis as free money without checking delivery frictions.
- Using a stale basis in a fast market.

## Done checklist

- [ ] Gross and net basis computed per bond.
- [ ] Carry components recorded.
- [ ] CTD identified with its margin.
- [ ] Delivery option valued.
- [ ] Switch yield computed.
- [ ] Basis structure dated.

The basis also has a term structure: near the delivery date the net basis of the CTD converges towards zero as the delivery option loses value, which is why a basis position has an expiry and why holding one without a plan for the delivery window is holding a position whose economics are changing daily.

## Sources

- Exchange delivery and conversion data: <https://www.cmegroup.com/>
- Treasury yields and auction results: <https://www.federalreserve.gov/>
- Rate and inflation data: <https://fred.stlouisfed.org/>
