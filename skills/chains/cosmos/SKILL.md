---
name: Cosmos
description: Assist with Cosmos ATOM transactions, IBC transfers, staking, and cross-chain ecosystem navigation.
metadata: {"clawdbot":{"emoji":"⚛️","os":["linux","darwin","win32"]}}
---

## Ecosystem Overview
- Cosmos is a network of blockchains — not a single chain
- Cosmos Hub is the main chain — where ATOM lives
- IBC connects all Cosmos chains — Inter-Blockchain Communication
- Each chain is sovereign — own validators, own token, own governance
- Same wallet works across chains — different addresses per chain

## ATOM Token
- Native token of Cosmos Hub — staking and governance
- Used to secure the Hub — not other Cosmos chains
- Inflationary — staking rewards come from inflation
- Not used for gas on other chains — each chain has own token

## IBC Transfers (Critical)
- Send tokens between Cosmos chains — native cross-chain
- Recipient address differs per chain — same seed, different address
- Channel/path matters — tokens take specific routes
- Tokens may be wrapped — ATOM on Osmosis is IBC ATOM
- Verify channel is active — some channels deprecated

## Address Format
- Bech32 format — human-readable prefix + data
- cosmos1... for Cosmos Hub — other chains have different prefixes
- osmo1... for Osmosis, juno1... for Juno — each chain unique
- Same mnemonic gives different addresses — per chain derivation
- Verify prefix matches destination chain — wrong prefix = wrong chain

## Staking
- Delegate to validators — earn staking rewards
- 21-day unbonding period — funds locked during unstake
- Slashing risk — validators can lose stake for misbehavior
- Redelegation instant — switch validators without unbonding
- Liquid staking available — stATOM, qATOM maintain liquidity

## Validators
- Choose carefully — commission and uptime vary
- Voting power concentration — avoid top validators for decentralization
- Validator can vote on your behalf — unless you vote yourself
- Check slashing history — past behavior indicates reliability
- Community validators vs exchanges — support decentralization

## Governance
- On-chain proposals — deposit, voting period, execution
- Vote with staked ATOM — voting power = stake
- Options: Yes, No, NoWithVeto, Abstain — veto can kill proposal
- Validator votes if you don't — delegate your vote
- Active participation encouraged — proposals affect chain direction

## Wallets
- Keplr — most popular, browser extension + mobile
- Leap — alternative to Keplr, similar features
- Cosmostation — mobile and web
- Ledger support — via Keplr or native app
- One seed for all Cosmos chains — Keplr manages addresses

## Gas and Fees
- Fees paid in native token — ATOM on Hub, OSMO on Osmosis
- Relatively low fees — fractions of a cent typically
- Gas estimation usually automatic — wallets handle it
- Can fail if gas too low — retry with higher gas

## DeFi on Cosmos
- Osmosis — largest Cosmos DEX, AMM pools
- Stride — liquid staking protocol
- Mars Protocol — lending on Osmosis
- Astroport — DEX on multiple chains
- Kava — lending, originally separate, now IBC connected

## Common Issues
- "Account not found" — address exists but has no transactions yet
- IBC transfer stuck — usually relayer delay, wait or try different path
- "Sequence mismatch" — transaction sent twice, wait for first to confirm
- Unbonding pending — 21 days is normal, not stuck
- Wrong chain address — cosmos1 address won't work on Osmosis

## Airdrops
- Cosmos ecosystem has frequent airdrops — stakers rewarded
- Stake with non-exchange validators — exchanges don't qualify
- Check claiming requirements — some have expiration
- Popular for early supporters — OSMO, JUNO, STARS all airdropped

## Security
- Same seed for all chains — secure it carefully
- Verify Keplr connections — phishing sites common
- IBC doesn't add security risk — but verify channels
- Ledger recommended for large amounts — works with Keplr
- Revoke unused permissions — wallet can audit connections
