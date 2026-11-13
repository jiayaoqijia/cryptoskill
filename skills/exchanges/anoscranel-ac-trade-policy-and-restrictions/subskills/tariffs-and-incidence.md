---
name: tariffs-and-incidence
domain: investing/tariffs-and-incidence
trigger: "Working out who actually pays a tariff and where the margin moves."
anti_trigger: "Not for predicting trade policy, and not for legal advice."
scope: "Who bears a tariff, and how the incidence moves through a supply chain."
status: seedling
---

# Tariffs and incidence

## Standard

A tariff is a tax on an import, collected at the border from the importer of record. Who bears it economically depends on elasticities: if the exporting producer has substitutes and the importer does not, the producer absorbs it in a lower price; if the importer has no alternative supplier, the importer passes it to the customer; in most cases it is split, and the split depends on the market power at each stage.

For an investor, the traceable question is which line in which company's accounts the tariff reaches. An importer with pricing power loses little margin; a distributor competing on price absorbs it; a manufacturer that supplies the tariffed input faces a higher cost that may or may not be recoverable. The record should name the entity, the line item, and the assumption about pass-through rather than treating the tariff as a sector-wide event.

Primary sources: <https://www.wto.org/> and <https://www.imf.org/>.

## Decision rules

- Record the tariff, its rate, its scope, and its effective date.
- Record the importer of record, which is the entity legally liable.
- Record the pass-through assumption and the evidence for it.
- Record the exposure as a share of cost of goods sold and of revenue.
- Record any exemption, quota, or exclusion the product may qualify for.
- Record the second-order exposure through suppliers and customers.

## Procedure

1. Record the measure, rate, scope, and date.
2. Identify the importer of record in the chain.
3. Estimate the gross cost at the affected volume.
4. Record the pass-through assumption and its basis.
5. Compute the margin effect at both extremes.
6. Write the incidence summary with the assumption named.

## Anti-patterns

- Assuming the exporter pays because the duty is collected abroad.
- Applying the rate to total revenue rather than affected volume.
- Ignoring exemptions and exclusions.
- Treating pass-through as certain in either direction.
- Overlooking suppliers who face the same measure upstream.

## Done checklist

- [ ] Measure, rate, scope, date recorded.
- [ ] Importer of record identified.
- [ ] Gross cost computed on affected volume.
- [ ] Pass-through assumption recorded.
- [ ] Margin effect at both extremes computed.
- [ ] Second-order exposure recorded.

The asymmetry worth recording is that a tariff collected at the border is paid by the importer in cash regardless of who bears it economically, so a company with strong pricing power can face a working-capital and cash-tax timing effect even when it fully passes the cost through, which is a liquidity consequence that a margin analysis alone misses.

## Sources

- Trade policy and tariff data: <https://www.wto.org/>
- Macroeconomic and trade statistics: <https://www.imf.org/>
- Regulatory and trade publications: <https://www.sec.gov/investor>
