---
name: Chainlink
description: Assist with Chainlink LINK tokens, oracle integrations, staking, and price feed usage.
metadata: {"clawdbot":{"emoji":"⬡","os":["linux","darwin","win32"]}}
---

## LINK Token Basics
- LINK is an ERC-20 token on Ethereum — standard wallet and exchange support
- Also available on multiple chains — Arbitrum, Optimism, Polygon, Avalanche, BSC
- Bridging LINK between chains uses official Chainlink bridge — verify bridge address before using
- Different chains have different LINK contract addresses — verify correct address per network

## Token Transfers
- Standard ERC-20 transfer rules apply — gas paid in native token (ETH, MATIC, etc.)
- Some DeFi protocols accept LINK as collateral — Aave, Compound
- LINK has no special transfer restrictions — no tax tokens, no rebasing
- Decimals: 18 — same as ETH, standard precision

## Staking (v0.2)
- Community staking allows LINK holders to stake — earn rewards for securing network
- Staking has capacity limits — pool may be full, waitlist exists
- Unbonding period applies — can't withdraw instantly after unstaking
- Rewards in LINK — automatically added to staked balance
- Slashing risk exists — node operators can lose stake for misbehavior

## Price Feeds (For Developers)
- Chainlink price feeds are the standard for DeFi — Aave, Synthetix, and most protocols use them
- Feed addresses differ per network and pair — always verify on docs.chain.link
- Feeds update based on deviation threshold and heartbeat — not every block
- Check `latestRoundData()` not just `latestAnswer()` — includes timestamp and round info
- Stale data check critical — verify `updatedAt` timestamp is recent

## Oracle Integration Patterns
- Direct consumer: your contract calls feed directly — simplest approach
- Chainlink Automation (Keepers): trigger actions based on conditions — no server needed
- VRF (Verifiable Random Function): provably fair randomness — for NFT mints, games, lotteries
- Functions: connect to any API — custom off-chain computation
- CCIP: cross-chain messaging — official Chainlink interoperability protocol

## VRF Usage
- Request/receive pattern: request randomness, receive in callback — not synchronous
- Each request costs LINK — fund subscription or pay per request
- Confirmation blocks add security but delay — more confirmations = more secure
- Randomness is verifiable on-chain — anyone can verify it wasn't manipulated

## Common Developer Mistakes
- Hardcoding feed addresses — use address registry or config
- Not checking for stale data — price feeds can stop updating
- Assuming instant updates — deviation thresholds mean prices can be slightly stale
- Not handling VRF callback failures — callback can revert, losing the randomness
- Insufficient LINK for subscriptions — requests fail silently when underfunded

## Network Comparisons
- Ethereum mainnet: highest security, highest gas costs
- L2s (Arbitrum, Optimism): lower cost, same security model
- Alt-L1s (Polygon, Avalanche): native integration, different trust assumptions
- Testnets: Sepolia for Ethereum, network-specific for others

## Security Considerations
- Only use official Chainlink feeds — verify contract addresses on docs.chain.link
- Monitor for feed deprecation — Chainlink announces deprecated feeds
- Multi-oracle pattern for critical systems — don't rely on single source
- Circuit breakers for extreme price movements — protect against oracle manipulation

## CCIP (Cross-Chain)
- Send messages and tokens across chains — official Chainlink bridge
- Lane availability varies — not all chain pairs supported
- Fee estimation before sending — paid in LINK or native token
- Message finality depends on source and destination chains

## Ecosystem
- Node operators earn LINK for providing data — professional infrastructure required
- BUILD program for projects integrating Chainlink — access to resources and support
- Extensive documentation at docs.chain.link — primary reference for developers
- Community resources: Discord, Stack Overflow, GitHub
