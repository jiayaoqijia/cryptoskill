---
name: dexter-mcp
description: "Use Dexter MCP for authenticated access to Dexter's full tool suite: x402 marketplace search and payments, Solana trading (Jupiter swaps, token resolution, balances, sends), on-chain analytics, Hyperliquid perps, media generation (Sora video, meme images), Twitter analysis, Pokedexter battles, stream shouts, and 50+ more tools. Trigger whenever the user wants to trade tokens, search paid APIs, generate media, analyze on-chain data, check Solana balances, do anything with Dexter, or access any x402 marketplace functionality through their Dexter account."
---

# Dexter MCP — Authenticated Dexter Platform

The authenticated Dexter MCP gives you full access to the Dexter platform through the user's Dexter account. This includes the x402 marketplace tools plus 50+ additional Dexter-native tools for trading, analytics, media, games, and more.

Payment is automatic — the user's managed Dexter wallet handles all x402 settlements without any manual funding step.

## x402 Marketplace Tools

These five tools work the same as OpenDexter but with automatic payment through the user's Dexter wallet. No session funding needed.

### `x402_search` — Find paid APIs
Search the x402 marketplace across Solana and EVM chains. Pass the user's job as the query. Use `maxPriceUsdc` or `minPriceUsdc` for a hard API invocation-price bound, `paidOnly: true` for known positive primary USDC prices, and `sortBy` for `relevance`, `price_asc`, or `price_desc`. Confirm typed controls in `appliedConstraints` and `appliedOrdering`. Price order applies inside each relevance tier; strong results remain ahead of related results. The selected endpoint still needs `x402_check` because alternate payment options can quote a different amount.

### `x402_check` — Preview pricing
Probe an endpoint to see payment requirements per chain without paying. Shows pricing options for each supported chain. Use before `x402_fetch` to show the user what it'll cost.

### `x402_fetch` — Call and pay automatically
Call any x402 endpoint with automatic payment from the user's Dexter wallet on the appropriate chain. No manual funding — it just works. The user gets the API response directly along with a payment receipt.

### `x402_wallet` — View wallet
Shows the authenticated wallet address and balances. The Dexter managed wallet is pre-funded through the user's account.

## Dexter-Native Tools

Beyond the x402 marketplace, the authenticated MCP provides direct access to Dexter's platform tools. These are organized by category:

### Solana Trading
- **solana_resolve_token**: Look up any Solana token by name, symbol, or mint address
- **solana_list_balances**: Show the user's Solana token balances
- **solana_send**: Send SOL or SPL tokens to another wallet
- **solana_swap_preview**: Get a Jupiter DEX quote for a token swap
- **solana_swap_execute**: Execute a swap through Jupiter

When the user wants to trade, the typical flow is: resolve the token → preview the swap → confirm with the user → execute.

### Market Data
- **markets_fetch_ohlcv**: Get OHLCV candlestick data for any token from Birdeye

### On-Chain Analytics
- **onchain_activity_overview**: Real-time on-chain activity feed for Solana
- **onchain_entity_insight**: Deep analysis of a specific token, wallet, or transaction

### Research & Social
- **twitter_topic_analysis**: Analyze Twitter conversation volume, sentiment, and engagement for a topic or cashtag
- **search**: Web search powered by Tavily
- **fetch**: Fetch and extract content from any URL

### Hyperliquid Perps
- **hyperliquid_markets**: Browse available perpetual futures markets
- **hyperliquid_perp_trade**: Execute a perp trade
- **hyperliquid_fund**: Fund the Hyperliquid sub-account
- **hyperliquid_bridge_deposit**: Bridge USDC to Hyperliquid

### Games
- **Pokedexter**: Wagered Pokemon battles (create challenges, accept battles, make moves)
- **King of Dexter**: Pay to become King, submit decrees
- **Infinite Story**: Append words to a collaborative on-chain story

### Stream
- **stream_public_shout**: Broadcast a paid message to the Dexter stream

### Bundles
- **list_bundles**, **get_bundle**, **create_bundle**, etc.: Create and manage curated collections of x402 resources

## Workflow Patterns

### "Swap 10 USDC for SOL"
1. `solana_resolve_token` for SOL and USDC (get mint addresses)
2. `solana_swap_preview` with the amounts
3. Show the quote to the user (price, slippage, route)
4. On confirmation, `solana_swap_execute`

### "What's trending on Solana?"
1. `onchain_activity_overview` for a real-time feed
2. Or search for trending tools: `x402_search` query "trending tokens"

### "Generate a meme about Bitcoin"
1. `meme_generator_job` with the prompt

### "Find me a paid API for sentiment analysis"
1. `x402_search` query "sentiment analysis"
2. `x402_check` on the best result
3. `x402_fetch` to call it

### "What are my balances?"
1. `solana_list_balances` for token balances
2. `x402_wallet` for the x402 settlement wallet specifically

## Key Differences from OpenDexter

| Aspect | This (Authenticated) | OpenDexter |
|--------|---------------------|------------|
| Auth | Dexter OAuth required | No auth |
| Wallet | Managed by Dexter, pre-funded | Session wallet, persists 30 days, needs manual funding |
| Tools | 50+ (trading, analytics, media, games + x402) | 5 (x402 marketplace only) |
| Payment | Automatic, zero friction | Automatic after session funding |
| Best for | Power users with Dexter accounts | Anyone, quick marketplace access |

## Tips

- The user is already authenticated. Don't ask them to log in or set up a wallet — it's handled.
- For x402 marketplace searches, quality scores and verification status help the user choose. Highlight verified endpoints.
- For swaps, always preview before executing. Show the user the quote and get confirmation.
- Sora video generation is expensive ($8/job) — mention the price before submitting.
- The marketplace search is fuzzy and supports typos. Search broadly.
