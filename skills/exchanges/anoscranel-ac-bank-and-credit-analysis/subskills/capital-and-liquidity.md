---
name: capital-and-liquidity
domain: investing/capital-and-liquidity
trigger: "Reading a bank's capital and liquidity ratios against the regulatory minimums."
anti_trigger: "Not for predicting supervisory action, and not for valuation."
scope: "CET1, leverage ratios, and liquidity coverage, and what the minimums actually constrain."
status: seedling
---

# Capital and liquidity

## Standard

Capital and liquidity are different defences against different failures. Capital absorbs losses: common equity tier one against risk-weighted assets says how much loss the bank can take before depositors are exposed. Liquidity survives a run: the liquidity coverage ratio says whether the bank can meet thirty days of stressed outflows with high-quality liquid assets.

The distinction matters because a bank can be well capitalised and still fail on liquidity, and the reverse. Reading the ratios means knowing which risk each addresses, what the minimum is in the relevant jurisdiction, and what buffers sit above it. A ratio comfortably above the minimum in a calm year can be close to the line in a stress year, because risk-weighted assets rise as credit quality falls.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record CET1, the leverage ratio, and the liquidity coverage ratio separately, with the jurisdiction's minimum for each.
- Note the buffer above each minimum, not just the ratio.
- Remember that risk-weighted assets rise in stress, so the CET1 ratio falls without any new loss.
- Record the quality of capital: common equity is not the same as other instruments counted in the ratio.
- Liquidity is assessed by the composition of the liquid asset buffer, not only the ratio.
- Supervisory exercises and their outcomes are recorded with dates.

## Procedure

1. Pull the capital and liquidity disclosures.
2. Compute each ratio and the buffer above the stated minimum.
3. Verify the composition of capital and of the liquid asset buffer.
4. Compare with the prior year and with the peer group.
5. Note any supervisory action or stress-test result.
6. Record the assessment with the jurisdiction's framework named.

## Anti-patterns

- Treating the capital ratio as sufficient without liquidity.
- Comparing ratios across jurisdictions with different rules.
- Ignoring the risk-weight denominator's sensitivity.
- Counting non-equity capital as equivalent to common equity.
- Reading the ratio at a single date as the structural position.

## Done checklist

- [ ] CET1, leverage, and liquidity ratios recorded with minimums.
- [ ] Buffers computed.
- [ ] Capital and liquid-asset composition verified.
- [ ] Prior-year and peer comparison made.
- [ ] Supervisory actions noted.
- [ ] Jurisdictional framework named.

## Sources

- Basel Committee capital and liquidity standards: <https://www.bis.org/>
- Federal Reserve supervisory framework: <https://www.federalreserve.gov/>
- Investor education on bank regulation: <https://www.investor.gov/introduction-investing>

The most useful habit is to read the two ratios as a pair and ask which failure each one is absorbing. A bank with strong capital and weak liquidity is vulnerable to a run; one with strong liquidity and weak capital is vulnerable to a loss. The record should name which of the two is doing the work, because that is the one that will fail first.
