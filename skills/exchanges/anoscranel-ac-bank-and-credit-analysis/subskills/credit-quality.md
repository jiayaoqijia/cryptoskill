---
name: credit-quality
domain: investing/credit-quality
trigger: "Assessing a loan book's quality and where it sits in the credit cycle."
anti_trigger: "Not for predicting defaults, and not for capital adequacy."
scope: "Non-performing loans, provisions, coverage, and charge-offs through the credit cycle."
status: seedling
---

# Credit quality

## Standard

Credit quality is measured with three numbers that must be read together: the non-performing loan ratio, the provision coverage against those loans, and the charge-off rate. A low NPL ratio with thin coverage means the losses have not been recognised yet; a high ratio with strong coverage means the losses are known and provided for. The combination tells you where in the cycle the book is.

The cycle matters more than the snapshot. Loans are underwritten in good times and default in bad ones, so a book grown quickly during a credit expansion carries risk that does not appear in current ratios. Comparing the loan growth rate with the peer group, and the current provisioning with the prior downturn's, is how the record captures that.

Primary sources: <https://www.fdic.gov/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record NPL ratio, coverage ratio, and charge-off rate together, with dates.
- Separate the NPL ratio by loan category; a blended ratio hides concentration.
- Compare current provisioning with the prior cycle's peak as a reserve-adequacy check.
- Record loan growth against peer growth; rapid growth in a late cycle is a flag.
- Restructured and forbearance loans are recorded separately from performing loans.
- Where categories are not disclosed, record the gap and cap the confidence.

## Procedure

1. Pull NPLs, provisions, charge-offs, and the loan book by category.
2. Compute the three ratios and their year-on-year change.
3. Break the NPL ratio down by category.
4. Compare provisioning with the prior cycle's peak.
5. Compute loan growth and compare with peers.
6. Write the cycle-position assessment with confidence.

## Anti-patterns

- Reading the NPL ratio alone.
- Treating a low charge-off rate as evidence of quality in a young book.
- Ignoring restructured loans.
- Comparing ratios across regimes with different classification rules.
- Assuming the prior cycle's peak is the maximum.

## Done checklist

- [ ] Three ratios computed with dates.
- [ ] NPL ratio broken down by category.
- [ ] Provisioning compared with the prior cycle.
- [ ] Loan growth compared with peers.
- [ ] Restructured loans recorded separately.
- [ ] Cycle position stated with confidence.

## Sources

- FDIC bank data and quarterly profile: <https://www.fdic.gov/>
- Federal Reserve supervisory data: <https://www.federalreserve.gov/>
- Investor education on credit risk: <https://www.investor.gov/introduction-investing>

The provisioning history is where the honesty of a loan book shows. A bank that provisioned heavily in the last downturn and lightly in this expansion is telling a consistent story; one that provisioned lightly in both is either unusually well underwritten or deferring the recognition, and the record cannot distinguish those without the cycle evidence.
