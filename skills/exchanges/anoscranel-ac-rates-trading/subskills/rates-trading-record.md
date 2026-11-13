---
name: rates-trading-record
domain: investing/rates-trading-record
trigger: "Writing the record of a rates position and its hedge."
anti_trigger: "Not for recommending a rate view, and not for the account statement."
scope: "The written record: contract, CTD, DV01, financing, and curve exposure."
status: seedling
---

# Rates trading record

## Standard

The rates record must state which contract, which deliverable, which DV01, which financing rate, and which curve exposure the position carries. Those five facts are what make a rates position reproducible and reviewable, and each of them can change while the position sits unchanged: the CTD switches, the repo rate resets, the curve moves.

The record's second job is to separate the intended exposure from the incidental one. A curve trade carries a small duration exposure if the weights drift; a hedge carries basis risk if the CTD changes; a long bond position financed in repo carries roll risk at every reset. Writing those down at entry is what allows a review to attribute a result to the right cause.

Primary sources: <https://www.cmegroup.com/> and <https://osf.io/prereg/>.

## Decision rules

- The record states contract, month, size, price, and the CTD with its conversion factor.
- DV01 per leg and the hedge ratio are recorded with the yields used.
- The repo rate, collateral, and haircut are recorded where financing applies.
- The curve exposure is stated in spread terms with the weights.
- The event calendar for the holding period is recorded with the treatment of each event.
- Review entries record CTD changes, repo resets, and hedge drift.

## Procedure

1. Record the contract, price, and CTD.
2. Record DV01 per leg and the weights.
3. Record the financing terms.
4. Record the event calendar and the treatments.
5. Review at each trigger and record what changed.
6. At exit, record the result decomposed into level, curve, and carry.

## Anti-patterns

- Recording the price and not the CTD.
- Reporting a result without decomposing carry.
- Leaving the repo assumption out of the record.
- Reviewing only the profit and loss.
- Editing the entry record after the fact.

## Done checklist

- [ ] Contract and CTD recorded.
- [ ] DV01 and weights recorded.
- [ ] Financing terms recorded.
- [ ] Event calendar with treatments recorded.
- [ ] Reviews record changes to CTD and repo.
- [ ] Exit decomposed into level, curve, carry.

The decomposition matters more in rates than in most markets because the same profit can come from three unrelated sources: a parallel move, a change in the curve's shape, and the carry of the financing. Attributing the result to the wrong source is how a strategy gets credited with skill it does not have.

## Sources

- Exchange contract and delivery data: <https://www.cmegroup.com/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Treasury and repo data: <https://www.federalreserve.gov/>
