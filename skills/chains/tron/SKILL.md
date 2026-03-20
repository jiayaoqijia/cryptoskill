---
name: TRON
description: Assist with TRON TRX transactions, bandwidth, energy, and TRC-20 token transfers.
metadata: {"clawdbot":{"emoji":"⚡","os":["linux","darwin","win32"]}}
---

## Resource Model (Critical)
- TRON uses bandwidth and energy instead of gas — different from Ethereum
- Bandwidth for simple transfers — TRX transfers and basic operations
- Energy for smart contracts — TRC-20 tokens and dApps require energy
- Both resources regenerate over time — or can be obtained by freezing TRX
- Transactions fail without sufficient resources — no partial execution

## Bandwidth
- Free bandwidth allocation daily — ~1,500 bandwidth points per account
- TRX transfers cost ~280 bandwidth — enough for ~5 free transfers per day
- Bandwidth regenerates over 24 hours — used bandwidth recovers gradually
- If bandwidth depleted, TRX is burned for transaction — more expensive than using free bandwidth
- Check bandwidth before batch transfers — running out mid-batch wastes TRX

## Energy
- Required for TRC-20 transfers (USDT, etc.) — simple TRX doesn't need energy
- USDT transfer costs ~65,000 energy — significant amount
- No free energy allocation — must freeze TRX or pay
- Energy regenerates slowly after use — 24 hours for full recovery
- Without energy, TRX burned at high rate — can cost several TRX per transfer

## Freezing TRX
- Freeze TRX 2.0: stake TRX to get bandwidth or energy — choose one per stake
- Minimum freeze is 1 TRX — but need substantial amount for meaningful resources
- Unfreezing takes 14 days — funds locked during unstaking period
- Frozen TRX still counts as balance — but not spendable until unfrozen
- Can delegate resources to other accounts — useful for managing multiple wallets

## TRC-20 Tokens (USDT)
- TRON is major network for USDT transfers — lower fees than Ethereum
- TRC-20 USDT is different from ERC-20 USDT — not interchangeable without bridge
- Transfers require energy — freeze TRX or pay from balance
- Contract interaction may need approval — similar to ERC-20 approve
- Verify contract address — TRC-20 addresses start with T

## Address Format
- TRON addresses start with "T" — base58 encoding
- 34 characters total — always verify full address
- Addresses are case-sensitive — unlike Ethereum checksums
- One address for TRX and all TRC tokens — unlike Solana's multiple accounts

## Wallet Options
- TronLink is most popular — browser extension and mobile
- Ledger support via TronLink — hardware wallet integration
- Trust Wallet supports TRON — multi-chain option
- Klever wallet — TRON-focused option
- Never share private key — standard security applies

## Transaction Characteristics
- Block time ~3 seconds — fast finality
- Transactions are free if bandwidth available — major advantage
- Failed transactions don't consume resources — unlike Ethereum gas
- Transaction ID (hash) for tracking — use tronscan.org

## Staking and Voting
- Super Representatives (SR) produce blocks — 27 elected SRs
- Vote with frozen TRX — 1 TRX = 1 vote (Stake 2.0)
- Voting rewards vary by SR — some distribute rewards to voters
- Governance participation — SRs decide on network upgrades

## Common Issues
- "Out of energy" — freeze more TRX or wait for regeneration
- "Bandwidth exceeded" — daily limit reached, wait or use TRX
- USDT transfer expensive — didn't have energy, paid in TRX
- "Invalid address" — check address format starts with T
- Slow transaction — network congestion, usually resolves

## Exchanges and Transfers
- Most exchanges support TRC-20 USDT — often preferred for lower fees
- Verify network selection — sending TRC-20 to ERC-20 address = lost funds
- Memo/tag rarely required on TRON — unlike XRP, but verify
- Some exchanges require minimum balance — activation fee for new accounts

## Security
- Private keys control everything — never share
- TronLink permissions persist — revoke dApp connections regularly
- Phishing sites common — always verify tronscan.org domain
- No smart contract risk for simple transfers — but dApps can have vulnerabilities
