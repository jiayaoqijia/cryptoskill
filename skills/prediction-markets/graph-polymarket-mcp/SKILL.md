---
name: graph-polymarket-mcp
version: 2.1.2
description: Query Polymarket prediction market data via The Graph subgraphs + Polymarket REST APIs (Gamma + CLOB) — 35 tools for market search, live prices, on-chain analytics, trader P&L, open interest, resolution status, and CLOB V2 builder attribution.
metadata:
  clawdbot:
    emoji: "🔮"
    requires:
      bins: ["node"]
      env: ["GRAPH_API_KEY"]
    primaryEnv: "GRAPH_API_KEY"
    # Declared explicitly rather than left implicit: this server reads one env var and
    # talks to three hosts, and nothing else. Anything outside this list is a bug.
    capabilities:
      env:
        - name: GRAPH_API_KEY
          purpose: "Authenticates subgraph queries to The Graph gateway. Sent only to gateway.thegraph.com; never logged, never forwarded to Polymarket or any other host."
          required: false
      network:
        - host: gateway.thegraph.com
          purpose: "Subgraph queries. Receives GRAPH_API_KEY."
        - host: gamma-api.polymarket.com
          purpose: "Public market metadata. No credentials sent."
        - host: clob.polymarket.com
          purpose: "Public prices and order books. No credentials sent."
      filesystem: none
      transports: ["stdio (default)", "sse (opt-in, --http)"]
---

# Graph Polymarket MCP

> **Transport note.** The default is **stdio** — no network surface, nothing listening. The
> optional `--http` SSE transport is **unauthenticated**: anyone who can reach the port can call
> every tool and spend your `GRAPH_API_KEY` quota. Bind it to localhost and front it with TLS and
> auth if it must be reachable.

Query Polymarket prediction market data via The Graph subgraphs and Polymarket REST APIs (Gamma + CLOB) — market search, live prices, order books, trader P&L, positions, open interest, resolution status, and trader profiles.

## Try it

### Polymarket REST API (no API key needed)

- **search_markets** — Search markets by text query with filters (active, closed, sort by volume/liquidity)
- **get_market_info** — Get detailed market metadata by slug or condition ID
- **list_polymarket_events** — Browse events (groups of related markets) with tag/status filters
- **get_polymarket_event** — Get a single event with all its associated markets
- **get_live_prices** — Real-time CLOB prices for outcome tokens (buy/sell, single or batch)
- **get_live_spread** — Bid-ask spread + midpoint for assessing market liquidity
- **get_live_orderbook** — Full order book (all resting bids and asks) for a token
- **get_price_history** — Historical price time-series (1m to max interval, configurable fidelity)
- **get_last_trade** — Last trade price for an outcome token
- **get_clob_market** — CLOB market details: token IDs, live prices, min order/tick sizes
- **search_markets_enriched** — Power tool: search + auto-enrich with live CLOB prices AND on-chain resolution status

### The Graph Subgraphs (requires GRAPH_API_KEY)

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

## 20 tools available

- **Runtime:** Node.js >= 18 (runs via `npx`)
- **Environment variables:**
  - `GRAPH_API_KEY` (required for subgraph tools) — Free API key from [The Graph Studio](https://thegraph.com/studio/). Free tier: 100K queries/month.
  - REST API tools (search, prices, order books) work without any API key.

## Install

```bash
GRAPH_API_KEY=your-key npx graph-polymarket-mcp
```

Get a free API key at [The Graph Studio](https://thegraph.com/studio/) (free tier: 100K queries/month).

- Subgraph tools make GraphQL requests to The Graph Gateway (`gateway.thegraph.com`) using your API key.
- REST API tools query Polymarket's public endpoints (`gamma-api.polymarket.com` and `clob.polymarket.com`) directly — no authentication needed.
- Eight subgraphs are queried: Main, Beefy P&L, Slimmed P&L, Activity, Orderbook, Open Interest, Resolution, and Traders.
- No local database or persistent storage is used.
- The SSE transport (`--http` / `--http-only`) starts a local HTTP server on port 3851 (configurable via `MCP_HTTP_PORT` env var).

| Endpoint | Data sent | Purpose |
|----------|-----------|---------|
| `gateway.thegraph.com` | GraphQL queries with your API key | Queries 8 Polymarket subgraphs |

- Search and discover prediction markets by topic, category, or keyword
- Get real-time prices, order books, and spreads for any market
- Analyze price history and market trends
- Get platform-wide stats, volume, and market rankings
- Analyze trader P&L, performance metrics, and leaderboards
- Track open interest trends and market positions
- Monitor market resolution lifecycle and disputed markets
- Run custom GraphQL queries against 8 specialized Polymarket subgraphs
