---
name: philidor-mcp
description: >
  DeFi vault risk analytics MCP server: search 1000+ vaults, compare risk scores,
  list lending markets, underwrite loop venues, analyze protocols, run due diligence.
  Connect via Streamable HTTP — no API key needed. Use when setting up or using the
  Philidor MCP server for DeFi vault analysis, risk scoring, market monitoring,
  loop venue checks, protocol research, or yield comparison.
---

# Philidor MCP Server — DeFi Vault Risk Analytics

An MCP server that gives AI agents access to institutional-grade DeFi vault risk analytics. Search vaults, compare risks, list lending markets, underwrite collateral/debt loops, analyze protocols, and perform due diligence across Aave, Morpho, Spark, Compound, Yearn, Beefy, Uniswap, Nest, Maple, and Kamino.

No API key required. No installation needed. Read-only: Philidor does not compute health factor and does not prepare transactions.

## When to Use This Skill

- User wants to set up the Philidor MCP server in Claude Desktop, Claude Code, Cursor, or Windsurf
- User asks about DeFi vault risk, safety, yield, or depositability
- User wants to compare vaults or analyze protocols via MCP tools
- User needs due diligence on a vault, or a pre-deposit / loop-venue check (`check_loop_venue`)
- User asks about lending markets, market events, or vaults with recent critical incidents
- User asks about DeFi market stats or risk methodology

## When NOT to Use This Skill

- User asks about token prices, swaps, or trading (read-only analytics only)
- User wants the CLI tool instead (use the `philidor-cli` skill)
- User asks about NFTs or non-DeFi topics
- User needs baskets, oracle vectors, enriched/RWA breakdowns, the event stream, or Risk Graph — point them at the Philidor API docs instead of inventing figures

## Setup

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "philidor": {
      "url": "https://mcp.philidor.io/api/mcp"
    }
  }
}
```

### Claude Code

```bash
claude mcp add philidor --transport http https://mcp.philidor.io/api/mcp
```

### Cursor

Install the Philidor Cursor plugin when listed, or add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "philidor": {
      "url": "https://mcp.philidor.io/api/mcp"
    }
  }
}
```

### Windsurf

Add to your MCP settings:

```json
{
  "mcpServers": {
    "philidor": {
      "serverUrl": "https://mcp.philidor.io/api/mcp"
    }
  }
}
```

### Docker (stdio)

```bash
docker run -i --rm ghcr.io/philidor-labs/philidor-mcp
```

## Tools (14)

### `search_vaults`

Search and filter DeFi vaults by chain, protocol, asset, risk tier, TVL, and more.

| Parameter | Type | Description |
| --- | --- | --- |
| `query` | string | Search by vault name, symbol, asset, protocol, curator |
| `chain` | string | Filter by chain name or slug (Ethereum, Base, Solana, ...) |
| `protocol` | string | `aave`, `morpho`, `spark`, `compound`, `yearn`, `beefy`, `uniswap`, `nest`, `maple`, `kamino` |
| `protocolVersion` | string | `v3`, `v4`, `v3-lido`, `v3-horizon`, `klend`, `kvault` — use with `protocol=aave` for V4 |
| `asset` | string | Filter by asset symbol (USDC, WETH, ...) |
| `riskTier` | string | Prime, Core, or Edge |
| `minTvl` | number | Minimum TVL in USD |
| `depositable` | boolean | Filter by current deposit capacity |
| `sortBy` | string | `tvl_usd`, `apr_net`, `name`, `last_synced_at` |
| `sortOrder` | string | `asc` or `desc` |
| `limit` | number | Max results (default 10, max 50) |

Aave V4 is `protocol=aave` plus `protocolVersion=v4` (`aave-v4` is an accepted alias).

### `get_vault`

Full vault detail including risk breakdown, events, and snapshots. Lookup by `id` **or** `network` + `address`.

### `get_vault_risk_breakdown`

Four risk vectors: Asset Composition, Platform and Strategy, Control and Governance, and History. Requires `network` and `address`.

### `list_markets`

Lending markets (Aave/Spark pools, Aave V4 spokes, Compound Comet, Morpho Blue pairs, Kamino K-Lend). Parameters: `protocol`, `version`, `chain`, `limit`, `sortBy` (`total_supplied_usd`, `total_borrowed_usd`, `reserve_count`, `name`). Aave V4 hubs are composed parents (e.g. `aave-v4-1-hub-core`); the API still keys on the spoke. Not the same as `get_market_overview`.

### `get_market`

One market with every reserve: supplied, supply APR, borrowed, borrow APR, utilization, tier. Requires `marketId`.

### `get_market_events`

Published risk events for one market. Requires `marketId`; optional `limit` (1–100, default 20). Hub ids union spoke feeds.

### `check_loop_venue`

Underwrite a collateral/debt loop on one market: score, tier, utilization, borrow APR, deposit status, incidents for both legs. Requires `marketId`, `collateral`, `debt`. Does **not** compute health factor or prepare txs — hand those to the protocol MCP.

### `compare_vaults`

Side-by-side comparison of 2–3 vaults. `vaults` is an array of `{ network, address }`.

### `find_safest_vaults`

Top 10 audited vaults by Philidor risk score (higher = lower assessed risk; not a safety guarantee). Optional `asset`, `chain`, `minTvl`.

### `get_protocol_info`

Protocol detail including TVL, vault count, versions, auditors, incidents. Requires `protocolId`.

### `get_curator_info`

Curator track record and managed vaults. Requires `curatorId`.

### `get_market_overview`

Platform-wide vault TVL, vault count, risk distribution, TVL by protocol. No parameters.

### `explain_risk_score`

Explain a 0–10 score and its Prime/Core/Edge tier. Requires `score`.

### `list_vaults_with_incidents`

Vaults with a critical incident in the last 365 days (severity Critical or `incident_severity` major). No parameters.

## Resources

| URI | Description |
| --- | --- |
| `philidor://methodology` | Vector Risk Framework documentation |
| `philidor://supported-chains` | Supported chains with vault counts / TVL |
| `philidor://supported-protocols` | Supported protocols with vault counts / TVL |

## Prompts

| Prompt | Description |
| --- | --- |
| `vault_due_diligence` | Due diligence report for one vault (`network`, `address`) |
| `portfolio_risk_assessment` | Portfolio-level risk across positions |
| `defi_yield_comparison` | Yield comparison with risk-score context |
| `review_loop_venue` | Loop venue review then hand off to a protocol MCP |

## Reporting rules

- Never invent risk scores, tiers, APRs, addresses, vault ids, or market ids. Cite values returned by tools.
- Keep base yield and reward APR separate when both are present.
- Treat deposit status `closed` / `unknown` as non-executable until confirmed open.
- For loops: call `check_loop_venue` (or `list_markets` then `get_market`) before any protocol MCP `preview_action` / `prepare_action`.
- A higher Philidor score means lower assessed risk under the current methodology — not a guarantee.
