# gate-info-marketoverview

## Overview

An AI Agent skill that provides **market-wide overview** (snapshot for major coins, coin rankings, platform metrics, events, macro) on Gate. Use when the user asks about the overall market, not a single coin or comparison. **5 tools are called in parallel** (all that are available); omit a call only when the tool does not exist. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Market overview** | Broad market move, representative coins, volume/sentiment | "How is the market now" / "Market overview" |
| **6-section report** | Market Summary, Sectors & Leaderboard, DeFi Overview, Recent Major Events, Macro Environment, Overall Assessment; "No data" per section if tool unavailable | Per SKILL.md Report Template |
| **Whole-market focus** | Not single-coin or multi-coin comparison | "How is the overall market" |

### Routing

| User intent | Action |
|-------------|--------|
| Market overview | Execute this skill |
| Single-coin analysis | Route to `gate-info-coinanalysis` |
| News only | Route to `gate-news-briefing` |
| DeFi deep-dive | Route to `gate-info-defianalysis` |
| Macro deep-dive | Route to `gate-info-macroimpact` |

### Architecture

- **Input**: User message asking about market as a whole.
- **Tools**: See SKILL.md — `info_marketsnapshot_get_market_snapshot`, `info_coin_get_coin_rankings`, `info_platformmetrics_get_defi_overview`, `news_events_get_latest_events`, `info_macro_get_macro_summary`. All in parallel; if a tool is missing, that report section shows "No data".
- **Output**: 6-section report. **Decision Logic** (fear_greed, dominance, gainer/loser ratio, TVL), **Error Handling**, **Safety** (read-only) — see SKILL.md.
