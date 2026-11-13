---
name: capacity-and-crowding
domain: investing/capacity-and-crowding
trigger: "Assessing how much capital a factor can absorb and what happens when it is crowded."
anti_trigger: "Not for predicting returns, and not for fund selection."
scope: "Turnover, market impact, and what happens when everyone holds it."
status: seedling
---

# Capacity and crowding

## Standard

Capacity is the amount of capital a factor can absorb before its own trading erodes the premium. The binding constraints are turnover, which determines how much must be traded each rebalancing, market impact, which determines what that trading costs, and the breadth of the universe, which determines how much can be held without becoming the market in each name.

Crowding is capacity's second face. When many participants hold the same factor, they sell it together when it underperforms, which amplifies drawdowns and can produce a sharp reversal that has no fundamental cause. The record should note both: the estimated capacity of the strategy and the evidence that its ownership is concentrated, since the two together determine how the factor behaves when it is tested.

Primary sources: <https://www.nber.org/> and <https://www.bis.org/>.

## Decision rules

- Record the turnover implied by the rebalancing frequency.
- Record the estimated market impact per unit traded, at the position sizes contemplated.
- Record the capacity estimate and the method behind it.
- Record the breadth of the universe and the share of each name held.
- Record the evidence on crowding: ownership data, short interest, or fund flows.
- Record the drawdown the factor experienced when it was last tested.

## Procedure

1. Compute turnover from the rebalancing schedule.
2. Estimate impact at the intended size.
3. Derive capacity from turnover and impact.
4. Record breadth and per-name share.
5. Assess crowding from ownership evidence.
6. Write the capacity and crowding summary.

## Anti-patterns

- Estimating capacity from returns without accounting for impact.
- Ignoring turnover when comparing factor definitions.
- Assuming a crowded factor is safe because its premium is documented.
- Measuring breadth as the number of names rather than the tradable float.
- Treating capacity as fixed when the universe changes.

## Done checklist

- [ ] Turnover computed.
- [ ] Impact estimated.
- [ ] Capacity derived with method.
- [ ] Breadth and per-name share recorded.
- [ ] Crowding evidence recorded.
- [ ] Prior drawdown recorded.

A practical warning sign is a factor whose recent returns have been strong while its breadth has narrowed: when a small number of names drive the premium, the strategy is closer to a concentrated bet than to a broad exposure, and the capacity estimate computed from the full universe overstates what the current portfolio can absorb.


## Sources

- Research on factor capacity and crowding: <https://www.nber.org/>
- Market liquidity and stability analysis: <https://www.bis.org/>
- Market data for impact estimation: <https://fred.stlouisfed.org/>
