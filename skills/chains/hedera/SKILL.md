---
name: Hedera
description: Assist with Hedera HBAR transactions, account creation, token service, and consensus features.
metadata: {"clawdbot":{"emoji":"ℏ","os":["linux","darwin","win32"]}}
---

## Account Model (Critical Difference)
- Hedera accounts must be created before receiving funds — unlike Bitcoin/Ethereum, addresses don't exist until created
- Account creation costs HBAR — someone must fund the initial creation
- Account IDs are numeric (0.0.12345) — not cryptographic hashes like other chains
- Memo field available on accounts — can store small amounts of data
- Accounts can be deleted to recover balance — but requires all tokens and associations removed first

## Account Creation
- New users need someone to create their account — can't just generate address and receive
- Exchanges create accounts on withdrawal — but self-custody requires creation first
- HashPack and other wallets offer account creation — may require payment or sponsor
- Testnet accounts free to create — use for development and testing

## Transaction Fees
- Fees are extremely low and predictable — typically $0.0001 or less
- Fees paid in HBAR only — no gas token complexity
- Transaction fees set by network, not auction — no priority fee bidding
- Scheduled transactions cost extra — pay for scheduling plus execution

## Token Service (HTS)
- Native token support without smart contracts — create tokens via Hedera Token Service
- Token association required before receiving — must explicitly associate with token ID
- Association costs small HBAR fee — limits spam tokens
- Fungible and NFT tokens supported natively — no need for custom contracts
- Token admin keys control supply, freeze, wipe — verify token permissions before trusting

## Memo Field
- Transactions can include memo — used for exchange deposits like destination tags
- Memo is public and permanent — don't include sensitive data
- Some services require specific memo format — verify before sending
- Max memo size is 100 bytes — keep it short

## Consensus and Finality
- Transactions finalize in 3-5 seconds — no waiting for confirmations
- Hashgraph consensus provides ordering guarantees — no MEV or frontrunning possible
- Fair ordering prevents manipulation — transactions processed in order received
- Mirror nodes provide historical data — main network doesn't store full history

## Smart Contracts
- Hedera supports Solidity smart contracts — EVM compatible
- Contracts interact with native HTS tokens — best of both worlds
- Contract deployment costs more than simple transactions — plan accordingly
- State storage costs ongoing rent — unused contracts still cost

## Staking
- Native staking to nodes — no minimum, no lockup
- Rewards paid automatically every 24 hours — no claiming needed
- Staking doesn't transfer funds — HBAR stays in your account
- Choosing a node affects decentralization — spread stakes across nodes

## Keys and Security
- Accounts can have multiple keys — threshold signatures supported
- Key rotation possible without changing account ID — update keys if compromised
- Different key types: Ed25519, ECDSA (secp256k1) — affects wallet compatibility
- Admin keys on tokens can freeze/wipe holdings — check before acquiring tokens

## Common Issues
- "INSUFFICIENT_PAYER_BALANCE" — need more HBAR for fees
- "INVALID_ACCOUNT_ID" — account doesn't exist, needs creation
- "TOKEN_NOT_ASSOCIATED" — must associate with token before receiving
- "INSUFFICIENT_TX_FEE" — rare, fee estimate was too low
- "ACCOUNT_FROZEN_FOR_TOKEN" — token admin has frozen transfers

## Exchanges and Transfers
- Most major exchanges support HBAR — verify account ID format (0.0.xxxxx)
- Memo often required for exchange deposits — critical like XRP destination tags
- Account ID is not a wallet address — don't confuse with Ethereum-style addresses
- Verify recipient account exists before sending — non-existent accounts reject transfers

## Network Services
- Hedera Consensus Service (HCS) — ordered message logging
- Hedera File Service (HFS) — store larger data on network
- Mirror nodes for queries — don't query mainnet for historical data
- SDKs available for major languages — JavaScript, Java, Go, Python
