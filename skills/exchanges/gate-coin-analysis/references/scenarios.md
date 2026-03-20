# gate-info-coinanalysis — Scenarios & Prompt Examples

## Scenario 1: Single-coin full analysis (Chinese)

**Context**: User wants a full analysis of one coin (SOL).

**Prompt Examples**:
- "Analyze SOL"
- "Give me a full analysis of SOL"
- "How is SOL, analyze it"

**Expected Behavior**:
1. Extract symbol `SOL`; call in parallel: `info_coin_get_coin_info`, `info_marketsnapshot_get_market_snapshot`(symbol=SOL, timeframe=1d, source=spot), `info_markettrend_get_technical_analysis`, and if news MCP is configured: `news_feed_search_news`, `news_feed_get_social_sentiment`.
2. Aggregate into five sections: fundamental overview, market & technical (with bullish/bearish/neutral), sentiment, recent events, summary & risk. **Output MUST follow the 5-section structure**; do not omit sections; use "No data" for unavailable data.
3. Output structured report.

## Scenario 2: Single-coin full analysis (English)

**Context**: User asks to analyze BTC in English.

**Prompt Examples**:
- "Analyze SOL"
- "Help me analyze SOL"
- "Give me a full analysis of ETH"

**Expected Behavior**:
1. Extract symbol; parallel call coin info, market snapshot, technical analysis (and news tools if configured).
2. Output same five-section report; technical section must give bullish / bearish / neutral.
3. If a tool returns empty, show "No data" for that section.

## Scenario 3: No news MCP configured

**Context**: Only Gate-info is available; Gate-news is not configured.

**Prompt Examples**:
- "Analyze ETH"

**Expected Behavior**:
1. Call only the 3 Gate-info tools (info_coin_get_coin_info, info_marketsnapshot_get_market_snapshot with timeframe=1d and source=spot, info_markettrend_get_technical_analysis).
2. Sections 3 (Sentiment) and 4 (Recent events) show **"No data"**.
3. Other sections populated from tool results.

## Scenario 4: Multi-coin comparison (route away)

**Context**: User asks to compare two or more coins — do not run this skill.

**Prompt Examples**:
- "Compare BTC and ETH"
- "Compare SOL and AVAX"

**Expected Behavior**:
1. Route to **gate-info-coincompare**; do not execute this skill.
2. Do not call the 5 tools or produce a single-coin report.
