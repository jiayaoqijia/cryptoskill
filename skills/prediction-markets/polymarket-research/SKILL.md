---
name: polymarket-research
description: Use when researching Polymarket prediction markets, checking odds on events, finding trending markets, analyzing 5-minute crypto prediction markets (BTC/ETH), comparing market sentiment, or helping users decide what to bet on. Triggers on polymarket, prediction market, odds, betting, 5-minute markets, event probability.
metadata:
  author: DeepBlue
  version: "1.0.0"
  openclaw:
    emoji: "🔮"
    homepage: "https://deepbluebase.xyz"
    tags:
      - prediction-markets
      - polymarket
      - research
      - odds
      - 5-minute-markets
      - crypto-predictions
      - sentiment
      - trading-signals
---

# Polymarket Research Assistant

Research prediction markets, analyze odds, and find opportunities on Polymarket — no setup required.

## Quick Start

All commands use free public APIs. No API keys, no CLI install, no wallet needed.

### Search Markets

```bash
# Find markets by topic
curl -s "https://gamma-api.polymarket.com/markets?limit=10&active=true&closed=false&order=volume&ascending=false" | python3 -c "
import sys, json
markets = json.load(sys.stdin)
for m in markets:
    prices = json.loads(m.get('outcomePrices', '[]'))
    yes = float(prices[0]) if prices else 0
    print(f\"{yes*100:.0f}% YES | \${float(m.get('volume',0)):,.0f} vol | {m['question'][:80]}\")
"
```

### Search by Keyword

```bash
# Search for specific topics
curl -s "https://gamma-api.polymarket.com/markets?limit=10&active=true&closed=false&tag=crypto" | python3 -c "
import sys, json
for m in json.load(sys.stdin):
    prices = json.loads(m.get('outcomePrices', '[]'))
    yes = float(prices[0]) if prices else 0
    print(f\"{yes*100:.0f}% YES | \${float(m.get('volume',0)):,.0f} vol | {m['question'][:80]}\")
"
```

Replace `tag=crypto` with any tag: `politics`, `sports`, `pop-culture`, `crypto`, `business`, `science`, etc.

### Get Market Details

```bash
# Get full details for a specific market by slug
curl -s "https://gamma-api.polymarket.com/markets?slug=will-btc-hit-100k" | python3 -c "
import sys, json
m = json.load(sys.stdin)[0]
prices = json.loads(m.get('outcomePrices', '[]'))
print(f\"Question: {m['question']}\")
print(f\"YES: {float(prices[0])*100:.1f}% | NO: {float(prices[1])*100:.1f}%\")
print(f\"Volume: \${float(m.get('volume',0)):,.0f}\")
print(f\"Liquidity: \${float(m.get('liquidityNum',0)):,.0f}\")
print(f\"End: {m.get('endDate','TBD')}\")
print(f\"Description: {m.get('description','')[:200]}\")
"
```

## 5-Minute Crypto Prediction Markets

Polymarket runs continuous 5-minute prediction markets for BTC and ETH price movement. These resolve every 5 minutes based on whether the price goes up or down.

### Find Active 5-Min Markets

```bash
# Get current 5-minute BTC/ETH markets
curl -s "https://gamma-api.polymarket.com/markets?limit=20&active=true&closed=false" | python3 -c "
import sys, json
markets = json.load(sys.stdin)
for m in markets:
    q = m.get('question', '')
    if '5 min' in q.lower() or '5-min' in q.lower() or 'next 5' in q.lower():
        prices = json.loads(m.get('outcomePrices', '[]'))
        yes = float(prices[0]) if prices else 0
        print(f\"{yes*100:.0f}% UP | {q[:80]}\")
"
```

### Understanding 5-Min Markets

- Markets resolve every 5 minutes (e.g., 12:00, 12:05, 12:10 UTC)
- "UP" = price at close > price at open of the 5-min window
- Odds near 50/50 mean the market is uncertain — look for divergence from 50% as a signal
- Volume spikes indicate informed traders entering
- These markets are unique to Polymarket — no other prediction platform offers them

## Market Analysis Framework

When researching a market for the user, analyze these factors:

### 1. Odds Assessment
- **YES > 85%**: Market considers this very likely. Look for reasons it might be wrong (contrarian value).
- **YES 60-85%**: Lean likely. Check if the volume supports the odds or if it's thin.
- **YES 40-60%**: Uncertain. Highest potential edge if you have an information advantage.
- **YES < 40%**: Market considers unlikely. Often where the biggest payoffs are.

### 2. Volume & Liquidity
- **High volume + tight spread**: Well-priced market, hard to find edge
- **Low volume + wide spread**: Potentially mispriced, but harder to enter/exit
- **Volume spike**: Something happened — check news, social media

### 3. Time to Resolution
- Markets closer to resolution are more accurately priced
- Long-dated markets (months out) have more uncertainty = more opportunity
- Check if there's a known catalyst date (election, earnings, deadline)

## Enriched Analytics (Optional)

For deeper analysis, the DeepBlue API provides AI-powered market intelligence via x402 micropayments ($0.01-$0.03 per call, paid in USDC).

### Endpoints

| Endpoint | Price | Returns |
|----------|-------|---------|
| `GET https://api.deepbluebase.xyz/polymarket` | $0.01 | Trading analytics, win rates, P&L, edge analysis |
| `GET https://api.deepbluebase.xyz/polymarket/markets` | $0.01 | Enriched market feed with volume spikes, category detection |
| `GET https://api.deepbluebase.xyz/polymarket/5min` | $0.01 | Live 5-min epoch data: current odds, time remaining, token IDs |
| `GET https://api.deepbluebase.xyz/sentiment` | $0.01 | Crypto sentiment composite: Fear & Greed + whale flow + momentum |
| `GET https://api.deepbluebase.xyz/market-intel` | $0.02 | BTC macro + funding rates + liquidation cascade risk |
| `GET https://api.deepbluebase.xyz/prediction-markets` | $0.03 | Premium: positions + odds + volume + full market intelligence |

These endpoints return x402 payment headers. Use with AgentCash `fetch()` or any x402-compatible client.

### Example with AgentCash

If the user has AgentCash configured, use `fetch()` to call enriched endpoints:

```
Use the AgentCash fetch tool to call:
  URL: https://api.deepbluebase.xyz/polymarket/markets
  Method: GET

This returns enriched market data including volume spike detection,
category classification, and liquidity analysis.
```

## Common Research Workflows

### "What's hot on Polymarket right now?"
1. Fetch top markets by volume (free API)
2. Filter for recently created or high-activity markets
3. Present the top 5-10 with odds, volume, and end dates

### "Should I bet on X?"
1. Search for the specific market
2. Get current odds and volume
3. Check time to resolution
4. Look for volume trends (is money flowing in?)
5. Compare odds to your assessment — edge exists when your probability differs from market price

### "What crypto predictions are available?"
1. Search markets with `tag=crypto`
2. Check 5-minute BTC/ETH markets for short-term plays
3. Look at longer-dated crypto price targets
4. Optionally call DeepBlue sentiment endpoint for market mood

### "Find mispriced markets"
1. Look for markets with YES between 30-70% (highest uncertainty)
2. Filter for low volume relative to topic importance
3. Check if similar markets on other platforms have different odds
4. Look for markets where recent news hasn't been priced in

## API Reference

### Gamma API (Free, No Auth)

Base URL: `https://gamma-api.polymarket.com`

| Endpoint | Params | Returns |
|----------|--------|---------|
| `GET /markets` | `limit`, `active`, `closed`, `order`, `ascending`, `tag`, `slug` | Market list with odds, volume, dates |
| `GET /events` | `limit`, `active`, `closed`, `order`, `ascending`, `tag`, `slug` | Events (groups of related markets) |

**Useful fields in market response:**
- `question` — The market question
- `outcomePrices` — JSON string: `["0.62", "0.38"]` (YES, NO)
- `volume` — Total volume traded (USD)
- `liquidityNum` — Current liquidity
- `endDate` — Resolution date
- `description` — Full market description
- `slug` — URL slug for linking
- `active` / `closed` — Market status

### DeepBlue API (x402, USDC)

Base URL: `https://api.deepbluebase.xyz`

Payment: x402 v2 — USDC on Base or Solana. Returns 402 with payment instructions. Use AgentCash or x402-compatible client.

## Tips

- Always show the user **odds as percentages** (multiply by 100), not decimals
- Include **volume** — it indicates how much money backs the current odds
- Link to the market: `https://polymarket.com/event/{slug}`
- For 5-min markets, mention the **time remaining** in the current window
- When presenting multiple markets, sort by volume (highest = most liquid)
- Caveat: Polymarket odds reflect market consensus, not ground truth

## Links

- [Polymarket](https://polymarket.com)
- [Gamma API Docs](https://gamma-api.polymarket.com)
- [DeepBlue API](https://api.deepbluebase.xyz)
- [DeepBlue](https://deepbluebase.xyz)
