---
name: yield-and-price-mechanics
domain: investing/yield-and-price-mechanics
trigger: "Working the arithmetic between a bond's price, its cash flows, and its yield."
anti_trigger: "Not for predicting rates, and not for credit assessment."
scope: "The inverse relationship between price and yield, the arithmetic of a bond's cash flows, and what a yield does not tell you."
status: seedling
---

# Yield and price mechanics

## Standard

A bond's price is the present value of its promised cash flows discounted at a yield. Because the discounting is in the denominator, price and yield move in opposite directions, and the relationship is convex rather than linear. That is the whole of the basic arithmetic, and most confusion in fixed income comes from using yield as if it were a return.

Yield to maturity assumes the bond is held to maturity, every coupon is reinvested at that same yield, and the issuer does not default. None of those assumptions is guaranteed. A bond bought at a yield of five percent returns five percent only if all three hold; if rates fall, reinvestment earns less, and if the issuer defaults, the arithmetic changes entirely.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://fred.stlouisfed.org/>.

## Decision rules

- Quote price and yield together, with the settlement date and the day-count convention.
- Distinguish yield to maturity from current yield and from realised return; record which is used.
- Never present a yield as a return without stating the three assumptions.
- For a callable bond, use yield to worst and say so.
- Accrued interest is separated from clean price in every quotation.
- A price change is explained by the rate change and the duration, not by narrative.

## Procedure

1. List the cash flows with dates and amounts.
2. Compute the price at the stated yield and confirm against the market quote.
3. Compute yield to maturity from the market price and check the inverse relationship.
4. Note the assumptions behind the yield figure.
5. For callable instruments, compute yield to worst.
6. Record price, yield, convention, and date together.

## Anti-patterns

- Treating the coupon as the return.
- Comparing yields on different day-count conventions.
- Quoting a yield to maturity for a callable bond without noting the call.
- Explaining a price move with news when the rate move explains it.
- Ignoring accrued interest in a transaction price.

## Done checklist

- [ ] Cash flows listed with dates.
- [ ] Price computed and confirmed against the quote.
- [ ] Yield computed from price; inverse relationship checked.
- [ ] Yield assumptions stated.
- [ ] Yield to worst computed where callable.
- [ ] Price, yield, convention, and date recorded together.

## Sources

- Investor education on bond mechanics: <https://www.investor.gov/introduction-investing>
- Interest-rate and yield data: <https://fred.stlouisfed.org/>
- Regulatory context for fixed-income disclosure: <https://www.sec.gov/investor>
