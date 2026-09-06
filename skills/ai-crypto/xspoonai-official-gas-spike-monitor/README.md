# gas-spike-monitor

Monitor gas prices and detect price spikes across different blockchain networks using real-time RPC data.

## Overview

This skill monitors gas prices on multiple blockchain networks and detects significant spikes by comparing current prices against baseline values. It provides real-time alerts and actionable recommendations for transaction execution.

## Features

- ✅ Real-time gas price monitoring from Ethereum RPC
- ✅ Multi-network support (Ethereum, Polygon, Arbitrum, Optimism, BSC)
- ✅ Live price fetching with optional `use_live_prices` flag
- ✅ Spike detection with customizable percentage thresholds
- ✅ Status categorization (critical/elevated/normal)
- ✅ Comprehensive parameter validation
- ✅ Network-specific RPC endpoints

## Usage

### With Provided Prices
```bash
python scripts/main.py --params '{"network":"ethereum","current_gas_gwei":85,"baseline_gas_gwei":30,"spike_threshold_percentage":50}'
```

### With Live RPC Fetching
```bash
python scripts/main.py --params '{"network":"ethereum","baseline_gas_gwei":30,"use_live_prices":true,"spike_threshold_percentage":50}'
```

### Monitor Polygon
```bash
python scripts/main.py --params '{"network":"polygon","current_gas_gwei":120,"baseline_gas_gwei":50,"spike_threshold_percentage":75}'
```

## Parameters

- `network` (string, required): Blockchain network (ethereum, polygon, arbitrum, optimism, bsc)
- `current_gas_gwei` (number, required if not using live_prices): Current gas price in Gwei
- `baseline_gas_gwei` (number, required): Baseline/normal gas price in Gwei for comparison
- `spike_threshold_percentage` (number, optional): Spike trigger threshold (default: 25)
- `use_live_prices` (boolean, optional): Fetch live prices from RPC (default: false)
- `average_baseline` (number, optional): Default baseline if none provided (default: 30)

## Output

Returns JSON with:
- `network`: Blockchain network identifier
- `current_gas_gwei`: Current or fetched gas price
- `baseline_gas_gwei`: Baseline price used for comparison
- `spike_percentage`: Calculated percentage change
- `is_spike`: Boolean alert trigger status
- `status`: Status level (critical/elevated/normal)
- `alert_triggered`: Alert flag
- `price_source`: Source of price data (provided/live_rpc)
- `recommendation`: Action guidance
- `check_timestamp`: ISO timestamp of check

## Supported Networks

- **ethereum**: Ethereum mainnet (eth.llamarpc.com)
- **polygon**: Polygon PoS (polygon-rpc.com)  
- **arbitrum**: Arbitrum One (arb1.arbitrum.io)
- **optimism**: Optimism mainnet (mainnet.optimism.io)
- **bsc**: Binance Smart Chain (bsc-dataseed1.binance.org)

## Status Levels

- **critical**: Spike > 50% above baseline - immediate action needed
- **elevated**: Spike >= threshold but < 50% - caution recommended
- **normal**: Spike < threshold - no alert

## Error Handling

Returns error JSON for:
- Invalid/unsupported network
- Missing required parameters
- RPC endpoint unreachable (if using live_prices)
- Invalid parameter types

## Track

web3-data-intelligence
