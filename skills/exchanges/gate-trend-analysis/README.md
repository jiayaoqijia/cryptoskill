# gate-info-trendanalysis

## Overview

An AI Agent skill that performs **single-coin trend and technical analysis** (kline, multi-timeframe signals, RSI/MACD/MA, support/resistance) on Gate. Use when the user asks for technical or trend analysis of one coin. **4 tools are called in parallel** (no optional): `info_markettrend_get_kline`, `info_markettrend_get_indicator_history`, `info_markettrend_get_technical_analysis`, `info_marketsnapshot_get_market_snapshot`. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Technical analysis** | Multi-timeframe signals, bullish/bearish/neutral, support/resistance | "Do a BTC technical analysis" / "ETH technicals" |
| **Trend analysis** | Kline, indicator history (RSI, MACD, Bollinger, MA) | "Do a SOL trend analysis" |
| **7-section report** | Current snapshot, trend assessment, indicator details, key levels, multi-timeframe summary, overall assessment, risk warnings; "No data" when tool unavailable | Per SKILL.md Report Template |

### Routing

| User intent | Action |
|-------------|--------|
| Technical / trend analysis | Execute this skill |
| Comprehensive (incl. fundamentals) | Route to `gate-info-coinanalysis` |
| Price only | Call `info_marketsnapshot_get_market_snapshot` directly |
| Raw K-line only | Call `info_markettrend_get_kline` directly |

### Architecture

- **Input**: User message with one coin symbol and technical/trend intent. **Parameter extraction**: symbol, timeframe (default 1d/4h), indicators (default all), period (kline default 90).
- **Tools**: See SKILL.md — `info_markettrend_get_kline`, `info_markettrend_get_indicator_history`, `info_markettrend_get_technical_analysis`, `info_marketsnapshot_get_market_snapshot`. All 4 in parallel.
- **Output**: 7-section report. **Judgment Logic** (RSI/MACD/MA/Bollinger/volume/divergence/funding), **Error Handling**, **Cross-Skill**, **Safety** — see SKILL.md.
