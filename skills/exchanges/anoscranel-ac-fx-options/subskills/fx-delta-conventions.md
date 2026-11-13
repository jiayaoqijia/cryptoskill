---
name: fx-delta-conventions
domain: investing/fx-delta-conventions
trigger: "Working out which delta an FX option quote is using and what it hedges."
anti_trigger: "Not for generic greeks, and not for predicting the rate."
scope: "Spot, forward, and premium-adjusted delta, and why three exist."
status: seedling
---

# FX delta conventions

## Standard

FX options have three deltas in common use, and they differ because the hedge and the premium are in different currencies. Spot delta measures the change in the option's value for a move in spot, expressed in the base currency. Forward delta measures the same against the forward, which is what a hedger actually trades when the premium settles later. Premium-adjusted delta subtracts the effect of the premium itself, because the premium is paid in one currency and changes the exposure when it is converted.

The reason to care is that a strike quoted as "25 delta" means a different price under each convention, and a hedge sized on one convention while the position is quoted in another will be systematically wrong. The market convention varies by pair: premium-adjusted delta is common in the pairs where the premium currency is the one being bought or sold in size, and spot delta is common elsewhere.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record which delta convention the quote uses, per pair.
- Record the hedge instrument: spot or forward.
- Convert between conventions when comparing quotes from different sources.
- Record the premium currency and its effect on the adjusted delta.
- Record the strike in both delta and price terms.
- Where the convention is unclear, record it as a question rather than assuming.

## Procedure

1. Identify the convention for the pair in the market being traded.
2. Convert the quoted delta into the strike price.
3. Record the hedge instrument and the resulting hedge ratio.
4. Convert the strike back to delta under the alternative convention for comparison.
5. Record the premium currency effect.
6. Write the delta summary with the convention named.

## Anti-patterns

- Comparing deltas from two sources without checking the convention.
- Hedging a premium-adjusted position with a spot delta.
- Treating a 25-delta strike as a fixed price.
- Ignoring the premium currency in the exposure.
- Assuming one convention applies to every pair.

## Done checklist

- [ ] Convention recorded per pair.
- [ ] Strike computed from delta.
- [ ] Hedge instrument recorded.
- [ ] Alternative convention computed for comparison.
- [ ] Premium currency effect recorded.
- [ ] Summary names the convention.

## Sources

- Foreign exchange market conventions and surveys: <https://www.bis.org/>
- Market rates and data: <https://www.federalreserve.gov/>
- Investor education on options: <https://www.investor.gov/introduction-investing>
