# gate-info-marketoverview — Scenarios & Prompt Examples

## Scenario 1: Current market status (English)

**Context**: User wants to know how the market is doing overall.

**Prompt Examples**:
- "How is the market now"
- "Market overview"
- "Broad market"

**Expected Behavior**:
1. Call in parallel (per SKILL): `info_marketsnapshot_get_market_snapshot` (BTC, ETH; timeframe=1d/4h, source=spot), `info_coin_get_coin_rankings` (gainers, optionally losers), `info_platformmetrics_get_defi_overview`, `news_events_get_latest_events` (time_range=24h), `info_macro_get_macro_summary`. If a tool is not available, omit that call and mark the section "No data".
2. Output **6-section report**: Market Summary, Sectors & Leaderboard, DeFi Overview, Recent Major Events, Macro Environment, Overall Assessment.
3. When user asks about a single coin (e.g. "How is BTC"), route to **gate-info-coinanalysis** instead.

## Scenario 2: Market overview (Chinese)

**Context**: User asks for overall market view in Chinese.

**Prompt Examples**:
- "Market overview"
- "How is the overall market"
- "How is the broad market"

**Expected Behavior**:
1. Same 5-tool parallel chain as Scenario 1; if a tool returns empty, that section shows "No data".
2. Return 6-section report in natural language; read-only.

## Scenario 3: Unspecified period

**Context**: User does not specify time range.

**Prompt Examples**:
- "Give me a market overview"

**Expected Behavior**:
1. Use default timeframe `1d` or `4h`, source `spot`.
2. Fetch snapshot, rankings, platformmetrics, events, macro (as available); output 6-section overview.
3. Any tool empty → that section "No data".
