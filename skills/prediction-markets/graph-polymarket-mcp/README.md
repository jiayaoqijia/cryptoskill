# graph-polymarket-mcp

<div align="center">

[![npm version](https://img.shields.io/npm/v/graph-polymarket-mcp)](https://www.npmjs.com/package/graph-polymarket-mcp)
[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-published-blue)](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.PaulieB14/graph-polymarket-mcp)
[![smithery badge](https://smithery.ai/badge/paulieb14/graph-polymarket-mcp)](https://smithery.ai/servers/paulieb14/graph-polymarket-mcp)

<a href="https://glama.ai/mcp/servers/@PaulieB14/graph-polymarket-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@PaulieB14/graph-polymarket-mcp/badge" />
</a>

**MCP server for querying [Polymarket](https://polymarket.com/) prediction market data via [The Graph](https://thegraph.com/) subgraphs and Polymarket REST APIs.**

Exposes 31 tools that AI agents (Claude, Cursor, etc.) can use to search markets, get real-time CLOB prices and order books, query on-chain data, trader P&L, positions, activity, open interest, market resolution status, and trader profiles.

**v2.0.0** — adds 10 new tools powered by Polymarket's Gamma and CLOB APIs (inspired by [polymarket-cli](https://github.com/Polymarket/polymarket-cli)): market search, event browsing, live prices, spreads, order books, price history, and more. No API key needed for these tools — they hit Polymarket's public REST endpoints directly.

</div>

> Published to the [MCP Registry](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.PaulieB14/graph-polymarket-mcp) as `io.github.PaulieB14/graph-polymarket-mcp`

## Prerequisites

You need a **free** Graph API key (takes ~2 minutes):

1. Go to [The Graph Studio](https://thegraph.com/studio/)
2. Connect your wallet (MetaMask, WalletConnect, etc.)
3. Click **"API Keys"** in the sidebar and create one
4. Free tier includes 100,000 queries/month

## Installation

```bash
npm install -g graph-polymarket-mcp
```

Or use directly with npx:

```bash
npx graph-polymarket-mcp
```

## Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "graph-polymarket": {
      "command": "npx",
      "args": ["-y", "graph-polymarket-mcp"],
      "env": {
        "GRAPH_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add graph-polymarket -- npx -y graph-polymarket-mcp
```

Set the environment variable `GRAPH_API_KEY` before running.

### Cursor / Other MCP Clients

Use the stdio transport with `npx graph-polymarket-mcp` as the command, passing `GRAPH_API_KEY` as an environment variable.

### OpenClaw / Remote Agents (SSE)

> **The SSE transport has no authentication.** Anyone who can reach the port can call every tool,
> and those calls spend *your* `GRAPH_API_KEY` quota. `--http` binds `0.0.0.0` inside a container,
> so publish it to `127.0.0.1` on the host and put a reverse proxy with TLS and auth in front of
> anything reachable off-box. For local agents, prefer the default stdio transport — it has no
> network surface at all.


Start the server with the HTTP transport:

```bash
# Dual transport — stdio + SSE on port 3851
GRAPH_API_KEY=your-key npx graph-polymarket-mcp --http

# SSE only (for remote/server deployments)
GRAPH_API_KEY=your-key npx graph-polymarket-mcp --http-only

# Custom port
MCP_HTTP_PORT=4000 GRAPH_API_KEY=your-key npx graph-polymarket-mcp --http
```

Then point your agent at the SSE endpoint:

```json
{
  "mcpServers": {
    "graph-polymarket": {
      "url": "http://localhost:3851/sse"
    }
  }
}
```

### Transport Modes

| Invocation | Transports | Use case |
|---|---|---|
| `npx graph-polymarket-mcp` | stdio | Claude Desktop, Cursor, Claude Code |
| `npx graph-polymarket-mcp --http` | stdio + SSE :3851 | Dual — local + remote agents |
| `npx graph-polymarket-mcp --http-only` | SSE :3851 | OpenClaw, remote deployments |

A `/health` endpoint is available at `http://localhost:3851/health` when HTTP transport is active.

## Available Tools

### Core Tools

| Tool | Description |
|------|-------------|
| `list_subgraphs` | List all available Polymarket subgraphs with descriptions and key entities |
| `get_subgraph_schema` | Get the full GraphQL schema for a specific subgraph |
| `query_subgraph` | Execute a custom GraphQL query against any subgraph |

### Domain-Specific Tools

| Tool | Description | Subgraphs |
|------|-------------|-----------|
| `get_market_data` | Get market/condition data with outcomes and resolution status | Main |
| `get_global_stats` | Get platform stats: market counts + real volume/fees/trades | Main + Orderbook |
| `get_account_pnl` | Get a trader's P&L and performance metrics (winRate, profitFactor, maxDrawdown) | Beefy P&L |
| `get_top_traders` | Leaderboard ranked by PnL, winRate, volume, or profitFactor. Cross-refs Orderbook to flag rows where OB volume exceeds Beefy-tracked volume and surface OB-only traders absent from the leaderboard. | Beefy P&L + Orderbook |
| `get_daily_stats` | Daily volume, fees, trader counts, and market activity (1–90 days) | Beefy P&L |
| `get_market_positions` | Top holders for a specific outcome token with their P&L | Beefy P&L |
| `get_user_positions` | Current token positions. Cross-refs Orderbook: flags ⚠ orderbook-only entry when `totalBought=0` but OB volume exists, and ⚠ mixed entry when OB volume > 2× split collateral. | Slimmed P&L + Orderbook |
| `get_recent_activity` | Unified chronological feed interleaving splits, merges, and redemptions with orderbook fills. Supports optional address filter. | Activity + Orderbook |
| `get_orderbook_trades` | Get recent order fills with maker/taker filtering | Orderbook |
| `get_market_open_interest` | Top markets ranked by USDC locked in outstanding positions. Cross-refs Main subgraph to flag ⚠ dead money OI on resolved markets (losing-side tokens that will never be redeemed on-chain). | Open Interest + Main |
| `get_oi_history` | Hourly OI snapshots for a specific market (for charting trends) | Open Interest |
| `get_global_open_interest` | Total platform-wide open interest and market count | Open Interest |
| `get_market_resolution` | UMA oracle resolution status with filtering by status | Resolution |
| `get_disputed_markets` | Markets disputed during oracle resolution (high-signal events) | Resolution |
| `get_market_revisions` | Moderator interventions and updates on market resolution | Resolution |
| `get_trader_profile` | Full trader profile combining CTF events and USDC flows with Orderbook fills. Classifies wallet as hybrid / orderbook-only / split-collateral-only and warns when P&L subgraphs are unreliable. | Traders + Orderbook |
| `get_trader_usdc_flows` | USDC deposit/withdrawal history with direction filtering | Traders |

### Polymarket REST API Tools (no Graph API key needed)

| Tool | Description | API |
|------|-------------|-----|
| `search_markets` | Search markets by text query with filters (active, closed, sort by volume/liquidity) | Gamma |
| `get_market_info` | Get detailed market metadata by slug or condition ID | Gamma |
| `list_polymarket_events` | Browse events (groups of related markets) with tag/status filters | Gamma |
| `get_polymarket_event` | Get a single event with all its associated markets | Gamma |
| `get_live_prices` | Real-time CLOB prices for outcome tokens (buy/sell, single or batch) | CLOB |
| `get_live_spread` | Bid-ask spread + midpoint for assessing market liquidity | CLOB |
| `get_live_orderbook` | Full order book (all resting bids and asks) for a token | CLOB |
| `get_price_history` | Historical price time-series (1m to max interval, configurable fidelity) | CLOB |
| `get_last_trade` | Last trade price for an outcome token | CLOB |
| `get_clob_market` | CLOB market details: token IDs, live prices, min order/tick sizes | CLOB |
| `search_markets_enriched` | **Power tool**: search + auto-enrich with live CLOB prices AND on-chain resolution status in one call | Gamma + CLOB + Graph |

### CLOB V2 Tools

Polymarket migrated to V2 exchange contracts on **2026-04-28**. These tools read the V2 subgraphs,
which index from block 84902353 and hold **no pre-migration history** — V1 and V2 are different
eras, not old and new.

| Tool | Description | Subgraphs |
|------|-------------|-----------|
| `get_builder_leaderboard` | Rank V2 builders by routed volume, order count or fees, with each builder's share of V2 volume. **No V1 equivalent** — the V1 contracts never emitted a builder code | V2 Orderbook |
| `get_builder_activity` | Recent fills routed by one builder code, plus that builder's aggregate totals | V2 Orderbook |
| `get_v2_top_traders` | Top real V2 traders, with the exchange contracts filtered out | V2 Orderbook |
| `check_subgraph_freshness` | How far behind chainhead any subgraph is, read live from its `_meta` block | Any |

**Builder attribution** is the capability V2 adds. Every V2 fill carries the `builder` code of the
frontend, bot or integrator that routed it, so "who is actually routing this flow" becomes an
answerable question — 3,325 builders as of 2026-08-08.

**Two traps these tools handle for you.** The V2 exchange contracts appear as `Account` rows, because
the exchange is the `taker` when an order matches the book — ranking accounts naively returns
`0xe111…996b` (176M fills) and `0xe222…0f59` (41M fills) above every human. `get_v2_top_traders`
excludes them. And `v2_main` is still syncing, so it answers with stale data rather than erroring;
`check_subgraph_freshness` tells you how stale before you trust a number.

## Data Sources

### The Graph Subgraphs (requires `GRAPH_API_KEY`)

On-chain indexed data — authoritative for historical analytics, P&L, open interest, and resolution status.

## Subgraphs

| Name | IPFS Hash | Description |
|------|-----------|-------------|
| Main | `QmdyCguLEisTtQFveEkvMhTH7UzjyhnrF9kpvhYeG4QX8a` | Complete ecosystem data |
| Beefy P&L | `QmbHwcGkumWdyTK2jYWXV3vX4WyinftEGbuwi7hDkhPWqG` | Comprehensive P&L tracking |
| Slimmed P&L | `QmZAYiMeZiWC7ZjdWepek7hy1jbcW3ngimBF9ibTiTtwQU` | Minimal position data |
| Activity | `Qmf3qPUsfQ8et6E3QNBmuXXKqUJi91mo5zbsaTkQrSnMAP` | Position management events |
| Orderbook | `QmVGA9vvNZtEquVzDpw8wnTFDxVjB6mavTRMTrKuUBhi4t` | Order fill analytics |
| Open Interest | `QmbT2MmS2VGbGihiTUmWk6GMc2QYqoT9ZhiupUicYMWt6H` | Per-market and global OI with hourly snapshots |
| Resolution | `QmZnnrHWCB1Mb8dxxXDxfComjNdaGyRC66W8derjn3XDPg` | UMA oracle resolution lifecycle |
| Traders | `QmfT4YQwFfAi77hrC2JH3JiPF7C4nEn27UQRGNpSpUupqn` | Per-trader event logs and USDC flows |

### CLOB V2 (from block 84902353 — no earlier history)

| Name | IPFS Hash | Status | Description |
|------|-----------|--------|-------------|
| V2 Orderbook | `QmNtJGxpAjFgoHhMwdijyvbLrpPPiHHX2qct56nTpk42Bs` | at chainhead | V2 fills with **builder-code attribution** |
| V2 P&L | `QmT21E4p8r6FCzW2EPK4NVj1dbcggdvKxZr8uuMcB4P5Cu` | at chainhead | Cost basis and realized P&L from V2 fills only |
| V2 Main | `QmTKrqyYg23BjhihmsrRjbV9cVS2piNmnHsr7cjYaTgdWu` | ⚠️ **syncing** | Conditions and counters — ~86 days behind as of 2026-08-08 |

Open Interest (above) is already a V2 deployment; it reads ConditionalTokens, which V2 left
unchanged, so it has no migration discontinuity.

Which era to ask: **all-time or pre-2026-04-28 → V1.** Post-migration activity, or anything about
builders → V2. `beefy_pnl` keeps the hedge-fund metrics (winRate, profitFactor, maxDrawdown, daily
series) that V2 P&L does not have, so trader-quality scoring stays on V1.

## Example Queries

Once connected, an AI agent can:

### Market Discovery (Gamma API)
- "Search for prediction markets about AI"
- "Show me the most active Polymarket events right now"
- "Find markets about the 2024 election sorted by volume"
- "What markets are in the 'crypto' category?"

### Live Trading Data (CLOB API)
- "What's the current price for the Trump YES token?"
- "Show me the full order book for this market"
- "What's the bid-ask spread on this token?"
- "Show me the price history for this market over the last week"

### On-Chain Analytics (The Graph)
- "What are the current Polymarket global stats?"
- "Show me the latest 20 orderbook trades"
- "What are the positions for address 0x...?" *(flags if wallet entered via OB buys only)*
- "Get the P&L for trader 0x...?"
- "Which markets have the most open interest right now?" *(flags dead-money OI on resolved markets)*
- "Show me disputed markets on Polymarket"
- "Who are the top traders?" *(flags any with OB volume not captured by Beefy P&L)*
- "Show me the full trading history for wallet 0x..." *(includes OB fills + entry type classification)*

## Development

```bash
git clone https://github.com/PaulieB14/graph-polymarket-mcp.git
cd graph-polymarket-mcp
npm install
npm run build
GRAPH_API_KEY=your-key node build/index.js
```

## License

MIT
