# Trading Analyzer Skill

A comprehensive multi-source trading analysis tool that combines cryptocurrency, stock, and market intelligence data into unified analysis reports with price trends, technical indicators, and sentiment analysis.

## Features

- **Cryptocurrency Analysis**: Real-time TradingView data with technical indicators
- **Stock Analysis**: Fundamental metrics, earnings data, and news sentiment from Yahoo Finance & Alpha Vantage
- **Market Screening**: Identify opportunities through volume, momentum, and pattern analysis
- **Unified Reports**: Consolidated analysis combining multiple data sources
- **Sentiment Analysis**: Latest news and market sentiment tracking

## Prerequisites

- **Node.js** 14+ or higher
- **Python 3.7+**
- **mcporter** - MCP (Model Context Protocol) tool manager

## Installation

MCPorter is a TypeScript runtime and CLI toolkit that auto-discovers MCP servers already configured in your AI editors (Cursor, Claude Desktop, Codex, Windsurf, VS Code, etc.). You have multiple installation options:

### Option 1: Run Instantly (No Installation Required)

Use `npx` to run mcporter immediately without installing globally:

```bash
# List available MCP servers
npx mcporter list

# Call a specific MCP tool
npx mcporter call tradingview-m.coin_analysis symbol=BTCUSDT exchange=BINANCE timeframe=15m
```

**Best for**: Quick testing and one-off commands

### Option 2: Install Globally (Recommended for Regular Use)

Install via your preferred package manager:

**npm:**

```bash
npm install -g mcporter
```

**pnpm:**

```bash
pnpm add -g mcporter
```

**Homebrew (macOS/Linux):**

```bash
brew tap steipete/tap
brew install steipete/tap/mcporter
```

Verify installation:

```bash
mcporter --version
mcporter list
```

### Option 3: Add to Your Project

For Node.js projects, add mcporter as a dev dependency:

```bash
pnpm add -D mcporter
# or
npm install --save-dev mcporter
```

Then use via `pnpm mcporter` or `npm exec mcporter`.

### Step 2: Configure MCP Servers

MCPorter auto-discovers MCP servers from your editors. However, if you need to manually configure the trading data providers or add them to a custom config, edit or create `config/mcporter.json`:

```json
{
  "mcpServers": {
    "tradingview-m": {
      "description": "TradingView crypto analysis",
      "command": "npx",
      "args": ["-y", "tradingview-m-mcp@latest"]
    },
    "alpha-vantage": {
      "description": "Alpha Vantage stock data",
      "command": "npx",
      "args": ["-y", "alpha-vantage-mcp@latest"],
      "env": {
        "ALPHAVANTAGE_API_KEY": "$env:ALPHAVANTAGE_API_KEY"
      }
    },
    "yahoo-finance": {
      "description": "Yahoo Finance market data",
      "command": "npx",
      "args": ["-y", "yahoo-finance-mcp@latest"]
    }
  },
  "imports": [
    "cursor",
    "claude-code",
    "claude-desktop",
    "codex",
    "windsurf",
    "opencode",
    "vscode"
  ]
}
```

Or use the interactive CLI to manage servers:

```bash
# List all discovered servers
mcporter config list

# Add a new server
mcporter config add tradingview-m --http-url "https://api.example.com/mcp"

# Add with alternate config location
mcporter config --config ~/.mcporter/mcporter.json add global-server https://api.example.com/mcp
```

### Step 3: Set Up API Keys

#### Alpha Vantage API Key (Required for Stock Analysis)

Get a free API key at: https://www.alphavantage.co/api/

**Set as environment variable:**

```bash
export ALPHAVANTAGE_API_KEY="your_api_key_here"
```

**Add to shell profile (~/.bashrc, ~/.zshrc, etc.) for persistence:**

```bash
echo 'export ALPHAVANTAGE_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Or set in mcporter config:**

```json
{
  "mcpServers": {
    "alpha-vantage": {
      "env": {
        "ALPHAVANTAGE_API_KEY": "$env:ALPHAVANTAGE_API_KEY"
      }
    }
  }
}
```

#### Other API Keys (Optional)

- **TradingView**: No API key needed for basic analysis (public data)
- **Yahoo Finance**: No API key needed (public data)

## Quick Start

### Analyze a Cryptocurrency

```bash
# Get detailed technical analysis for Bitcoin
mcporter call tradingview-m.coin_analysis symbol=BTCUSDT exchange=BINANCE timeframe=15m
```

**Output includes:**

- Current price and 24h changes
- Technical indicators (RSI, MACD, Bollinger Bands)
- Support/Resistance levels
- Trend direction and signals

### Analyze a Stock

```bash
# Get company fundamentals
mcporter call alpha-vantage.get_ticker_info symbol=AAPL

# Get latest news
mcporter call yahoo-finance.get_ticker_news symbol=AAPL count=10

# Get historical data for trend analysis
mcporter call alpha-vantage.get_price_history symbol=AAPL period=1y interval=1d

# Get earnings data
mcporter call alpha-vantage.ticker_earning symbol=AAPL period=quarterly
```

**Output includes:**

- Company metrics (P/E ratio, market cap, dividend)
- Latest news with sentiment
- Historical price trends
- Upcoming earnings dates

### Identify Market Opportunities

```bash
# Crypto: Find top gainers with bullish signals
mcporter call tradingview-m.top_gainers exchange=BINANCE timeframe=4h limit=25

# Crypto: Volume breakout detection
mcporter call tradingview-m.volume_breakout_scanner \
  exchange=KUCOIN \
  timeframe=15m \
  volume_multiplier=2.0 \
  price_change_min=3.0

# Stock: Find top performing companies
mcporter call yahoo-finance.get_top_entities \
  entity_type=performing_companies \
  sector=technology \
  count=10
```

## MCP Tools Reference

### TradingView Tools (Crypto Analysis)

| Tool                           | Purpose                                         | Parameters                                                         |
| ------------------------------ | ----------------------------------------------- | ------------------------------------------------------------------ |
| `coin_analysis`                | Detailed technical analysis for specific coin   | symbol, exchange, timeframe                                        |
| `top_gainers`                  | Best performing coins (Bollinger Band filtered) | exchange, timeframe, limit                                         |
| `top_losers`                   | Worst performing coins                          | exchange, timeframe, limit                                         |
| `smart_volume_scanner`         | Volume + RSI + price change analysis            | exchange, min_volume_ratio, min_price_change, rsi_range, limit     |
| `volume_breakout_scanner`      | Coins with volume and price breakouts           | exchange, timeframe, volume_multiplier, price_change_min, limit    |
| `advanced_candle_pattern`      | Progressive candle size patterns                | exchange, base_timeframe, pattern_length, min_size_increase, limit |
| `consecutive_candles_scan`     | Growing/shrinking consecutive candles           | exchange, timeframe, pattern_type, candle_count, min_growth, limit |
| `bollinger_scan`               | Low Bollinger Band Width (squeeze detection)    | exchange, timeframe, bbw_threshold, limit                          |
| `rating_filter`                | Filter coins by Bollinger Band rating           | exchange, timeframe, rating, limit                                 |
| `volume_confirmation_analysis` | Detailed volume analysis for specific coin      | symbol, exchange, timeframe                                        |

### Alpha Vantage Tools (Stock Data)

| Tool                | Purpose                          | Parameters               |
| ------------------- | -------------------------------- | ------------------------ |
| `get_ticker_info`   | Company fundamentals and metrics | symbol                   |
| `get_price_history` | Historical OHLC data             | symbol, period, interval |
| `ticker_earning`    | Earnings data and upcoming dates | symbol, period, date     |

### Yahoo Finance Tools (Market Intelligence)

| Tool               | Purpose                             | Parameters                 |
| ------------------ | ----------------------------------- | -------------------------- |
| `get_ticker_news`  | Recent news articles with sentiment | symbol, count              |
| `get_top_entities` | Top stocks/ETFs by sector           | entity_type, sector, count |

## Common Use Cases

### 1. Quick Crypto Analysis

1. Call `coin_analysis()` for immediate technical overview
2. Use `smart_volume_scanner()` to identify breakout opportunities
3. Check `top_gainers()` for bullish signals

**Time:** ~2-3 seconds

### 2. Fundamental Stock Research

1. Call `get_ticker_info()` for company metrics
2. Fetch `get_ticker_news()` for sentiment analysis
3. Review `get_price_history()` for trend confirmation

**Time:** ~3-5 seconds

### 3. Market Screening

1. Use crypto screeners (`top_gainers`, `top_losers`, `volume_breakout_scanner`)
2. Use stock screeners (`get_top_entities` by sector)
3. Consolidate results into unified trading strategy

**Time:** ~5-10 seconds per scan

### 4. Consolidated Report

Generate unified analysis combining:

- Price action and technical indicators
- Fundamental metrics and earnings
- Latest news and sentiment
- Technical patterns and signals

## Asset Detection Logic

The skill automatically routes assets to the correct analyzer:

1. **Crypto Assets**:
   - ends with USDT, USDC, BTC, ETH, BNB
   - Common crypto pairs (BTC, ETH, SOL, ADA, etc.)

2. **Stock Assets**:
   - 1-5 letter tickers (AAPL, TSLA, MSFT, etc.)

3. **Fallback**:
   - Attempts stock lookup first, then crypto

## Configuration

### Exchange Options (Crypto)

- `BINANCE` (default, highest liquidity)
- `KUCOIN`
- `BYBIT`

### Timeframes (Supported by most tools)

- `5m` - 5 minutes
- `15m` - 15 minutes
- `1h` - 1 hour
- `4h` - 4 hours
- `1D` - 1 day (default)
- `1W` - 1 week
- `1M` - 1 month

### RSI Ranges (Volume Scanner)

- `oversold` - RSI < 30 (potential buying)
- `overbought` - RSI > 70 (potential selling)
- `neutral` - RSI 30-70
- `any` - All RSI values

## Example Output

### Cryptocurrency Report

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
Next Support: $44,200 | Next Resistance: $46,500
```

### Stock Report

```
# Trading Analysis: AAPL

## Price Overview
Current: $278.12 (+0.80%) | Open: $277.12 | Volume: 50.4M
52-week High: $305.25 | Low: $201.50

## Company Fundamentals
P/E Ratio: 28.5 | Market Cap: $2.8T | Dividend: 0.92%
Revenue Growth: 2.3% | Profit Margin: 28.1%

## Latest News (Top 5)
1. "Apple announces AI features" - CNBC (2h ago) [Positive]
2. "Q1 earnings beat estimates" - Reuters (1d ago) [Positive]
3. "Analyst upgrades price target" - Bloomberg (1d ago) [Positive]

## Next Earnings
Date: 2026-02-28 | Expected EPS: $2.15

## Recommendation
Outlook: BULLISH | Target: $295 | Risk: Low
```

## Troubleshooting

### McPorter command not found

If you installed globally and the command isn't available:

```bash
# Try with npx (no installation needed)
npx mcporter list

# Reinstall globally
npm install -g mcporter
# or
brew reinstall steipete/tap/mcporter

# Verify installation
mcporter --version

# Check PATH if using Homebrew
echo $PATH
echo "$(brew --prefix)/bin"
```

### MCP servers not discovered

```bash
# List all available MCP servers (auto-discovers from editors)
mcporter list

# List with verbose output to see config sources
mcporter list --verbose

# Show JSON summary
mcporter list --json

# Check home config
cat ~/.mcporter/mcporter.json
```

### MCP server not connecting

```bash
# Use npx to bypass any stdio transport issues
npx mcporter call tradingview-m.coin_analysis symbol=BTCUSDT exchange=BINANCE timeframe=15m

# Test with ad-hoc HTTP URL (for server you control)
npx mcporter call --http-url "https://api.example.com/mcp" list

# Check if specific server is configured properly
mcporter config get tradingview-m
```

### Alpha Vantage API errors

- Verify API key is set: `echo $ALPHAVANTAGE_API_KEY`
- Check rate limits (5 requests/min on free tier at alphavantage.co)
- Get free API key: https://www.alphavantage.co/api/
- Ensure key is exported properly: `export ALPHAVANTAGE_API_KEY="key_here"`

### Configuration issues

```bash
# View primary config being used
mcporter config list

# Add MCP server to project config
mcporter config add myserver --http-url "https://api.example.com/mcp"

# Use custom config location
mcporter --config ~/custom/mcporter.json list

# Set default config via environment
export MCPORTER_CONFIG=~/.mcporter/mcporter.json
mcporter list
```

### Timeout or slow response

- Increase timeout: `mcporter list --log-level debug` to see what's slow
- Set environment variables:
  ```bash
  export MCPORTER_LIST_TIMEOUT=60000  # 60 seconds
  export MCPORTER_CALL_TIMEOUT=60000  # 60 seconds
  ```
- Try with a different exchange (KUCOIN instead of BINANCE for crypto)

### Data fetch errors

- Check internet connection: `ping api.example.com`
- Try using npx which has better error handling: `npx mcporter call ...`
- Verify MCP server is online (for HTTP-based servers)
- Check logs: `mcporter daemon start --log` to enable daemon logging

## Performance Notes

- **Single Coin Analysis**: 2-3 seconds
- **Market Scan (50 coins)**: 5-8 seconds
- **Stock Analysis**: 3-5 seconds
- **Consolidated Report**: 5-10 seconds
- Results are typically cached within 5-minute windows

## Supported Operating Systems

- **macOS** (Intel & Apple Silicon)
- **Linux** (Ubuntu, Debian, etc.)
- **Windows** (PowerShell, WSL, Git Bash)

## License

MIT

## Support & Documentation

- **mcporter Documentation**: https://github.com/steipete/mcporter
- **MCP Specification**: https://modelcontextprotocol.io/spec
- **TradingView API**: https://www.tradingview.com/
- **Alpha Vantage Docs**: https://www.alphavantage.co/documentation
- **Yahoo Finance**: https://finance.yahoo.com/

## Related Skills

- Trading Analyzer MCP: Cryptocurrency and stock analysis
- Portfolio Manager: Track and manage trading positions
- Market Alerts: Real-time notifications for price movements

---

**Last Updated**: February 2026  
**Version**: 1.0.0
