---
name: web3-api-orchestrator
description: "Use when tasks must orchestrate crypto data and Web3 AI APIs across free/demo/paid providers with capability probes, fallback routing, and report-safe data_gaps handling."
---

# Web3 API Orchestrator

Use this as a top-level planning skill when one workflow needs multiple providers.

## Scope

- Market data providers: CMC, CoinGecko, Deribit, Coinglass, Glassnode, Nansen, Santiment, Alternative.me.
- AI providers from research JPG: Token Metrics, ChainGPT, Coinfeeds, Messari AI, ASCN, Kaito, altFINS.

## Workflow

1. Probe capabilities first (one lightweight endpoint per provider).
2. Build an `available_sources` map and `blocked_sources` map with reasons.
3. Route each metric/task to the highest-priority available source.
4. If blocked, fallback to next source and add one `data_gaps` item.
5. Never fail the entire report due to a single blocked provider.

## Output contract

- `available_sources`: list of providers with probe status.
- `blocked_sources`: provider + endpoint + raw error code/message.
- `selected_calls`: per metric/task chosen provider and endpoint.
- `data_gaps`: concise unresolved gaps.

## References

- `references/access-matrix.md`
