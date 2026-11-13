---
name: single-name-liquidity
domain: investing/single-name-liquidity
trigger: "Sizing a position from what one stock's book can actually absorb."
anti_trigger: "Not for measuring market-wide liquidity, and not for the investment case."
scope: "Spread, depth, and average volume per name, and the position size they permit."
status: seedling
---

# Single-name liquidity

## Standard

Liquidity in a single stock is measurable at the moment of trading and in aggregate. At the moment, it is the quoted spread and the size available at the touch; in aggregate, it is the average daily volume and the typical range around it. The two together decide the largest position that can be entered and exited without moving the price or waiting longer than the thesis allows.

The screening question is not whether a name is liquid but whether it is liquid enough for the size the idea deserves. A small-cap with a wide spread can be a fine investment and an impossible trade at size, and the position that would be prudent on the fundamentals may be several times what the book can absorb in a day. The record states the size the liquidity permits, and the trade is sized to the smaller of that and the risk budget.

Primary sources: <https://www.finra.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record average daily volume and the spread at the intended trading hour.
- Record the depth available within a stated distance from the mid.
- Compute the days-to-liquidate at the intended size, and require it to be short.
- Compare the computed size with the risk-budget size and take the smaller.
- Record the name's behaviour in its last high-volatility period, when liquidity thinned.
- Where the name is thinly traded, record the exit plan explicitly.

## Procedure

1. Collect average daily volume, spread, and depth for the name.
2. Compute the position size the book absorbs in a stated participation rate.
3. Compute days to liquidate at that size.
4. Compare with the risk-budget size.
5. Check the name's liquidity in its last stress period.
6. Record the permitted size and the exit plan.

## Anti-patterns

- Sizing from the idea and assuming the market will absorb it.
- Using average daily volume without a participation limit.
- Ignoring the spread, which is a cost paid on entry and exit.
- Treating calm-period liquidity as the stress case.
- Holding an illiquid position whose exit would take weeks.

## Done checklist

- [ ] Volume, spread, and depth recorded.
- [ ] Permitted size computed with a participation rate.
- [ ] Days to liquidate computed.
- [ ] Risk-budget size compared.
- [ ] Stress-period liquidity checked.
- [ ] Exit plan recorded.

## Sources

- Trading and liquidity guidance: <https://www.finra.org/>
- Market structure context: <https://www.sec.gov/investor>
- Investor education on trading costs: <https://www.investor.gov/introduction-investing>
