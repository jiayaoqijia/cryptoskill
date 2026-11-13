---
name: commodity-spreads
domain: investing/commodity-spreads
trigger: "Expressing a commodity view through a spread rather than an outright position."
anti_trigger: "Not for recommending a spread, and not for predicting prices."
scope: "Calendar spreads, crack and crush spreads, and basis versus the physical market."
status: seedling
---

# Commodity spreads

## Standard

A spread trades a relationship rather than a price: one contract month against another, a product against its input, or a futures price against the physical. The attraction is that the spread removes the outright direction, which lets a view about storage, processing margins, or logistics be expressed without taking a position on the market's level. The cost is that the risk moves into the relationship, which can be more volatile and less liquid than either leg.

The three families that matter are calendar spreads, which price storage and timing; processing spreads such as crack and crush, which price the margin between a raw commodity and its products; and basis, which is the difference between a futures price and a physical quote at a location. Each has its own liquidity profile, and the execution risk sits in the leg that is harder to trade.

Primary sources: <https://www.cmegroup.com/> and <https://www.eia.gov/>.

## Decision rules

- State the relationship being traded and why it should change or persist.
- Record the historical range of the spread and its liquidity.
- Record the execution plan for both legs, including which leg is harder to fill.
- Compute the margin for a spread position, which differs from the outright margin.
- Record the delivery and notice dates for each leg separately.
- Record what happens if one leg is assigned or expires while the other is open.

## Procedure

1. Define the spread precisely: legs, months, and ratio.
2. Collect the spread's history and its typical range.
3. Assess liquidity on each leg and plan the execution order.
4. Record spread margin and the risk of a leg moving alone.
5. Record notice and expiry dates per leg.
6. Write the trade with its relationship thesis and its leg risk.

## Anti-patterns

- Trading a spread without checking the liquidity of the far leg.
- Assuming a spread is low risk because the legs offset.
- Ignoring the different notice dates of the two legs.
- Using outright margin to size a spread position.
- Treating an historical spread range as a bound.

## Done checklist

- [ ] Spread defined with legs and ratio.
- [ ] History and range recorded.
- [ ] Liquidity assessed per leg.
- [ ] Spread margin recorded.
- [ ] Notice dates recorded per leg.
- [ ] Leg risk written into the trade.

## Sources

- Exchange spread specifications and margin: <https://www.cmegroup.com/>
- Energy and product market data: <https://www.eia.gov/>
- Market positioning data: <https://www.cftc.gov/>
