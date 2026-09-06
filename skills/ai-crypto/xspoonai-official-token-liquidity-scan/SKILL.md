---
name: token-liquidity-scan
track: web3-data-intelligence
version: 0.2.0
summary: Analyze token liquidity across DEX pools with real API data
---

## Description

Analyzes token liquidity across decentralized exchanges (DEX) using the Uniswap v3 subgraph. Fetches real pool data, calculates liquidity metrics, and scores token health based on liquidity depth and trading volume.

## Features

- Real Uniswap v3 subgraph integration
- Multi-network support (Ethereum, Polygon)
- Liquidity depth analysis
- Volume-to-liquidity ratio calculation
- Pool ranking by liquidity
- Health score assessment
- Dual-mode operation (API + Parameter)

## Inputs

### API Mode
```json
{
  "use_api": true,
  "token": "USDC",
  "network": "ethereum",
  "min_liquidity_usd": 100000
}
```

### Parameter Mode
```json
{
  "use_api": false,
  "token": "USDC",
  "pools": [
    {
      "address": "0xpool1",
      "token0": "USDC",
      "token1": "WETH",
      "liquidity_usd": 5000000,
      "volume_24h_usd": 1000000
    }
  ],
  "min_liquidity_usd": 100000
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "status": "success",
    "source": "uniswap_api",
    "network": "ethereum",
    "token": "USDC",
    "pools_analyzed": 12,
    "min_liquidity_usd": 100000,
    "total_liquidity_usd": 45200000,
    "total_volume_24h_usd": 8500000,
    "avg_liquidity_per_pool": 3766666.67,
    "volume_to_liquidity_ratio_pct": 18.81,
    "liquidity_health_score": "very_high",
    "top_pools": [
      {
        "address": "0xpool1",
        "token0": "USDC",
        "token1": "WETH",
        "liquidity_usd": 15000000,
        "volume_24h_usd": 3000000,
        "source": "uniswap_v3_subgraph"
      }
    ],
    "summary": {
      "highly_liquid": 8,
      "moderately_liquid": 3,
      "lowly_liquid": 1
    },
    "analysis_timestamp": "2026-02-07T09:30:00.000Z"
  }
}
```

## Parameters

### API Mode Parameters
- `use_api` (boolean, required): Enable Uniswap subgraph API integration
- `token` (string, required): Token symbol or address (e.g., "USDC", "0xA0b...")
- `network` (string, required): Blockchain network - "ethereum" or "polygon"
- `min_liquidity_usd` (number, required): Minimum pool liquidity threshold

### Parameter Mode Parameters
- `use_api` (boolean, required): Disable API (false)
- `token` (string, required): Token identifier
- `pools` (array, required): Pool objects with liquidity data
- `min_liquidity_usd` (number, required): Minimum liquidity filter

## Liquidity Health Scores

- **Excellent** (> $50M total): Maximum liquidity, very tight spreads
- **Very High** ($10M-$50M): Strong liquidity, low slippage
- **High** ($5M-$10M): Good liquidity, acceptable spreads
- **Medium** ($1M-$5M): Moderate liquidity, normal spreads
- **Low** (< $1M): Limited liquidity, higher slippage

## Usage Examples

### Analyze USDC Liquidity on Ethereum (API Mode)
```bash
python scripts/main.py --params '{
  "use_api": true,
  "token": "USDC",
  "network": "ethereum",
  "min_liquidity_usd": 100000
}'
```

### Analyze USDT on Polygon (API Mode)
```bash
python scripts/main.py --params '{
  "use_api": true,
  "token": "USDT",
  "network": "polygon",
  "min_liquidity_usd": 50000
}'
```

### Custom Pool Analysis (Parameter Mode)
```bash
python scripts/main.py --params '{
  "use_api": false,
  "token": "USDC",
  "pools": [
    {
      "address": "0x8ad599c3A0ff1de082011efdDc58f1908761f7e8",
      "token0": "USDC",
      "token1": "WETH",
      "liquidity_usd": 7500000,
      "volume_24h_usd": 1500000
    },
    {
      "address": "0x5777d3d545f40867652424e757029d3348dd4d6b",
      "token0": "USDC",
      "token1": "DAI",
      "liquidity_usd": 2000000,
      "volume_24h_usd": 400000
    }
  ],
  "min_liquidity_usd": 100000
}'
```

## Supported Tokens

### Ethereum
- USDC, USDT, DAI, WETH, UNI

### Polygon
- USDC, USDT, DAI, WMATIC

## Liquidity Health Calculation

Volume-to-Liquidity Ratio = (24h Volume / Total Liquidity) × 100

Healthy ratios indicate:
- > 50%: Excellent turnover
- 20-50%: Good turnover
- 10-20%: Normal turnover
- < 10%: Conservative turnover
