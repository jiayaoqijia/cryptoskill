# Solscan Pro — AI-agent skill

> **Generated distribution mirror.** The canonical source, issues, and releases live in [https://github.com/Vo1ganin/crypto-claude-skills](https://github.com/Vo1ganin/crypto-claude-skills). Do not hand-edit generated files in this repository.

AI-agent skill and Python examples for batched Solscan Pro v2 analytics with credit controls.

- Canonical skill: [https://github.com/Vo1ganin/crypto-claude-skills/tree/main/skills/solscan](https://github.com/Vo1ganin/crypto-claude-skills/tree/main/skills/solscan)
- Collection: [https://github.com/Vo1ganin/crypto-claude-skills](https://github.com/Vo1ganin/crypto-claude-skills)
- Provenance: [`.source.json`](.source.json)

## Skill documentation

Solana wallet / token / NFT / transaction analytics via [Solscan Pro API v2](https://pro-api.solscan.io) for Claude Code.

## What it does

- Queries 50+ Solscan Pro endpoints with correct `page_size` values
- Writes async Python scripts for batch tasks (no MCP-in-a-loop)
- Uses `*/export` endpoints for bulk history (15× cheaper than pagination past ~500 rows)
- Uses `*/multi` endpoints (50× cheaper than per-item calls)
- Monitors live CU / rate limit via response headers

## When it triggers

Solana wallet addresses, SPL token mints, tx signatures, or any Solana on-chain data request — even without "Solscan" keyword.

## Files

| File | Purpose |
|------|---------|
| [`SKILL.md`](SKILL.md) | Workflow, three hard rules, tool reference |
| [`references/endpoints.md`](references/endpoints.md) | All 50+ endpoints with parameters, enum values |
| [`references/limits.md`](references/limits.md) | Tier 2 (150M CU/mo, 1000 req/min), page_size trap, response headers |
| [`references/batch-patterns.md`](references/batch-patterns.md) | MCP vs script decision tree, async template, multi/export endpoints |
| [`references/examples/fetch_defi_activities.py`](references/examples/fetch_defi_activities.py) | Async DeFi activity fetch for N wallets with resume |
| [`references/examples/batch_tx_details.py`](references/examples/batch_tx_details.py) | `transaction/detail/multi` pattern (50× savings) |
| [`references/examples/export_full_history.py`](references/examples/export_full_history.py) | Synchronous CSV export with auto-chunking on 5000-row cap |

## Key rules

1. **Scripts for batches, MCP for exploration** — any task > 10 calls → write Python script
2. **Multi-endpoints are 50× cheaper** — before looping, check if `*/multi` exists
3. **`page_size` is discrete** — only `10, 20, 30, 40, 60, 100`. `page_size=50` silently fails
4. **Export endpoints return CSV directly** (not async jobs) — max 5000 rows, chunk by time window for longer history
5. **`token/holders` max `page_size` is 40** (not 100)

## Live discovery (2026-04-24)

Tier 2 plan details confirmed via live `monitor/usage` response on user's account:
- Quota: 150,000,000 CU/month
- Rate: 1000 req/60s
- Each response includes `ratelimit-remaining`, `cu-ratelimit-remaining` headers for live monitoring

## Quick example

```
> "Fetch DeFi history for 50 wallets from wallets.txt, last 7 days"

Skill:
  → Generates async script using fetch_defi_activities.py template
  → semaphore=25, page_size=100, resume-safe JSONL output
  → Estimated throughput: 50 wallets / 170 wpm ≈ 20 seconds
  → Runs and writes to defi.jsonl
```

## Setup

Set `SOLSCAN_API_KEY` in `.env`. For MCP integration see [`INSTALL.md`](INSTALL.md).
