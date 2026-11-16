---
name: crypto-project-research
description: Research one crypto project or protocol with AlphaGrowth data, covering TVL, price, revenue, community growth, funding and upcoming unlocks. Use when the user asks about a specific project or token ("what's going on with Aave?", "is Pendle growing?", "who funded EigenLayer?", "brief me on Hyperliquid").
compatibility: Needs the AlphaGrowth MCP server (https://alphagrowth.io/mcp) connected in Hermes as `alphagrowth`. No account or API key.
---

# Crypto project research

Answer from the AlphaGrowth tools (`mcp__alphagrowth__*`). If they aren't available, tell the user to enable the plugin (`hermes plugins enable alphagrowth`) and start a new session, then stop.

## 1. Find the project

Call `mcp__alphagrowth__find_projects` with the name or symbol as `query`. Results come largest TVL first. If several plausible matches remain (a protocol and its versions, two tokens with one symbol), list them and ask which. A result flagged `is_chain: true` is a blockchain: use `mcp__alphagrowth__chain_metrics` for the chain and `mcp__alphagrowth__project_metrics` for its coin.

## 2. Gather what the question needs

Use the project's `slug` throughout. Call only what the question needs:

- Current state: `mcp__alphagrowth__project_metrics` (TVL, price, market cap, volume, revenue, users, followers, each with 1d/7d/30d changes, plus categories and chains).
- TVL trend or chain split: `mcp__alphagrowth__project_tvl_history` with `days`, and `chain_history: "yes"` for a per-chain series.
- Fees and revenue over time: `mcp__alphagrowth__fees_history` with `days`. For a version-split protocol (Uniswap), ask for a version slug (`uniswap-v3`) to get the chain split.
- Community growth: `mcp__alphagrowth__project_community`, optionally with `network` (`twitter`, `telegram`, `discord`, `reddit`).
- Funding: `mcp__alphagrowth__project_funding` (rounds, investors, total raised).
- Supply overhang: `mcp__alphagrowth__token_unlocks` with the project's token symbol as `token`.
- Forks: `mcp__alphagrowth__forks`.

## 3. Answer

Lead with what the user asked. Give numbers with their dates and changes, and link the AlphaGrowth source block each result carries. Say plainly when a metric is missing or stale rather than filling it from general knowledge. This is market data, not investment advice: don't tell the user to buy or sell.
