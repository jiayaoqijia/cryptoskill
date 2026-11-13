---
name: repo-and-financing
domain: investing/repo-and-financing
trigger: "Working out the financing cost and collateral terms behind a rates position."
anti_trigger: "Not for predicting policy rates, and not for bond portfolio mechanics."
scope: "Repo rates, specials, and the carry of a long or short position."
status: seedling
---

# Repo and financing

## Standard

A cash bond position is financed in the repo market, where the bond is pledged as collateral against cash for a term. The repo rate is the cost of that financing, and for a particular bond it can trade below the general rate when the bond is scarce — a special — because holders pay to borrow it. The futures basis is built on the general rate, so a special in the deliverable bond changes the arbitrage.

For a short, the direction reverses: the position earns the repo rate on the cash proceeds and pays the coupon to the lender, and the net carry is what the basis is measured against. That is why a basis trade that looks profitable can be a financing trade in disguise, and why the repo rate assumption belongs in the record next to the price.

Primary sources: <https://www.federalreserve.gov/> and <https://www.newyorkfed.org/>.

## Decision rules

- Record the repo rate used for the term, and its source.
- Record whether the deliverable bond trades special and by how much.
- Record the carry of the position: coupon accrual less financing.
- Record the counterparty and collateral terms for a repo trade.
- Record what happens if the repo rolls at a different rate.
- Record the haircut applied to the collateral.

## Procedure

1. Collect the general collateral rate for the relevant term.
2. Check whether the deliverable trades special.
3. Compute carry as coupon accrual less financing cost.
4. Record the collateral and haircut terms.
5. Test the carry at a higher and lower repo rate.
6. Record the financing assumption alongside the price.

## Anti-patterns

- Using the policy rate as the repo rate.
- Ignoring a special in the deliverable bond.
- Assuming the repo rolls at the same rate.
- Treating carry as riskless when the roll is uncertain.
- Omitting the haircut from the capital calculation.

## Done checklist

- [ ] Repo rate and term recorded.
- [ ] Specials checked.
- [ ] Carry computed.
- [ ] Collateral and haircut recorded.
- [ ] Rate sensitivity tested.
- [ ] Financing assumption recorded with the position.

The financing also determines the maximum size of a basis position: a trade that earns a few basis points over the delivery window only works if the repo rate is stable and the haircut is small, and a widening haircut can turn a profitable basis into a funding problem before the position ever reaches delivery.

## Sources

- Repo market data and operations: <https://www.newyorkfed.org/>
- Policy rates and Treasury data: <https://www.federalreserve.gov/>
- Short-rate series: <https://fred.stlouisfed.org/>
