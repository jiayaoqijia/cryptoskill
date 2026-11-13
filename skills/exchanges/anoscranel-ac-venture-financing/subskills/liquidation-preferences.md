---
name: liquidation-preferences
domain: investing/liquidation-preferences
trigger: "Reading the preference stack that governs payout order in a sale."
anti_trigger: "Not for a valuation opinion, and not for trading positions."
scope: "The preference stack, participation, and seniority in a sale."
status: seedling
---

# Liquidation preferences

## Standard

A liquidation preference is the amount a preferred series collects before common stock receives anything. The archetypal terms: the preference is a multiple of the original issue price — one-times is standard — and it either participates in the residual after collecting its preference (participating) or converts to common when that is worth more (non-participating). Seniority decides which series pays first when the proceeds cannot satisfy everyone, and the modern convention of "pari passu" across series makes all preferred share the same rank, which is simpler until a scarce exit reveals that it was still a negotiation.

The preference stack exists because venture returns are power-law distributed: most companies return little, and the preference defines who recovers what in those outcomes. A company that raised at high valuations with one-times non-participating preferences has a stack whose economics differ sharply from the same cap table with participating preferences, and the difference widens in the middle outcomes — the exits between the jelly and the jackpot — which are exactly where most exits land.

Primary sources: <https://www.law.cornell.edu/> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- Record every series' preference multiple, its original issue price, and the preference amount in currency.
- Record participation rights and their caps, if any.
- Record seniority across series — pari passu or stacked — and the payout order that follows.
- Distinguish the treatment of a deemed liquidation event (acquisition) from an IPO, whose typical effect is to convert all preferred to common.
- Record the conversion price of each series, including any changes from anti-dilution adjustments.
- Compute the minimum exit value at which each series prefers conversion over its preference.

## Procedure

1. List every preferred series with preference multiple, participation, and issue price.
2. Compute each series' preference amount in currency.
3. Fix the seniority order and identify the pari passu groupings.
4. Model the exit waterfall at several exit values to find the conversion crossover points.
5. Note the IPO conversion trigger and its effect on the stack.
6. Write the stack summary with the crossover exit values visible.

## Anti-patterns

- Assuming "1x non-participating" is the only form the preference ever takes.
- Treating pari passu as equality of payout: within a pari passu tier the preference amounts still differ.
- Reading the stack without a conversion-crossover analysis.
- Forgetting that an IPO typically collapses the stack by converting everything to common.
- Discussing "percentage ownership" without the preference stack beneath it.

## Done checklist

- [ ] Every series' preference recorded with multiple and participation.
- [ ] Seniority and pari passu tiers fixed.
- [ ] Conversion crossovers computed.
- [ ] Deemed-liquidation vs IPO treatment stated.
- [ ] Conversion prices verified against current terms.
- [ ] Stack summary written with crossover values.

## Sources

- Statutory reference on preferred stock rights: <https://www.law.cornell.edu/>
- Form D and other private placements filings: <https://www.sec.gov/edgar/search/>
- Stock-based compensation and equity: <https://www.fasb.org/>
