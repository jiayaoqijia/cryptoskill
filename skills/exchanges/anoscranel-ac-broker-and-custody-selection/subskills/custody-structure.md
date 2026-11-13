---
name: custody-structure
domain: investing/custody-structure
trigger: "Establishing who legally owns the assets behind an account."
anti_trigger: "Not for assessing the firm's solvency, and not for legal advice."
scope: "Nominee and omnibus holding, beneficial ownership, and what the account holder actually owns."
status: seedling
---

# Custody structure

## Standard

Most retail accounts hold assets through a nominee: the broker's name appears on the register, and the client holds a beneficial entitlement recorded in the broker's books. That arrangement is normal and, in a well-regulated jurisdiction, it keeps client assets separate from the firm's own. But the details decide what happens in a failure, and they differ by structure.

The distinctions worth recording are whether client assets are segregated or pooled, whether the firm lends them out, whether the account is held directly in the client's name, and what the local rules say about rehypothecation. A nominee account with strict segregation and no lending is a different object from one that permits both, and the difference is disclosed in terms most clients never read.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record the legal holder of the assets: nominee, custodian, or the client directly.
- Record whether client assets are segregated from the firm's own and whether they are pooled with other clients'.
- Record whether the firm may lend or pledge client assets, and under what conditions.
- Record the jurisdiction whose insolvency rules would apply.
- Distinguish cash held at the broker from cash swept to a bank, since the two have different protections.
- Where the terms are silent, record that as a gap rather than assuming the favourable reading.

## Procedure

1. Read the client agreement and the custody section.
2. Identify the legal holder and the segregation arrangement.
3. Record lending and pledging permissions.
4. Identify the applicable jurisdiction and its asset-protection rules.
5. Check how cash balances are held and swept.
6. Write the structure summary with the gaps named.

## Anti-patterns

- Assuming the account holder is the registered owner.
- Treating "segregated" as meaning "protected in all circumstances".
- Ignoring securities lending buried in the terms.
- Assuming cash at the broker is insured the same way as cash at a bank.
- Reading a marketing page instead of the client agreement.

## Done checklist

- [ ] Legal holder recorded.
- [ ] Segregation and pooling recorded.
- [ ] Lending and pledging permissions recorded.
- [ ] Applicable jurisdiction recorded.
- [ ] Cash treatment recorded.
- [ ] Gaps named.

The discussion with the provider should end with a sentence the client can repeat: what do I own, in whose name, and what may the firm do with it while I hold it. A provider that cannot answer that plainly has answered it.

## Sources

- Investor education on brokerage accounts and custody: <https://www.investor.gov/introduction-investing>
- Market structure and settlement context: <https://www.sec.gov/investor>
- Client asset protection standards: <https://www.bis.org/>
