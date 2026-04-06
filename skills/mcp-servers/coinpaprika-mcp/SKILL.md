---
name: coinpaprika-mcp
description: "Official CoinPaprika MCP server — real-time crypto market data for 12K+ coins and 350+ exchanges. 30 tools for tickers, OHLCV, exchange data, search, and price conversion. Free tier available."
version: 1.0.0
metadata:
  openclaw:
    tags: [coinpaprika, market-data, prices, exchanges, mcp, official]
    official: true
    source: "https://github.com/coinpaprika/coinpaprika-mcp"
---

# CoinPaprika MCP Server

Official CoinPaprika MCP server providing real-time cryptocurrency market data for 12,000+ coins and 350+ exchanges. 30 tools for tickers, OHLCV candles, exchange data, search, price conversion, and contract lookup. Free tier with 10,000 requests/day, no API key required.

## Installation

```bash
# NPM (local)
npx @coinpaprika/mcp

# Claude Code
claude mcp add coinpaprika -- npx @coinpaprika/mcp

# Hosted (zero setup)
claude mcp add coinpaprika --transport http https://mcp.coinpaprika.com/streamable-http
```

## Tools (30)

### Discovery & System
- `getCapabilities` — Server capabilities and workflow patterns
- `status` — Server status and configuration
- `getGlobal` — Global market overview (market cap, volume, BTC dominance)

### Coins
- `getCoins` — List all coins
- `getCoinById` — Coin details (description, team, links)
- `getCoinEvents` — Upcoming events
- `getCoinExchanges` — Exchanges listing a coin
- `getCoinMarkets` — Markets/trading pairs

### Tickers & Prices
- `getTickers` — All tickers with price quotes
- `getTickersById` — Ticker for a specific coin
- `getCoinOHLCVLatest` — OHLCV for last full day
- `getCoinOHLCVToday` — OHLCV for today
- `priceConverter` — Convert between currencies

### Exchanges
- `getExchanges` — List all exchanges
- `getExchangeByID` — Exchange details
- `getExchangeMarkets` — Markets on a specific exchange

### Search & Resolution
- `search` — Search coins, exchanges, ICOs, people, tags
- `resolveId` — Resolve fuzzy query to canonical IDs

## Links

- **GitHub**: https://github.com/coinpaprika/coinpaprika-mcp
- **Hosted MCP**: https://mcp.coinpaprika.com
- **API Docs**: https://api.coinpaprika.com
- **npm**: https://www.npmjs.com/package/@coinpaprika/mcp
