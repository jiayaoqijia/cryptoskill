# nft-trader-watch

Real NFT trader analysis with OpenSea API integration for live trading data.

## Overview

This skill monitors NFT trading activity with real data from OpenSea API. It tracks trader performance, detects flipping patterns, and analyzes profit margins for popular collections.

## Features

- ✅ **OpenSea API Integration**: Fetch real-time sales data
- ✅ **CoinGecko ETH Price**: Live ETH/USD conversion
- ✅ **Flip Detection**: Identifies profitable re-sales
- ✅ **Trader Analytics**: Volume, profit, ROI calculations
- ✅ **Dual-mode Operation**: API mode (live) + parameter mode (custom)
- ✅ **Popular Collections**: BAYC, CryptoPunks, Pudgy Penguins, Cool Cats, Art Blocks
- ✅ **Profit Tracking**: ETH and USD profit metrics
- ✅ **Trading Patterns**: Buy/sell volume analysis

## Usage

### Fetch Real OpenSea Data
```bash
python scripts/main.py --params '{"use_api":true,"collection":"0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE","collection_slug":"boredapeyachtclub"}'
```

### Analyze Custom Trades
```bash
python scripts/main.py --params '{"collection":"0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE","trades":[{"type":"buy","nft_id":"1234","price_eth":45.5}]}'
```

## Parameters

### API Mode
- `use_api` (boolean): Set to true to fetch live OpenSea data
- `collection` (string, required): NFT collection address
- `collection_slug` (string): OpenSea collection slug (e.g., "boredapeyachtclub")
- `min_volume` (number): Minimum trades to track trader (default: 5)

### Parameter Mode
- `collection` (string, required): NFT collection address
- `trades` (array, required): Trade data with type (buy/sell), nft_id, price_eth
- `network` (string): ethereum (default)

## Output

Returns JSON with:
- `source`: Data source (opensea_api or parameters)
- `eth_price`: Current ETH price in USD
- `total_traders`: Number of active traders
- `flips_detected`: Count of profitable flips
- `traders`: Top traders with buy/sell volumes and profit
- `top_flips`: Most profitable individual flips
  - `profit_eth`: Profit in ETH
  - `profit_pct`: Profit percentage
  - `nft_id`: NFT token ID
- `analysis_timestamp`: Time of analysis

## Examples

### BAYC Trader Analysis
```bash
python scripts/main.py --params '{"use_api":true,"collection":"0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE","collection_slug":"boredapeyachtclub"}'
```

### CryptoPunks Flips
```bash
python scripts/main.py --params '{"use_api":true,"collection":"0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB","collection_slug":"cryptopunks"}'
```

### Custom Trade Analysis
```bash
python scripts/main.py --params '{"collection":"0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE","trades":[{"type":"buy","nft_id":"1234","price_eth":45.5},{"type":"sell","nft_id":"1234","price_eth":52.75}]}'
```

## Supported Collections

- **BAYC** (boredapeyachtclub) - 0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE
- **CryptoPunks** (cryptopunks) - 0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB
- **Pudgy Penguins** (pudgy-penguins) - 0xBd3531dA5DD0A74fb411a9b847beAeC30DC5511B
- **Cool Cats** (cool-cats-nft) - 0x1A92de1e5EC850f0385d3a010937198afb8b5AAF
- **Art Blocks** (artblocks-engine) - 0xa7d8d9ef8D8Ce8992Df33D8b8f37e3a930B5CFfD

## Track

web3-data-intelligence
