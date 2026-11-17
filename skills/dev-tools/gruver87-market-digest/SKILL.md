---
name: market-digest
description: >-
  Build honest 1h movers, funding, and status digests from DUP Market Radar
  Telegram commands or HTTP API. Use when the user wants a market summary,
  digest, funding extremes, or bubble movers — never invent prices.
license: MIT
compatibility: Best with running dup-market-radar on localhost:8787 or Telegram bot configured.
metadata:
  author: dup-labs
  version: "0.1.6"
  product: dup-market-radar
---

# Market digest

## When to Use

- «дайджест / что выросло / funding / status рынка»

## Prefer live radar

- Telegram: `/digest`, `/funding`, `/status`, `/price`, `/bubbles`
- HTTP: `/api/health`, `/api/snapshot` (API key if required)
- MCP tools (if enabled): `radar_snapshot_summary`, `radar_health`

## Rules

1. Integer money / bps — no float profit theater.
2. If `ok=false` or stale → refuse digest claims.
3. Label source + pin if known.
4. Always: not financial advice.

## Output shape

```text
1h digest · n=<with_1h>
Gainers: …
Losers: …
Funding (if asked): …
scan_ok=… age_ms=… · not advice
```

## Refuse

- Fabricating symbols when radar is down.
- Turning digest into auto-order instructions.
