# Crypto Diligence — Tiered Checklist

Operative checklist for token, protocol, subnet and DeFi-position analysis inside `professional-investor-analysis`. Tier 1 items can hold the investability gate at `fail` or `insufficient evidence`. Tier 2 sets the economics. Tier 3 is monitoring.

Every state claim carries chain, block and retrieval time; where a token contract exists, also the full contract address and function/selector. Issuer documentation and dashboards are claims until reconciled with chain state or primary records. Record a status per item: `doğrulandı — geçerli`, `doğrulandı — başarısız`, `iddia — doğrulanmadı`, `değerlendirilmedi + neden`.

Related references: `crypto-unit-economics.md` (revenue/margin), `crypto-valuation.md` (business vs token value), `crypto-onchain-flows.md` (holders/flows/control), `crypto-technical.md` (market structure), `crypto-market-intelligence.md` (community/news/catalysts), `crypto-legal-security.md` (legal/security), `team-and-org.md` (team/funding), `portfolio-fit.md` (suitability/macro).

## Tier 1 — gate items (non-compensatory)

### 1. Identity and contract map

- Chain(s) and chain ID; full checksummed contract address(es); token standard; proxy and implementation addresses.
- Resolve ticker → contract address before any metric. List bridged, wrapped and synthetic variants and state which one the user would actually hold.
- Is the source verified on an explorer, and does it match the deployed implementation rather than a previous deployment?
- Token migrations, redenominations and splits: what changed, when, and whether the price series is adjusted.
- **Name collisions and impersonators:** one project name can map to unrelated companies or products, and an unrelated token can use the same brand/ticker on another chain. Confirm the entity, domain and chain before analysis; check the token for an impersonator flag (DossierScan or equivalent) and state the chosen entity in a one-line scope note in the report. If several unrelated entities share the name, proceed with the context-supported one and name the alternative; ask only if the choice changes the decision.

### 2. Supply truth

Table with one row each for max, total, circulating, effective float, treasury-held, locked/vesting and unclaimed emissions — value, definition, source, date.

- Reconcile aggregator vs issuer vs on-chain `totalSupply`; explain each difference instead of choosing one silently.
- State which basis backs market cap and which backs FDV. Never compare one asset's float cap with another's FDV.
- Circulating supply that excludes treasury, market-maker loans or pledged tokens is a definition, not a fact — name it.

### 3. Privileged control

| Ability | Function / role | Holder type | Threshold / signers | Timelock | Renounced? | Evidence |
|---|---|---|---|---|---|---|

Cover at least: mint, burn, pause/unpause, upgradeTo, setFee, setOracle, blacklist/freeze, rescue/sweep, treasury spend.

- A single unrenounced EOA holding mint or upgrade power is a gate-level finding, not a paragraph.
- Distinguish "renounced" from "held by a multisig whose signers cannot be identified".

### 4. Claim chain and redemption

- Trace: native → canonical bridge → third-party bridge → custodied wrapper → synthetic. For each hop record issuer, validator/guardian set, upgrade authority, collateral attestation, redemption terms and prior incidents.
- Redeemability test: can the specific token held be redeemed for the underlying, by whom, on what terms and with what delay?
- Withdrawal gating: queue, pause, per-address limits, KYC, jurisdiction blocks, minimum/maximum transaction sizes.

### 5. Legal eligibility and transferability

- Issuer entity and jurisdiction; the issuer's own stated classification and restrictions (not a legal opinion); sanctions exposure; whether the venues used actually serve the user's jurisdiction.

### 6. Verifiability of critical claims

- Which load-bearing numbers can be read from chain or primary documents, and which exist only in issuer material or dashboards?
- If supply, reserves or redemption cannot be verified, the gate is not `pass`.

## Bittensor subnet alpha — Tier 1 mapping

A Bittensor subnet token is chain-native alpha, not an ERC-20; the general contract checks do not apply. Map the gate as follows:

- **Identity:** `netuid`, subnet name, owner hotkey and coldkey; the instrument is the subnet's alpha in its AMM pool. There is no token contract, proxy or `totalSupply()` to read.
- **Supply truth:** maximum 21M alpha per subnet; record total minted, protocol-burned and company-burned alpha separately, plus pool-held and staked alpha. Dashboards disagree on burned/supply definitions — use chain state at a recorded block and a source/date per row.
- **Privileged control:** owner hotkey and owner cut (default 18%), who can set weights, whether a project-specific master validator or allowlist exists, conviction locks and takeover threshold. "Renounced" is not a meaningful status here; identify who controls the hotkey and what the owner can change.
- **Claim chain:** native alpha, no bridge; redeemability is the AMM pool, and unstaking/cooldown timing is part of the exit path.
- **Legal eligibility:** alpha is not equity or a revenue share; jurisdiction and tax treatment are separate questions.

## Tier 2 — economics, market and quality

### 7. Rights ladder

1. Enforceable cash-flow claim; 2. active fee switch; 3. funded buyback/burn; 4. voting only; 5. points/airdrop expectation; 6. wrapped or bridged claim; 7. no economic claim.

For each claimed right, name the contract, function and current state that implements it — or write "docs claim — not verified in code". A governance-only token has no DCF anchor.

### 8. Demand quality

- Paid versus incentive-farmed usage: fee-paying addresses excluding known incentive recipients where data permits; wash/round-trip indicators; retention of fee payers at 30/90/180 days where available; share of activity funded by emissions or treasury.
- TVL: state whether recursive, looped or double-counted; report gross and incentive-adjusted.
- Protocol fees versus token incentives paid over the same window; incentives spent per dollar of TVL attracted and retained.
- Volume: venue-reported versus aggregator-reported versus order-book derived; check for mirrored or wash books.
- **Related-party demand:** check whether sibling products, the same team's other subnets, or the project's own agents default to this API/endpoint. Internal usage inflates token/request counts; separate it or label the share undisclosed.

### 9. Unlock overhang

Month-by-month table: tokens unlocking, % of current float, % of 30-day volume, cumulative % of float, beneficiary class (team, investor, advisor, treasury, foundation, market-maker loan, pledged).

- Source hierarchy: vesting-contract state first, issuer schedule second, dashboard last. A blog schedule is a claim.
- Include treasury and foundation releases that are discretionary but plausible.

### 10. Value capture

- Separate gross protocol fees, supply-side payments, incentives, net protocol revenue and holder-distributed value.
- For any burn or buyback, state who funds it and from what — fees, treasury or emissions. An on-chain burn proves the burn, not the revenue link; require treasury or inflow evidence before calling it revenue-funded.
- Discretionary value capture (governance vote, treasury-funded burn) is weaker than a contractual or code-enforced claim; label which one applies.

### 10a. Bittensor subnet economics

- Emission split: read `owner_cut`, `server_emission`, `validator_emission` and `root_alpha_divs` from `/subnets/epochs`; the observed split is 18% owner / 41% miners / 41% validators, but owner cut is a hyperparameter — read it, do not hard-code. Owner cut is a claim on emissions, not on revenue; compute its spot value and compare it with any disclosed revenue.
- Daily alpha emission: `alpha_out_emission` is **per block**; daily = that value × 7,200 (12-second blocks). Do not assume 1 α/block — halving makes it subnet-specific. The SN53 case happened to be 1 α/block (7,200 α/day); that is an observation, not a protocol constant.
- Annual emission as % of current supply and of the 21M cap; staking APR = validator/staker alpha per day ÷ staked alpha × 365. Use the validator slice excluding root; state the block time, per-block emission and annualization convention, and say whether the figure is gross or net of root cut.
- Market-cap basis: in the observed Taostats feed, `market_cap` uses pool + staked float, not total supply; compute FDV separately as 21M × price and label both.
- Buyback offset: company burn ÷ same-period emission; a burn of a few percent of emissions does not offset the dilution.
- Conviction/ownership: owner stake lock, takeover threshold and whether any non-owner hotkey holds a meaningful lock.

### 11. Governance

- Top-10/top-100 holder share with labels; team, foundation and treasury share; delegate concentration; quorum as % of supply; average turnout; proposal count and pass rate.
- Timelock, on-chain execution versus signaling snapshot, and emergency powers that bypass governance.
- Governance-attack cost versus treasury controlled, where estimable.

### 12. Security

- Key-control table from Tier 1.3.
- Audit ledger: firm/contest and independence, report date, audited commit and repository, modules in and out of scope, findings by severity, remediation status per critical/high, re-audit after fixes, bounty platform and maximum payout.
- Binding check: does the verified source of the deployed implementation at the recorded address correspond to the audited commit? If not established → `audit kapsamı doğrulanmadı`, not "safe".
- Oracle: provider, heartbeat, deviation threshold, fallback, manipulation surface.
- Custody: self-custody, MPC, qualified custodian or exchange; segregation and insurance only if evidenced.

### 13. Incidents

| Date | Chain / contract | Mechanism | Loss | Recovery | Root cause | Fix verified on-chain? | Recurred? | Post-mortem |
|---|---|---|---|---|---|---|---|---|

Read the post-mortem or governance report, not the announcement post. Repeated incidents or unrecovered losses are strong negative evidence; an undocumented history is a risk factor, not a clean record.

### 14. Team and execution (crypto form)

- Doxxed status and strength of identity evidence; prior projects including failed or abandoned ones; insider allocation versus float.
- Repositories and licence; fork of what; commits in the last 90 days; distinct contributors; top-contributor share (bus factor); last release; open critical issues; documentation last-updated date.
- Shipped versus promised over 12–24 months, delay pattern, incident response and disclosure speed.
- Pseudonymity is a graded risk with named consequences (no legal counterparty, no background check, higher exit-scam probability), not a neutral unknown.

### 15. Treasury and runway

- Composition by asset; stable-denominated runway; monthly operating spend; committed grants; entity P&L versus protocol revenue; reliance on token sales; who can move funds and at what threshold.

### 16. Venue, liquidity and exit

- Venues with rough share and whether each is accessible to the reader; spot versus perpetual open interest; funding and basis with a stated lookback; price-discovery venue; quote asset and stablecoin risk.
- Depth at a stated timestamp for the stated size; days to exit at a participation cap; withdrawal limits, transfer tax, pause/blacklist, maximum transaction size, LP lock status.
- **Pool size is not exit liquidity.** Where available, fetch a sell-off price (all circulating float sold at once) and the ratio of alpha outside the pool to alpha in the pool; otherwise compute the all-float sale against the pool. A pool that looks large versus market cap can realize a small fraction of it — use the shallower depth estimate for planning and state the method.

### 17. Community, news and catalysts

Record dated snapshots; social metrics are signals, not evidence.

- Channels: X followers and engagement rate; Discord/Telegram members and online; GitHub stars, forks, open issues, contributors and commit cadence; governance-forum proposals and turnout; Reddit/public social sentiment; news flow.
- Separate company claims, independent reporting and community sentiment. Check engagement quality (reply/quote ratio, bot-like repetition) rather than follower count alone; follower count is not demand.
- Catalyst table: event | date or `unknown` | what it changes | how to monitor. Include product/model launches, listings, Phase 2/upgrade dates, buyback cadence, token unlocks, competitor pricing and regulatory dates.
- A small but technical community (e.g. a few hundred Discord members, single-digit GitHub stars, four contributors) is a risk signal for a large market cap, not a disqualifier. State the comparison.

### 18. Technical and market structure

Pin the conventions before calculating: daily UTC closes, 30/90/130-day and 1-year windows, simple versus log returns, annualisation stated, price return versus total return. A full report always includes this section; a short note may compress it to one paragraph and label it market context, not a timing call.

- Trend and relative strength versus TAO, BTC or the sector index; MA20/MA50/MA200; RSI(14); volatility (annualised); maximum drawdown with the peak date; volume/ADV; beta and correlation.
- Liquidity: depth at a stated timestamp for the stated size, days to exit at a participation cap, all-in round-trip cost. Use the shallower of the pool-based and sell-off-based estimates.
- Derivatives: if a perpetual exists, record venue, annualised funding with sign history, open interest and its change versus price, basis and visible liquidation levels; label all of it descriptive positioning context, never a valuation input. If no perpetual exists, say so and use the parent-asset beta as an indirect proxy.
- No validated-edge claim without the backtest protocol in the main skill; otherwise report descriptive context only.

### 19. Valuation bridge and unit economics

- If the token has no enforceable cash-flow claim, do not run a DCF. Use a labelled pricing bridge: revenue × margin × multiple → enterprise/token value, with the multiple's source and the float basis stated; call it a market-pricing proxy, not intrinsic value.
- Scenario table: identical driver rows for bear/base/bull/thesis-break; each yields a per-unit value and a total return. Probabilities are judgmental unless a base rate and method are shown.
- Reverse valuation: state what revenue or growth the current price implies at a given multiple; compare with the disclosed or estimated revenue range.
- Unit economics, where measurable: revenue per GPU/day, cost per token, gross margin, miner payback, customer concentration, prepaid balances and churn. If unavailable, show the stress-test range and label every assumption.

### 20. Holder and flow analysis

- Top-10/50/100 holder share with labels (team, foundation, treasury, exchange, bridge, market maker) and the Nakamoto coefficient where available.
- Net flows: staking/unstaking, protocol buybacks, root sells, cross-subnet flows and user net buys/sells; reconcile the contributions against the price change instead of listing them separately.
- Concentration and exit: conviction locks, takeover threshold, alpha outside the pool versus inside it (ADR), all-float sell-off price and realised value versus market cap. A large pool can still realise a small fraction of the mark.

## Tier 3 — monitoring

Unlock dates and sizes; governance proposals with treasury impact; upgrade announcements and timelock expiry; treasury outflows; holder-concentration change; fee/revenue trend versus incentives; incident disclosures; venue delistings; regulatory actions.

## Source map (ranked)

1. Verified contract source and state on a block explorer, read at a recorded block; repeat critical reads on a second independent RPC.
2. Protocol treasury and vesting wallets.
3. Governance forum, executed proposals and timelock transactions.
4. Audit reports with scope, commit and date; bug-bounty scope.
5. Repository releases, commit history and contributor activity.
6. Venue order books and DEX pool state at a timestamp.
7. Aggregators (DefiLlama, Dune, Token Terminal, CoinGecko, CMC) as cross-checks only — they frequently share one upstream dataset.
8. **Bittensor:** Taostats chain endpoints (`subnet/latest`, `dtao/pool/latest`, `dtao/pool/history`, `dtao/subnet_emission`, `dtao/stake_balance`, `subnets/epochs`) as primary; Taosis, SubnetStats, Taoswap and bittensor.ai as cross-checks, expecting supply/burn definition conflicts. Check the current Taostats API documentation for endpoint contracts and rate limits; do not assume a remembered schema.
9. **Social and news:** X, Discord/Telegram invite APIs, GitHub API, governance forum, public social search and dated news. Date every snapshot; label sentiment as signal, never as evidence.

## Reporting

The report carries the status of gate-relevant items only, in one line per item. The workpaper carries the full tables, unresolved unknowns and the evidence behind each status.
