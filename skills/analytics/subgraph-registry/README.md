# Subgraph Registry

<a href="https://glama.ai/mcp/servers/PaulieB14/subgraph-registry">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/PaulieB14/subgraph-registry/badge" />
</a>

Agent-friendly semantic classification of all subgraphs on [The Graph Network](https://thegraph.com).

Pre-computed index of 15,500+ subgraphs with domain classification, protocol type detection, schema fingerprinting, canonical entity mapping, and composite reliability scoring.

## The Problem

Agents querying The Graph need to discover and select the right subgraph before they can query data. Today this requires 3-4 tool calls (search, check volumes, fetch schema, infer structure) before any real work happens. This registry flips that: agents start with structured knowledge, not a blank slate.

## What It Does

1. **Crawls** all active subgraphs from the Graph Network meta-subgraph (subgraphs indexing subgraphs)
2. **Fetches** the GraphQL schema for every deployment
3. **Classifies** each subgraph by:
   - **Domain**: DeFi, NFTs, DAOs, Gaming, Identity, Infrastructure, Social, Analytics
   - **Protocol Type**: DEX, Lending, Bridge, Staking, Options, Perpetuals, Marketplace, etc.
   - **Canonical Entities**: Maps schema types to a standard vocabulary (Pool -> `liquidity_pool`, Swap -> `trade`, etc.)
   - **Schema Family**: Groups forks/clones by schema fingerprint
4. **Scores** reliability (see [Reliability Score](#reliability-score) below)
5. **Publishes** as JSON registry + SQLite database + REST API

## Quick Start

```bash
cd python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Create .env with your Graph API key
echo "GATEWAY_API_KEY=your-key-here" > .env

# Full crawl + classify (all 15K+ subgraphs, ~11 min)
python registry.py

# Or limit to top N by signal
python registry.py --max 500

# Start API server
python server.py
```

## API Endpoints

```
GET /summary                    Registry overview and stats
GET /domains                    Domain breakdown
GET /networks                   Network breakdown
GET /families                   Schema family groups (fork/clone detection)
GET /subgraphs                  Filter subgraphs
GET /subgraphs/{id}             Full detail for one subgraph
GET /search?q=uniswap           Free-text search
GET /recommend?goal=...&chain=  Agent-optimized recommendation
```

### Example: Agent Recommendation

```bash
curl "http://localhost:3847/recommend?goal=query+DEX+trades+on+Arbitrum&chain=arbitrum-one"
```

Returns the top subgraphs matching the intent, with reliability scores and query instructions.

### Example: Filter by Entity Type

```bash
curl "http://localhost:3847/subgraphs?entity=liquidity_pool&network=base&min_reliability=0.5"
```

## Weekly Sync

```bash
# Run weekly incremental updates (only fetches new/changed subgraphs)
python scheduler.py

# One-shot incremental
python scheduler.py --once
```

## Architecture

```
Graph Network Subgraph (meta-subgraph, 140M queries/month)
    |
    v
crawler.py ---- async httpx, ID-based cursor pagination (bypasses 5K skip limit)
    |
    v
classifier.py - rule-based domain/protocol classification + schema fingerprinting
    |
    v
registry.py --- builds JSON registry + SQLite + indices
    |
    v
server.py ----- FastAPI REST API with /recommend endpoint (:3847)
    |
    v
scheduler.py -- weekly incremental sync via updatedAt filtering

MCP Server (src/index.js)
    |
    ├── stdio transport  ←── Claude Desktop / Claude Code (npx command)
    └── SSE/HTTP :3848   ←── OpenClaw / remote agents (--http flag)
```

## Output

| File | Size | Description |
|---|---|---|
| `registry.json` | ~130 MB | Full registry with all entity details |
| `registry.db` | ~8 MB | SQLite with indexed lookups |
| `sync-state.json` | <1 KB | Last sync timestamp for incremental updates |

## Classification Results (as of March 2026)

| Domain | Count | | Network | Count |
|---|---|---|---|---|
| DeFi | 11,841 | | Ethereum | 2,471 |
| NFTs | 893 | | Base | 1,845 |
| Infrastructure | 602 | | BSC | 1,664 |
| DAO | 450 | | Arbitrum | 1,442 |
| Identity | 424 | | Polygon | 1,364 |
| Analytics | 348 | | Optimism | 593 |
| Gaming | 255 | | Avalanche | 454 |
| Social | 78 | | | |

## Reliability Score

Each subgraph gets a composite reliability score (0–1) based on four on-chain signals:

| Signal | Weight | What it measures | Source |
|---|---|---|---|
| **Query Fees** | 30% | GRT fees earned from actual usage — proves real demand | Network subgraph |
| **Query Volume** | 30% | 30-day query count — recent activity level | QoS subgraph |
| **Curation Signal** | 20% | GRT tokens curated — community vote of confidence | Network subgraph |
| **Indexer Stake** | 20% | GRT staked by indexers — skin in the game | Network subgraph |

All values are log-scaled and capped at 1.0. Usage signals (fees + volume) are weighted higher at 60% because they prove real demand. A 0.5 penalty is applied if the subgraph has been denied/deprecated.

**What the scores mean:**
- **0.7–1.0**: High reliability — strong signal, active indexers, real usage (e.g. Uniswap, Aave)
- **0.3–0.7**: Moderate — some signal and usage, likely functional
- **0.0–0.3**: Low — minimal signal, may be inactive or a test deployment

## MCP Server

The registry is available as an MCP server for agent integration. It supports **dual transport** — stdio for local clients (Claude Desktop, Claude Code) and SSE/HTTP for remote agents (OpenClaw, custom agent frameworks).

It exposes 4 tools:

- **search_subgraphs** — filter by domain, network, protocol type, entity, or keyword
- **recommend_subgraph** — natural language goal to best subgraphs
- **get_subgraph_detail** — full classification for a specific subgraph
- **list_registry_stats** — registry overview (domains, networks, counts)

### Install via NPM

```bash
npx subgraph-registry-mcp
```

### Add to Claude Desktop (stdio)

```json
{
  "mcpServers": {
    "subgraph-registry": {
      "command": "npx",
      "args": ["subgraph-registry-mcp"]
    }
  }
}
```

### Add to OpenClaw / Remote Agents (SSE)

Start the server with the HTTP transport:

```bash
# Dual transport — stdio + SSE on port 3848
npx subgraph-registry-mcp --http

# SSE only (for remote/server deployments)
npx subgraph-registry-mcp --http-only

# Custom port
MCP_HTTP_PORT=4000 npx subgraph-registry-mcp --http
```

Then point your agent at the SSE endpoint:

```json
{
  "mcpServers": {
    "subgraph-registry": {
      "url": "http://localhost:3848/sse"
    }
  }
}
```

### Transport Modes

| Invocation | Transports | Use case |
|---|---|---|
| `npx subgraph-registry-mcp` | stdio | Claude Desktop, Claude Code |
| `npx subgraph-registry-mcp --http` | stdio + SSE :3848 | Dual — local + remote agents |
| `npx subgraph-registry-mcp --http-only` | SSE :3848 | OpenClaw, remote deployments |

A `/health` endpoint is available at `http://localhost:3848/health` when HTTP transport is active.

The server auto-downloads the pre-built registry (8MB SQLite) from GitHub on first run — no local build needed.

## How It Stays Current

The Graph Network subgraph indexes all subgraph deployments on-chain. The crawler queries `updatedAt_gte: lastSyncTimestamp` to fetch only what changed since the last run. Weekly syncs keep the registry fresh without full rebuilds.

## License

MIT
