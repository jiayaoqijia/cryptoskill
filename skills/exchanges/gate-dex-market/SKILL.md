---
name: gate-dex-market
version: "2026.3.24-1"
updated: "2026-03-24"
description: "Gate DEX read-only market data skill. Use when the user asks for prices, K-lines, rankings, holders, or liquidity without signing a tx. Triggers on 'DEX price', 'token K-line', 'holder analysis'. Do NOT use for swaps or wallet auth — use gate-dex-trade or gate-dex-wallet."
---

# Gate DEX Market

> **Pure Routing Layer** — READ-ONLY data queries only. Never executes transactions. All specifications in `references/`.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)

**Trigger Scenarios**: Use when the user wants to **look up or analyze** market data without executing any transaction:
- Price lookup: "what is the price of ETH", "check SOL price", "price of 0x1234..."
- Charts: "show K-line", "candlestick chart", "price trend"
- Rankings: "top gainers", "trending tokens", "token rankings"
- Security: "is this token safe", "security audit", "honeypot check", "risk analysis"
- Discovery: "new tokens", "newly listed", "holder analysis", "whale tracking"
- Volume: "trading volume", "buy-sell pressure", "liquidity events"


---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate-Dex | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- dex_market_get_kline
- dex_token_get_coin_info
- dex_token_ranking
- dex_token_get_risk_info
- dex_token_list_swap_tokens
- dex_token_list_cross_chain_bridge_tokens

### Authentication
- API Key Required: No for MCP market queries
- OAuth `mcp_token` Required: No for MCP market queries
- Note: This skill is read-only. In MCP mode, market-data tools can be called without authentication. OpenAPI mode has its own credential model and is only used when the user explicitly requests it.

### Installation Check
- Required: Gate-Dex
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Project convention — MCP only

No OpenAPI unless user explicitly asks. MCP setup: see `gate-dex-trade/references/setup.md`.

---

**NOT this skill** (common misroutes):
- "quote for swapping X to Y" → `gate-dex-trade` (swap execution)
- "check my balance" → `gate-dex-wallet` (account query)
- "buy ETH" / "sell USDT" → `gate-dex-trade` (transaction execution)

---

## Routing Flow

```text
User triggers market data query
  |
Step 1: OpenAPI only if user explicitly asks. Else MCP only.
Step 2: MCP discovery → success = MCP mode; fail = MCP setup guide (no OpenAPI fallback).
```

---

## Feature Matrix

| Feature | MCP | OpenAPI | Notes |
|---------|-----|---------|-------|
| K-line / Candlestick | Yes | Yes | |
| Token basic info | Yes | Yes | |
| Token rankings | Yes | Yes | |
| Security risk audit | Yes | Yes | |
| Tradable token list | Yes | Yes | |
| Cross-chain bridge tokens | Yes | No | MCP only |
| Holder analysis (Top N) | No | Yes | OpenAPI only |
| New token discovery | No | Yes | OpenAPI only |
| Liquidity events (Rug Pull) | No | Yes | OpenAPI only |
| Volume stats (multi-period) | No | Yes | OpenAPI only |

---

## Mode Dispatch

### MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), execute according to its complete workflow.

Includes: connection detection, 6 market data tools (dex_market_get_kline, dex_token_get_coin_info, dex_token_ranking, dex_token_get_risk_info, dex_token_list_swap_tokens, dex_token_list_cross_chain_bridge_tokens), no authentication required for market queries.

### OpenAPI Mode (Progressive Loading)

Explicit user request only. Load files progressively:

1. **Always load first**: [`references/openapi/_shared.md`](./references/openapi/_shared.md) — env detection, credentials, API call method (via helper script)
2. **Then load based on query type**:

| Query Type | Load File |
|-----------|-----------|
| Token info, rankings, new tokens, security, holders | [`openapi/token-data.md`](./references/openapi/token-data.md) |
| Volume stats, K-line, liquidity events | [`openapi/market-data.md`](./references/openapi/market-data.md) |

> Legacy monolithic file preserved at [`references/openapi.md`](./references/openapi.md) for backward compatibility.

---

## Supported Chains

Actual supported chains are determined by runtime API/Resource returns:
- **MCP Mode**: determined by MCP tool responses for the given `chain` argument
- **OpenAPI Mode**: chain parameter in request

Common chains: eth, bsc, polygon, arbitrum, optimism, avax, base, sol.

---

## Security Rules

1. **Data objectivity**: Present prices and rankings objectively, no investment advice
2. **Risk warnings**: Clearly remind users to judge investment risks themselves when showing security audits
3. **Credential security**: Follow §3 of [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) for auth/credential handling
4. **Read-only**: All operations are data queries, no on-chain write operations
