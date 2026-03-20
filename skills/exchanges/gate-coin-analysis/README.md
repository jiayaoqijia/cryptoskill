# gate-info-coinanalysis

## Overview

An AI Agent skill that performs **comprehensive single-coin analysis** (fundamentals, market snapshot, technicals, news, sentiment) on Gate. After intent recognition, **5 tools are called in parallel** (or 3 when no news MCP is configured), then the LLM aggregates a structured report. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Single-coin analysis** | Fundamentals + market + technicals + sentiment + events in one report | "Analyze SOL" / "Analyze BTC" |
| **Five-section report** | Fundamental overview → Market & technical (bullish/bearish/neutral) → Sentiment → Recent events → Summary & risk; **strong constraint**; "No data" when a tool is unavailable | Per SKILL.md Report Template |
| **Parallel tool calls** | info_coin_get_coin_info, info_marketsnapshot_get_market_snapshot, info_markettrend_get_technical_analysis, news_feed_search_news, news_feed_get_social_sentiment (see SKILL.md tool table for params) | 5 tools, or 3 when no news MCP |

### Routing (when NOT to use)

| Intent | Route instead |
|--------|----------------|
| Price only | Call `info_marketsnapshot_get_market_snapshot` directly |
| Multi-coin comparison | `gate-info-coincompare` |
| News only | `gate-news-briefing` |
| Technicals only | `gate-info-trendanalysis` |
| Address input | `gate-info-addresstracker` |

### Architecture

- **Input**: User message with coin symbol (e.g. SOL, BTC).
- **Tools**: See SKILL.md tool table — `info_coin_get_coin_info`, `info_marketsnapshot_get_market_snapshot`, `info_markettrend_get_technical_analysis`, `news_feed_search_news`, `news_feed_get_social_sentiment`.
- **Output**: Fixed five-section report; technical section must state bullish / bearish / neutral. **Judgment Logic** (RSI/volume/funding/fear_greed/unlock), **Error Handling** (empty → "No data"), **Cross-Skill** routing, **Safety** (read-only, no advice) — see SKILL.md.
