---
name: avee-mcp
description: Connect Claude Code, Claude Desktop, Cursor, VS Code, Windsurf or any MCP client to avee's remote MCP server (keyless, read-only, streamable HTTP) and pick the right avee tool — find_asset to resolve a symbol to chain and address, get_token_brief for "is this token safe", pair screeners, candles, trades, deployers, leaderboards and wallet analytics. Use when the user wants to add or configure the avee MCP server, asks which avee tool answers a question, hits an avee MCP rate limit or error, or asks about paying per call with x402 over MCP.
license: MIT
metadata:
  author: avee
  version: "0.1.0"
---

# avee MCP server

A remote Model Context Protocol server over the avee DEX index. Every tool is read-only. **No key,
no install.**

- URL: `https://mcp.preview.avee.tech/mcp` (streamable HTTP, stateless; one POST per exchange)
- Docs: https://docs.preview.avee.tech

## Connect

**Claude Code**

```bash
claude mcp add --transport http avee https://mcp.preview.avee.tech/mcp
claude mcp add --transport http --scope user avee https://mcp.preview.avee.tech/mcp   # every project
```

**Cursor**: one click with
[this install link](cursor://anysphere.cursor-deeplink/mcp/install?name=avee&config=eyJ1cmwiOiJodHRwczovL21jcC5wcmV2aWV3LmF2ZWUudGVjaC9tY3AifQ%3D%3D),
or add to `~/.cursor/mcp.json` (or `.cursor/mcp.json` in a project) the block below.

**Claude Desktop and claude.ai**: Settings → Connectors → add a custom connector with the URL.
**VS Code, Windsurf and most other clients** take the same JSON block in their MCP configuration:

```json
{ "mcpServers": { "avee": { "type": "http", "url": "https://mcp.preview.avee.tech/mcp" } } }
```

Check the connection by listing tools: the server advertises its tools and two resources
(`avee://chains`, `avee://reasons`).

## Pick the right tool

1. **Name, symbol or ticker → `find_asset` first.** Every pair, token and wallet tool needs an address
   **and** a chain. Also call it when an address arrives without a chain.
2. **"Is this safe / what is this token?" → `get_token_brief`.** One call instead of
   `get_token` + `get_pair` + `get_token_verdict`. Read the verdict carefully: `ok` means nothing is
   recorded against the token, not that it is safe; `unknown` means nobody evaluated it.
3. **Lists and rankings → `get_pair_list` or `get_token_list`** with `sort_by` and filters; use
   `only_trustable: true` to drop scam-flagged pairs.
4. **Price history → `get_candles`; recent trades → `get_order_book`; a launcher's record →
   `get_deployer_launches`; chain or venue rankings → `get_leaderboard`.**
5. **Freshness doubts → `get_latest_blocks`.** Which chains are served → `get_chains`.

The full list, with the tools that only some deployments carry and their fallbacks:
[references/tools.md](references/tools.md).

## Conventions

- `chain` takes a name from a fixed enum (`robinhood`, `hyperevm`, `ton`, `hyperliquid`, …); the enum
  is wider than what one server serves, so `get_chains` is the truth. `chain_id` is the numeric
  alternative.
- Ranked lists come back highest first; pass `order_by: "asc"` for the other end.
- Paged tools return `next_cursor`; pass it back as `cursor`.
- `limit` is capped at 500. An answer is capped at about 80 kB: an oversized page comes back with
  `"truncated": true` and how many rows were dropped. Narrow the filters or lower `limit` rather
  than paging blind.
- EVM addresses are matched in any case and come back lower-case **without** `0x`. TON, Solana and
  Hyperliquid addresses are used as given.
- Bad arguments fail the call with a message saying what to fix; correct and retry.

## Limits

Keyless callers share the same per-address budget as the REST API: 5 tool calls per second, burst
20; each tool call counts as one call, and so does a resource read. Over it, the tool returns a
rate-limit error: wait a few seconds and retry, and do not fan out parallel calls. A key
(`X-API-Key` header) only raises the budget; nothing in the tool set requires one.

## x402 on MCP (when enabled)

When x402 is enabled on the server, a keyless client past its budget may pay per call, **only if
the user has supplied a payer and agreed to pay**:

- Send the HTTP header `Accept-Payment: x402`. A call over budget then returns an `isError` result
  whose `structuredContent` is the x402 `PaymentRequired` document.
- Repeat the call with the signed payment in `_meta["x402/payment"]`. It skips the budget, and the
  receipt comes back in `_meta["x402/payment-response"]`. A tool error is never charged.

`tools/list` and calls with a valid key are never priced. Without the header, nothing changes.
