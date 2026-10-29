# DeFi Diligence

Core checklist for any DeFi protocol, vault, pool or structured position. Load this first; load the category-specific reference when the protocol type is known.

## 1. Exact target

- Protocol name, product, version and chain(s).
- Full contract address, proxy and implementation; explorer links.
- Market/vault/pool ID, asset(s), curator/operator and front end.
- Legal entity, jurisdiction and official docs; check name collisions, forks and bridged versions.
- Block height and UTC timestamp for every on-chain read.

A brand is not a deployment. Two products with the same name can have different contracts, collateral and risk.

## 2. Investability gate

| Component | Pass looks like | Fail / insufficient evidence |
|---|---|---|
| Exact deployment | Verified contract, proxy and product match the docs | Unverified code, unknown proxy, wrong chain or lookalike |
| Control | Named multisig + timelock for upgrades, pause, mint and treasury | Single EOA, no timelock, hidden owner, arbitrary pause |
| Security coverage | Audit covers the live commit; critical/high findings resolved | Audit predates deployment, custom code unaudited, critical findings open |
| Asset and liability | Claim, collateral, lockup, queue and exit understood | Hidden transfer restriction, unclear claim, unreconciled TVL |
| Price integrity | Oracle class, fallback, staleness and manipulation resistance known | Single spot feed, no staleness check, liquidation tape invisible |
| Legal eligibility | Intended investor can hold it; custody and sanctions addressed | Blocked jurisdiction, unregistered security risk, no entity |

Statuses: `pass`, `conditional`, `fail`, `insufficient evidence`. An unknown critical component is `insufficient evidence`, not `conditional`.

## 3. Five-layer stack

1. **Venue protocol:** the contracts that hold funds or execute the market.
2. **Vault/strategy/curator:** who allocates, rebalances and sets risk parameters.
3. **Underlying assets and counterparties:** collateral, stablecoin, RWA issuer, custodian, borrower.
4. **Infrastructure:** oracles, bridges, keepers, RPCs, sequencers, governance.
5. **Distribution:** front end, wallet, aggregator, API and the domain users actually sign on.

A “USDC vault” can be a leveraged BTC credit book. Look through every wrapper to the final cash flow or named counterparty.

## 4. Category checks

### DEX / AMM / CLMM

- Volume/TVL, fee tier, turnover, active pools and concentration.
- LP economics after fees, emissions, impermanent loss/LVR, MEV and gas.
- Depth at the user's size; slippage; routing; aggregator share.
- Pool asset quality, oracle use, hooks/extensions, admin and fee switch.
- Wash trading, incentivized volume and mercenary liquidity.

### Lending / money market

- Collateral list, LTV/LLTV, liquidation threshold/bonus, close factor.
- Oracle per collateral, staleness, fallback and liquidation venue depth.
- Utilization, borrow/supply APR, reserve factor, caps and isolation/eMode.
- Keeper incentives, bad-debt history, reserve/insurance fund and loss socialization.
- Recursive collateral, rehypothecation and correlated depeg.

### CDP / stablecoin

- Collateral, mint/redeem rights, peg mechanism, collateral ratio and stability fee.
- Oracle and liquidation design; surplus/deficit and bad-debt auction.
- Reserve attestation, custodial backing, redemption gates and sanctions.
- Peg history and behavior in stress.

### Perps / derivatives

- Margin, funding, open interest, insurance fund, ADL and liquidation waterfall.
- Oracle/index composition, mark versus index, and stale-price behavior.
- Counterparty/venue risk, keeper liveness and settlement asset.
- Volume quality; wash trading; OI concentration.

### Yield vault / aggregator / curator

- Strategy allocation, leverage, recursive exposure and liquidity mismatch.
- Curator mandate, track record, fees, skin in the game and risk limits.
- Underlying protocols, assets and oracles; first-loss and backstop.
- Queue/epoch, caps, redemption terms and who can change them.

### LST / LRT / restaking

- Validator/operator set, slashing conditions, withdrawal queue and liquidity.
- Restaking layer, AVS exposure, reward source and penalty pass-through.
- Peg/depeg history; secondary-market depth.
- Governance and upgrade control across each layer.

### Bridge / cross-chain

- Verification model, validator set and threshold; 1-of-1 is a fail.
- Rate limits, mint caps, pause/kill switch and upgrade authority.
- Asset canonicality, wrapped/bridged representation and redemption path.
- Historical incidents and message replay/finality assumptions.

### RWA / tokenized fund

- Legal claim, issuer, custodian, fund administrator, auditor and NAV reporter.
- Mint/redemption windows, transfer restrictions, eligibility and secondary market.
- NAV oracle/attestation cadence and stale-price controls.
- Credit, duration, liquidity and counterparty risk of the underlying.

### Options / structured products

- Payoff, Greeks, collateral and counterparty; path dependency.
- Oracle/settlement source and early-exercise/knock-in terms.
- Liquidity of the hedge and the unwind path.
- Fee stack and who is short the tail.

### Insurance / coverage

- Trigger and covered perils; exclusions and waiting period.
- Claims process, capital/reinsurance, payout asset and counterparty risk.
- Coverage limit versus the position and correlation with the same event.
- A policy is not a guarantee; price the residual risk.

## 5. Diligence request list

Ask for these before relying on the protocol's own narrative. Missing items are findings, not blanks to fill with optimism.

- Docs/whitepaper, architecture and contract-address list; deployment and upgrade history.
- Audit reports (full text), scope/commit, findings and remediation; bug bounty terms.
- Financials: fees, revenue, tokenholder revenue, earnings, treasury and runway; definitions and dates.
- Cap table, token allocation, vesting/unlock schedule and insider/VC holdings.
- Governance: proposals, votes, delegates, quorum, timelock and emergency powers.
- Incident/postmortem history and current monitoring/alerting.
- Oracle configuration, feed addresses, heartbeat/deviation and fallback.
- Reserve/custody attestations for stablecoins, RWA or off-chain collateral.
- Legal entity, terms, risk disclosures, jurisdiction and eligibility.
- Insurance/coverage policy and claims terms.
- Data room index and who is accountable for each answer.

## 6. Evidence table

| Claim | Type | Value | As-of | Source | Independence | Status |
|---|---|---:|---|---|---|---|
| TVL | Aggregator | | | DefiLlama | Cross-check | |
| Fees/revenue | Protocol/aggregator | | | Token Terminal / DAO | Cross-check | |
| Audit scope | Primary | | | Audit PDF | Auditor | |
| Admin powers | Chain/code | | | Explorer + source | Primary | |

## 7. Red flags

- TVL includes the protocol's own token, borrowed coins, recursive deposits or double counting.
- APY is mostly emissions, points or a related-party subsidy; emissions exceed revenue.
- Token is accepted as collateral for itself, or a wrapper is priced off its own pool.
- Single-source spot oracle, no staleness check, or liquidation relies on a venue with no depth.
- Upgradeable proxy with a single EOA, no timelock, or an undisclosed owner.
- Audit covers an old commit or the upstream fork, not the deployed custom code.
- Withdrawal queue, cap or cooldown is hidden until stress.
- Bridge has a 1-of-1 validator, no rate limit or no kill switch.
- Top holders or depositors control the exit; insider/VC unlock is near.
- Governance can be captured with flash loans or a small quorum; treasury is a multisig with unknown signers.
- Incident history is missing, postmortem is thin, or users were not made whole.
- The team is anonymous, custody is off-chain and there is no independent attestation.

## 8. Monitoring

- Contract upgrades, admin actions, pause/unpause and parameter changes.
- TVL by asset/chain/market; depositor concentration; inflow/outflow.
- Utilization, borrow/supply APY, liquidation volume and bad debt.
- Oracle price/deviation/staleness and collateral depeg.
- Fees, revenue, tokenholder revenue and emissions.
- Unlocks, governance proposals, audits, incidents, bridge health.
- Re-review after any material change; a quarterly cadence is a minimum, not a guarantee.
