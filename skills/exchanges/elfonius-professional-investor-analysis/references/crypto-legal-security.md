# Crypto Legal, Regulatory and Security

Purpose: identify legal and technical risks that can impair value, transferability or exit. This is analysis, not a legal opinion.

## Legal checklist

- Issuer entity, jurisdiction, legal wrapper and governing law.
- Token classification: security, commodity, utility, payment, e-money, fund unit; record the issuer's own characterization and the open question.
- Regimes to check: US securities/commodities, EU MiCA, UK, Switzerland, Singapore, UAE, Turkey and the user's jurisdiction.
- KYC/AML, sanctions, transfer restrictions, accredited-investor limits, venue eligibility.
- Tax treatment and reporting obligations; not tax advice.
- Consumer/investor protection, marketing rules, staking/lending regulation.
- Record source, date, jurisdiction and unresolved questions.

## Security checklist

- Audits: firm/contest and independence; report date; audited commit/repo; modules in and out of scope; findings by severity; remediation status; re-audit after fixes; bounty platform and maximum payout.
- Binding check: does the verified source of the deployed implementation at the recorded address correspond to the audited commit? If not established: `audit scope unverified`.
- Admin/upgrade: proxy and implementation; admin; multisig threshold and signers; timelock; renounce status; pause/blacklist; mint/burn; fee switch; oracle; rescue/sweep.
- Claim chain: native → canonical bridge → third-party bridge → wrapper → synthetic; validator/guardian set; collateral attestation; redemption terms.
- Custody: self-custody, MPC, qualified custodian or exchange; segregation, insurance, exchange insolvency and withdrawal-freeze terms only if evidenced.
- Incidents: date, mechanism, loss, recovery, root cause, fix verified on-chain, recurrence, post-mortem.

## Tables

**Audit ledger:** firm, date, commit, scope, findings, remediation, re-audit, bounty.

**Key-control matrix:** ability, function, holder type, threshold, timelock, renounced, evidence.

**Incident ledger:** date, mechanism, loss, recovery, root cause, fix, recurrence, post-mortem.

## Sources

- Official regulators, terms of service, audit reports, bug-bounty pages, block explorers, post-mortems, court/regulatory notices.
- Record jurisdiction, publication date and whether the source is the issuer or an independent party.

## Red flags

- Unaudited upgradeable proxy; EOA admin; no timelock; hidden mint or pause power.
- Audit scope excludes core modules; code changed after the audit; critical findings unresolved.
- Bridge/wrapper dependency; unverified reserves; redemption gated.
- Repeated incidents; paused withdrawals; no post-mortem; history undocumented.
- Token classified as a security in a major jurisdiction; transfer restrictions; venue ineligibility.

## Reporting

- Standard: 3–5 bullets. Deep: full tables and a claim-chain map.
- Always state "not legal advice", the jurisdiction assessed and the questions left open.
- A passing audit is evidence of scope, not proof of safety.
