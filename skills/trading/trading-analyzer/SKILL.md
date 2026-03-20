---
name: trading-analyzer
description: Multi-source trading analyzer (`/drunk-trading-analyzer`) combining crypto data (TradingView), stock data (Alpha Vantage), and market intelligence (Yahoo Finance) into unified analysis reports with price trends, technical indicators, and sentiment analysis.
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "os": ["darwin", "linux", "win32"],
        "mcp_servers":
          ["tradingview-mcp", "alphavantage", "yahoo-finance-server"],
        "description": "Uses MCP (Model Context Protocol) tools auto-discovered by mcporter for seamless integration with TradingView, Alpha Vantage, and Yahoo Finance APIs",
      },
  }
---

# Trading Analyzer Skill

Multi-source market analysis combining cryptocurrency and stock data with AI-powered insights.

## Quick Start

### Analyze Cryptocurrency

```bash
# List available TradingView tools
mcporter list tradingview-mcp

# Analyze a specific coin
mcporter call tradingview-mcp.coin_analysis symbol=BTCUSDT exchange=BINANCE timeframe=15m

# Find bullish coins
mcporter call tradingview-mcp.top_gainers exchange=BINANCE timeframe=4h limit=25

# Detect volume breakouts
mcporter call tradingview-mcp.volume_breakout_scanner exchange=KUCOIN timeframe=15m volume_multiplier=2.0
```

### Analyze Stock

```bash
# List available Alpha Vantage and Yahoo Finance tools
mcporter list alphavantage
mcporter list yahoo-finance-server

# Get company fundamentals
mcporter call alphavantage.get_ticker_info symbol=AAPL

# Fetch latest news
mcporter call yahoo-finance-server.get_ticker_news symbol=AAPL count=10

# Get stock price history
mcporter call alphavantage.get_price_history symbol=AAPL period=1y interval=1d

# Get earnings data
mcporter call alphavantage.ticker_earning symbol=AAPL period=quarterly
```

## Common Use Cases

### 1. Quick Crypto Analysis

```bash
# 1. Get immediate technical overview
mcporter call tradingview-mcp.coin_analysis symbol=BTCUSDT

# 2. Identify breakout opportunities
mcporter call tradingview-mcp.smart_volume_scanner \
  exchange=BINANCE min_volume_ratio=2.0 min_price_change=2.0

# 3. Find bullish signals
mcporter call tradingview-mcp.top_gainers exchange=BINANCE timeframe=4h
```

### 2. Fundamental Stock Research

```bash
# 1. Get company metrics
mcporter call alphavantage.get_ticker_info symbol=TSLA

# 2. Get sentiment from latest news
mcporter call yahoo-finance-server.get_ticker_news symbol=TSLA count=5

# 3. Confirm trend with historical data
mcporter call alphavantage.get_price_history symbol=TSLA period=1y interval=1d
```

### 3. Market Screening

Use crypto screeners to identify opportunities:

```bash
# Top performers
mcporter call tradingview-mcp.top_gainers exchange=BINANCE timeframe=1h limit=50

# Volume + momentum
mcporter call tradingview-mcp.smart_volume_scanner \
  exchange=KUCOIN min_volume_ratio=3.0 rsi_range=oversold

# Top stock sectors
mcporter call yahoo-finance-server.get_top_entities \
  entity_type=performing_companies sector=technology count=10
```

### 4. Consolidated Report

Combine multiple data sources for comprehensive analysis - use scripting or agent calls to orchestrate these tool calls together.

## MCP Tools Reference

### TradingView (Crypto Analysis)

| Tool                       | Purpose                                                  |
| -------------------------- | -------------------------------------------------------- |
| `coin_analysis`            | Detailed analysis on specific coin (indicators, metrics) |
| `smart_volume_scanner`     | Volume + RSI + price change combination scan             |
| `volume_breakout_scanner`  | Coins with volume and price breakouts                    |
| `top_gainers`              | Best performing coins (Bollinger Band filtered)          |
| `top_losers`               | Worst performing coins                                   |
| `advanced_candle_pattern`  | Progressive candle size patterns across timeframes       |
| `consecutive_candles_scan` | Growing/shrinking consecutive candles                    |

### Alpha Vantage (Stock Data)

| Tool                | Purpose                                   |
| ------------------- | ----------------------------------------- |
| `get_ticker_info`   | Company fundamentals, metrics, governance |
| `get_price_history` | Historical OHLC data for trend analysis   |
| `ticker_earning`    | Earnings data and upcoming dates          |

### Yahoo Finance (Market Intelligence)

| Tool               | Purpose                             |
| ------------------ | ----------------------------------- |
| `get_ticker_news`  | Recent news articles with sentiment |
| `get-top-entities` | Top stocks/ETFs by sector           |

## Configuration

### Exchange Options (Crypto)

- `BINANCE` (default highest liquidity)
- `KUCOIN`
- `BYBIT`

### Timeframes (Crypto)

- `5m`, `15m`, `1h`, `4h`, `1D` (default), `1W`, `1M`

### Output Formats

- `markdown` (default) - Formatted report
- `json` - Raw data structure

## Asset Detection

Automatically routes to correct analyzer:

1. **Crypto**: Ends with USDT, USDC, BTC, ETH, BNB OR common crypto pairs (BTC, ETH, SOL, ADA)
2. **Stock**: 1-5 letter tickers (AAPL, TSLA, MSFT)
3. **Fallback**: Attempts stock lookup first, then crypto

## Example Reports

### Crypto Report Structure

```
# Trading Analysis: BTCUSDT

## Price Overview
Current: $45,200 (-2.3%) | 24h High: $46,100 | Low: $44,800
Volume: $28.5B | Change: -$1,050

## Technical Analysis (1D)
Trend: Bearish | RSI: 35 (Oversold) | MACD: Negative
Bollinger Bands: Below MA | Support: $44,200 | Resistance: $46,500

## Market Data
Exchange: BINANCE | Sentiment: Neutral-Bearish

## Recommendation
Signal: HOLD | Risk: Moderate
```

### Stock Report Structure

```
# Trading Analysis: AAPL

## Price Overview
Current: $278.12 (+0.80%) | Open: $277.12 | Volume: 50.4M
52-week High: $305.25 | Low: $201.50

## Company Fundamentals
P/E Ratio: 28.5 | Market Cap: $2.8T | Dividend: 0.92%
Revenue Growth: 2.3% | Profit Margin: 28.1%

## Latest News (5 articles)
1. "Apple announces AI features" - CNBC (2h ago) [Positive]
2. "Q1 earnings beat estimates" - Reuters (1d ago) [Positive]

## Recommendation
Outlook: BULLISH | Target: $295 | Risk: Low
```

## Error Handling

- Graceful fallback if MCP server unavailable
- Partial reports if single data source fails
- Caching support for repeated queries
- Clear error messages with retry guidance

## Performance Notes

- Cache queries within 5-minute windows
- Parallel data fetching for multi-source reports
- Typical analysis time: 2-5 seconds per asset

## Troubleshooting

```bash
# Verify MCP servers running
echo "Check .vscode/mcp.json configuration"

# Debug API keys
echo "Ensure Alpha Vantage API key is set"

# Test connectivity
python3 -c "import requests; print(requests.__version__)"
```

## Extensions

To add new data sources:

1. Create new analyzer in `analyzers/` directory
2. Implement `analyze(symbol, options)` interface
3. Register in routing logic
4. Update tools reference

## License

MIT
