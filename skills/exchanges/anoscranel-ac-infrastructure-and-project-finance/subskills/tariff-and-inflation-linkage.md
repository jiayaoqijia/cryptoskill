---
name: tariff-and-inflation-linkage
domain: investing/tariff-and-inflation-linkage
trigger: "Reading how a project's tariff moves with inflation."
anti_trigger: "Not for forecasting inflation, and not for legal advice."
scope: "How the tariff moves with prices, and where the linkage breaks."
status: seedling
---

# Tariff and inflation linkage

## Standard

Infrastructure revenue is often indexed, and the index matters more than the level. A tariff linked to a published consumer price index preserves real revenue if the index reflects the costs the asset actually faces; a tariff linked to a different measure, or capped for a period, does not. The linkage is the difference between an asset whose real return survives inflation and one whose nominal return quietly erodes.

Two limitations appear repeatedly. The first is a cap or a collar on the indexation, which limits the pass-through in high-inflation periods. The second is a regulatory or contractual reset that changes the allowed return at a review, which can remove the benefit of indexation entirely. Both are disclosed in the tariff mechanism, and both belong in the record alongside the headline index.

Primary sources: <https://www.worldbank.org/> and <https://www.eib.org/>.

## Decision rules

- Record the index the tariff references and its publication source.
- Record the frequency and timing of the adjustment.
- Record any cap, collar, or floor on the indexation.
- Record any regulatory reset and the basis on which the allowed return is set.
- Compare the indexed revenue's growth with the asset's cost inflation.
- Record the effect of a high-inflation period on the coverage ratio.

## Procedure

1. Read the tariff mechanism from the contract or the regulatory determination.
2. Record the index and its source.
3. Record the adjustment frequency and any caps.
4. Record any reset mechanism.
5. Compare the index with the asset's cost base.
6. Write the analysis with the coverage effect stated.

## Anti-patterns

- Assuming the tariff index matches the asset's cost inflation.
- Ignoring a cap that binds in the periods that matter.
- Overlooking a regulatory reset that changes the allowed return.
- Treating indexation as protection without checking the base it applies to.
- Using a long-run average inflation assumption for a period with a cap.

## Done checklist

- [ ] Index and source recorded.
- [ ] Adjustment frequency recorded.
- [ ] Caps and collars recorded.
- [ ] Reset mechanism recorded.
- [ ] Index compared with cost inflation.
- [ ] Coverage effect stated.

The index's base period is worth recording as well: a tariff adjusted from a base that has already drifted away from the asset's cost structure will index faithfully while preserving a real-terms gap, and the gap is invisible unless the base and the cost base are compared rather than assumed to match.


## Sources

- Infrastructure regulation and tariff guidance: <https://www.worldbank.org/>
- Project finance standards: <https://www.eib.org/>
- Inflation data: <https://fred.stlouisfed.org/>
