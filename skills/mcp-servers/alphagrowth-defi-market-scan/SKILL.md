---
name: defi-market-scan
description: Scan the crypto market with AlphaGrowth data, ranking projects, chains, fees, yields, stablecoins and token unlocks, or comparing them. Use for market-wide questions ("top DeFi protocols on Base by TVL", "which protocols earn the most fees?", "best stablecoin yields over $10M TVL", "what unlocks are coming next week?", "which chains are growing fastest?").
compatibility: Needs the AlphaGrowth MCP server (https://alphagrowth.io/mcp) connected in Hermes as `alphagrowth`. No account or API key.
---

# DeFi market scan

Answer from the AlphaGrowth tools (`mcp__alphagrowth__*`). If they aren't available, tell the user to enable the plugin (`hermes plugins enable alphagrowth`) and start a new session, then stop.

## Pick the tool

| The user wants | Call |
|---|---|
| Projects ranked by TVL, market cap, revenue, users or followers, or by their 1d/7d/30d change | `mcp__alphagrowth__rank_projects` with `sort_by` (`tvl`, `tvl-change-7d`, `market-cap-value`, `revenue-30d`, `twitter-followers`, ...), optionally `category` and `chain` |
| Category slugs for that filter | `mcp__alphagrowth__categories` |
| Blockchains by TVL | `mcp__alphagrowth__chains`; then `mcp__alphagrowth__chain_metrics` for one chain |
| Protocols by fees or revenue | `mcp__alphagrowth__fees` with `sort_by` (`fees`, `revenue`, `fees_7d`, `fees_24h_change`, ...); `mcp__alphagrowth__chain_fees` for one chain |
| DEX, options or aggregator volume | `mcp__alphagrowth__volumes` with `kind` |
| Yield and lending pools | `mcp__alphagrowth__yield_pools` with `sort_by` (`supply_apy`, `borrow_apy`, `tvl`), `chain`, `token`, `stablecoins_only: "yes"` and `min_tvl_usd` (1000000 or more skips thin pools whose APYs swing) |
| Stablecoins | `mcp__alphagrowth__stablecoins`, `mcp__alphagrowth__stablecoin_chains`, `mcp__alphagrowth__stablecoin_history` |
| Token unlocks | `mcp__alphagrowth__token_unlocks` with `days`, `min_value_usd`, `sort_by` (`date` or `value`) |
| New projects and TGEs | `mcp__alphagrowth__upcoming_projects`, `mcp__alphagrowth__upcoming_tges` |
| DAO treasuries | `mcp__alphagrowth__dao_treasuries`, then `mcp__alphagrowth__dao_treasury_history` for one DAO |
| Token prices | `mcp__alphagrowth__token_prices`, `mcp__alphagrowth__token_price_history` |

Lists come 50 per page: pass `page` for more instead of guessing what lies beyond.

## Answer

Show a short ranked table with the metric the user asked about, its change, and the date the data is for. Flag `apy_spike` pools as unusual rather than recommending them. Link the AlphaGrowth source block each result carries. This is market data, not investment advice: don't tell the user to buy, sell or deposit.
