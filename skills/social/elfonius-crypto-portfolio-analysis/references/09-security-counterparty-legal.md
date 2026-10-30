# 09 — Security, Counterparty and Legal

## Purpose

Identify loss channels that price charts do not show: keys, custody, bridges, admins, oracles, issuers, venues, and jurisdiction.

## Inputs

- Custody model, signer policy, approval hygiene.
- Protocol, bridge, oracle, admin, and audit details.
- Counterparty and issuer information.
- Jurisdiction, account type, and tax status.
- Incident history and insurance/backstop terms.

## Method

1. Map each position to its custody and contract dependency.
2. Check approvals, signer policy, and key recovery.
3. Review audit, admin, timelock, oracle, and bridge status.
4. Review incidents, bad debt, and unresolved claims.
5. Map issuer, venue, curator, and custodian counterparties.
6. Flag legal, regulatory, and tax issues for professional review.
7. Record `not assessable` where evidence is missing.

## Custody and keys

- Hardware wallet, multisig, or exchange custody? Who holds the keys?
- Is there a single signer? A recovery plan? A documented inheritance path?
- Are approvals unlimited or scoped? Has the wallet interacted with a verified front end?
- Is the seed phrase ever stored digitally or shared? If yes, stop; do not ask for it.
- Is the signing device separate from the browsing device?

The skill must never request a seed phrase, private key, password, or 2FA code.

## Protocol and bridge

- Audit coverage and date; unaudited code is a red flag.
- Admin keys, proxy upgradeability, timelock, multisig threshold.
- Oracle class, fallback, deviation threshold, manipulation history.
- Bridge model: lock-and-mint, liquidity network, light client; pause and exploit history.
- Incident history: exploits, pauses, bad debt, governance attacks.
- Insurance/backstop: scope, limit, exclusions, claims process.

## Counterparties

- Stablecoin issuer: reserve quality, attestations, redemption terms, peg history.
- Exchange/CeFi: proof of reserves, withdrawal history, jurisdiction, segregation.
- Curator/vault manager: track record, fees, liquidity gates.
- Custodian: legal segregation, bankruptcy remoteness, insurance.
- Validator/operator: slashing, downtime, commission, concentration.

## Legal and tax flags

- Jurisdiction and eligibility; sanctions exposure.
- Securities/commodity classification risk.
- Transfer restrictions, lock-ups, vesting.
- Tax treatment of staking, rewards, buybacks, burns, and DeFi yield.
- Reporting obligations and cost-basis records.

The skill flags issues and questions; it does not provide legal or tax advice.

## Incident evidence

Use incident history as a probability modifier, not a guarantee. A protocol with no incident is not “safe”; it may be young or untested. A protocol with an incident may have fixed the cause; verify the fix.

## Output checklist

- [ ] Custody model and key concentration.
- [ ] Approval hygiene and front-end verification.
- [ ] Audit/admin/timelock/oracle/bridge status.
- [ ] Incident history and unresolved bad debt.
- [ ] Stablecoin/venue/curator counterparties.
- [ ] Insurance and recovery assumptions.
- [ ] Jurisdiction, eligibility, tax flags.
- [ ] No signing or transaction step.

## Failure modes

- Treating “audited” as “safe.”
- Ignoring admin keys and upgradeability.
- Assuming a bridge is trustless because it says so.
- Treating insurance as a guarantee.
- Confusing a protocol incident with a portfolio loss that was actually reimbursed.

## Sources

- Chainalysis, *2025 Crypto Theft Reaches $3.4 Billion* (2025-12-18): private-key, centralized-service, and personal-wallet compromise.
- FSB, *The Financial Stability Risks of Decentralised Finance* (2023): operational fragility and interconnectedness.
