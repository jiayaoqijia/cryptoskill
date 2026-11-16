---
name: crypto-funding-research
description: Research crypto venture funding with AlphaGrowth data, covering recent rounds, the most active investors, an investor's portfolio and a project's raises. Use when the user asks who is raising or investing ("latest crypto funding rounds", "who led the biggest raises this month?", "what has Paradigm invested in?", "most active crypto VCs").
compatibility: Needs the AlphaGrowth MCP server (https://alphagrowth.io/mcp) connected in Hermes as `alphagrowth`. No account or API key.
---

# Crypto funding research

Answer from the AlphaGrowth tools (`mcp__alphagrowth__*`). If they aren't available, tell the user to enable the plugin (`hermes plugins enable alphagrowth`) and start a new session, then stop.

## Pick the tool

- Latest rounds, optionally in one category: `mcp__alphagrowth__recent_funding_rounds` (newest first, with amount, type and investors; `category` takes a slug from `mcp__alphagrowth__categories`).
- Most active investors: `mcp__alphagrowth__top_investors` with `sort_by: "projects"` (deal count) or `"amount"` (dollars invested).
- One investor's profile and portfolio: find its slug in `mcp__alphagrowth__top_investors` or in a round's investor list, then `mcp__alphagrowth__investor_profile`.
- One project's raises: `mcp__alphagrowth__find_projects` for the slug, then `mcp__alphagrowth__project_funding`.

## Answer

Give each round's date, amount, type and lead investors where known, and say when an amount or valuation is undisclosed rather than estimating it. The data covers public profiles only: it has no contact details for investors or founders, so don't offer to find them. Link the AlphaGrowth source block each result carries.
