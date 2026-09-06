---
name: gate-info-marketoverview-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for market overview synthesis: market snapshot, macro summary, sector/defi metrics, ranking and event feed integration."
---

# Gate Info MarketOverview MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Market-wide overview and regime summary
- Sector/ranking snapshots + DeFi + macro + event overlay

Out of scope:
- Single-token deep analysis -> `gate-info-coinanalysis`
- Pure news briefing -> `gate-news-briefing`

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate-Info tools are available.
2. Probe one market overview endpoint.

Fallback:
- If partial datasets unavailable, output partial dashboard with explicit missing blocks.

## 3. Authentication

- API key not required.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

| Tool | Role |
|---|---|
| `info_marketsnapshot_get_market_overview` | core market breadth and trend context |
| `info_marketsnapshot_get_market_snapshot` | market movement snapshot |
| `info_coin_get_coin_rankings` | top movers/rankings |
| `info_platformmetrics_get_defi_overview` | DeFi TVL/activity context |
| `info_macro_get_macro_summary` | macro drivers summary |
| `news_events_get_latest_events` | event overlay for interpretation |

## 6. Execution SOP (Non-Skippable)

1. Gather all 6 feeds in parallel where possible.
2. Normalize timestamps and compare time windows.
3. Build layered overview: market breadth -> sectors -> macro -> event catalysts.
4. Mark stale/missing sources explicitly.

## 7. Output Templates

```markdown
## Market Overview
- Market Regime: {risk_on_or_off_or_mixed}
- Breadth: {gainers_vs_losers}
- Major Sectors: {sector_summary}
- DeFi: {tvl_and_activity_summary}
- Macro: {macro_summary}
- Event Overlay: {top_event_impacts}
- Watchlist: {next_risks_or_opportunities}
```

## 8. Safety and Degradation Rules

1. Separate factual metrics from interpretation.
2. Do not fabricate missing macro/defi/event data.
3. Include source freshness notes when data windows differ.
4. Avoid deterministic predictions; provide scenario-style outlook.
5. Keep output concise when source quality is low.
