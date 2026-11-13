---
name: structure-and-counterparty
domain: investing/structure-and-counterparty
trigger: "Understanding what a fund's structure exposes the holder to."
anti_trigger: "Not for fund selection, and not for predicting defaults."
scope: "Physical versus synthetic replication, securities lending, and the counterparty chain."
status: seedling
---

# Structure and counterparty

## Standard

A fund that owns the underlying securities has one set of risks; a fund that holds a swap with a bank to deliver the index's return has another. Physical replication exposes the holder to the securities, to lending activity, and to the fund's operations. Synthetic replication exposes the holder to the swap counterparty, mitigated by collateral whose quality and marking matter more than the fund's marketing.

The counterparty chain is the point. In a physical fund, securities lending can put assets into a borrower's hands against collateral; in a synthetic fund, the swap provider's failure is the risk, and the collateral is the mitigation. Either way, the fund's documents describe it, and the record should state which structure is in use and who stands behind it.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record the replication method: physical, synthetic, or a hybrid.
- For synthetic funds, record the swap counterparty and the collateral terms.
- For securities lending, record the proportion lent, the collateral quality, and who receives the revenue.
- Record whether the fund can use derivatives beyond replication.
- Note any leverage embedded in the structure.
- Where disclosure is thin, cap the confidence and record the gap.

## Procedure

1. Read the fund's structure and replication disclosures.
2. Identify counterparties and collateral where applicable.
3. Record securities-lending practices and revenue split.
4. Note permitted derivative use and leverage.
5. Assess the mitigation and its limits.
6. Record the structure summary with confidence.

## Anti-patterns

- Assuming all index funds are physically replicated.
- Ignoring securities lending because it is "standard".
- Treating collateral as risk-free without checking its quality.
- Overlooking permitted derivative use.
- Accepting a summary instead of the fund documents.

## Done checklist

- [ ] Replication method recorded.
- [ ] Counterparties and collateral identified where applicable.
- [ ] Lending practices and revenue split recorded.
- [ ] Derivative permissions and leverage noted.
- [ ] Mitigation assessed with limits.
- [ ] Structure summary written with confidence.

## Sources

- Fund structure disclosure: <https://www.sec.gov/investor>
- Regulatory standards for collateral and counterparty risk: <https://www.bis.org/>
- Investor education on fund structures: <https://www.investor.gov/introduction-investing>

The record's purpose here is to make an invisible exposure visible. Most holders never think about the swap provider or the securities-lending collateral, which is precisely why the documents spell them out and why the fund record should carry the summary alongside the return figures it usually emphasises.
