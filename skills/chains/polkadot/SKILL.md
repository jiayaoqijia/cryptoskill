---
name: Polkadot
description: Assist with Polkadot DOT transactions, staking, parachains, and cross-chain transfers.
metadata: {"clawdbot":{"emoji":"⚪","os":["linux","darwin","win32"]}}
---

## Network Architecture
- Relay Chain is the main chain — coordinates security and consensus
- Parachains are independent chains — connected to Relay Chain for security
- DOT is the native token — used for staking, governance, and parachain bonds
- Kusama is the canary network — experimental, real value, faster upgrades

## Address Format
- Addresses are different per network — same seed gives different addresses on Polkadot vs Kusama
- Polkadot addresses start with "1" — Kusama starts with capital letters
- SS58 format — different from Ethereum's hex addresses
- One seed for all Substrate chains — but displayed address differs per chain

## DOT Token
- Redenominated 100x in 2020 — old 1 DOT = new 100 DOT
- 10 decimals (planck is smallest unit) — different from 18 decimals on Ethereum
- Existential deposit: 1 DOT minimum — accounts below this are reaped (deleted)
- Locked DOT still counts for governance — can vote while staking

## Staking (Nomination)
- Nominate up to 16 validators — your stake backs their validation
- Minimum to earn rewards varies — currently around 250 DOT due to competition
- 28-day unbonding period — funds locked during unstaking
- Slashing risk exists — bad validators can lose portion of stake
- Rewards claimed manually or auto-compound — depends on wallet

## Staking Pools
- Minimum 1 DOT to join pool — lower barrier than direct nomination
- Pool operator manages validator selection — less control, more convenience
- Rewards distributed by pool — minus pool commission
- Same unbonding period applies — 28 days to unstake

## Governance
- OpenGov system — proposals, referenda, voting
- Conviction voting — lock tokens longer for more voting power
- Anyone can submit proposals — DOT holders vote
- Treasury funds ecosystem development — community-controlled spending

## Parachains
- Parachain slots won via auctions — projects bid DOT
- Crowdloans let users contribute DOT — locked for lease period (2 years)
- Contributed DOT returned after lease — plus project tokens as reward
- System parachains have permanent slots — Statemint, Bridge Hub

## Cross-Chain (XCM)
- XCM is cross-consensus messaging — transfer assets between parachains
- Teleport vs Reserve transfer — different trust models
- Not all parachains support all assets — check compatibility
- Fees paid in DOT or parachain token — depends on route

## Wallets
- Polkadot.js is power-user wallet — full features, complex UI
- Nova Wallet, Talisman — better UX for most users
- Ledger support — via compatible wallets
- SubWallet for mobile — good mobile experience

## Common Issues
- "Existential deposit" error — balance would go below 1 DOT, add more or send all
- Staking not earning — below minimum active stake threshold
- Can't transfer while staking — must leave some unlocked for fees
- Wrong network address — Kusama address won't work on Polkadot
- Unbonding takes 28 days — patience required

## Transaction Characteristics  
- Transactions finalize in ~12 seconds — deterministic finality
- Fees in DOT — relatively low, paid from transferable balance
- Nonce-based like Ethereum — transactions processed in order
- Tips for priority — optional, not usually needed

## Security
- Seed phrase controls all Substrate chains — secure it carefully
- Verify addresses match network — different display per chain
- Check validator reputation before nominating — slashing affects you
- Governance attacks possible — vote on important proposals
