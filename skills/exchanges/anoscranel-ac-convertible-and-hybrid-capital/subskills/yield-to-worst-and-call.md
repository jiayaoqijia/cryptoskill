---
name: yield-to-worst-and-call
domain: investing/yield-to-worst-and-call
trigger: "Working out the yield a convertible actually offers and when it can be called."
anti_trigger: "Not for predicting the call decision, and not for bond pricing theory."
scope: "Yield to worst, the issuer's call, and the holder's put."
status: seedling
---

# Yield to worst and call

## Standard

A convertible's yield depends on which of several dates the instrument ends on, and the issuer usually decides. Yield to worst computes the return under the outcome least favourable to the holder within the issuer's rights: typically the first call date at the call price, or maturity if no call applies. It is the honest comparison against a straight bond, because it assumes the issuer acts in its own interest.

The call structure is where that asymmetry lives. An issuer calls when refinancing is cheaper or when the stock is above the conversion price and forcing conversion is attractive; the holder receives the call price, not the conversion value, unless the terms give a period to convert. The put, where it exists, is the holder's protection and its terms — the put date, the put price, and whether it is a one-time or periodic right — decide how much that protection is worth.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the call schedule, the call price, and any notice period.
- Record the put schedule, the put price, and whether the right is periodic.
- Compute yield to maturity, yield to first call, and yield to each put date.
- Record the yield to worst and which date produces it.
- Record the conversion value at each call date against the call price.
- Record the forced-conversion mechanics and the notice period given to holders.

## Procedure

1. Extract the call and put schedules with prices.
2. Build the cash flows for each termination scenario.
3. Compute the yield for each scenario.
4. Identify the worst outcome and record it.
5. Compare conversion value with the call price at each date.
6. Write the yield and call summary.

## Anti-patterns

- Quoting yield to maturity as the instrument's yield.
- Ignoring a call that is already in the money.
- Assuming the issuer will not call when refinancing is cheaper.
- Treating a put as certain protection without its date and price.
- Overlooking the notice period in a forced conversion.

## Done checklist

- [ ] Call schedule and prices recorded.
- [ ] Put schedule and prices recorded.
- [ ] Yields computed for each scenario.
- [ ] Yield to worst identified.
- [ ] Conversion value versus call price recorded.
- [ ] Notice mechanics recorded.

## Sources

- Convertible terms and disclosure: <https://www.sec.gov/investor>
- Investment analysis standards: <https://www.cfainstitute.org/>
- Rate data: <https://fred.stlouisfed.org/>
