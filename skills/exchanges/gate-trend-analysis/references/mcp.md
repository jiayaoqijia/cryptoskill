---
name: gate-info-trendanalysis-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for trend analysis: kline, indicator history, technical snapshots, and multi-timeframe synthesis."
---

# Gate Info TrendAnalysis MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Technical trend analysis for a target coin/pair
- Multi-timeframe signal interpretation
- Indicator/Kline driven summaries

Out of scope:
- Full fundamental/news comprehensive reports
- Multi-coin comparative analysis

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate-Info trend tools are available.
2. Probe with technical analysis or kline endpoint.

Fallback:
- If indicator history unavailable, use kline + technical snapshot only.

## 3. Authentication

- API key not required.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

| Tool | Role |
|---|---|
| `info_marketsnapshot_get_market_snapshot` | current price/market context |
| `info_markettrend_get_kline` | OHLCV series by timeframe |
| `info_markettrend_get_indicator_history` | historical indicator series |
| `info_markettrend_get_technical_analysis` | consolidated technical signal summary |

## 6. Execution SOP (Non-Skippable)

1. Resolve symbol and requested timeframe(s).
2. Pull current snapshot + kline + technical signals.
3. Pull indicator history when requested/available.
4. Build trend narrative with explicit timeframe tags.

## 7. Output Templates

```markdown
## Trend Analysis ({symbol})
- Current Snapshot: {price_context}
- Short-term Trend: {short_tf_signal}
- Mid-term Trend: {mid_tf_signal}
- Key Indicators: {rsi_macd_ma_summary}
- Critical Levels: {support_resistance}
- Signal Confidence: {confidence_note}
```

## 8. Safety and Degradation Rules

1. Always label the timeframe of each conclusion.
2. Avoid overconfidence when timeframe signals conflict.
3. If indicator data is missing, disclose and downgrade confidence.
4. Separate indicator facts from interpretation.
5. No direct trade execution recommendations in this skill.
