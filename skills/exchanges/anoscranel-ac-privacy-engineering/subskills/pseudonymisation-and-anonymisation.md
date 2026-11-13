---
name: pseudonymisation-and-anonymisation
domain: software-engineering/pseudonymisation-and-anonymisation
trigger: "Judging whether data is pseudonymised, anonymised, or neither."
anti_trigger: "Not for legal determination, and not for analytics methodology."
scope: "Reversible identifiers versus data that cannot be re-identified."
status: seedling
---

# Pseudonymisation and anonymisation

## Standard

Pseudonymisation replaces a direct identifier with a token that can be mapped back, so the data is harder to attribute but remains personal data because the mapping exists. Anonymisation removes the possibility of re-identification, which is a stronger and much harder claim: a dataset with no names can still be re-identified by joining on a quasi-identifier combination such as postcode, birth date, and sex.

The engineering distinction is where the mapping lives and who can reach it. A tokenisation service that holds the mapping in a separate store with access controls is pseudonymisation done well; the same token with the mapping in the same table is a renamed column. The record must state which of these the system implements, because the answer decides what obligations follow.

Primary sources: <https://ico.org.uk/> and <https://www.nist.gov/privacy-framework>.

## Decision rules

- Record whether a mapping exists and where it is stored.
- Record who has access to the mapping and under what control.
- Record the quasi-identifiers retained and the re-identification risk they create.
- Record any aggregation or generalisation applied and its granularity.
- Record the residual risk assessment and who performed it.
- Record the claim made about the dataset, stated precisely, since "anonymous" is a legal conclusion.

## Procedure

1. Record whether identifiers are direct, tokenised, or removed.
2. Record the mapping's location and access control.
3. Enumerate quasi-identifiers and assess the combination.
4. Record the generalisation or aggregation applied.
5. Record the residual risk and its assessor.
6. State the claim precisely and record who approved it.

## Anti-patterns

- Calling tokenised data anonymous because the column was renamed.
- Removing names while retaining postcode, birth date, and sex.
- Assuming a small sample protects against re-identification.
- Making the anonymisation claim in code comments rather than in the record.
- Ignoring that risk rises as external datasets become available.

## Done checklist

- [ ] Identifier treatment recorded.
- [ ] Mapping location and access recorded.
- [ ] Quasi-identifiers enumerated.
- [ ] Generalisation recorded.
- [ ] Residual risk recorded with assessor.
- [ ] Claim stated precisely with approval.

The practical test is to ask what an attacker would need to re-identify the dataset, and whether they could obtain it: if the answer is a public voter roll or a purchased marketing list, the dataset is not anonymous regardless of what was removed, and the record should say which external source was considered.


## Sources

- Anonymisation guidance: <https://ico.org.uk/>
- NIST privacy framework: <https://www.nist.gov/privacy-framework>
- Statistical disclosure control reference: <https://www.ons.gov.uk/>
