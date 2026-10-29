# DeFi On-Chain Metrics and Sources

## Source hierarchy

1. **Primary chain state:** contract storage, events, bytecode, proxy slots, governance contracts, timelocks.
2. **Primary documents:** audit reports, DAO proposals, treasury reports, legal terms, official docs.
3. **Protocol APIs/dashboards:** useful but self-reported; reconcile with chain.
4. **Independent aggregators:** DefiLlama, Token Terminal, Dune, Nansen/Arkham, block explorers.
5. **Media/social:** discovery and sentiment only.

Two aggregators sharing one upstream dataset count as one source.

## Metric definitions

| Metric | What it measures | Trap |
|---|---|---|
| TVL | User assets deposited in contracts | Includes own token/borrowed/double-counted TVL if not cleaned |
| TVS (oracle) | TVL dependent on an oracle | A failure estimate, not a safety score |
| Fees | Total user payments | Not protocol revenue |
| Revenue | Fees minus supply-side revenue | Not tokenholder revenue |
| Tokenholder revenue | Buyback/burn/distribution funded by receipts | Treasury-funded buyback is not revenue |
| Earnings | Revenue minus token incentives | Not free cash flow |
| Volume | Traded/borrowed throughput | Wash trading and incentives |
| Active users | Unique addresses interacting | Sybils, aggregators, bots |
| Retention | Cohorts returning | Incentive-driven churn |
| Utilization | Borrowed / supplied | 100% can block withdrawals |
| Market cap | Circulating supply × price | Float definitions differ |
| FDV | Max supply × price | Not current value |
| P/F, P/S, P/E | Valuation multiples | Definitions and fee splits differ |
| Depth | Cost to move price 1–2% | Changes with volatility and size |
| Funding/basis | Perp carry | Venue and liquidation risk |

## On-chain read discipline

- Record chain ID, contract address, proxy/implementation, function/selector, block and UTC.
- Resolve the proxy: EIP-1967 implementation/admin/beacon slots; do not read the proxy's own storage as logic.
- Verify source and compiler settings; compare to the audited commit.
- Read `totalAssets()`, `totalSupply()` and the settlement asset balance at the vault address separately; book value can exceed liquid assets.
- For a token, read `totalSupply()` and `decimals()` from the token contract; treat CoinGecko/CMC supply as a cross-check, not the primary source.
- For lending: total supply, total borrows, reserves, utilization, oracle price, LT/LLTV per collateral.
- For DEX: pool reserves, fee tier, tick/liquidity range, volume and LP concentration.
- For governance: proposal count, quorum, timelock, signer set, execution history.
- Prefer a private RPC/archive node for historical state; public RPCs may prune or rate-limit.

## Event and flow metrics

- Deposits/withdrawals by cohort and size; net flow.
- Borrow/repay/liquidation events; bad-debt transfers.
- Protocol buys, treasury sales, buybacks, burns and fee distributions.
- Holder concentration: top 1/10/100, labeled wallets, locked/unlocked.
- Staking/unstaking, validator/operator concentration, slashing.
- Bridge inflows/outflows, mint/burn and rate-limit usage.
- Governance proposals, votes, delegation and execution.

## Source map

| Source | Use | Caveat |
|---|---|---|
| Block explorer | Contract, tx, events, proxy | Labels are claims; source may be unverified |
| DefiLlama | TVL, fees, revenue, yields, chains | Definitions must be read; double counting |
| Token Terminal | Fees, revenue, earnings, P/F, P/S | Standardized; may differ from protocol |
| Dune/Nansen/Arkham | Custom queries, wallet labels | Query logic and labels need review |
| Snapshot/Tally/Boardroom | Governance proposals/votes | Off-chain vs on-chain execution |
| Immunefi/Code4rena/Sherlock/Cantina | Bounties/contests | Scope and status differ |
| Rekt/DefiLlama hacks/SlowMist | Incident history | Verify against primary postmortem |
| CoinGecko/CMC | Price, supply, volume | Aggregator definitions; cross-check |
| Exchange APIs | Depth, funding, OI | Venue-specific; API limits |

## Reconciliation

- Compare TVL, fees and revenue across at least two sources; show the difference and choose a basis.
- Align timestamps: daily close vs block-level; UTC vs local.
- Align units: token vs USD; native vs wrapped; share vs asset.
- Check supply: circulating vs total vs max; treasury-held and locked.
- If sources conflict, do not average silently. State both and explain why one is primary.

## Evidence tiers

| Tier | Evidence | Use |
|---|---|---|
| A | Direct chain read / verified source / audit PDF | Supports a finding |
| B | Protocol API / DAO report | Cross-check, label self-reported |
| C | Aggregator | Context; reconcile |
| D | Media/social | Discovery only |

Record the tier and the gap. A missing field is `not assessable`, not zero.
