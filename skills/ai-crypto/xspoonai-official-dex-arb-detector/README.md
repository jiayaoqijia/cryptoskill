# dex-arb-detector

Detect significant price deltas across decentralized exchanges (DEXs) for arbitrage opportunities.

## Overview

This skill analyzes price differences across multiple DEXs and identifies profitable arbitrage opportunities. It scans liquidity pools and calculates potential profit margins when buying on one DEX and selling on another.

## Features

- ✅ Multi-DEX price comparison
- ✅ Arbitrage opportunity detection
- ✅ Profit margin calculation (USD and percentage)
- ✅ Configurable minimum profit threshold
- ✅ Support for major DEXs (Uniswap, SushiSwap, Curve, Balancer)
- ✅ Real-time price scanning
- ✅ Comprehensive error handling

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### With Parameters
```bash
python scripts/main.py --params '{"token_pair": ["WETH", "USDC"], "dexes": ["uniswap", "sushiswap"], "min_profit_percentage": 0.5}'
```

## Parameters

- `token_pair` (array, required): Two-element array of token symbols
- `dexes` (array, required): List of DEX names to scan
- `min_profit_percentage` (number, optional): Minimum profit threshold (default: 0.5)

## Output

Returns JSON with:
- `opportunities`: Array of profitable arbitrage positions
- `buy_dex`: DEX with lower price
- `sell_dex`: DEX with higher price
- `profit_percentage`: Calculated profit margin
- `estimated_profit_usd`: Estimated profit in USD
- `prices`: Current prices on each DEX

## Examples

### Find ETH/USDC Arbitrage
```bash
python scripts/main.py --params '{"token_pair": ["WETH", "USDC"], "dexes": ["uniswap", "sushiswap"], "min_profit_percentage": 0.3}'
```

### Scan All Major DEXs
```bash
python scripts/main.py --params '{"token_pair": ["DAI", "USDC"], "dexes": ["uniswap", "sushiswap", "curve", "balancer"]}'
```

## Integration

This skill integrates with:
- Uniswap V2 and V3
- SushiSwap
- Curve Finance
- Balancer

## Error Handling

Returns error JSON for:
- Invalid token pair format
- Missing required parameters
- Unsupported DEXs
- Invalid profit threshold

## Track

web3-data-intelligence
