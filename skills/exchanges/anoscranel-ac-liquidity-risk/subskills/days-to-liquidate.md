---
name: days-to-liquidate
domain: investing/days-to-liquidate
trigger: "Computing how long a position or a portfolio would take to exit."
anti_trigger: "Not for predicting volume, and not for position sizing on one name."
scope: "Participation rates, volume baselines, and the portfolio-level ladder."
status: seedling
---

# Days to liquidate

## Standard

Days to liquidate divides a position by the volume the market can absorb each day at a stated participation rate. A position equal to one day's average volume, exited at ten percent participation, takes ten days. The participation rate is the key assumption: it encodes how much price impact is acceptable, and a higher rate shortens the schedule while raising the concession.

At portfolio level the measure is not the sum of individual days, because the positions compete for the same liquidity and because the largest holdings dominate. The portfolio's liquidity is set by the slowest meaningful position, and by how many of the positions would have to be sold in the same window if a large cash requirement arrived.

Primary sources: <https://www.bis.org/> and <https://www.finra.org/>.

## Decision rules

- Record the position size and the volume baseline, with the window used.
- Record the participation rate assumed, and its justification.
- Compute days to liquidate per holding.
- Rank holdings by their contribution to the portfolio total.
- Record the portfolio figure as the time to raise a stated percentage of value.
- Record the volume baseline's date and whether it includes stressed periods.

## Procedure

1. Collect position sizes and volume baselines.
2. Choose a participation rate and record why.
3. Compute days per holding.
4. Rank by contribution.
5. Compute the time to raise 25, 50, and 75 percent of value.
6. Write the ladder with its assumptions.

## Anti-patterns

- Summing days across holdings as if liquidity were pooled.
- Using a volume baseline from one calm month.
- Choosing a participation rate without stating the price impact it implies.
- Treating the average volume as available on the day it is needed.
- Reporting a single number without the percentage of value it refers to.

## Done checklist

- [ ] Size and volume baseline recorded.
- [ ] Participation rate recorded with justification.
- [ ] Days computed per holding.
- [ ] Holdings ranked by contribution.
- [ ] Time to raise stated percentages computed.
- [ ] Baseline date and coverage recorded.

A further refinement is to compute the figure at two participation rates and record the pair: the difference between a ten percent and a twenty-five percent schedule is the price of urgency expressed in days, and a portfolio whose two figures diverge sharply is one whose exit cost depends heavily on how much time the holder has.


## Sources

- Market liquidity and infrastructure standards: <https://www.bis.org/>
- Trading volume and reporting guidance: <https://www.finra.org/>
- Volume series: <https://fred.stlouisfed.org/>
