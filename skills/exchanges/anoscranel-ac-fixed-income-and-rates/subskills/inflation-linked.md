---
name: inflation-linked
domain: investing/inflation-linked
trigger: "Working the arithmetic of inflation-linked bonds and the breakeven."
anti_trigger: "Not for inflation forecasting, and not for choosing between issuers."
scope: "Real versus nominal yields, inflation-linked mechanics, and the breakeven arithmetic."
status: seedling
---

# Inflation-linked

## Standard

An inflation-linked bond pays a real yield: the coupons and principal are adjusted for an inflation index, so the investor's return is protected against that index's measure of inflation rather than against inflation as experienced. The difference between the nominal yield on a conventional bond and the real yield on a linked bond of the same maturity is the breakeven inflation rate — the rate at which the two would return the same.

The breakeven is not a forecast. It is a market price that embeds a risk premium, a liquidity premium, and the difference between the index and the investor's own basket. Reading it as an inflation prediction is the common error; reading it as the price at which the two instruments are equivalent is the correct one.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Real and nominal yields are quoted together with the breakeven shown as their difference.
- The index used for the link is named, with its known limitations.
- The breakeven is described as a price, not a forecast.
- Liquidity differences between linked and nominal markets are recorded, because they enter the breakeven.
- The deflation floor is noted where the instrument has one.
- Tax treatment of inflation adjustments is recorded separately; it affects the realised return.

## Procedure

1. Identify the linked bond, its index, and its maturity.
2. Record the real yield and the nominal yield for the same maturity.
3. Compute the breakeven as the difference.
4. Note the liquidity and index differences that enter the breakeven.
5. Check whether a deflation floor applies.
6. Record the finding and the tax note.

## Anti-patterns

- Treating the breakeven as an inflation forecast.
- Comparing linked and nominal yields at different maturities.
- Ignoring the index's coverage limits.
- Forgetting the tax on inflation adjustments.
- Assuming liquidity is equal across the two markets.

## Done checklist

- [ ] Linked bond, index, and maturity identified.
- [ ] Real and nominal yields recorded for the same maturity.
- [ ] Breakeven computed and labelled a price.
- [ ] Liquidity and index differences noted.
- [ ] Deflation floor checked.
- [ ] Tax note recorded.

## Sources

- Real and nominal yield series: <https://fred.stlouisfed.org/>
- Investor education on inflation protection: <https://www.investor.gov/introduction-investing>
- Regulatory context for inflation-linked disclosure: <https://www.sec.gov/investor>

The honest framing for a long-horizon investor is that the linked instrument protects the real value of a known nominal amount against a published index, which is narrower and more specific than 'inflation protection' as it is usually sold. Recording exactly which index and which basket makes the difference visible.
