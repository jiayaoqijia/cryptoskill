---
name: trade-finance-fraud
domain: investing/trade-finance-fraud
trigger: "Checking a transaction for the patterns that recur in trade-finance fraud."
anti_trigger: "Not for alleging fraud, and not for legal advice."
scope: "Double financing, fictitious cargo, and the patterns that recur."
status: seedling
---

# Trade finance fraud

## Standard

The recurring patterns are structural rather than clever. The same cargo is financed twice with two sets of documents; the cargo does not exist and the documents are fabricated; the warehouse issues receipts for goods it does not hold; the goods are worth less than described, or are the wrong grade entirely. Each exploits the gap between a document and the thing it represents.

The controls that detect them are correspondingly structural. Independent verification of the goods at the point of storage or shipment, a register of financing against a specific shipment, and a check for documentary inconsistency are the measures that work, and their absence is the vulnerability. A facility that relies on the borrower's own documentation without independent verification is relying on the party with the incentive to falsify.

Primary sources: <https://www.icc-ccs.org/> and <https://www.bis.org/>.

## Decision rules

- Record which party independently verifies the goods, and how.
- Record whether the cargo can be checked against a shipment register.
- Record the documentary consistency checks applied.
- Record the warehouse's independence from the borrower.
- Record the transaction's commercial logic: does the route and the margin make sense.
- Record the red flags observed and how each was resolved.

## Procedure

1. Record the verification arrangements.
2. Record the register check.
3. Record documentary consistency.
4. Record the warehouse's independence.
5. Record the commercial logic.
6. Write the fraud-risk assessment with each flag addressed.

## Anti-patterns

- Relying on the borrower's documents without independent verification.
- Ignoring a route that is commercially implausible.
- Assuming a warehouse receipt is genuine because it looks standard.
- Skipping the register check because the financing is small.
- Treating a resolved flag as evidence that no others exist.

## Done checklist

- [ ] Verification arrangements recorded.
- [ ] Register check recorded.
- [ ] Documentary consistency recorded.
- [ ] Warehouse independence recorded.
- [ ] Commercial logic recorded.
- [ ] Flags addressed individually.

The register check is the control that most directly addresses double financing, and it works only if it is centralised: a register held by one lender and not consulted by another provides no protection, which is why participation in a shared or industry register changes the risk profile of a facility rather than merely improving its paperwork. Recording whether the exposure is registered, and where, is a substantive control question.

## Sources

- Trade finance and fraud guidance: <https://www.icc-ccs.org/>
- Financial crime and trade standards: <https://www.bis.org/>
- Consumer and fraud reporting: <https://www.ftc.gov/>
