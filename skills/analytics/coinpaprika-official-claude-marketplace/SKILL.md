---
name: coinpaprika-official-claude-marketplace
description: "Official Claude Code plugins for **CoinPaprika** and **DexPaprika** — free crypto market data and DeFi analytics."
---

# coinpaprika-official-claude-marketplace

_Source: [github.com/coinpaprika/claude-marketplace](https://github.com/coinpaprika/claude-marketplace). The body below is the upstream README.md captured at the time of registration._

---

# CoinPaprika Claude Marketplace

Official Claude Code plugins for **CoinPaprika** and **DexPaprika** — free crypto market data and DeFi analytics.

- **CoinPaprika**: 12,000+ coins, 350+ exchanges, 29 MCP tools
- **DexPaprika**: 34+ blockchains, 30M+ pools, 14 MCP tools

Both APIs are free with no API key required.

## Quick Start

### Option 1: Auto-Install (Recommended)
```bash
git clone https://github.com/coinpaprika/claude-marketplace.git
cd claude-marketplace
# Open in Claude Code — plugins install automatically via .claude/settings.json
```

### Option 2: Plugin Marketplace
```bash
# In Claude Code
/plugin marketplace add coinpaprika/claude-marketplace
/plugin install coinpaprika@coinpaprika-plugins
/plugin install dexpaprika@coinpaprika-plugins
```

## What You Get

### CoinPaprika Plugin

**29 MCP tools** for centralized exchange market data:
- Prices, tickers, market caps for 12,000+ coins
- OHLCV candlestick data (historical, latest, today)
- Exchange and market data for 350+ exchanges
- Contract address lookups across chains
- Tags, categories, search, price converter
- People profiles, ID mappings, changelog

**1 agent** (`@crypto-analyst`): Market analysis, price trends, risk assessment

**1 skill** (`crypto-market-search`): Search, discover, and analyze coins

**Free tier**: 20,000 calls/month, no API key needed. Pro tier via `api-pro.coinpaprika.com`.

### DexPaprika Plugin

**14 MCP tools** for decentralized exchange data:
- Token prices and details across 34+ blockchains
- Liquidity pool discovery, filtering, and details
- OHLCV charts for any pool
- Pool transactions and trading activity
- Batch price lookups (up to 10 tokens)
- Cross-chain search for tokens, pools, and DEXes

**1 agent** (`@defi-data-analyst`): DeFi security analysis, honeypot detection, scam identification

**4 skills**: Token Security Analyzer, Technical Analyzer, Batch Token Price Lookup, Trending Pools Analyzer

**Free tier**: 10,000 requests/day, no API key needed.

## Quick Test

```
# CoinPaprika
Using CoinPaprika, show me Bitcoin price and market cap

# DexPaprika
Using DexPaprika, show top 10 pools on Base by 24h volume

# Security analysis (auto-activates)
Is this token safe? 0x1234567890abcdef on Ethereum
```

## Repository Structure

```
claude-marketplace/
├── .claude/
│   └── settings.json                       # Auto-install config
├── .claude-plugin/
│   └── marketplace.json                    # Marketplace definition (2 plugins)
├── plugins/
│   ├── coinpaprika-claude-plugin/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json                 # Plugin manifest (29 MCP tools)
│   │   ├── .mcp-hosted.json                # MCP server connection
│   │   ├── agents/
│   │   │   └── crypto-analyst.md           # Market analyst agent
│   │   ├── skills/
│   │   │   └── crypto-market-search/
│   │   │       └── SKILL.md                # Coin search & analysis skill
│   │   └── README.md
│   └── dexpaprika-claude-plugin/
│       ├── .claude-plugin/
│       │   └── plugin.json                 # Plugin manifest (14 MCP tools)
│       ├── agents/
│       │   └── defi-data-analyst.md        # DeFi security agent
│       ├── skills/
│       │   ├── token-security-analyzer/
│       │   │   └── SKILL.md                # Honeypot/rug pull detection
│       │   ├── technical-analyzer/
│       │   │   └── SKILL.md                # OHLCV chart analysis
│       │   ├── batch-token-price-lookup/
│       │   │   └── SKILL.md                # Multi-token price checks
│       │   └── trending-pools-analyzer/
│       │       └── SKILL.md                # Top pools by volume
│       └── README.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Verification

```bash
# Check MCP servers are connected
claude mcp list
# Should show: coinpaprika (SSE) and dexpaprika (SSE)

# Test CoinPaprika
Using CoinPaprika, what's the price of Ethereum?

# Test DexPaprika
Using DexPaprika, show me trending pools on Solana
```

## API Rate Limits

| API | Free Tier | Auth Required |
|-----|-----------|---------------|
| CoinPaprika | 20,000 calls/month | No |
| DexPaprika | 10,000 requests/day | No |

Global rate limit: 10 requests/second per IP.

## Resources

- [CoinPaprika Docs](https://docs.coinpaprika.com) | [DexPaprika Docs](https://docs.dexpaprika.com)
- [CoinPaprika API](https://api.coinpaprika.com) | [DexPaprika API](https://api.dexpaprika.com)
- [AI Agents Showcase](https://agents.dexpaprika.com)
- [LLM-readable docs](https://docs.coinpaprika.com/llms-full.txt)
- [Streaming API](https://streaming.dexpaprika.com) (real-time SSE, ~1s updates)
- [CoinPaprika CLI](https://github.com/coinpaprika/coinpaprika-cli) | [DexPaprika CLI](https://github.com/coinpaprika/dexpaprika-cli)

**SDKs**: [Go](https://github.com/coinpaprika/coinpaprika-api-go-client) | [Python](https://github.com/coinpaprika/coinpaprika-api-python-client) | [Node.js](https://github.com/coinpaprika/coinpaprika-api-nodejs-client) | [PHP](https://github.com/coinpaprika/coinpaprika-api-php-client) | [Swift](https://github.com/coinpaprika/coinpaprika-api-swift-client) | [Kotlin](https://github.com/coinpaprika/coinpaprika-api-kotlin-client)

## Support

- [GitHub Issues](https://github.com/coinpaprika/claude-marketplace/issues)
- support@coinpaprika.com

## License

MIT — see [LICENSE](LICENSE)
