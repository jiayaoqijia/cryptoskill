---
name: calls-and-refunding
domain: investing/calls-and-refunding
trigger: "Working out the yield a callable municipal bond will actually deliver."
anti_trigger: "Not for predicting whether a call occurs, and not for bond pricing theory."
scope: "Call schedules, refunding logic, and the yield to call that matters."
status: seedling
---

# Calls and refunding

## Standard

Most municipal bonds are callable, and the call schedule decides the bond's real maturity. When yields fall, the issuer calls the bond and refunds it at lower cost, which returns the investor's principal at exactly the moment when reinvestment is least attractive. That asymmetry is why the yield to call, not the yield to maturity, is the number that describes a callable bond's return.

Refunding logic explains when a call is likely. An issuer refunds when the present value of the interest savings exceeds the cost of the transaction, which is a function of the level of rates relative to the bond's coupon and the time remaining to the call. The record should state the yield to each call date as well as to maturity, and note the call protection period, which is the window in which the bond cannot be called and therefore behaves most like a non-callable bond.

Primary sources: <https://www.msrb.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the call schedule and the call prices by date.
- Record the call protection period and its end date.
- Compute yield to maturity and yield to each call date.
- Record which of those yields is the lowest, since that is the conservative measure.
- Record the coupon against the current market yield, which indicates call likelihood.
- Record any make-whole or special call provisions that change the arithmetic.

## Procedure

1. Read the call provisions from the official statement.
2. Record each call date and price.
3. Compute yield to call at each date.
4. Identify the lowest yield across the schedule.
5. Compare the coupon with the current market level.
6. Write the analysis with the call-adjusted yield.

## Anti-patterns

- Quoting yield to maturity on a bond that will almost certainly be called.
- Ignoring the call protection period's end date.
- Assuming a call is certain because the coupon is above market.
- Overlooking a make-whole provision that changes the call economics.
- Comparing a callable bond's yield with a non-callable one without adjustment.

## Done checklist

- [ ] Call schedule recorded with dates and prices.
- [ ] Protection period recorded.
- [ ] Yield to each call computed.
- [ ] Lowest yield identified.
- [ ] Coupon versus market recorded.
- [ ] Special provisions recorded.

## Sources

- Municipal bond disclosure and call information: <https://www.msrb.org/>
- Securities disclosure context: <https://www.sec.gov/investor>
- Investor education on callable bonds: <https://www.investor.gov/introduction-investing>
