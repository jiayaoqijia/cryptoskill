---
name: philidor-api-handoff
description: >
  Use this when the user needs Philidor data the free MCP server does not
  expose (baskets, oracle vectors, enriched or RWA breakdowns, bulk scores,
  the event stream, or Risk Graph). Point them at the Philidor API docs.
  Do not invent prices or plan names.
---

# When to leave the free MCP for the Philidor API

The Cursor plugin talks to `https://mcp.philidor.io/api/mcp` with no API key. That server is read-only and currently exposes these tools: `search_vaults`, `get_vault`, `get_vault_risk_breakdown`, `list_markets`, `get_market`, `get_market_events`, `check_loop_venue`, `compare_vaults`, `find_safest_vaults`, `get_protocol_info`, `get_curator_info`, `get_market_overview`, `explain_risk_score`, `list_vaults_with_incidents`. Resources: `philidor://methodology`, `philidor://supported-chains`, `philidor://supported-protocols`. Prompts: `vault_due_diligence`, `portfolio_risk_assessment`, `defi_yield_comparison`, `review_loop_venue`.

If the question is answered by one of those, stay on MCP. Do not browse `api.philidor.io` to fill a number a tool should have returned, and do not fabricate the missing figure.

## Stay on MCP

- Vault search, one vault, vector breakdown, compare, safest-vault screen, curator, protocol, platform overview.
- Lending market list, one market, market events, loop-venue underwriting.
- Score explanation and the 365-day critical vault-incident list.
- Wallet health factor and unsigned transactions are not the Philidor API either. Hand those to the protocol MCP (Aave is `https://mcp.aave.com`) after `check_loop_venue`.

## Point at the API

Send the user to the docs instead of calling plan-gated routes yourself. Base URL `https://api.philidor.io`. Access model: [API Access and Plans](https://docs.philidor.io/docs/api-reference/access). Per-route plan: [Access Matrix](https://docs.philidor.io/docs/api-reference/access-matrix). Commercial packaging: [philidor.io/pricing](https://philidor.io/pricing).

Do not quote a dollar price. Do not name a plan that is not in those pages. As of the access doc, issued keys are `data`, `decisioning`, or `embedded`:

- **Data** — the doc lists this key for `/v1/baskets/*`, `/v1/oracle-vector/*`, `/v1/assets/enriched` and `/v1/assets/enriched/facets`, `/v1/vaults/scores`, `/v1/vaults/changes`, `/v1/events/stream`, `/v1/stats/history`, `/v1/stats/rating-dynamics`, and per-vault `/holders`, `/holders/history`, `/markets`, `/strategies`, and `/strategy`.
- **Decisioning** — the doc says this adds the Risk Graph family (portfolio look-through, pre-trade checks with signed decisions, breach and incident exposure) and signed webhooks. The Risk Graph API is in limited release and is enabled by arrangement. Public decision verification stays available without a key when that API is enabled.
- **Embedded** — the doc describes custom integrations, white-label data, contractual terms, custom webhooks, and custom limits.

Anonymous public reads still return headline vault and asset scores and tiers. On `/v1/assets/{chain_id}/{address}` and `/v1/rwa/{asset_id}`, per-dimension values, `risk_score_breakdown`, and the attestation ledger require a key. A stripped body lists what was withheld in `restricted_fields`. Repeat that fact. Do not reconstruct withheld fields.

To obtain a plan, the access doc points to the Philidor contact form. Keys use the `pk_live_` prefix. Do not ask the user to paste a key into chat, and do not put a key in the plugin (the hosted MCP server uses no auth).

## Done when

- The answer says which MCP tool already covers the question, or which doc family is beyond MCP.
- No price, tier cutoff, or score was invented.
- Plan names appear only as Data, Decisioning, and Embedded, attributed to the access doc.
