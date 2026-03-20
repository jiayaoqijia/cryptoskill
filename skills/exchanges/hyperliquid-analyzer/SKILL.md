---
name: hyperliquid-analyzer
version: 1.0.0
description: Analyze Hyperliquid market data and provide trading insights. Real-time price monitoring, trend analysis, and risk assessment.
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["curl", "jq"]
    primaryEnv: HYPERLIQUID_WALLET_ADDRESS
---

# Hyperliquid Market Analyzer

Analyze market conditions on Hyperliquid DEX and provide actionable trading insights.

## Features

- Real-time price monitoring for BTC, ETH, SOL, HYPE
- Market trend analysis (bullish/bearish/neutral)
- Risk assessment based on volatility
- Portfolio balance tracking
- Price alerts on significant movements

## Usage

### Check Market Status

```bash
curl -s https://api.hyperliquid.xyz/info -X POST \
  -H "Content-Type: application/json" \
  -d '{"type": "metaAndAssetCtxs"}' | jq '.[0:4]'
```

### Get Current Prices

```bash
curl -s https://api.hyperliquid.xyz/info -X POST \
  -H "Content-Type: application/json" \
  -d '{"type": "allMids"}' | jq '{BTC: .BTC, ETH: .ETH, SOL: .SOL}'
```

## Analysis Capabilities

1. **Trend Detection**: Identifies short-term and medium-term trends
2. **Volatility Analysis**: Measures price swings for risk assessment
3. **Support/Resistance**: Calculates key price levels
4. **Sentiment**: Aggregates market sentiment indicators

## Example Output

```
📊 Hyperliquid Market Analysis

Current Prices:
  BTC: $67,743 (+2.1% 24h)
  ETH: $1,971 (+1.5% 24h)
  SOL: $84.14 (-0.3% 24h)

Trend: BULLISH
Volatility: MEDIUM
Risk Level: 3/5

Recommendation: 
  BTC showing strong momentum. Consider long positions 
  with stop loss at $66,500.
```

## Configuration

Optional environment variables:
- `HYPERLIQUID_WALLET_ADDRESS`: Your wallet for portfolio tracking
- `HYPERLIQUID_API_KEY`: API key for authenticated requests

## Notes

- Free to use, no API key required for basic features
- Rate limit: 120 requests/minute
- Data refreshes every 5 seconds
