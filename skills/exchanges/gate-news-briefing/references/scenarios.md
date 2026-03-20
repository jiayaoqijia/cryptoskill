# gate-news-briefing — Scenarios & Prompt Examples

## Scenario 1: Recent events (Chinese)

**Context**: User wants to know what happened recently.

**Prompt Examples**:
- "What happened recently"
- "Today's hot topics"
- "Any big news lately"

**Expected Behavior**:
1. Intent: news briefing. Call in parallel: `news_events_get_latest_events` (time_range=24h, limit=10), `news_feed_search_news` (sort_by=importance, limit=10), `news_feed_get_social_sentiment`. De-duplicate events and news (events take priority when similar).
2. LLM aggregates into **4 parts**: Major Events, Trending News (by category), Social Sentiment, Worth Watching. **Output MUST follow SKILL.md template**; use "No data" for empty tool result; do not omit sections.
3. If a tool returns no data, show "No data" for that part.

## Scenario 2: Hot topics (English)

**Context**: User asks for today's hot topics in English.

**Prompt Examples**:
- "What happened recently"
- "Today's hot topics"
- "Any big news"
- "What's the buzz"

**Expected Behavior**:
1. Same parallel 3-tool call in spec order as Scenario 1.
2. Output structured briefing (Major Events, Trending News, Social Sentiment, Worth Watching); read-only.

## Scenario 3: Tool returns empty

**Context**: One of the three tools returns no data.

**Prompt Examples**:
- "Any big news lately"

**Expected Behavior**:
1. Call all three tools; for any empty result, fill that part with "No data".
2. Other parts populated normally; do not block the whole report.

## Scenario 4: Single-coin news (route away)

**Context**: User asks for news about a specific coin — route to coin analysis.

**Prompt Examples**:
- "Any SOL news lately"
- "Any ETH news lately"

**Expected Behavior**:
1. Route to **gate-info-coinanalysis** (or suggest user rephrase for general briefing).
2. Execute this skill in **Coin-Specific Mode** (same 3 tools with coin param); use Coin-Specific report template per SKILL.md. Do not route away — coin-specific is supported.
