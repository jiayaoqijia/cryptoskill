---
name: cost-decomposition
domain: investing/cost-decomposition
trigger: "Splitting trading cost into spread, impact, delay, and opportunity."
anti_trigger: "Not for predicting impact, and not for venue selection."
scope: "Spread, impact, delay, and opportunity cost as separate measurements."
status: seedling
---

# Cost decomposition

## Standard

Total cost decomposes into four parts that have different causes and different remedies. The spread is what is paid to cross the bid-ask. Impact is the price movement caused by the order itself, which grows with size and falls with patience. Delay is the drift between the decision and the execution, which is a function of process rather than of market structure. Opportunity cost is the value of the portion not filled.

Separating them tells you what to fix. A high spread component suggests smaller orders or better venues; a high impact component suggests slicing or longer horizons; a high delay component suggests an execution process problem rather than a market problem; and a high opportunity component suggests orders are being given limits they cannot reach. A single blended number cannot distinguish those, which is why the decomposition is the point.

Primary sources: <https://www.cfainstitute.org/> and <https://www.finra.org/>.

## Decision rules

- Record each component separately and the method used to attribute it.
- Record the spread at the time of execution, not a daily average.
- Record impact against a stated model or measurement approach.
- Record delay as the difference between decision and arrival.
- Record opportunity cost at a stated reference price.
- Record the attribution method's assumptions where it relies on a model.

## Procedure

1. Record the four components and their definitions.
2. Compute the spread component from the quotes at execution.
3. Compute impact from the price path after the fills.
4. Compute delay from decision to arrival.
5. Compute opportunity cost for the unfilled portion.
6. Write the decomposition with the largest component named.

## Anti-patterns

- Reporting a blended cost with no attribution.
- Attributing all cost to impact by default.
- Using a daily average spread for intraday executions.
- Ignoring the model behind an impact estimate.
- Treating the components as additive when they interact.

## Done checklist

- [ ] Four components defined and recorded.
- [ ] Spread computed from quotes at execution.
- [ ] Impact computed with method stated.
- [ ] Delay computed.
- [ ] Opportunity computed.
- [ ] Largest component named.

The interaction between components is the reason the decomposition should be read as a set of signs rather than as an arithmetic sum: a patient order lowers impact and raises delay, so a strategy that reduces one by increasing the other has not necessarily improved, and the record should show which component moved and what offset it.

## Sources

- Trading cost and performance standards: <https://www.cfainstitute.org/>
- Execution quality guidance: <https://www.finra.org/>
- Market structure context: <https://www.sec.gov/investor>
