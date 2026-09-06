---
name: gate-info-coinanalysis-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for single-coin comprehensive analysis: fundamentals, market snapshot, technical analysis, news and social sentiment synthesis."
---

# Gate Info CoinAnalysis MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Single-coin comprehensive analysis
- Multi-source synthesis: fundamentals + market + technical + news + sentiment

Out of scope:
- Multi-coin comparison -> `gate-info-coincompare`
- Risk-only analysis -> `gate-info-riskcheck`
- Multi-dimension custom research workflows -> `gate-info-research`

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate-Info/Gate-News tool availability.
2. Probe with `info_coin_search_coins` or `info_coin_get_coin_info`.

Fallback:
- If some feeds fail, continue with available feeds and mark degraded sections.

## 3. Authentication

- API key not required.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

| Tool | Role |
|---|---|
| `info_coin_search_coins` | symbol disambiguation |
| `info_coin_get_coin_info` | fundamentals and profile |
| `info_marketsnapshot_get_market_snapshot` | latest market performance |
| `info_markettrend_get_technical_analysis` | technical indicators/signals |
| `news_feed_search_news` | recent headlines/events |
| `news_feed_get_social_sentiment` | social sentiment and discussion heat |

## 6. Execution SOP (Non-Skippable)

1. Resolve target coin (disambiguate symbol when needed).
2. Run all analysis feeds in parallel when independent.
3. Normalize timestamps/window across feeds.
4. Build structured report: fundamentals -> market -> technical -> news -> sentiment.
5. Explicitly tag missing data blocks as degraded.

## 7. Output Templates

```markdown
## {coin} Comprehensive Analysis
- Fundamentals: {project_summary}
- Market Snapshot: {price_change_volume_summary}
- Technicals: {trend_signal_summary}
- News: {top_headlines_summary}
- Social Sentiment: {sentiment_summary}
- Overall View: {balanced_conclusion}
```

## 8. Safety and Degradation Rules

1. Separate factual data from model interpretation.
2. Avoid deterministic investment advice.
3. If symbol resolution is ambiguous, block and ask user to confirm target coin.
4. Do not fabricate unavailable technical/news/sentiment data.
5. Include uncertainty notes when signals conflict across sources.
