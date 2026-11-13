---
name: credit-option-liquidity
domain: investing/credit-option-liquidity
trigger: "Assessing whether a credit option can be priced and exited."
anti_trigger: "Not for predicting spreads, and not for venue due diligence."
scope: "Dealer liquidity, size, and the bid-offer in spread terms."
status: seedling
---

# Credit option liquidity

## Standard

Credit options trade through dealers, and liquidity concentrates in the major indices and in the most-traded single names. Outside those, a quote may exist but a market may not: the dealer will show a level and may not trade size at it, which is the distinction that matters when the position needs to be reduced.

The bid-offer is expressed in volatility points, and it is wide relative to the level in quiet markets. A position that is right about direction can still lose money on entry and exit if the spread is several volatility points wide, which is why the round-trip cost belongs in the trade's economics rather than in a footnote.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record two-way prices at the intended size, not one-way indications.
- Record the bid-offer in volatility points and convert it into a price cost.
- Record the size at which the market remains two-way.
- Record which expiries and strikes are quoted continuously.
- Record the counterparty and its credit standing.
- Record the exit route if the dealer stops quoting.

## Procedure

1. Request two-way prices at size.
2. Record the spread in volatility points.
3. Convert into cost per round trip.
4. Record the size threshold for a firm market.
5. Record counterparty exposure.
6. Write the liquidity assessment.

## Anti-patterns

- Treating an indicative level as a firm market.
- Ignoring the round-trip cost in the trade's economics.
- Assuming index liquidity extends to single names.
- Overlooking counterparty risk on an uncollateralised option.
- Sizing beyond the market's demonstrated depth.

## Done checklist

- [ ] Two-way prices recorded at size.
- [ ] Spread converted to cost.
- [ ] Size threshold recorded.
- [ ] Continuous quotes recorded.
- [ ] Counterparty recorded.
- [ ] Exit route written.

The practical test is the same as in any dealer market: request a price for the size the strategy needs, in both directions, and record whether the response was a market or an indication. A dealer who will buy protection but not sell it has told you which side is crowded, and that asymmetry is more informative than the spread itself when the position's exit depends on someone taking the other side.

Because the market is thin, the record should also say when the price was taken: a level sampled on a quiet morning and one sampled during a spread widening are not comparable, and a liquidity assessment without a timestamp becomes an anecdote within days.


## Sources

- Market documentation and conventions: <https://www.isda.org/>
- Regulatory market context: <https://www.federalreserve.gov/>
- Investor education on complex products: <https://www.investor.gov/introduction-investing>
