---
name: brinson-attribution
domain: investing/brinson-attribution
trigger: "Attributing a portfolio's excess return to allocation or selection."
anti_trigger: "Not for predicting returns, and not for judging a manager."
scope: "Allocation, selection, and interaction, and what each reveals."
status: seedling
---

# Brinson attribution

## Standard

Brinson attribution splits the excess return over a benchmark into three parts. Allocation measures the effect of holding different weights in the benchmark's segments, assuming the benchmark's returns within each. Selection measures the effect of holding different securities within those segments, assuming the benchmark's weights. Interaction captures the part that arises from being different on both dimensions at once.

The decomposition answers a specific question: was the result produced by being in the right places or by picking the right things inside them. That distinction matters because the two are different skills with different persistence, and because a portfolio that is overweight a segment that rose will show allocation gains even if every security it held underperformed its segment.

Primary sources: <https://www.cfainstitute.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the segment definition: sector, region, or whatever the benchmark uses.
- Record portfolio and benchmark weights per segment, and their returns.
- Compute allocation as the sum of weight differences times benchmark segment returns.
- Compute selection as the sum of benchmark weights times segment return differences.
- Compute interaction as the sum of weight differences times return differences.
- Record the residual and confirm the three components sum to the excess return.

## Procedure

1. Define segments consistently for portfolio and benchmark.
2. Collect weights and returns per segment.
3. Compute the three components.
4. Verify the sum against the actual excess return.
5. Record which component dominated and why.
6. Write the attribution with the segment definition stated.

## Anti-patterns

- Attributing with segments defined differently for portfolio and benchmark.
- Reporting the components without checking that they sum.
- Treating allocation gains as skill when they came from a single overweight.
- Ignoring interaction, which can be material in concentrated portfolios.
- Using one period's attribution to conclude a durable capability.

## Done checklist

- [ ] Segment definition recorded.
- [ ] Weights and returns recorded.
- [ ] Three components computed.
- [ ] Sum verified against excess return.
- [ ] Dominant component identified.
- [ ] Period and definition stated.

A further discipline is to run the attribution at more than one segment definition, because a result that appears as selection at the sector level can decompose into allocation inside the sector, and a conclusion that survives both readings is stronger than one that depends on the grouping chosen.


## Sources

- Performance attribution standards: <https://www.cfainstitute.org/>
- Investor education on performance: <https://www.investor.gov/introduction-investing>
- Market and index data: <https://fred.stlouisfed.org/>
