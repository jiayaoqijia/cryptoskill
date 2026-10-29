# DeFi Governance and Legal

## Governance map

- Token distribution: insiders, VCs, treasury, community, unlocks.
- Delegates and voter concentration; top holders and their relationships.
- Quorum, proposal threshold, voting period and execution delay.
- Timelock, guardian/council, emergency powers and veto.
- Treasury control: multisig signers, threshold, spending limits and disclosure.
- Proposal history: upgrades, parameter changes, fee switches, grants, incidents.
- Governance attacks: flash-loan voting, vote buying, low quorum, hostile takeover, timelock bypass.

A governance token with concentrated ownership is a control asset, not a broad community.

## Control questions

| Question | Why it matters |
|---|---|
| Who can upgrade the contracts? | Code risk can change after audit |
| Who can pause/freeze? | Exit may be blocked |
| Who can mint/burn? | Supply and value capture |
| Who sets collateral/LTV/oracle? | Risk parameters can be changed |
| Who controls the treasury? | Buybacks and runway |
| What is the timelock? | Users' exit window |
| Are signers independent? | Multisig is not decentralization by itself |
| What is the emergency path? | Crisis powers can become permanent |

## Legal and regulatory

- Issuer/entity, jurisdiction, legal wrapper and governing law.
- Token classification: security, commodity, e-money, utility, fund unit or unclear.
- MiCA (EU), local securities law, derivatives rules and licensing.
- KYC/AML, sanctions screening, restricted jurisdictions and eligible investors.
- Custody: self-custody, MPC, qualified custodian, exchange; segregation and insurance.
- Transfer restrictions, lockups, redemption gates and tax treatment.
- Consumer/risk disclosures and terms of service; who is the counterparty?

State clearly: “This is not legal or tax advice; confirm with counsel in the relevant jurisdiction.” Do not improvise a legal conclusion from a docs page.

## Tax and accounting

- Treatment differs by jurisdiction and entity: income versus capital gain, staking/LP/airdrop/points, withholding and reporting.
- Record dates, amounts, cost basis and wallet/entity for every acquisition, reward, fee, burn and disposal.
- LP positions create share/asset accounting and impermanent-loss questions; rewards and fees may be income.
- Airdrops/points can be income, capital, or zero-basis until conversion; do not assume.
- Accounting standards (GAAP/IFRS) may not yet address DeFi; record fair value, NAV, audit trail and auditor sign-off.
- Tax is not an afterthought to yield: a 6% yield can be negative after tax, fees and gas.
- This is factual context, not tax advice; confirm with a qualified adviser in the relevant jurisdiction.

## Insurance and risk transfer

- Is there coverage (Nexus Mutual, InsurAce, Protocol insurance, custodian policy)? What is the limit, scope and exclusion?
- Does it cover smart-contract exploits, oracle failure, depeg, bridge failure, governance attack or only custody?
- Claims process, waiting period, deductible, payout asset and counterparty risk of the insurer.
- Coverage is not a guarantee; a policy can be insufficient, disputed or correlated with the same event.
- Price the residual risk after coverage, not the headline APY.

## Evidence quality

- Holder tables are addresses, not beneficial owners. The largest address may be a staking contract, a treasury, a bridge or a CEX; label it before inferring control.
- Forum posts, screenshots and delegate claims are **claims**, not findings. Tie voting-power allegations to on-chain delegates/ownership or mark them unverified.
- An announced buyback, burn or tokenomics upgrade is a catalyst, not an approved program; require proposal, vote, funding, execution and destination.
- A timelock reduces speed, not agenda control; a concentrated delegate can still direct the outcome.

## Governance red flags

- A single EOA or a small insider multisig controls upgrades or treasury.
- No timelock, or a timelock shorter than the exit queue.
- Quorum so low that a small holder can pass a proposal.
- Vote buying/bribes dominate; delegation is concentrated.
- Emergency powers can pause withdrawals indefinitely.
- Treasury spending is undisclosed or unrelated to the mandate.
- A buyback/burn is approved but paused, unfunded, or sends tokens to a reserve rather than burning them.
- Governance token holders have no claim on fees or treasury.
- A proposal changes the fee split, collateral rules or oracle after deposit.

## Disclosure standard

- Terms, docs, audits, governance forum and treasury reports should be dated and versioned.
- A “decentralized” claim is not evidence; show the signer set and the upgrade path.
- An offshore entity does not remove regulatory exposure; it changes who you can sue.
- A DAO vote does not make an illegal offer legal.
