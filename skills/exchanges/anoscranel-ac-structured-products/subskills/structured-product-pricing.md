---
name: structured-product-pricing
domain: investing/structured-product-pricing
trigger: "Decomposing a note into its bond and option components to see the cost."
anti_trigger: "Not for pricing a note with proprietary models, and not for recommending it."
scope: "Decomposition into bond plus options, the issue-price gap, and the secondary-market spread."
status: seedling
---

# Structured product pricing

## Standard

The standard decomposition is a zero-coupon bond plus one or more options. The bond returns the protected amount at maturity; the options produce the participation. The sum of their fair values, at issue, is typically below the issue price, and the difference is the structuring and distribution margin. That gap is the single most informative number about a note, and it is rarely disclosed.

A second cost appears when the holder sells before maturity: the issuer's secondary-market quote carries a spread, and that spread widens in stress exactly when the holder might want to sell. Both costs are measurable in principle, and both belong in the record even when the measurement is approximate.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Decompose the payoff into a zero-coupon bond and the option components.
- Price the bond from the risk-free curve for the issuer's term where data permits.
- Value the options from listed or observable implied volatility, and record the input.
- Compute the gap between the components' value and the issue price, and state it as a percentage.
- Record the secondary-market terms and any early-sale penalty.
- Where inputs are unavailable, record the range and the uncertainty rather than a point.

## Procedure

1. Write the payoff as a bond plus option legs.
2. Discount the protected amount at the risk-free rate for the term.
3. Value each option leg with a stated volatility input.
4. Sum the components and compare with the issue price.
5. Record the gap and the assumptions behind it.
6. Record the secondary-market terms.

## Anti-patterns

- Comparing a note's coupon with a bond's coupon directly.
- Assuming the issue price equals the fair value of the components.
- Using an unstated volatility input.
- Ignoring the secondary-market spread.
- Treating an approximate decomposition as a precise price.

## Done checklist

- [ ] Payoff decomposed into bond and option legs.
- [ ] Bond leg priced with a stated curve.
- [ ] Option legs valued with stated inputs.
- [ ] Issue-price gap computed as a percentage.
- [ ] Secondary-market terms recorded.
- [ ] Uncertainty recorded where inputs were estimates.

A useful sanity check is to ask what the same participation would cost as a listed option and what the same protection would earn as a deposit: when those two numbers sum to less than the issue price, the difference is the price of being sold the combination, and it should be compared with the value of the convenience the combination offers.

## Sources

- Structured note disclosure context: <https://www.sec.gov/investor>
- Retail product and pricing transparency guidance: <https://www.finra.org/>
- Interest-rate data for discounting: <https://fred.stlouisfed.org/>
