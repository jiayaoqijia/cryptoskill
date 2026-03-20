# gate-info-trendanalysis — Scenarios & Prompt Examples

## Scenario 1: Technical analysis (English)

**Context**: User wants technical analysis for BTC.

**Prompt Examples**:
- "Do a BTC technical analysis"
- "How is ETH technically?"
- "Do a SOL trend analysis"

**Expected Behavior**:
1. Extract symbol; call **4 tools in parallel** (no optional): `info_marketsnapshot_get_market_snapshot`, `info_markettrend_get_technical_analysis`, `info_markettrend_get_kline` (e.g. limit=90), `info_markettrend_get_indicator_history` (rsi, macd, bollinger, ma). Use default timeframe 1d (or 4h) and source spot.
2. Output **7-section report**: Current Market Snapshot, Trend Assessment, Technical Indicator Details, Key Price Levels, Multi-Timeframe Signal Summary, Overall Technical Assessment, Risk Warnings. If a tool returns empty, show "No data" for that part.

## Scenario 2: Technical / trend (Chinese)

**Context**: User asks about technicals or trend in Chinese.

**Prompt Examples**:
- "How is ETH technically"
- "Do a trend analysis for SOL"

**Expected Behavior**:
1. Extract symbol; same 4-tool parallel chain as Scenario 1.
2. Return 7-section technical/trend summary; read-only.

## Scenario 3: Default timeframe

**Context**: User does not specify timeframe.

**Prompt Examples**:
- "Technical analysis for BTC"

**Expected Behavior**:
1. Use default **timeframe 1d** (or 4h), **period 90** for kline, source `spot`.
2. Fetch snapshot, technical_analysis, kline, indicator_history; output 7-section report. Any tool empty → "No data".
