# graph-polymarket-mcp

<div align="center">

[![npm version](https://img.shields.io/npm/v/graph-polymarket-mcp)](https://www.npmjs.com/package/graph-polymarket-mcp)
[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-published-blue)](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.PaulieB14/graph-polymarket-mcp)
[![smithery badge](https://smithery.ai/badge/paulieb14/graph-polymarket-mcp)](https://smithery.ai/servers/paulieb14/graph-polymarket-mcp)

<a href="https://glama.ai/mcp/servers/@PaulieB14/graph-polymarket-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@PaulieB14/graph-polymarket-mcp/badge" />
</a>

**MCP server for querying [Polymarket](https://polymarket.com/) prediction market data via [The Graph](https://thegraph.com/) subgraphs.**

Exposes 20 tools that AI agents (Claude, Cursor, etc.) can use to query market data, trader P&L, positions, activity, orderbook trades, open interest, market resolution status, and trader profiles.

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

| Tool | Description | Subgraph |
|------|-------------|----------|
| `get_market_data` | Get market/condition data with outcomes and resolution status | Main |
| `get_global_stats` | Get platform stats: market counts + real volume/fees/trades | Main + Orderbook |
| `get_account_pnl` | Get a trader's P&L and performance metrics (winRate, profitFactor, maxDrawdown) | Beefy P&L |
| `get_top_traders` | Leaderboard of top traders ranked by PnL, winRate, volume, or profitFactor | Beefy P&L |
| `get_daily_stats` | Daily volume, fees, trader counts, and market activity (1–90 days) | Beefy P&L |
| `get_market_positions` | Top holders for a specific outcome token with their P&L | Beefy P&L |
| `get_user_positions` | Get a user's current token positions | Slimmed P&L |
| `get_recent_activity` | Get recent splits, merges, and redemptions | Activity |
| `get_orderbook_trades` | Get recent order fills with maker/taker filtering | Orderbook |
| `get_market_open_interest` | Top markets ranked by USDC locked in outstanding positions | Open Interest |
| `get_oi_history` | Hourly OI snapshots for a specific market (for charting trends) | Open Interest |
| `get_global_open_interest` | Total platform-wide open interest and market count | Open Interest |
| `get_market_resolution` | UMA oracle resolution status with filtering by status | Resolution |
| `get_disputed_markets` | Markets disputed during oracle resolution (high-signal events) | Resolution |
| `get_market_revisions` | Moderator interventions and updates on market resolution | Resolution |
| `get_trader_profile` | Full trader profile: first seen, CTF events, USDC flows | Traders |
| `get_trader_usdc_flows` | USDC deposit/withdrawal history with direction filtering | Traders |

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

## Example Queries

Once connected, an AI agent can:

- "What are the current Polymarket global stats?"
- "Show me the latest 20 orderbook trades"
- "What are the positions for address 0x...?"
- "Get the P&L for trader 0x...?"
- "Query the main subgraph for all conditions with more than 100 trades"
- "Which markets have the most open interest right now?"
- "Show me the OI trend for market 0x..."
- "What's the total open interest across all Polymarket markets?"
- "Show me disputed markets on Polymarket"
- "What's the resolution status of market 0x...?"
- "Show me the full trading history for wallet 0x..."
- "Track USDC deposits and withdrawals for trader 0x..."

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
