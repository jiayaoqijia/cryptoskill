---
name: rebalancing-with-tax
domain: investing/rebalancing-with-tax
trigger: "Rebalancing without realising more gains than necessary."
anti_trigger: "Not for tax advice, and not for allocation policy."
scope: "Rebalancing with new money, in-kind, and the realised-gain cost."
status: seedling
---

# Rebalancing with tax

## Standard

Rebalancing normally means selling what has risen and buying what has fallen, which in a taxable account realises gains. The tax-aware alternative is to rebalance with new money: contributions and income are directed to the underweight holdings, which corrects the drift without any sale. The cost is that the correction is slower and bounded by the size of the flows.

Where a sale is necessary, the tools are to choose which lots to sell and to prefer holdings with a loss or a small gain. The choice of lot matters because identical shares can have different bases, and selling the highest-basis lot realises the least gain. The record should state the drift, the correction achieved by flows, and the residual that required a sale.

Primary sources: <https://www.irs.gov/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the drift per holding and the tolerance band.
- Record the flows available in the period and the correction they can achieve.
- Record the lots available and their bases.
- Record which lots would be sold if a sale is required.
- Record the realised gain the sale would produce.
- Record the residual drift left unaddressed.

## Procedure

1. Measure drift against the target weights.
2. Estimate the correction achievable with flows.
3. Identify the residual requiring a sale.
4. Select lots by basis.
5. Compute the realised gain.
6. Record the result and the remaining drift.

## Anti-patterns

- Selling to rebalance without using available flows first.
- Ignoring lot selection and selling the oldest position by default.
- Rebalancing to a precision that costs more in tax than it returns in risk control.
- Forgetting that a sale in one account can be offset by a purchase in another.
- Treating the tolerance band as a target rather than a boundary.

## Done checklist

- [ ] Drift and tolerance recorded.
- [ ] Flow correction estimated.
- [ ] Residual recorded.
- [ ] Lots selected by basis.
- [ ] Realised gain computed.
- [ ] Remaining drift recorded.

The tolerance band is the parameter that decides whether rebalancing helps or costs: a wide band trades more drift for fewer sales, and the right width depends on how much the risk control is worth relative to the tax, which is a comparison that should be recorded rather than inherited from a default.


## Sources

- Tax administration guidance on gains: <https://www.irs.gov/>
- Investor education on rebalancing: <https://www.investor.gov/introduction-investing>
- Portfolio policy context: <https://www.sec.gov/investor>
