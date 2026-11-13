---
name: corporate-actions-record
domain: investing/corporate-actions-record
trigger: "Writing the record of a corporate action and its effects."
anti_trigger: "Not for the tax computation, and not for judging the action."
scope: "The written record: action, terms, dates, effects on position, basis, and data."
status: seedling
---

# Corporate actions record

## Standard

The record of a corporate action is written once, at the time, and it answers four questions later: what happened, what the terms were, how the position changed, and how the data was adjusted. A record that answers all four makes the position auditable and the backtest reproducible; one that answers two leaves the rest to reconstruction.

The record is per action and per holding, dated, and sourced. Where a deal was revised, the amendment is appended — never a rewrite — so the chain from the original terms to the final position is visible.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- One record per action per holding, dated and sourced.
- The terms are quoted from the issuer's document, with its date.
- The position effect is stated in shares, cash, and basis.
- The data effect is stated as which series were adjusted and how.
- Amendments are appended with dates; the original is retained.
- The record is stored with the position and the tax inputs.

## Procedure

1. State the action and its source document.
2. Record the terms and dates.
3. Record the position effect: shares, cash, basis.
4. Record the data effect: series and adjustment.
5. Append any amendment.
6. File with the position record.

## Anti-patterns

- Writing the record after the position has changed and reconstructing.
- Omitting the data effect, which makes the chart unreproducible.
- Rewriting the record when terms change.
- Leaving the source document unnamed.
- Filing the record away from the position.

## Done checklist

- [ ] Action and source stated.
- [ ] Terms and dates recorded.
- [ ] Position effect recorded.
- [ ] Data effect recorded.
- [ ] Amendments appended.
- [ ] Filed with the position record.

## Sources

- Regulatory context for corporate action disclosure: <https://www.sec.gov/investor>
- Investor education on reorganisations: <https://www.investor.gov/introduction-investing>
- Rule context for processing and settlement: <https://www.finra.org/rules-guidance>

The record also protects against the quiet failure mode: a broker applies a ratio, the data vendor applies a different one, and the position and the chart drift apart without either looking wrong in isolation. Writing the data effect down is what makes that drift visible at the next reconciliation.

Store the record where the position is stored, and reference it from the tax pack rather than duplicating it. A single record read by both is auditable; two copies that diverge are not, and divergence is the normal outcome when the same facts are maintained twice.
