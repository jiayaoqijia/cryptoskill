---
name: ownership-reconstruction
domain: investing/ownership-reconstruction
trigger: "Combining filings into a picture of who owns a security."
anti_trigger: "Not for predicting what holders will do, and not for the investment case."
scope: "Combining filings into a holding picture, and the double-counting that breaks it."
status: seedling
---

# Ownership reconstruction

## Standard

Reconstructing ownership means adding filings together without double counting. The same shares can appear in a manager's holdings report, in a fund family's aggregate disclosure, and in an index provider's basket, and a naive sum inflates the institutional share of a company well past a hundred percent. The discipline is to define the unit of aggregation before adding anything.

The second problem is coverage. Filing thresholds exclude small managers, some vehicles report only annually, and short positions are largely invisible. A reconstructed ownership picture is therefore a floor on institutional holding rather than a measurement of it, and the residual — the shares not attributed — is where the retail, insider, and unreported positions live.

Primary sources: <https://www.sec.gov/investor> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- Define the aggregation unit and record it: manager, fund family, or beneficial owner.
- Record each source's reporting date and threshold.
- Deduplicate before summing, and record the method used.
- Record the residual share that remains unattributed.
- Record the short positions that the sources do not capture.
- Where two sources conflict, record both rather than choosing one silently.

## Procedure

1. Define the unit of aggregation.
2. Collect filings with their dates and thresholds.
3. Deduplicate by the defined unit.
4. Sum and compute the attributed share.
5. Compute the residual.
6. Write the reconstruction with its method and gaps.

## Anti-patterns

- Summing filings across different reporting dates as if simultaneous.
- Double counting the same shares in a manager and its fund family.
- Presenting an attributed share as the total held.
- Ignoring short positions entirely.
- Choosing one source over another without recording the conflict.

## Done checklist

- [ ] Aggregation unit defined.
- [ ] Sources and dates recorded.
- [ ] Deduplication method recorded.
- [ ] Attributed share computed.
- [ ] Residual computed.
- [ ] Conflicts recorded.

The residual is also the most interesting number when it is large: a company whose attributed institutional holding is a minority of its shares is one where the price is set by participants the filings never describe, and a conclusion built entirely from institutional data will be describing a minority of the market. Stating the residual keeps that limit visible.


The date discipline matters as much as the deduplication: filings issued for different quarter ends describe different worlds, and adding a position disclosed as of March to one disclosed as of June produces a number that never existed on any day.


## Sources

- Filing search and ownership disclosures: <https://www.sec.gov/edgar/search/>
- Disclosure framework: <https://www.sec.gov/investor>
- Investor education on ownership: <https://www.investor.gov/introduction-investing>
