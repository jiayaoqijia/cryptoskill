# gate-news-briefing

## Overview

An AI Agent skill that aggregates **recent news and today's hot topics** from Gate-news MCP. Intent recognition → **three parallel tool calls in spec order**: `news_feed_search_news`, `news_feed_get_social_sentiment`, `news_events_get_latest_events` → LLM aggregates into a structured briefing. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **News briefing** | Major events + hot news + market sentiment in one report | "What happened recently" / "Today's hot topics" |
| **Hot topics** | Today's hot topics, important news | "Today's hot topics" / "Any big news" |
| **Structured briefing** | Major Events, Trending News (by category), Social Sentiment, Worth Watching; General vs Coin-Specific mode; **strong constraint**; de-duplicate event/news; "No data" when tool unavailable | Per SKILL.md Report Template |

### Routing

| User intent | Action |
|-------------|--------|
| General news / hot topics | Execute this skill |
| Coin-specific news | Execute this skill (Coin-Specific Mode with coin param) |
| Event explanation (why did X move) | Route to `gate-news-eventexplain` |
| Market overview | Route to `gate-info-marketoverview` |

### Architecture

- **Input**: User message asking for general news/hot topics, or coin-specific news (coin parameter).
- **Tools** (parallel): `news_events_get_latest_events`, `news_feed_search_news`, `news_feed_get_social_sentiment`. General vs Coin-Specific mode params — see SKILL.md.
- **Output**: Major Events, Trending News (by category), Social Sentiment, Worth Watching; or Coin-Specific template. De-duplicate event/news; "No data" if a tool returns empty. **De-duplication & Ranking**, **Error Handling**, **Cross-Skill**, **Safety** (source attribution, no fabrication) — see SKILL.md.
