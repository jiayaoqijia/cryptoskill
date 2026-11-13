---
name: index-futures-record
domain: investing/index-futures-record
trigger: "Writing the record of an index futures position or hedge."
anti_trigger: "Not for recommending a position, and not for the broker statement."
scope: "The written record: contract, basis, roll plan, hedge ratio, and margin."
status: seedling
---

# Index futures record

## Standard

The record for an index futures position states the contract, the price relative to fair value, the hedge ratio if it is a hedge, the margin posted, and the roll plan. Those five items are what allow a review to distinguish a position that lost because the market moved from one that lost because the roll was late, the basis was rich, or the hedge ratio was wrong.

Its second function is to keep the exposure visible while the position is open. An index future is leveraged: the notional can be many times the margin, and a move that seems small in index points can be large relative to the capital committed. Recording notional and margin side by side makes that ratio explicit at every review rather than only at the moment of a margin call.

Primary sources: <https://www.cmegroup.com/> and <https://osf.io/prereg/>.

## Decision rules

- The record states contract, month, direction, size, price, and timestamp.
- Notional and margin are recorded together, so the leverage is visible.
- The basis at entry and fair value at entry are recorded with the inputs.
- The roll plan is dated, with the window and the fallback.
- For a hedge, the beta, window, and contract count are recorded with the residual exposures.
- Review entries record basis changes, margin changes, and roll proximity.

## Procedure

1. Record the contract, price, size, and timestamp.
2. Record notional and margin.
3. Record fair value, the basis, and the inputs used.
4. Write the roll plan with dates.
5. Record the hedge ratio and residuals where applicable.
6. Review at each trigger and record what changed.

## Anti-patterns

- Recording the price without the notional.
- Leaving the roll plan implicit.
- Recording a hedge without its beta and residual.
- Reporting a result without roll cost.
- Reviewing only the profit and loss.

## Done checklist

- [ ] Contract and price recorded.
- [ ] Notional and margin recorded.
- [ ] Basis and inputs recorded.
- [ ] Roll plan dated.
- [ ] Hedge ratio and residuals recorded.
- [ ] Reviews record basis, margin, roll status.

The record's review cadence should match the contract's cycle rather than the calendar: a position reviewed quarterly, just before the roll, will always be reviewed at the same point in the basis's life, and the comparison across periods then means something.


## Sources

- Exchange contract and margin data: <https://www.cmegroup.com/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Investor education on futures risk: <https://www.investor.gov/introduction-investing>
