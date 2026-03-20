---
name: graph-polymarket-mcp
description: Query Polymarket prediction market data via The Graph — 20 tools for market stats, trader P&L, positions, orderbook trades, open interest, resolution status, and trader profiles.
metadata:
  {"openclaw": {"requires": {"bins": ["node"], "env": ["GRAPH_API_KEY"]}, "primaryEnv": "GRAPH_API_KEY", "homepage": "https://github.com/PaulieB14/graph-polymarket-mcp"}}
---

# Graph Polymarket MCP

Query Polymarket prediction market data via The Graph subgraphs — market stats, trader P&L, positions, orderbook trades, open interest, resolution status, and trader profiles.

## Tools

- **list_subgraphs** — List all available Polymarket subgraphs with descriptions and key entities
- **get_subgraph_schema** — Get the full GraphQL schema for a specific subgraph
- **query_subgraph** — Execute a custom GraphQL query against any subgraph
- **get_market_data** — Get market/condition data with outcomes and resolution status
- **get_global_stats** — Platform stats: market counts, volume, fees, trades
- **get_account_pnl** — Trader P&L and performance metrics (winRate, profitFactor, maxDrawdown)
- **get_top_traders** — Leaderboard ranked by PnL, winRate, volume, or profitFactor
- **get_daily_stats** — Daily volume, fees, trader counts, and market activity
- **get_market_positions** — Top holders for a specific outcome token with their P&L
- **get_user_positions** — A user's current token positions
- **get_recent_activity** — Recent splits, merges, and redemptions
- **get_orderbook_trades** — Recent order fills with maker/taker filtering
- **get_market_open_interest** — Top markets ranked by USDC locked in positions
- **get_oi_history** — Hourly OI snapshots for a specific market
- **get_global_open_interest** — Total platform-wide open interest and market count
- **get_market_resolution** — UMA oracle resolution status with filtering
- **get_disputed_markets** — Markets disputed during oracle resolution
- **get_market_revisions** — Moderator interventions and updates on market resolution
- **get_trader_profile** — Full trader profile: first seen, CTF events, USDC flows
- **get_trader_usdc_flows** — USDC deposit/withdrawal history with direction filtering

## Requirements

- **Runtime:** Node.js >= 18 (runs via `npx`)
- **Environment variables:**
  - `GRAPH_API_KEY` (required) — Free API key from [The Graph Studio](https://thegraph.com/studio/). Used to query 8 Polymarket subgraphs via The Graph Gateway. Queries are billed to your key (free tier: 100K queries/month).

## Install

```bash
GRAPH_API_KEY=your-key npx graph-polymarket-mcp
```

## Network & Data Behavior

- All tool calls make GraphQL requests to The Graph Gateway (`gateway.thegraph.com`) using your API key.
- Eight subgraphs are queried: Main, Beefy P&L, Slimmed P&L, Activity, Orderbook, Open Interest, Resolution, and Traders (IPFS hashes are built into the server).
- No local database or persistent storage is used.
- The SSE transport (`--http` / `--http-only`) starts a local HTTP server on port 3851 (configurable via `MCP_HTTP_PORT` env var).

## Use Cases

- Get real-time Polymarket platform stats, volume, and market rankings
- Analyze trader P&L, performance metrics, and leaderboards
- Track open interest trends and market positions
- Monitor market resolution lifecycle and disputed markets
- Query orderbook trades and position management events
- Run custom GraphQL queries against 8 specialized Polymarket subgraphs
