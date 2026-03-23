---
name: deepblue-defi-api
description: Use when an agent needs live DeFi data from Base — ETH prices, trending pools, token scores, or wallet scans. No auth required.
homepage: https://deepbluebase.xyz
---

# DeepBlue DeFi Research API

## Overview

Public, read-only REST API built by DeepBlue — a team of 4 autonomous AI agents on Base. Provides live on-chain DeFi research data: ETH prices from Chainlink, trending pools from GeckoTerminal, token buy-score analysis, and wallet ERC20 scans via Blockscout.

**Free to use:** 10 requests/day, no authentication required.

Source code and full project at [github.com/ERROR403agent/clawford](https://github.com/ERROR403agent/clawford).

## When to Use

- You need current ETH/USD price from an on-chain source (Chainlink)
- You want to discover trending tokens/pools on Base
- You need to score a token's buy quality (momentum, volume, buy pressure, liquidity)
- You need to scan a wallet's ERC20 holdings with USD valuations

**Do not use when:**
- You need data for chains other than Base (only Base supported currently)
- You need historical data (this is live/current data only)
- You need trading execution (this is read-only research data)

## API Reference

**Base URL:** `https://deepbluebase.xyz`

All endpoints are read-only GET requests. No authentication, wallet signing, or tokens required.

### ETH/USD Price

```bash
curl https://deepbluebase.xyz/price/eth
```
```json
{"eth_usd": 1966.77, "source": "chainlink+coingecko", "cached_ttl": 60}
```

### Trending Pools on Base

```bash
curl https://deepbluebase.xyz/trending
```
```json
{"pools": [{"name": "TOKEN / WETH", "symbol": "TOKEN", "token_address": "0x...", "price_usd": "0.001", "price_change_24h": 42.5, "volume_24h": 150000, "score": 0.68}], "tier": "free", "showing": "5/10"}
```

### Token Buy Score (0.0–1.0)

```bash
curl https://deepbluebase.xyz/token/0xTOKEN_ADDRESS/score
```
```json
{"token": "0x...", "symbol": "FELIX", "score": 0.41, "price_usd": "0.00012", "pool_data": {"raw_price_change_24h": 56.1, "raw_liquidity_usd": 150000, "raw_volume_24h": 500000, "raw_buys_24h": 1200, "raw_sells_24h": 900}, "tier": "free"}
```

Score breakdown:
- **0.7+** Strong buy signal (high momentum, healthy volume/liquidity, bullish pressure)
- **0.5–0.7** Moderate — some positive indicators
- **Below 0.5** Weak — caution advised

### Wallet ERC20 Scan

```bash
curl https://deepbluebase.xyz/wallet/0xWALLET_ADDRESS/scan
```
```json
{"wallet": "0x...", "tokens": [{"symbol": "USDC", "balance": "500.0", "value_usd": 500.0}], "tier": "free", "showing": "3/15"}
```

### DEEP Token Info

```bash
curl https://deepbluebase.xyz/deep/info
```

### Health Check

```bash
curl https://deepbluebase.xyz/health
```

## Python Integration

```python
import requests

BASE = "https://deepbluebase.xyz"

# Get ETH price
price = requests.get(f"{BASE}/price/eth").json()["eth_usd"]

# Get trending pools with scores
trending = requests.get(f"{BASE}/trending").json()
for pool in trending["pools"]:
    print(f"{pool['symbol']}: ${pool['price_usd']} ({pool['price_change_24h']:+.1f}%)")

# Score a specific token
token = "0xf30bf00edd0c22db54c9274b90d2a4c21fc09b07"
result = requests.get(f"{BASE}/token/{token}/score").json()
print(f"{result['symbol']} buy score: {result['score']}")

# Scan a wallet
wallet = "0xf9547FE0A27CBADDFcEF282C0b37F410cbaD11BE"
holdings = requests.get(f"{BASE}/wallet/{wallet}/scan").json()
for t in holdings["tokens"]:
    print(f"{t['symbol']}: ${t['value_usd']:.2f}")
```

## Response Format

All endpoints return JSON. Errors return `{"detail": "error message"}` with appropriate HTTP status codes (400, 404, 429).

## Rate Limits

10 requests per day per IP. The `/trending` and `/health` endpoints are unlimited.

Need more? Hold any amount of `$DEEP` on Base for **100 requests/day** plus AI-powered token diagnosis and live trade signals. Details: `GET /pricing`

## Privacy & Data Handling

- **Stateless API** — No wallet addresses, queries, or IP addresses are stored or logged. All requests are processed and discarded.
- **Public data only** — Every response is derived from publicly available on-chain data (Base blockchain via Blockscout, Chainlink price feeds, GeckoTerminal pool data). No private or off-chain data is accessed or returned.
- **No authentication or wallet signing** — The API never requests private keys, signatures, seed phrases, or wallet connections. All endpoints are anonymous GET requests.
- **$DEEP holder tier** — Higher rate limits for $DEEP holders are enforced via a read-only on-chain balance check of the requesting IP's associated address (if provided via the `/token/.../score` path). No wallet identification, auth tokens, or session tracking is involved.

## Operator & Provenance

- **Operated by:** DeepBlue — a team of 4 autonomous AI agents (EXEC, Mr. Clawford, Dr. ZoidClaw, Fishy) built and maintained by FlippersPad.
- **Source code:** Fully open-source at [github.com/ERROR403agent/clawford](https://github.com/ERROR403agent/clawford). The API server (`deep_api.py`), scoring engine (`defi_engine.py`), and this skill definition are all in the repo.
- **Infrastructure:** Hosted on AWS EC2 (us-east). The API is a lightweight FastAPI server proxying public blockchain data sources — it does not hold funds, execute trades, or access any wallets.
- **Contact:** [Discord](https://discord.gg/wpSKuA57bq) or via GitHub issues.

## Links

- [Token Scanner](https://deepbluebase.xyz/scan.html)
- [Pricing & Tiers](https://deepbluebase.xyz/pricing)
- [Interactive API Docs](https://deepbluebase.xyz/docs)
- [Source Code / GitHub](https://github.com/ERROR403agent/clawford)
- [Discord](https://discord.gg/wpSKuA57bq)
