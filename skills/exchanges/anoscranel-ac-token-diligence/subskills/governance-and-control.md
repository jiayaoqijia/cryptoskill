---
name: governance-and-control
domain: crypto-trading/governance-and-control
trigger: "Establishing who can change a token's rules, supply, or contracts."
anti_trigger: "Not for predicting governance votes or evaluating token price."
scope: "Admin keys, multisigs, upgradeability, and who can change supply or rules unilaterally."
status: seedling
---

# Governance and control

## Standard

Decentralisation is a spectrum of permissions, and the diligence question is not whether a protocol is decentralised but what any single party can do without asking. An admin key that can mint, pause transfers, or upgrade a contract to arbitrary code is a control fact that outweighs every economic metric in the record.

Governance tokens add a second layer: voting power that can change supply schedules, fee switches, or treasury spending. The relevant question is concentration of that power and whether any threshold is reachable by insiders alone. A governance process that cannot be captured is a real asset; one that can be captured is a risk the token's price rarely reflects until it happens.

Primary sources: <https://ethereum.org/en/developers/docs/standards/tokens/> and <https://www.sec.gov/investor>.

## Decision rules

- Record every privileged role: owner, admin, minter, pauser, upgrader, fee setter. For each, record who holds it and whether it is a multisig, a timelock, or a single key.
- A single key with mint or upgrade rights is a material finding and belongs at the top of the record.
- Multisig thresholds matter: three of five with independent signers is different from two of three where two are colleagues.
- Check for timelocks on upgrades; an upgrade without a delay is an immediate control risk.
- For governance tokens, record voting-power concentration and the quorum required to pass a change.
- Record what has already been changed by these powers; precedent is evidence.

## Procedure

1. Read the contract's privileged functions and their access controls, from verified source or documentation.
2. Map each role to its holder (address) and to the control structure (single key, multisig with threshold, timelock).
3. Check the upgrade mechanism and any timelock duration.
4. For governance tokens, pull voting-power distribution and quorum.
5. List historical changes made through these powers, with dates.
6. Write the control summary as a table: role, holder, structure, risk.

## Anti-patterns

- Reading "owned by the community" as an absence of admin keys.
- Treating a multisig as decentralised without checking who signs.
- Ignoring upgrade rights because the contract is "audited".
- Assuming governance tokens confer control without checking quorum and concentration.
- Skipping the historical record of what the powers have already done.

## Done checklist

- [ ] Every privileged role listed with its holder and structure.
- [ ] Single-key risks identified and ranked.
- [ ] Multisig thresholds and signer independence assessed.
- [ ] Timelocks checked and durations recorded.
- [ ] Governance concentration and quorum recorded where applicable.
- [ ] Historical changes through these powers listed with dates.

## Sources

- Ethereum token standards and contract patterns: <https://ethereum.org/en/developers/docs/standards/tokens/>
- Securities disclosure context for control and governance: <https://www.sec.gov/investor>
- Investor education on ownership structures: <https://www.investor.gov/introduction-investing>
