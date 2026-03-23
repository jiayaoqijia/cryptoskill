---
name: deepblue-x402-api
description: Use when an agent needs live crypto trading signals, BTC macro intelligence, Polymarket prediction market odds, or sentiment data — paid per-call via x402 USDC micropayments on Base. No API keys needed; agents pay autonomously.
homepage: https://deepbluebase.xyz
price_range: "$0.001–$0.03 USDC per call"
network: "eip155:8453 (Base)"
wallet_address: "0x47ffc880cfF2e8F18fD9567faB5a1fBD217B5552"
tags:
  - x402
  - crypto-signals
  - polymarket
  - prediction-markets
  - sentiment
  - btc
  - trading
  - base
  - usdc
  - pay-per-call
---

# DeepBlue x402 API

AI-powered crypto intelligence for agents. Pay-per-call with USDC on Base via x402. No API keys, no subscriptions — agents pay autonomously using the x402 payment protocol.

**Base URL:** `https://api.deepbluebase.xyz`
**Facilitator:** `https://facilitator.payai.network`
**Network:** Base (eip155:8453)
**Asset:** USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)

## When to Use

- You need live 5-minute BTC/ETH/SOL/XRP trading signals with confidence scores
- You want Polymarket prediction market odds on upcoming events
- You need crypto market sentiment (Fear & Greed, whale flow, funding rates)
- You want BTC macro analysis (liquidation risk, open interest, regime detection)
- You need Polymarket performance analytics and market discovery

## Available Endpoints

| Endpoint | Price | Description |
|----------|-------|-------------|
| `GET /signals` | $0.01 | 5-min trading signals: direction (UP/DOWN), confidence (0.50–0.78), RSI, orderbook imbalance, volume regime |
| `GET /sentiment` | $0.01 | Fear & Greed index, whale flow direction, momentum regime, funding rate sign |
| `GET /market-intel` | $0.02 | BTC macro: open interest, liquidation cascade risk, funding rates, dominance, regime classification |
| `GET /polymarket` | $0.01 | Active Polymarket market discovery — slugs, prices, volume, categories |
| `GET /prediction-markets` | $0.03 | Premium: full Polymarket intelligence with odds, edge analysis, volume trends |
| `GET /crypto-sentiment` | $0.03 | Premium: combined sentiment + funding + momentum + regime analysis |
| `GET /performance` | $0.01 | DeepBlue live trading track record on Polymarket |
| `GET /price/{token}` | $0.001 | Token spot price (ETH, BTC, SOL, etc.) |

## Quick Start (Node.js)

```javascript
import { wrapFetchWithPayment } from "@x402/fetch";

const fetch = wrapFetchWithPayment(globalThis.fetch, {
  wallet: privateKeyToAccount(process.env.PRIVATE_KEY),
});

// Get BTC trading signals — pays ~$0.01 USDC automatically
const signals = await fetch("https://api.deepbluebase.xyz/signals").then(r => r.json());
console.log(signals);
// { coin: "BTC", direction: "UP", confidence: 0.67, regime: "trending_bull", ... }
```

## Quick Start (Python)

```python
from x402.client import x402_session
import os

with x402_session(private_key=os.environ["PRIVATE_KEY"]) as session:
    # Get live market sentiment — pays ~$0.01 USDC automatically
    sentiment = session.get("https://api.deepbluebase.xyz/sentiment").json()
    print(sentiment)
    # {"fear_greed": 62, "regime": "greed", "whale_flow": "accumulation", ...}

    # Get BTC macro intelligence
    intel = session.get("https://api.deepbluebase.xyz/market-intel").json()
    print(f"Liquidation risk: {intel['liquidation_risk']}")
    print(f"Regime: {intel['regime']}")
```

## Quick Start (AgentCash / mcp)

Compatible with AgentCash MCP — use the `mcp__agentcash__fetch` tool to call any endpoint:

```
mcp__agentcash__fetch("https://api.deepbluebase.xyz/signals")
```

AgentCash handles x402 payment automatically from your USDC balance.

## Response Examples

### `/signals`
```json
{
  "timestamp": "2026-03-23T04:00:00Z",
  "signals": [
    {
      "coin": "BTC",
      "direction": "UP",
      "confidence": 0.67,
      "indicators": {
        "rsi": 58.2,
        "orderbook_imbalance": 0.12,
        "volume_spike": true,
        "aggressor_ratio": 0.61
      },
      "regime": "trending_bull"
    }
  ],
  "window_seconds_remaining": 180
}
```

### `/market-intel`
```json
{
  "btc_price": 84200,
  "open_interest_usd": 18500000000,
  "funding_rate": 0.0012,
  "liquidation_risk": "moderate",
  "dominance": 62.4,
  "regime": "bull_trending",
  "fear_greed": 68,
  "recommendation": "bullish_bias"
}
```

### `/prediction-markets`
```json
{
  "markets": [
    {
      "slug": "btc-updown-5m-1742700000",
      "question": "Will BTC be higher in 5 minutes?",
      "yes_price": 0.54,
      "no_price": 0.46,
      "volume_24h": 12400,
      "closes_in_seconds": 180
    }
  ]
}
```

## Payment Flow

1. Agent calls `GET https://api.deepbluebase.xyz/signals`
2. Server responds with HTTP 402 + payment requirements (price, payTo address, network)
3. x402 client signs a USDC transfer on Base and attaches it as `X-Payment` header
4. Agent retries with payment — server verifies and returns data
5. Total round-trip: ~1-2 seconds

This is the standard x402 flow. Any x402-compatible client works: `@x402/fetch`, `@x402/axios`, AgentCash, x402-langchain, or any client from the [coinbase/x402](https://github.com/coinbase/x402) SDK.

## Use Case: Autonomous Trading Agent

```python
# Agent loop: check signals, trade on Polymarket if confident
with x402_session(private_key=PRIVATE_KEY) as session:
    signals = session.get(f"{BASE}/signals").json()
    best = max(signals["signals"], key=lambda s: s["confidence"])

    if best["confidence"] >= 0.55:
        markets = session.get(f"{BASE}/prediction-markets").json()
        # Find matching 5-min market and place order
        ...
```

## Built by DeepBlue

DeepBlue is a 5-agent autonomous system running live on Polymarket since January 2026. Our trading loop places real USDC bets using these signals every 5 minutes. We eat our own cooking.

- **Live at:** [deepbluebase.xyz](https://deepbluebase.xyz)
- **Examples:** [github.com/ERROR403agent/deepblue-x402-examples](https://github.com/ERROR403agent/deepblue-x402-examples)
- **Discord:** [discord.gg/wpSKuA57bq](https://discord.gg/wpSKuA57bq)
- **Twitter:** [@error403agent](https://x.com/error403agent)
