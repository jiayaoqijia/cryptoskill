---
name: Arbitrum
description: Assist with Arbitrum One transactions, bridging, gas optimization, and L2 ecosystem navigation.
metadata: {"clawdbot":{"emoji":"🔵","os":["linux","darwin","win32"]}}
---

## Network Basics
- Arbitrum One is an optimistic rollup — L2 scaling for Ethereum
- EVM equivalent — same tools, wallets, contracts as Ethereum
- ETH is the gas token — not a separate token
- ARB is governance token — not used for gas
- Same addresses as Ethereum — but different network, different balances

## Bridging
- Official bridge: bridge.arbitrum.io — most secure
- Deposits (L1→L2): ~10 minutes — after Ethereum confirmation
- Withdrawals (L2→L1): 7 days — optimistic rollup security delay
- Third-party bridges faster — Hop, Across, Stargate, but add risk
- Always bridge some ETH first — need gas on Arbitrum

## The 7-Day Withdrawal
- Optimistic rollups assume transactions valid — fraud proofs during 7 days
- Cannot speed up native bridge withdrawal — security requirement
- Plan ahead for exits — don't bridge if you need funds in <7 days
- Third-party bridges use liquidity — faster but fees apply
- Withdrawal can be claimed after 7 days — requires L1 transaction

## Gas and Fees
- Much cheaper than Ethereum mainnet — typically 10-50x lower
- Two components: L2 execution + L1 data posting
- L1 data costs can spike — when Ethereum is congested
- Gas prices in gwei — same units as Ethereum
- Fast blocks — ~0.25 seconds

## ARB Token
- Governance token — vote on DAO proposals
- Not used for gas — ETH pays for transactions
- Airdropped to early users — claiming period ended
- Staking coming — ARB staking in development
- Available on major exchanges — high liquidity

## DeFi Ecosystem
- GMX — largest perps DEX on Arbitrum
- Uniswap, SushiSwap — major DEXs deployed
- Aave, Radiant — lending protocols
- Camelot — native Arbitrum DEX
- Significant TVL — billions in value locked

## Wallet Configuration
- MetaMask works natively — add network from chainlist.org
- Chain ID: 42161 — RPC: https://arb1.arbitrum.io/rpc
- Block explorer: arbiscan.io — verify transactions
- Same seed as Ethereum — different network selection

## Arbitrum Nova
- Separate chain from Arbitrum One — optimized for gaming/social
- Lower fees than One — less security guarantees
- Different bridge — don't confuse with One
- Chain ID: 42170 — verify you're on correct chain

## Stylus
- Run Rust, C, C++ contracts — not just Solidity
- WASM-based execution — alongside EVM
- Coming feature — expands developer options
- Same security as EVM contracts — audited runtime

## Common Issues
- "Insufficient ETH for gas" — need ETH, not just tokens
- Wrong network — sent to Arbitrum address on Ethereum (recoverable but complex)
- Withdrawal pending — 7-day wait is normal, not stuck
- Transaction reverted — check slippage, approvals, balance
- "Network not found" — add Arbitrum network to wallet

## Sequencer
- Single sequencer currently — Offchain Labs operated
- Centralization concern — decentralization roadmap exists
- Sequencer can't steal funds — only order transactions
- If sequencer down — delayed but not lost, can force include
- Decentralized sequencer coming — DAO governance

## Security
- Same security as Ethereum for assets — after 7-day challenge period
- Smart contracts same risks — audit status matters
- Fraud proof protects users — invalid state transitions challenged
- Bridge is secured by Ethereum — L1 is the settlement layer
- Use official bridge for large amounts — third-party bridges add risk
