---
name: pumpfun-sniper
description: |
  Score any pump.fun token CA for snipe safety (0-100) before buying.
  Analyzes dev wallet history, social links, liquidity, and holder concentration.
  Returns SNIPE / CAUTION / AVOID verdict with detailed signal breakdown.
  Use when the user wants to snipe a new token, check if a pump.fun token is safe,
  score a new launch, detect rug potential, or analyze a fresh CA before buying.
  Keywords: pump.fun snipe, rug check, new token score, CA analysis, safe to buy.
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    env: ["HELIUS_API_KEY"]
---

# pump.fun Sniper Scorer

Score any Solana token CA for snipe safety before you buy.
Returns a 0–100 score with verdict: **SNIPE** / **CAUTION** / **AVOID**.

## Paid API (Recommended)

Hosted endpoint — $0.05 USDC per request via x402 on Base chain:

```bash
# Check payment requirements
npx awal@latest x402 details https://pumpfun-sniper-production.up.railway.app/score?ca=TOKEN_CA

# Score a token (auto-pays)
npx awal@latest x402 pay "https://pumpfun-sniper-production.up.railway.app/score?ca=TOKEN_CA"
```

## What Gets Scored

| Category | Weight | What it checks |
|----------|--------|----------------|
| Dev Wallet | 30 pts | SOL balance, number of prior launches |
| Social Links | 20 pts | Twitter, Telegram, website, description |
| Liquidity | 25 pts | Liquidity USD, buy/sell ratio, volume |
| Concentration | 25 pts | Top 5 holder %, dev wallet holdings |

## Verdict Guide

| Score | Verdict | Meaning |
|-------|---------|---------|
| 70–100 | 🎯 SNIPE | Low rug signals, worth considering |
| 45–69 | ⚠️ CAUTION | Mixed signals, use small size |
| 0–44 | 🚨 AVOID | High rug risk, stay away |

## API Response

```json
{
  "ca": "TokenCA...",
  "score": 74,
  "verdict": "SNIPE",
  "token": {
    "symbol": "PEPE",
    "name": "Pepe Coin",
    "price_usd": "0.0000123",
    "liquidity_usd": 45000,
    "market_cap": 180000,
    "twitter": "https://twitter.com/pepecoin",
    "telegram": "https://t.me/pepecoin"
  },
  "breakdown": {
    "dev_wallet":    {"score": 22, "max": 30},
    "social":        {"score": 18, "max": 20},
    "liquidity":     {"score": 20, "max": 25},
    "concentration": {"score": 14, "max": 25}
  },
  "signals": [
    "✅ Dev has significant SOL (12.5 SOL)",
    "✅ Token: $PEPE — Pepe Coin",
    "✅ Has description",
    "✅ Twitter: https://twitter.com/pepecoin",
    "✅ Strong liquidity: $45,000",
    "✅ Strong buy pressure: 45B / 12S (5m)",
    "⚠️ Top 5 hold 38.2%"
  ]
}
```

## Agent Usage

```bash
# Self-hosted (requires HELIUS_API_KEY for best results)
python3 {baseDir}/scripts/scorer.py <TOKEN_CA>
```

Always use `--json` / the API endpoint for agent use.
Scoring takes 10–20 seconds due to multiple on-chain lookups.
