---
name: splits-and-consolidations
domain: investing/splits-and-consolidations
trigger: "Handling a share split or consolidation without corrupting the record."
anti_trigger: "Not for judging whether a split is bullish, and not for valuation."
scope: "Ratios, the share count change, and why the price is not a return."
status: seedling
---

# Splits and consolidations

## Standard

A split multiplies the share count and divides the price by the same ratio; a consolidation does the reverse. The economic position is unchanged at the moment of the split, which is why a chart showing the raw price falling by two thirds after a three-for-one split is telling you about the ratio, not about a loss.

The record must reflect three things: the new share count, the adjusted cost basis per share, and the adjustment applied to any historical series used for analysis. A split handled in the position but not in the data produces a backtest that sees a catastrophic return on the split date; a split handled in the data but not in the position produces a portfolio that appears to have gained or lost a third of its value overnight.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the ratio, the effective date, and the issuer's announcement as the source.
- Adjust the share count and the cost basis per share by the ratio; the total basis does not change.
- Confirm the broker applied the same ratio before treating the position as correct.
- Adjust every historical price and volume series used for analysis by the same ratio, or use a series already adjusted.
- A consolidation can produce fractional shares; record how the broker handled them.
- Never infer a return from a raw price change across a split date.

## Procedure

1. Record the ratio, effective date, and announcement source.
2. Recompute share count and basis per share.
3. Compare with the broker's post-action position.
4. Adjust or replace the historical series used.
5. Record the fractional-share treatment where relevant.
6. Note the action in the record with its date.

## Anti-patterns

- Reading a raw price chart across a split.
- Changing the total cost basis when only the per-share basis should change.
- Assuming the broker applied the ratio correctly without checking.
- Mixing adjusted and unadjusted series in one analysis.
- Ignoring fractional-share cash-in-lieu.

## Done checklist

- [ ] Ratio, date, and source recorded.
- [ ] Share count and basis per share recomputed.
- [ ] Broker position compared.
- [ ] Historical series adjusted or replaced.
- [ ] Fractional treatment recorded.
- [ ] Action noted in the record.

## Sources

- Regulatory context for issuer disclosures: <https://www.sec.gov/investor>
- Investor education on splits and share counts: <https://www.investor.gov/introduction-investing>
- Rule context for settlement of adjusted positions: <https://www.finra.org/rules-guidance>
