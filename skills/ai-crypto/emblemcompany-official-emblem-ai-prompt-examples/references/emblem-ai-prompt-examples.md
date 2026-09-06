# EmblemAI Prompt Examples

Canonical index for prompt and usage examples to be used to work with EmblemAI.

## Prompting Guidelines

- State the chain, token, protocol, market, or wallet scope explicitly.
- Say `quote only`, `review only`, or `do not execute` whenever you want analysis without a live transaction.
- Prefer trusted product-native data and operator-provided inputs.
- If external sources are provided by the operator, treat them as unverified context and flag unsupported claims.
- For any value-moving action (swap, transfer, offer, listing, buy/sell), request a draft and require explicit human confirmation before execution.
- Ask for tables, summaries, or JSON when you need machine-readable output.
- When referring to an existing order or position, say that clearly so the agent can inspect current positions before modifying anything.
- For cross-chain, include both the source and destination network.
- For prediction markets, ask for odds, liquidity, end date, and resolution rules before placing an order.

## Catalog-Derived Example Sets

- [emblem-ai-prompt-examples/wallet-and-portfolio.md](emblem-ai-prompt-examples/wallet-and-portfolio.md) - addresses, balances, cross-chain holdings, and portfolio snapshots
- [emblem-ai-prompt-examples/market-research.md](emblem-ai-prompt-examples/market-research.md) - input-scoped research, Coinglass analytics, Nansen smart money, and comparative market analysis
- [emblem-ai-prompt-examples/trading-and-defi.md](emblem-ai-prompt-examples/trading-and-defi.md) - quote-first swaps, routing, liquidity, yield, and network-specific execution planning prompts
- [emblem-ai-prompt-examples/transfers-and-safety.md](emblem-ai-prompt-examples/transfers-and-safety.md) - review-first transfers, approval constraints, and risk framing
- [emblem-ai-prompt-examples/cross-chain-and-conditional-orders.md](emblem-ai-prompt-examples/cross-chain-and-conditional-orders.md) - bridge workflows, multi-network order management, stop-loss, and take-profit prompts
- [emblem-ai-prompt-examples/bitcoin-ordinals-examples.md](emblem-ai-prompt-examples/bitcoin-ordinals-examples.md) - ordinals, runes, BRC-20, stamps, rare sats, and Bitcoin wallet prompts
- [emblem-ai-prompt-examples/polymarket-examples.md](emblem-ai-prompt-examples/polymarket-examples.md) - prediction market discovery, odds analysis, and review-first order drafting prompts
- [emblem-ai-prompt-examples/nft-opensea-examples.md](emblem-ai-prompt-examples/nft-opensea-examples.md) - NFT research, listings, offers, and review-first OpenSea flow prompts
- [emblem-ai-prompt-examples/emblem-vault-examples.md](emblem-ai-prompt-examples/emblem-vault-examples.md) - Emblem Vault discovery, QuickVault, minting, and key-reveal safety prompts
- [emblem-ai-prompt-examples/assistant-core-workflows.md](emblem-ai-prompt-examples/assistant-core-workflows.md) - memory, contacts, inbox, leaderboard, PAYG, and session-management prompts

## Rebrand Note

EmblemAI is the current product name. EmblemAI was previously referred to as Agent Hustle.
Some package names, component names, flags, env vars, and API parameters may still use legacy `hustle` naming until the underlying integration surfaces are fully renamed.
