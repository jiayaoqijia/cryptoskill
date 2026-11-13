---
name: index-deletion-flows
domain: investing/index-deletion-flows
trigger: "Estimating the forced flow from a likely index deletion or addition."
anti_trigger: "Not for predicting the index decision, and not for deal advice."
scope: "Forced selling, deletion candidates, and the flow estimate."
status: seedling
---

# Index deletion flows

## Standard

An index deletion forces every fund tracking that index to sell the shares by the effective date, and the selling is price-insensitive because the fund's mandate requires it. The size of the flow is estimable from the stock's index weight and the assets tracking the index, and the window in which it arrives is disclosed in the announcement.

The anticipation is the interesting part. A stock likely to be deleted can be identified in advance from the index's own rules, and the selling pressure often appears before the effective date as the market positions for it. That is why the flow estimate matters less than the timing: a flow that is known and dated is typically priced before it arrives, and the residual effect is in the days around the effective date rather than over the weeks preceding it.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the index, the announcement date, and the effective date.
- Record the stock's weight and the assets tracking the index.
- Estimate the flow in shares and in days of average volume.
- Record the criteria the index uses and whether the stock meets them.
- Record how much of the flow is likely to be anticipated.
- Record the days around the effective date and their historical volume pattern.

## Procedure

1. Identify candidate deletions or additions from the index rules.
2. Record weight and tracking assets.
3. Estimate the flow and express it in days of volume.
4. Record the announcement and effective dates.
5. Assess the anticipated portion.
6. Write the estimate with its error band.

## Anti-patterns

- Assuming the decision before it is announced.
- Quoting flow without expressing it in days of volume.
- Ignoring the anticipation that precedes the effective date.
- Using the wrong asset base for the tracked index.
- Treating the estimate as a certainty.

## Done checklist

- [ ] Index and dates recorded.
- [ ] Weight and assets recorded.
- [ ] Flow estimated in days of volume.
- [ ] Criteria assessed.
- [ ] Anticipation estimated.
- [ ] Error band stated.

The flow's counterpart is equally important: an addition forces buying of the same magnitude, and the two often occur together in a rebalance, so a stock being deleted from one index and added to another can face offsetting pressures that a single-index estimate would miss entirely.


## Sources

- Index methodology and announcements: <https://www.investor.gov/introduction-investing>
- Market structure context: <https://www.sec.gov/investor>
- Fund and index data: <https://fred.stlouisfed.org/>
