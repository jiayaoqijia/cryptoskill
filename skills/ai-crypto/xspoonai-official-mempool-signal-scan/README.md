# mempool-signal-scan

Real-time mempool scanning with RPC API integration for trading signals and MEV opportunities.

## Overview

This skill monitors pending transactions in the mempool using direct RPC calls to identify profitable opportunities including large swaps and stablecoin transfers. Detects DEX router interactions and high-value transactions in real-time.

## Features

- ✅ **RPC Mempool Integration**: Fetch live pending transactions via txpool_content
- ✅ **Real Gas Price Data**: Current gas price from network RPC
- ✅ **Swap Detection**: Identifies Uniswap v2/v3 and SushiSwap transactions
- ✅ **Transfer Detection**: Tracks large stablecoin transfers
- ✅ **Dual-mode Operation**: API mode (live data) + parameter mode (custom signals)
- ✅ **Multi-network Support**: Ethereum, Polygon, Arbitrum, Optimism, BSC
- ✅ **Value Thresholds**: Filter signals by minimum USD value

## Usage

### Fetch Real Mempool Data
```bash
python scripts/main.py --params '{"use_api":true,"network":"ethereum","signal_type":"swap","min_value_usd":100000}'
```

### Detect Transfers
```bash
python scripts/main.py --params '{"use_api":true,"network":"ethereum","signal_type":"transfer","min_value_usd":500000}'
```

### Analyze Custom Signals
```bash
python scripts/main.py --params '{"network":"polygon","signal_type":"swap","signals":[{"type":"swap","estimated_usd":150000}]}'
```

## Parameters

### API Mode
- `use_api` (boolean): Set to true to fetch live mempool data
- `network` (string, required): ethereum, polygon, arbitrum, optimism, bsc
- `signal_type` (string): swap, transfer, or all
- `min_value_usd` (number): Minimum transaction value in USD

### Parameter Mode
- `network` (string, required): Target network
- `signal_type` (string): swap, transfer, or all
- `min_value_usd` (number): Threshold value
- `signals` (array): Custom signal data to analyze

## Output

Returns JSON with:
- `source`: Data source (mempool_api or parameters)
- `network`: Target blockchain
- `current_gas_gwei`: Live gas price
- `total_pending_txs`: Count of pending transactions
- `signals_detected`: Number of signals above threshold
- `signals`: Array of detected trading opportunities
  - `from`: Sender address
  - `to`: Target address (DEX router)
  - `type`: swap or transfer
  - `value_eth`: ETH amount
  - `estimated_usd`: USD value estimate
  - `gas_price_gwei`: Transaction gas price

## Examples

### Ethereum Mempool Scan
```bash
python scripts/main.py --params '{"use_api":true,"network":"ethereum","signal_type":"swap"}'
```

### Polygon Liquidation Watch
```bash
python scripts/main.py --params '{"use_api":true,"network":"polygon","signal_type":"transfer","min_value_usd":1000000}'
```

## Supported Networks

- **ethereum** - Eth.llamarpc.com RPC
- **polygon** - Polygon-rpc.com
- **arbitrum** - Arbitrum One (arb1.arbitrum.io)
- **optimism** - Optimism mainnet
- **bsc** - Binance Smart Chain

## Track

web3-data-intelligence
