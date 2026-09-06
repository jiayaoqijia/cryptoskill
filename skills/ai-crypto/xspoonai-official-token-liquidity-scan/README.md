# token-liquidity-scan

Analyze token liquidity across DEX pools using real blockchain data.

## Overview

This skill analyzes token liquidity across decentralized exchange (DEX) pools using the Uniswap v3 subgraph. It fetches real pool data, calculates liquidity metrics, assesses token health, and provides actionable insights for trading and market analysis.

## Features

- ✅ Real Uniswap v3 subgraph API integration
- ✅ Multi-network support (Ethereum, Polygon)
- ✅ Total liquidity and volume calculation
- ✅ 24-hour trading volume analysis
- ✅ Pool ranking by liquidity
- ✅ Volume-to-liquidity ratio calculation
- ✅ Liquidity health scoring (Low/Medium/High/Very High/Excellent)
- ✅ Pool breakdown by liquidity tiers
- ✅ Known token address resolution
- ✅ Dual-mode operation (API + Parameter)

## Usage

### API Mode (Real Uniswap Data)
```bash
python scripts/main.py --params '{"use_api": true, "token": "USDC", "network": "ethereum", "min_liquidity_usd": 100000}'
```

### Parameter Mode (Custom Pool Data)
```bash
python scripts/main.py --params '{"use_api": false, "token": "USDC", "pools": [{"address": "0x...", "token0": "USDC", "token1": "WETH", "liquidity_usd": 5000000, "volume_24h_usd": 1000000}], "min_liquidity_usd": 100000}'
```

## Parameters

### API Mode Parameters
- `use_api` (boolean, required): Enable Uniswap v3 subgraph integration
- `token` (string, required): Token symbol or address
  - Symbols: USDC, USDT, DAI, WETH, UNI (Ethereum) / USDC, USDT, DAI, WMATIC (Polygon)
  - Or provide full contract address (0x...)
- `network` (string, required): "ethereum" or "polygon"
- `min_liquidity_usd` (number, optional): Minimum pool liquidity threshold (default: 100000)

### Parameter Mode Parameters
- `use_api` (boolean, required): Disable API (false)
- `token` (string, required): Token identifier
- `pools` (array, required): Array of pool objects with:
  - `address`: Pool contract address
  - `token0`: First token symbol
  - `token1`: Second token symbol
  - `liquidity_usd`: Pool liquidity in USD
  - `volume_24h_usd`: 24-hour trading volume in USD
- `min_liquidity_usd` (number, optional): Minimum liquidity filter

## Output

Returns JSON with:
- `status`: "success" or "error"
- `source`: "uniswap_api" or "parameters"
- `network`: Analyzed blockchain network
- `token`: Token analyzed
- `pools_analyzed`: Number of pools meeting criteria
- `total_liquidity_usd`: Total liquidity in USD
- `total_volume_24h_usd`: 24-hour trading volume
- `avg_liquidity_per_pool`: Average liquidity per pool
- `volume_to_liquidity_ratio_pct`: Turnover ratio percentage
- `liquidity_health_score`: Health assessment
- `top_pools`: Top 10 pools by liquidity (with addresses and volume)
- `summary`: Breakdown by liquidity tiers
- `analysis_timestamp`: ISO8601 timestamp

## Liquidity Health Scores

- **Excellent**: > $50M total liquidity
- **Very High**: $10M - $50M liquidity
- **High**: $5M - $10M liquidity
- **Medium**: $1M - $5M liquidity
- **Low**: < $1M liquidity

## Volume-to-Liquidity Ratio Interpretation

- **> 50%**: Excellent turnover and capital efficiency
- **20-50%**: Good turnover and market activity
- **10-20%**: Normal turnover, stable market
- **< 10%**: Conservative turnover, stable reserves

## Examples

### Analyze USDC on Ethereum
```bash
python scripts/main.py --params '{
  "use_api": true,
  "token": "USDC",
  "network": "ethereum",
  "min_liquidity_usd": 500000
}'
```

### Analyze USDT on Polygon
```bash
python scripts/main.py --params '{
  "use_api": true,
  "token": "USDT",
  "network": "polygon",
  "min_liquidity_usd": 100000
}'
```

### Custom Token Pool Analysis
```bash
python scripts/main.py --params '{
  "use_api": true,
  "token": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  "network": "ethereum",
  "min_liquidity_usd": 1000000
}'
```

## Supported Networks

- **Ethereum Mainnet**: USDC, USDT, DAI, WETH, UNI
- **Polygon**: USDC, USDT, DAI, WMATIC

## API Integration

**Uniswap v3 Subgraph GraphQL**
- Ethereum: api.thegraph.com/subgraphs/name/uniswap/uniswap-v3
- Polygon: api.thegraph.com/subgraphs/name/uniswap/uniswap-v3-polygon

Queries real-time pool data including:
- Pool liquidity
- Token pair information
- 24-hour trading volume
- Fee tier information

## Category

web3-data-intelligence
