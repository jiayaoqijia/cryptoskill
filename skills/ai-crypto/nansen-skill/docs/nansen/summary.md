# Nansen API — Documentation Summary

Собрано 2026-04-24 из docs.nansen.ai (официальный llms-full.txt на 5523 строки сохранён в `llms-full.txt`).

## Basics

- **Base URL:** `https://api.nansen.ai`
- **Auth:** header `apiKey: <your_key>` (camelCase, не `apikey`)
- **All endpoints: POST** (except where noted)
- **Content-Type:** `application/json`
- **Get API key:** https://app.nansen.ai (API tab)

## Plans (2026)

| Plan | Cost | Starter credits | Notes |
|------|------|-----------------|-------|
| **Pro** | $49/mo annual or $69/mo monthly | 1000 (one-time) | Flexi-Credits top-up, credits expire 1 год |
| **Free** | $0 | 1000 (one-time, trial) | **Consumes 10× faster** (1 Pro credit = 10 Free credits) |
| x402 pay-per-call | Per-request | N/A | USDC on Base или Solana, без subscription |

Enterprise: только при bulk purchase > $10,000.

## Rate Limits

### API key (standard)
- **20 requests per second**
- **300 requests per minute**
- 429 on exceed

### x402 (per wallet)
- 5 req/sec
- 60 req/min
- Rate-limited requests не списывают payment

### Response headers (use for live monitoring)
```
X-Nansen-Credits-Used: <credits this call>
X-Nansen-Credits-Remaining: <balance>
RateLimit-Limit / RateLimit-Remaining / RateLimit-Reset
X-RateLimit-Limit-Second / -Remaining-Second
X-RateLimit-Limit-Minute / -Remaining-Minute
Retry-After: <seconds>  (on 429)
```

## Credit Costs (Pro tier — multiply by 10 for Free)

### 1 credit
- All Profiler endpoints: current-balances, historical-balances, transactions, perp-positions, perp-trades, related-wallets, pnl-summary, pnl
- Most TGM: token-screener, perp-screener, transfers, dcas, flow-intel, who-bought-sold, dex-trades, token-information, token-ohlcv, flows
- portfolio/defi-holdings
- All Prediction Market endpoints (except top-holders, pnl-by-market, position-detail)

### 5 credits
- **ALL Smart Money endpoints** (holdings, dex-trades, netflow, historical-holdings, perp-trades, dcas, inflows)
- tgm/indicators (Nansen Score)
- profiler/perp-leaderboard
- profiler/address/counterparties
- prediction-market/top-holders, pnl-by-market, position-detail

### 5 credits / 150 with premium labels
- tgm/perp-positions
- tgm/perp-pnl-leaderboard
- tgm/holders
- tgm/pnl-leaderboard

### 100 / 500 credits (labels endpoint)
- profiler/address/labels (Common Labels): 100
- profiler/address/premium-labels: 500

### 200 / 750 credits (Agent)
- agent/fast-research: 200
- agent/expert-research: 750

## Supported Chains (37 total)

### EVM (24)
ethereum, arbitrum, avalanche, base, bitlayer, bnb, celo, chiliz, gravity, hyperevm, iotaevm, linea, mantle, monad, optimism, plasma, polygon, ronin, scroll, sei, sonic, unichain, viction, zksync

### Non-EVM (12)
algorand, aptos, bitcoin, hyperliquid, near, **solana**, stacks, starknet, stellar, sui, ton, tron

### Solana support matrix

**Solana fully supported for:**
- Smart Money: netflow, dex-trades, holdings, historical-holdings ✅
- TGM: flows, transfers, holders, pnl ✅
- Profiler: current-balances, historical-balances, transactions, pnl, related-wallets ✅

**Solana NOT supported for:**
- Profiler transaction lookup (single tx by hash)
- Labels endpoints (EVM only)

⚠️ **Update from old memory:** previous notes said "Solana coverage ~14 smart money wallets" — this is OUT OF DATE. Current coverage is on par with EVM for Smart Money endpoints.

## Endpoint Catalog

### Smart Money (`/api/v1/smart-money/*`) — 5 credits each
- `netflow` — net inflow/outflow per token (DEX + CEX aggregated)
- `dex-trades` — individual trades
- `holdings` — aggregated balances
- `historical-holdings` — time-series balances
- `perp-trades` — Hyperliquid perp trades
- `dcas` — Jupiter DCA orders (Solana)

Labels available for filtering:
- Fund, Smart Trader, 30D Smart Trader, 90D Smart Trader, 180D Smart Trader, Smart HL Perps Trader

### Profiler (`/api/v1/profiler/*`) — 1-5 credits
- `address/current-balances` (1)
- `address/historical-balances` (1)
- `address/transactions` (1)
- `address/counterparties` (5)
- `address/related-wallets` (1)
- `address/pnl-summary` (1)
- `address/pnl` (1)
- `address/labels` (100 / 500 premium)
- `perp-positions` (1)
- `perp-trades` (1)
- `perp-leaderboard` (5)

### Token God Mode (`/api/v1/tgm/*`) — 1-150 credits
- `token-information` (1)
- `token-screener` (1)
- `token-ohlcv` (1)
- `flow-intel` (1)
- `flows` (1)
- `transfers` (1)
- `dcas` (1)
- `dex-trades` (1)
- `who-bought-sold` (1)
- `indicators` — Nansen Score (5)
- `holders` (5 / 150 premium labels)
- `pnl-leaderboard` (5 / 150 premium)
- `perp-screener` (1)
- `perp-positions` (5 / 150 premium)
- `perp-pnl-leaderboard` (5 / 150 premium)
- `perp-trades` (5 / 150 premium)

### Portfolio
- `portfolio/defi-holdings` (1)

### Prediction Market
- 11 endpoints, mostly 1 credit

### Agent (AI-powered research)
- `agent/fast` (200 credits) — quick research
- `agent/expert` (750 credits) — deep analysis

### Hyperliquid (perpetuals only)
- Uses `hyperliquid` chain value
- Leaderboard, address perp positions/trades
- Note: chain supports perps only, no spot

## Common Request Pattern

```json
POST /api/v1/smart-money/netflow
Headers:
  apiKey: <your_key>
  Content-Type: application/json
Body:
{
  "chains": ["solana"],
  "filters": {
    "include_smart_money_labels": ["Fund", "Smart Trader"],
    "market_cap_usd": {"min": 10000000},
    "token_age_days": {"max": 90}
  },
  "pagination": {"page": 1, "per_page": 100},
  "order_by": [{"field": "net_flow_7d_usd", "direction": "DESC"}]
}
```

**Pagination max `per_page`: 1000** (default 10).

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Malformed request |
| 401 | Bad/missing `apiKey` header |
| 402 | x402 payment required (for pay-per-call users without key) |
| 403 | No subscription or endpoint not in plan |
| 404 | Endpoint/resource not found |
| 422 | Invalid parameters (wrong enum, out-of-range filter) |
| 429 | Rate limit — respect `Retry-After` |
| 500 | Server error |
| 504 | Gateway timeout — query too heavy, narrow it |

## MCP Server

Nansen provides its own MCP (raw details in llms-full.txt line ~3601). Can be used as alternative to direct HTTP. Authentication via API key.

Docs: https://docs.nansen.ai/mcp/connecting

## Sources

- https://docs.nansen.ai (GitBook, 2026-04)
- https://docs.nansen.ai/llms-full.txt (saved locally)
- https://docs.nansen.ai/api/smart-money
- https://docs.nansen.ai/about/credits-and-pricing-guide
- https://docs.nansen.ai/getting-started/rate-limits
