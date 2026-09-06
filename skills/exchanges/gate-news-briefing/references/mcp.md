---
name: gate-news-briefing-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Gate news briefing: parallel news/event/sentiment retrieval, deduplication, ranking, and degradation-safe reporting."
---

# Gate News Briefing MCP Specification

> Authoritative MCP execution document for `gate-news-briefing`.

## 1. Scope and Trigger Boundaries

In scope:
- Recent market news briefing
- Coin-specific headline and event updates
- Social sentiment snapshot integrated with event/news feeds

Out of scope:
- Event causality deep-dive -> `gate-news-eventexplain`
- Listing/delisting tracking -> `gate-news-listing`
- Multi-dimension analysis (news + technical/fundamental/risk) -> `gate-info-research`

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate-News MCP availability.
2. Probe one read tool (`news_feed_search_news`).

Fallback:
- MCP unavailable: return setup guidance and no-fabrication fallback.
- Partial tool failure: continue with available sources and mark missing sections as degraded.

## 3. Authentication

- API key not required.
- If service auth/rate-limit errors occur, return transparent message and fallback summary.

## 4. MCP Resources

No MCP Resources required.

## 5. Tool Calling Specification

| Tool | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `news_events_get_latest_events` | optional `coin`, `time_range`, `limit` | event title/time/impact/source | empty recent events |
| `news_feed_search_news` | optional `coin/topic`, sort, limit | news list, source, timestamp, importance | query too general |
| `news_feed_get_social_sentiment` | optional `coin` | sentiment polarity, volume trend, social focus | sentiment unavailable |

## 6. Execution SOP (Non-Skippable)

### 6.1 Intent gate
1. If user asks only for briefing/headlines, continue.
2. If mixed with technical/fundamental/risk requests, route to `gate-info-research`.

### 6.2 Parallel retrieval
Run these in parallel (coin-specific or global mode):
- `news_events_get_latest_events`
- `news_feed_search_news`
- `news_feed_get_social_sentiment`

### 6.3 Aggregation and dedup
1. Deduplicate by title/time/source similarity.
2. Prioritize by impact + freshness.
3. Group into categories (regulation, macro, project, exchange, ecosystem).
4. Merge sentiment as context, not as factual replacement.

### 6.4 Degradation handling
- If one source fails, keep briefing with remaining sources.
- Explicitly label degraded sections.

## 7. Output Templates

```markdown
## News Briefing ({time_range})
- Generated At: {timestamp}
- Coverage: {global_or_coin}

### Major Events
1. {event_1}
2. {event_2}

### Trending Headlines
1. {headline_1}
2. {headline_2}

### Social Sentiment
- Bias: {bullish_bearish_neutral}
- Heat: {high_medium_low}
- Notes: {key_social_signal}

### Watchlist
- {watch_item_1}
- {watch_item_2}
```

## 8. Safety and Degradation Rules

1. Distinguish factual event/news items from model summaries.
2. Do not fabricate missing headlines/events when feeds are empty or degraded.
3. Keep time range explicit (default 24h unless user requests otherwise).
4. If sentiment conflicts with news flow, report both and mark uncertainty.
5. Preserve source attribution fields whenever available.
