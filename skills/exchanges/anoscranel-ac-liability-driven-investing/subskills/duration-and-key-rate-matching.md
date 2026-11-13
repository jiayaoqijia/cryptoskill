---
name: duration-and-key-rate-matching
domain: investing/duration-and-key-rate-matching
trigger: "Matching asset and liability interest-rate exposure across the curve."
anti_trigger: "Not for predicting rates, and not for actuarial valuation."
scope: "Matching duration and key-rate exposures between assets and liabilities."
status: seedling
---

# Duration and key-rate matching

## Standard

A single duration number matches the average sensitivity of two cash-flow streams, but liabilities and assets are rarely parallel. A liability stream extending forty years has exposure concentrated at the long end; a bond portfolio with a similar average duration may have exposure spread across the middle of the curve. A parallel shift leaves them roughly matched, and a steepening or flattening does not.

Key-rate matching fixes that by decomposing each side into sensitivities at several points on the curve and matching each point. It is more work and it requires more instruments, but it removes the exposure that a duration match leaves behind: the residual that appears when the curve twists, which is the move that has historically done the most damage to hedged positions.

Primary sources: <https://www.federalreserve.gov/> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the duration of assets and liabilities on a stated basis.
- Record key-rate sensitivities at a minimum of three curve points.
- Record the residual exposure at each point after matching.
- Record the instruments available to hedge each key rate.
- Record the convexity difference between the two sides.
- Record the curve history over which the match was assessed.

## Procedure

1. Compute duration for both sides on a common basis.
2. Decompose each into key-rate sensitivities.
3. Compute the residual at each point.
4. Select instruments to close the residuals.
5. Record the convexity difference.
6. Write the matching summary with the largest residual named.

## Anti-patterns

- Treating a duration match as a rate hedge.
- Ignoring convexity differences between assets and liabilities.
- Using a swap or future with a maturity that does not match the curve point.
- Assuming the curve moves in parallel because it usually does.
- Matching on a basis that differs between the two sides.

## Done checklist

- [ ] Duration computed for both sides.
- [ ] Key-rate decomposition done.
- [ ] Residuals recorded.
- [ ] Hedge instruments listed.
- [ ] Convexity difference recorded.
- [ ] Largest residual named.

The residual that matters most in practice is at the long end, because liabilities extend beyond the maturities where liquid hedging instruments exist; a scheme that matches its twenty-year exposure still carries unhedged exposure at forty years, and the record should name the longest point it cannot hedge rather than reporting a matched figure that excludes it.

## Sources

- Yield curve and rate data: <https://www.federalreserve.gov/>
- Investment management standards: <https://www.cfainstitute.org/>
- Rate series: <https://fred.stlouisfed.org/>
