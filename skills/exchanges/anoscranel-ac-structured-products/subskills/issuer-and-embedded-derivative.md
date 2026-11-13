---
name: issuer-and-embedded-derivative
domain: investing/issuer-and-embedded-derivative
trigger: "Separating the bank credit from the derivative inside a note."
anti_trigger: "Not for assessing bank solvency in depth, and not for pricing the derivative."
scope: "The bank's credit, the hedge, and the two exposures a note bundles into one line."
status: seedling
---

# Issuer and embedded derivative

## Standard

A structured note is a debt obligation of the issuer, and the derivative is a promise inside that obligation, not a segregated asset. If the issuer fails, the derivative exposure fails with it — a fact that became concrete in the last major banking stress, when holders of structured notes discovered they were unsecured creditors rather than owners of a protected position.

The issuer usually hedges its exposure in the market, but the hedge protects the issuer, not the holder. What the holder owns is the note. That is why the assessment has two parts: the credit of the entity that must pay, and the terms of the derivative that determine how much it must pay. Neither is visible in the coupon alone.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Identify the issuing entity, its domicile, and its seniority in a resolution.
- Record the credit assessment with its date and the source used.
- Record whether the note is secured, guaranteed, or structurally subordinated.
- Note the issuer's hedge disclosure where it exists, and record that it does not protect the holder.
- Check whether the note's terms allow the issuer to substitute or terminate early.
- Where the issuer's disclosure is thin, cap the confidence in the assessment.

## Procedure

1. Identify the legal issuer from the terms, not from the brand.
2. Record the seniority and any guarantee or collateral.
3. Assess the issuer's credit with a dated source.
4. Read the early-termination and substitution clauses.
5. Record the hedge disclosure and its irrelevance to the holder's claim.
6. Write the assessment with confidence and a review date.

## Anti-patterns

- Treating the note as a segregated claim on the underlying.
- Assessing the brand rather than the issuing entity.
- Assuming the issuer's hedge protects the holder.
- Ignoring early-termination clauses that crystallise a loss.
- Using an undated credit assessment for a multi-year note.

## Done checklist

- [ ] Legal issuer and domicile identified.
- [ ] Seniority and guarantees recorded.
- [ ] Dated credit assessment written.
- [ ] Early-termination and substitution clauses recorded.
- [ ] Hedge disclosure noted as issuer protection.
- [ ] Review date set.

The practical consequence is that a note's yield must be compared with the issuer's own unsecured debt: if the note pays little more than the bank's senior bond, the extra is being paid for by the derivative rather than for the credit, and the holder is accepting equity-like risk for bond-like compensation.

## Sources

- Note disclosure and issuer obligations: <https://www.sec.gov/investor>
- Bank resolution and creditor hierarchy: <https://www.bis.org/>
- Investor education on counterparty risk: <https://www.investor.gov/introduction-investing>
