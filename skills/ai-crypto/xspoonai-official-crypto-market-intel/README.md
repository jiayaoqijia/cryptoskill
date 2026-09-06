# Crypto Market Intelligence

> Real-time crypto market data, token analysis, and comparison tools for Claude Code and SpoonOS.

[![Skill Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![APIs](https://img.shields.io/badge/APIs-Free%20Tier-orange)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()

## Why This Skill?

Crypto moves fast. By the time you switch tabs to CoinGecko, copy prices into a spreadsheet, and compare tokens manually, the data is already stale and the opportunity is gone.

**Crypto Market Intelligence** brings real-time market data directly into your development workflow. Ask questions in natural language, get structured data back instantly, and make informed decisions without leaving your terminal.

### The Problem

Developers building crypto applications need market data constantly:
- "Is this token liquid enough to integrate?"
- "What's the market sentiment before we launch?"
- "How does our target token compare to competitors?"
- "What's trending that we should support?"

Current solutions require context-switching to web dashboards, manual data gathering, and no easy way to pipe market data into development decisions.

### The Solution

Four focused scripts that cover the core market intelligence needs:

| Script | Purpose | Key Output |
|--------|---------|------------|
| `trending_tokens` | What's moving right now | Top tokens by volume, momentum scores |
| `token_price` | Deep dive on any token | Price, trends, moving averages, support/resistance |
| `market_overview` | Full market snapshot | Market cap, dominance, Fear & Greed, DeFi TVL |
| `token_compare` | Head-to-head token comparison | Side-by-side metrics, winner per category |

## Comparison vs Alternatives

| Feature | This Skill | CoinGecko Website | TradingView | CoinMarketCap |
|---------|-----------|-------------------|-------------|----------------|
| In-terminal access | Yes | No | No | No |
| Natural language queries | Yes | No | No | No |
| Structured JSON output | Yes | Requires scraping | Requires API key | Requires API key |
| Token comparison | Built-in | Manual | Manual | Manual |
| Momentum scoring | Built-in | No | Complex setup | No |
| Fear & Greed integration | Built-in | Separate site | No | Separate |
| DeFi TVL data | Built-in | Separate section | No | No |
| Free (no API keys) | Yes | Yes (web only) | Paid API | Paid API |
| Composable with other skills | Yes | No | No | No |
| Offline-capable | No | No | No | No |

## Quick Start

### With Claude Code

Once the skill is installed, just ask naturally:

```
> What's the crypto market looking like today?
> Price of ethereum
> Compare bitcoin and solana over 30 days
> What DeFi tokens are trending?
```

### With SpoonReactSkill

```javascript
import { SpoonReactSkill } from '@spoonos/react-skill';

function MarketDashboard() {
  return (
    <SpoonReactSkill
      skill="crypto-market-intel"
      script="market_overview"
      input={{}}
      render={({ data, loading, error }) => {
        if (loading) return <Spinner />;
        if (error) return <ErrorCard error={error} />;
        return (
          <div>
            <h2>Market Overview</h2>
            <MetricCard label="Total Market Cap" value={data.total_market_cap} />
            <MetricCard label="BTC Dominance" value={data.btc_dominance} />
            <MetricCard label="Fear & Greed" value={data.fear_greed.value} />
          </div>
        );
      }}
    />
  );
}
```

### Direct Script Execution

Each script reads JSON from stdin and writes JSON to stdout:

```bash
# Market overview
echo '{}' | python scripts/market_overview.py

# Token price
echo '{"token": "bitcoin"}' | python scripts/token_price.py

# Trending tokens
echo '{"category": "defi", "limit": 10}' | python scripts/trending_tokens.py

# Compare tokens
echo '{"token_a": "bitcoin", "token_b": "ethereum"}' | python scripts/token_compare.py
```

## API Documentation

### trending_tokens.py

Discovers trending tokens by combining trading volume rankings with price momentum signals.

**Input Schema:**

```json
{
  "category": "string (optional, default: 'all')",
  "limit": "integer (optional, default: 20, max: 100)"
}
```

**Category Options:**

| Category | Description | Filters |
|----------|-------------|---------|
| `all` | All tokens | No filter, sorted by volume |
| `defi` | DeFi protocols | Matches known DeFi token list |
| `layer1` | Layer 1 blockchains | BTC, ETH, SOL, ADA, AVAX, etc. |
| `layer2` | Layer 2 solutions | MATIC, ARB, OP, etc. |
| `meme` | Meme tokens | DOGE, SHIB, PEPE, BONK, etc. |
| `gaming` | Gaming / Metaverse | AXS, SAND, MANA, IMX, etc. |

**Output Schema:**

```json
{
  "status": "success",
  "data": {
    "trending": [
      {
        "rank": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "coingecko_id": "bitcoin",
        "current_price": 67234.00,
        "price_change_24h_pct": 2.45,
        "volume_24h": 28500000000,
        "market_cap": 1320000000000,
        "momentum_score": 8.5,
        "momentum_label": "Strong Bullish"
      }
    ],
    "category": "all",
    "count": 20,
    "timestamp": "2025-01-15T12:00:00Z"
  }
}
```

**Momentum Score Calculation:**
- Volume factor: normalized 24h volume relative to market cap
- Price momentum: weighted combination of 24h and 7d price changes
- Score range: 0-10 (0 = extremely bearish, 10 = extremely bullish)

---

### token_price.py

Detailed price analysis for a specific token with historical context and trend indicators.

**Input Schema:**

```json
{
  "token": "string (required - name, symbol, or CoinGecko ID)",
  "timeframe": "string (optional, default: '24h', options: '24h', '7d', '30d', '90d')"
}
```

**Output Schema:**

```json
{
  "status": "success",
  "data": {
    "name": "Ethereum",
    "symbol": "ETH",
    "coingecko_id": "ethereum",
    "current_price": 3456.78,
    "market_cap": 415000000000,
    "market_cap_rank": 2,
    "total_volume_24h": 15000000000,
    "circulating_supply": 120000000,
    "total_supply": null,
    "max_supply": null,
    "ath": 4878.26,
    "ath_date": "2021-11-10",
    "ath_distance_pct": -29.1,
    "atl": 0.432979,
    "atl_date": "2015-10-20",
    "price_change_24h_pct": 1.25,
    "price_change_7d_pct": 5.67,
    "price_change_30d_pct": -2.34,
    "sma_7": 3400.50,
    "sma_30": 3350.00,
    "trend": "bullish",
    "trend_reason": "Price above both 7-day and 30-day SMA with positive 7d momentum",
    "price_history_summary": {
      "timeframe": "7d",
      "high": 3520.00,
      "low": 3280.00,
      "avg": 3400.00,
      "volatility_pct": 3.5
    },
    "timestamp": "2025-01-15T12:00:00Z"
  }
}
```

---

### market_overview.py

Comprehensive crypto market snapshot combining data from multiple sources.

**Input Schema:**

```json
{
  "include_defi": "boolean (optional, default: true)"
}
```

**Output Schema:**

```json
{
  "status": "success",
  "data": {
    "total_market_cap": 2650000000000,
    "total_market_cap_change_24h_pct": 1.5,
    "total_volume_24h": 95000000000,
    "btc_dominance": 52.3,
    "eth_dominance": 16.8,
    "active_cryptocurrencies": 14500,
    "fear_greed": {
      "value": 72,
      "label": "Greed",
      "timestamp": "2025-01-15"
    },
    "top_gainers": [
      {"name": "Token A", "symbol": "TKNA", "change_24h_pct": 45.2}
    ],
    "top_losers": [
      {"name": "Token B", "symbol": "TKNB", "change_24h_pct": -22.1}
    ],
    "defi": {
      "total_tvl": 95000000000,
      "top_protocols": [
        {"name": "Lido", "tvl": 15000000000, "change_24h_pct": 0.5}
      ]
    },
    "market_sentiment": "The market is in a greed phase with moderate bullish momentum. BTC dominance above 50% suggests a risk-off environment within crypto.",
    "timestamp": "2025-01-15T12:00:00Z"
  }
}
```

---

### token_compare.py

Side-by-side comparison of two tokens across all key metrics.

**Input Schema:**

```json
{
  "token_a": "string (required - name, symbol, or CoinGecko ID)",
  "token_b": "string (required - name, symbol, or CoinGecko ID)",
  "timeframe": "string (optional, default: '24h', options: '24h', '7d', '30d', '90d')"
}
```

**Output Schema:**

```json
{
  "status": "success",
  "data": {
    "token_a": {
      "name": "Bitcoin",
      "symbol": "BTC",
      "current_price": 67234.00,
      "market_cap": 1320000000000,
      "volume_24h": 28500000000,
      "price_change_24h_pct": 2.45,
      "price_change_7d_pct": 5.10,
      "price_change_30d_pct": 12.30,
      "ath_distance_pct": -8.5,
      "circulating_supply": 19600000,
      "max_supply": 21000000
    },
    "token_b": {
      "name": "Ethereum",
      "symbol": "ETH",
      "current_price": 3456.78,
      "market_cap": 415000000000,
      "volume_24h": 15000000000,
      "price_change_24h_pct": 1.25,
      "price_change_7d_pct": 5.67,
      "price_change_30d_pct": -2.34,
      "ath_distance_pct": -29.1,
      "circulating_supply": 120000000,
      "max_supply": null
    },
    "comparison": {
      "market_cap_winner": "BTC",
      "volume_winner": "BTC",
      "24h_performance_winner": "BTC",
      "7d_performance_winner": "ETH",
      "30d_performance_winner": "BTC",
      "closer_to_ath": "BTC"
    },
    "summary": "Bitcoin leads in market cap, volume, and 30d performance. Ethereum shows stronger 7d momentum. BTC is closer to its ATH (-8.5% vs -29.1%), suggesting stronger recovery.",
    "timeframe": "24h",
    "timestamp": "2025-01-15T12:00:00Z"
  }
}
```

## Data Sources

| Source | Data Provided | Rate Limit | Auth Required |
|--------|--------------|------------|---------------|
| [CoinGecko Free API](https://www.coingecko.com/en/api) | Prices, market caps, volume, trending, historical data | 10-30 calls/min | No |
| [DeFiLlama](https://defillama.com/docs/api) | TVL, protocol rankings, DEX volumes | Generous (no stated limit) | No |
| [Alternative.me](https://alternative.me/crypto/fear-and-greed-index/) | Fear & Greed Index | Generous | No |

### Rate Limit Handling

All scripts implement exponential backoff for rate-limited responses:
1. First 429 response: wait 2 seconds, retry
2. Second 429 response: wait 4 seconds, retry
3. Third 429 response: return cached/partial data with warning

CoinGecko's free tier allows 10-30 calls per minute. Each script makes 1-3 API calls, so normal usage stays well within limits. Rapid consecutive calls (e.g., comparing 10 token pairs in a loop) may trigger rate limiting.

## Supported Categories

| Category | Example Tokens | CoinGecko Category ID |
|----------|---------------|----------------------|
| All | Any token | N/A |
| DeFi | AAVE, UNI, MKR, CRV, COMP, SNX, SUSHI, YFI | `decentralized-finance-defi` |
| Layer 1 | BTC, ETH, SOL, ADA, AVAX, DOT, ATOM, NEAR | `layer-1` |
| Layer 2 | MATIC, ARB, OP, METIS, MANTA, STRK | `layer-2` |
| Meme | DOGE, SHIB, PEPE, BONK, FLOKI, WIF | `meme-token` |
| Gaming | AXS, SAND, MANA, IMX, GALA, ENJ, ILV | `gaming` |

## Error Handling

All scripts return consistent error responses:

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Token 'foobar' not found. Did you mean 'foo-bar-token'?",
    "suggestions": ["foo-bar-token", "foobar-finance"]
  },
  "timestamp": "2025-01-15T12:00:00Z"
}
```

### Error Codes

| Code | Description | User Action |
|------|-------------|-------------|
| `INVALID_TOKEN` | Token not found on CoinGecko | Check spelling, try symbol or full name |
| `RATE_LIMITED` | Too many API requests | Wait 30 seconds, try again |
| `API_ERROR` | Upstream API returned an error | Retry; if persistent, API may be down |
| `NETWORK_ERROR` | Could not reach API endpoint | Check internet connection |
| `INVALID_INPUT` | Malformed JSON input | Verify JSON structure matches schema |
| `INVALID_TIMEFRAME` | Unsupported timeframe value | Use one of: 24h, 7d, 30d, 90d |
| `INVALID_CATEGORY` | Unsupported category value | Use one of: all, defi, layer1, layer2, meme, gaming |

## Use Cases

### 1. Pre-Integration Due Diligence
Before integrating a token into your DeFi application, check its liquidity, market cap, and trading volume to ensure it meets your thresholds.

```bash
echo '{"token": "uniswap"}' | python scripts/token_price.py
# Check: volume > $10M, market_cap > $100M, trend != "bearish"
```

### 2. Market Timing for Launches
Before launching a new feature or token, gauge overall market sentiment to choose the right timing.

```bash
echo '{}' | python scripts/market_overview.py
# Check: fear_greed > 50, market_cap_change_24h > 0
```

### 3. Competitive Analysis
Compare your project's token against direct competitors to understand relative positioning.

```bash
echo '{"token_a": "aave", "token_b": "compound", "timeframe": "30d"}' | python scripts/token_compare.py
```

### 4. Trend Monitoring Dashboard
Build automated alerts by piping trending data into your monitoring system.

```bash
echo '{"category": "defi", "limit": 10}' | python scripts/trending_tokens.py | jq '.data.trending[] | select(.momentum_score > 7)'
```

### 5. Portfolio Context
When managing a crypto portfolio, get quick context on holdings without switching to a browser.

```bash
echo '{"token": "solana", "timeframe": "30d"}' | python scripts/token_price.py
```

### 6. Market Briefings
Generate daily market briefings for your team or community by combining market overview with trending data.

```bash
echo '{"include_defi": true}' | python scripts/market_overview.py
echo '{"category": "all", "limit": 5}' | python scripts/trending_tokens.py
```

## Composability with Other Skills

Crypto Market Intelligence is designed to compose with other SpoonOS skills:

### With Smart Contract Auditor
```
1. Use token_price to identify a token of interest
2. Get the token's contract address from the output
3. Pipe the address into the smart-contract-auditor skill for security analysis
```

### With DeFi Protocol Skills
```
1. Use market_overview to assess market conditions
2. Use trending_tokens to find high-momentum DeFi tokens
3. Use defi-protocols skill to interact with the protocol (swap, lend, stake)
```

### With On-Chain Analysis
```
1. Use token_compare to identify outperforming tokens
2. Use onchain-analysis skill to examine wallet flows and whale activity
3. Correlate on-chain data with market data for deeper insights
```

### With Wallet Skills
```
1. Use token_price to check current prices of tokens in your wallet
2. Use market_overview to decide on rebalancing
3. Use wallet skill to execute transactions based on market intelligence
```

## Technical Architecture

```
market-intelligence/
├── SKILL.md              # Skill definition with YAML frontmatter
├── README.md             # This file
└── scripts/
    ├── trending_tokens.py    # Trending token discovery
    ├── token_price.py        # Single token deep dive
    ├── market_overview.py    # Full market snapshot
    └── token_compare.py      # Head-to-head comparison
```

### Design Principles

1. **Self-contained scripts** - Each script runs independently with no shared imports
2. **JSON in, JSON out** - Standard interface for composability
3. **Free APIs only** - No API keys required, zero configuration
4. **Graceful degradation** - If one data source fails, return partial data with warnings
5. **Rate limit awareness** - Built-in retry logic with exponential backoff
6. **Input flexibility** - Accept token names, symbols, or CoinGecko IDs

### Dependencies

- Python 3.8+ (standard library only)
- `urllib.request` for HTTP calls (no `requests` package needed)
- `json` for data serialization
- No external packages required

## Limitations

- **Data delay**: Free API data may be delayed by 1-5 minutes vs real-time feeds
- **Rate limits**: CoinGecko free tier limits to 10-30 calls/minute
- **Token coverage**: Only tokens listed on CoinGecko are supported
- **Historical depth**: Free tier limits historical data granularity
- **No trading**: This skill is read-only; it cannot execute trades
- **No alerts**: Point-in-time queries only; no persistent monitoring

## License

MIT License. See repository root for details.

## Contributing

Contributions welcome! Please follow the SpoonOS skill contribution guidelines:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a PR to the appropriate category directory
