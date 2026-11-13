---
name: bond-floor-and-credit
domain: investing/bond-floor-and-credit
trigger: "Working out what a convertible is worth as a bond and how that floor moves."
anti_trigger: "Not for plain bond pricing, and not for predicting credit."
scope: "The bond floor, credit spread sensitivity, and the floor that moves."
status: seedling
---

# Bond floor and credit

## Standard

The bond floor is the value of the convertible if the option were worthless: the present value of its coupons and principal at a discount rate that reflects the issuer's credit and the instrument's subordination. It is the number that stops the convertible from falling with the stock forever, and it is the number that moves most when credit changes.

The floor is not a fixed figure. It falls when the issuer's spread widens, when the remaining maturity shortens, and when the instrument is structurally subordinated to other claims. A convert whose stock has collapsed trades near its floor, and at that point the position's dominant risk has changed from equity to credit without any trade having been made.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record the coupons, the maturity, and the redemption terms.
- Record the discount rate used and its components: risk-free plus spread.
- Record the subordination and any structural disadvantage to senior claims.
- Compute the floor and the premium of the current price over the floor.
- Record the floor's sensitivity to a stated spread widening.
- Record what happens to the floor if the maturity is extended or the coupon deferred.

## Procedure

1. Extract the cash flow schedule and redemption terms.
2. Build the discount curve from the risk-free rate plus the issuer's spread.
3. Compute the present value as the floor.
4. Compute the price-to-floor ratio, which is the option's value.
5. Test the floor at a wider spread.
6. Record the analysis with its inputs.

## Anti-patterns

- Discounting at a generic corporate rate rather than the issuer's.
- Ignoring structural subordination in a holding company.
- Treating the floor as static across the instrument's life.
- Assuming the coupon will be paid when it can be deferred.
- Comparing floors across issues with different maturities.

## Done checklist

- [ ] Cash flows and maturity recorded.
- [ ] Discount rate and components recorded.
- [ ] Subordination recorded.
- [ ] Floor computed.
- [ ] Spread sensitivity recorded.
- [ ] Deferral terms recorded.

The floor's practical use is as a discipline against confusion: when a convertible trades within a few points of its floor, the correct question is a credit question, and when it trades far above it, the correct question is an equity question. Naming which one applies prevents the common error of analysing a distressed credit with equity tools, or a high-premium convert with bond arithmetic that assumes a floor the issuer may not honour.

## Sources

- Security terms and disclosure: <https://www.sec.gov/investor>
- Capital structure and subordination standards: <https://www.bis.org/>
- Rate data for discounting: <https://fred.stlouisfed.org/>
