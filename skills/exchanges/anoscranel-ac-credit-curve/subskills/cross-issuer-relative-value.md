---
name: cross-issuer-relative-value
domain: investing/cross-issuer-relative-value
trigger: "Comparing two issuers' curves for relative value."
anti_trigger: "Not for recommending a credit, and not for default prediction."
scope: "Comparing curves across issuers without confounding the comparison."
status: seedling
---

# Cross-issuer relative value

## Standard

Comparing two issuers' credit curves requires controlling for what differs between them: sector, rating, seniority, documentation, and the liquidity of the instruments. A spread difference between two issuers in different sectors at the same rating is not necessarily a relative-value opportunity; it may be the market pricing a sector difference that has a reason.

The disciplined comparison holds the controls fixed and looks at the residual. Two issuers in the same sector, same rating band, same seniority, and comparable liquidity, with a spread difference that has widened beyond its historical range, is a comparison that can be examined. The record should list the controls and state which differences remain unaddressed.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record both issuers' sector, rating, seniority, and documentation version.
- Record the spread at matched maturities.
- Record the spread difference and its historical range.
- Record the liquidity of each instrument, since a wide spread can be a liquidity premium.
- Record the controls applied and the differences that remain.
- Record the event or news that might explain the difference, rather than assuming mispricing.

## Procedure

1. Match the issuers on sector, rating, seniority, and documentation.
2. Record spreads at matched maturities.
3. Compute the difference and its history.
4. Assess liquidity on both sides.
5. List the remaining differences.
6. Write the comparison with its controls.

## Anti-patterns

- Comparing issuers across sectors without noting the sector difference.
- Treating a spread difference as mispricing when it is a liquidity premium.
- Ignoring seniority or documentation differences.
- Using one issuer's curve shape for another's roll calculation.
- Assuming the historical spread range will reassert.

## Done checklist

- [ ] Issuer characteristics recorded.
- [ ] Matched spreads recorded.
- [ ] Difference and range computed.
- [ ] Liquidity assessed.
- [ ] Remaining differences listed.
- [ ] Comparison written with controls.

The controls are also worth recording as a checklist rather than a sentence, because relative-value analysis fails most often at the control that was assumed rather than checked, and a named list makes the omission visible to a later reader.


Recording the date of each issuer's quote also protects the comparison from a mismatch that is invisible in the numbers, since two curves observed on different days can differ for reasons that have nothing to do with either issuer.


## Sources

- Credit market conventions and data: <https://www.isda.org/>
- Market context and rates: <https://www.federalreserve.gov/>
- Spread series: <https://fred.stlouisfed.org/>
