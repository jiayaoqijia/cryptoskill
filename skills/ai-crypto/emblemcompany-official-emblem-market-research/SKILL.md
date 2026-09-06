---
name: emblem-market-research
description: >
  Crypto market intelligence via EmblemAI. Trending tokens, on-chain analytics, derivatives data,
  and smart money tracking from CoinGecko, CoinGlass, Birdeye, and Nansen. Use when the user wants
  market data, trending tokens, derivatives analytics, or on-chain intelligence.
license: MIT
compatibility: >
  Requires Node.js >= 18.0.0, @emblemvault/agentwallet CLI, and internet access.
  Works on Claude Code, Cursor, Codex, OpenClaw, and other agents following the Agent Skills spec.
metadata:
  author: EmblemAI
  version: "1.1.0"
  homepage: https://emblemvault.ai
  docs: https://emblemvault.ai/docs
  docs-interactive: https://emblemvault.dev
---

# Emblem Market Research

Crypto market intelligence powered by **EmblemAI**. Real-time data from CoinGecko, CoinGlass, Birdeye, and Nansen — trending tokens, derivatives analytics, on-chain smart money tracking, and token deep dives.

**Requires**: `npm install -g @emblemvault/agentwallet`

---

## What This Skill Can Do

| Capability | Tools Used |
|-----------|------------|
| Trending tokens (all chains) | `getTrendingCoins`, `birdeyeTrendingTokens` |
| Token price lookup | `getCryptoPrice`, `searchCryptoByName` |
| Token deep dive (volume, trades, liquidity) | `birdeyeTradeData` |
| Open interest history | `getCoinglassOpenInterestHistory` |
| Derivatives risk/greed indices | `getCoinglassCDRIIndex`, `getCoinglassCGDIIndex` |
| Whale tracking (futures) | `getCoinglassFuturesWhaleIndex`, `getCoinglassHyperliquidWhaleAlert` |
| Funding rates | `getCoinglassPremiumIndex` |
| ETF flows (BTC/ETH) | `getCoinglassBitcoinETFNetAssetsHistory`, `getCoinglassEthereumETFNetAssetsHistory` |
| Smart money flows | `nansen_smart_money_flows`, `nansen_smart_money_trades` |
| Smart money holdings | `nansen_smart_money_holdings` |
| Token screening | `nansen_token_screener` |
| Wallet profiling | `nansen_wallet_profiler` |
| P&L leaderboard | `nansen_pnl_leaderboard` |

### Not Supported

These features have no backing tools:

- Technical analysis (RSI, MACD, support/resistance) — no charting or TA tools exist
- Social sentiment (Twitter, Telegram, Discord monitoring) — no social API tools
- Fear/Greed Index — no dedicated tool (CoinGlass CDRI is derivatives-specific, not the same)
- DeFiLlama TVL data — no DeFiLlama tools exist
- BTC dominance / total market cap — no dedicated tool

---

## Quick Start

```bash
npm install -g @emblemvault/agentwallet

# What's trending (uses getTrendingCoins)
emblemai --agent --profile default -m "Use getTrendingCoins to show what's trending in crypto right now"

# Token deep dive (uses birdeyeTradeData)
emblemai --agent --profile default -m "Use birdeyeTradeData to analyze SOL — show volume, trades, buy/sell ratio, and liquidity"
```

**Trigger phrases:**
- "What's trending in crypto?"
- "Analyze this token"
- "Show derivatives data for BTC"
- "What are whales buying?"
- "Show smart money flows"

---

## Data Sources

| Source | Tools | Coverage |
|--------|-------|----------|
| **CoinGecko** | `getTrendingCoins`, `getCryptoPrice`, `searchCryptoByName` | Trending coins, price lookup |
| **Birdeye** | `birdeyeTradeData`, `birdeyeTrendingTokens`, `searchEvmTokensBirdeye` | Token analytics, multi-chain trending, trade data |
| **CoinGlass** | `getCoinglassOpenInterestHistory`, `getCoinglassCDRIIndex`, `getCoinglassCGDIIndex`, `getCoinglassFuturesWhaleIndex`, `getCoinglassHyperliquidWhaleAlert`, `getCoinglassPremiumIndex`, `getCoinglassBitcoinETFNetAssetsHistory`, etc. | Derivatives, funding rates, open interest, whale tracking, ETF flows |
| **Nansen** | `nansen_smart_money_flows`, `nansen_smart_money_trades`, `nansen_smart_money_holdings`, `nansen_token_screener`, `nansen_wallet_profiler`, `nansen_pnl_leaderboard` | Smart money analytics, on-chain flows, wallet profiling |

---

## Workflow: Token Research

### Step 1: Discovery
Find what's moving.
```bash
emblemai --agent --profile default -m "Use getTrendingCoins to show trending tokens, then use birdeyeTrendingTokens for Solana-specific trending with volume data"
```

### Step 2: Deep Dive
Research a specific token with real trade data.
```bash
emblemai --agent --profile default -m "Use birdeyeTradeData to analyze JUP on Solana — show price, volume across timeframes, unique wallets, buy/sell ratio, and liquidity"
```

### Step 3: On-Chain Intelligence
Check what smart money is doing.
```bash
emblemai --agent --profile default -m "Use nansen_smart_money_flows to show token flows on solana in the last 24h. Then use nansen_smart_money_trades to show recent smart money trades"
```

### Step 4: Derivatives Context
Check funding rates and whale positioning.
```bash
emblemai --agent --profile default -m "Use getCoinglassOpenInterestHistory to show BTC open interest, and getCoinglassHyperliquidWhaleAlert for current whale positions"
```

---

## Research Patterns

### Trending Tokens
```bash
emblemai --agent --profile default -m "Use getTrendingCoins to show what's trending globally"
emblemai --agent --profile default -m "Use birdeyeTrendingTokens to show top trending tokens on Base by volume"
```

### Smart Money Analysis
```bash
emblemai --agent --profile default -m "Use nansen_smart_money_holdings to see what smart money is holding on solana"
emblemai --agent --profile default -m "Use nansen_who_bought_sold to check who bought and sold ETH recently"
emblemai --agent --profile default -m "Use nansen_pnl_leaderboard to show the top performing wallets"
```

### Derivatives & Funding
```bash
emblemai --agent --profile default -m "Use getCoinglassPremiumIndex to show funding rates for BTC across exchanges"
emblemai --agent --profile default -m "Use getCoinglassOpenInterestHistory to show ETH open interest trends"
```

### Whale Tracking
```bash
emblemai --agent --profile default -m "Use getCoinglassFuturesWhaleIndex to show whale activity for BTC"
emblemai --agent --profile default -m "Use getCoinglassHyperliquidWhaleAlert to show large positions on Hyperliquid"
```

### ETF Flows
```bash
emblemai --agent --profile default -m "Use getCoinglassBitcoinETFNetAssetsHistory to show recent BTC ETF inflows and outflows"
emblemai --agent --profile default -m "Use getCoinglassEthereumETFNetAssetsHistory for ETH ETF flow data"
```

### Token Screening
```bash
emblemai --agent --profile default -m "Use nansen_token_screener to find tokens with high smart money activity on ethereum"
```

---

## Communication Tips

Name the exact tool for reliable results:

| Bad | Good |
|-----|------|
| `"trending"` | `"Use getTrendingCoins to show what's trending"` |
| `"analyze sol"` | `"Use birdeyeTradeData to analyze SOL with volume, trades, and liquidity"` |
| `"whale activity"` | `"Use getCoinglassHyperliquidWhaleAlert to show large positions"` |

---

## Read-Only Skill

This skill only reads market data. No wallet interaction, no transactions, no confirmation needed. All queries execute immediately.

---

## Helper Script

```bash
bash scripts/market-scan.sh [chain]
```

See [scripts/market-scan.sh](scripts/market-scan.sh) for a daily market scan report.

---

## Links

- [Agent Wallet CLI](https://www.npmjs.com/package/@emblemvault/agentwallet)
- [EmblemVault Docs — canonical](https://emblemvault.ai/docs)
- [EmblemVault Docs — interactive](https://emblemvault.dev)
