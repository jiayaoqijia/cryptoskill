# DeFi Security

Security is evidence about the **live deployment**, not a logo on a landing page.

## Audit review

For each audit record:

| Field | What to capture |
|---|---|
| Firm / reviewer | Independent? Reputation? |
| Date | Before or after the deployed commit? |
| Commit / bytecode | Does the scope hash match the live implementation? |
| Scope | Which contracts, modules, chains and dependencies? |
| Exclusions | Oracles, keepers, front end, governance, upgrade admin? |
| Findings | Critical/high/medium count and status |
| Remediation | Fixed, acknowledged, disputed or open |
| Contest audits | Code4rena/Sherlock/Cantina findings and duplicates |
| Formal verification | What property, which tool, which assumptions? |

An audit of a fork or an older version is not coverage of the deployed custom code. A new module, chain deployment or upgrade needs new review.

## Code and provenance

- Verify source on the explorer; compare bytecode and compiler settings.
- Resolve proxy → implementation → all inherited modules.
- Check whether the deployed code matches the audited repository/commit.
- Look for unaudited custom modules, hooks, adapters, keepers and strategy contracts.
- Check dependencies: oracle adapters, bridges, vaults, libraries and upgradeable parents.
- Record closed source, partial source or unverified code as a first-class finding.

## Admin and upgrade control

Map every privileged power:

| Power | Holder | Threshold / delay | Can it move user funds? |
|---|---|---|---|
| Upgrade implementation | | | |
| Pause / freeze | | | |
| Mint / burn | | | |
| Change collateral/LTV/oracle | | | |
| Set fees / fee recipient | | | |
| Move treasury | | | |
| Whitelist / blacklist | | | |
| Emergency withdraw | | | |

Check multisig signers, threshold, independence and timelock. A 2-of-3 multisig with one team and two affiliates is not decentralized. A 48-hour timelock gives users an exit window; a zero-delay proxy does not.

## Oracle and price integrity

Name the class for every collateral:

- hardcoded par (stablecoin = $1);
- redemption rate (LST/RWA NAV);
- market TWAP;
- linear discount;
- single-source spot;
- multi-source median/aggregator.

For each: what it reads, who can update it, staleness/deviation bounds, fallback, and whether the liquidation venue has enough depth at the observed price. A price that is “correct” but not executable is still a liquidation risk.

## Common exploit classes

- Reentrancy and cross-function state manipulation.
- Oracle manipulation via thin pools, flash loans, donation or stale feeds.
- Accounting/share-price errors, donation attacks, fee-on-transfer and rebasing tokens.
- Access-control gaps, unprotected initializers and privileged functions.
- Proxy/storage collisions and unsafe upgrades.
- Signature replay, permit misuse and arbitrary call/execute.
- Liquidation logic: wrong health factor, close factor, bonus or bad-debt path.
- Bridge/message verification, replay, finality and validator collusion.
- Governance: flash-loan voting, low quorum, timelock bypass, treasury drain.
- MEV/sandwich and slippage on exits; keeper liveness failure.

## Bridges and cross-chain

- Verification model: light client, multisig, optimistic, ZK, liquidity network.
- Validator set, threshold, independence and key management.
- Rate limits, mint caps, circuit breaker and pause authority.
- Canonical versus bridged asset; redemption path and latency.
- Historical incidents and message replay/finality assumptions.
- What happens to the position if the bridge pauses during stress.

## Chain and infrastructure

- L1 finality/reorg risk; L2 sequencer downtime, forced inclusion and escape hatch.
- Chain halt, gas spike, censorship, RPC outage and stale state.
- Bridge/message layer: validator set, finality, rate limits and pause.
- Software supply chain: front-end hosting/DNS, package dependencies, CI/CD and signing keys; a compromised front end can drain approvals.
- What the user can do if the sequencer or front end is down: direct contract call, alternate RPC, exit path.
- A safe contract on an unsafe chain is not a safe position.

## Collateral acceptance

- A safe core does not validate a bridged collateral. For every bridged/LST/RWA asset, record the bridge verification model, issuer, canonical versus bridged status, and unbacked-mint risk.
- A **1-of-1 DVN**, single validator or unbacked bridged asset is a fail for collateral; an audit of the lending contract does not cover it.
- Caps and LTV limits reduce size, not the probability of a bridge invariant failure. After an incident, distinguish code exploit, collateral/bridge failure, oracle failure and governance failure.
- A clean core does not prove suppliers were made whole; check the recovery, provision and actual repayment separately.

## Incidents and response

- Search the protocol's postmortems, Rekt, DefiLlama hacks, SlowMist and the audit firms' advisories.
- Record date, loss, root cause, fix, user reimbursement and whether the same pattern exists now.
- Distinguish a code exploit from a governance, oracle, bridge, operational or counterparty failure.
- Check whether the incident response plan has named owners, a communication channel and a pause path.
- An incident does not permanently disqualify a protocol; an unremediated cause does.

## Bug bounty and monitoring

- Immunefi/Code4rena/Sherlock/Cantina program, maximum payout, scope and response time.
- A bounty is not a substitute for an audit; it is a live incentive.
- Monitor upgrades, admin transactions, oracle deviations, liquidity withdrawals and governance proposals.
- Re-review after any material upgrade; security is a moving target.
