---
name: mempool-signal-scan
track: web3-data-intelligence
version: 0.2.0
summary: Real-time mempool scanning with RPC API integration
---

## Description

Real-time mempool signal detection with direct RPC integration. Scans pending transactions for swap and transfer signals, detecting high-value trading opportunities with live gas price data. Supports Ethereum, Polygon, Arbitrum, Optimism, and BSC.

## Inputs (API Mode)

```json
{
  "use_api": true,
  "network": "ethereum",
  "signal_type": "swap",
  "min_value_usd": 100000
}
```

## Inputs (Parameter Mode)

```json
{
  "network": "ethereum",
  "signal_type": "swap",
  "min_value_usd": 100000,
  "signals": [
    {
      "type": "swap",
      "estimated_usd": 250000,
      "from": "0x1234...",
      "to": "0x5678..."
    }
  ]
}
```

## Outputs (API Mode)

```json
{
  "ok": true,
  "data": {
    "source": "mempool_api",
    "network": "ethereum",
    "signal_type": "swap",
    "current_gas_gwei": 45.5,
    "total_pending_txs": 2847,
    "signals_detected": 3,
    "signals": [
      {
        "tx_hash": "abc123def456",
        "from": "0x1234...5678",
        "to": "0xE592...1564",
        "type": "swap",
        "value_eth": 125.5,
        "estimated_usd": 250000.0,
        "gas_price_gwei": 48.5,
        "crosses_threshold": true
      }
    ],
    "scan_timestamp": "2026-02-07T08:30:00Z"
  }
}
```

## Usage

### Fetch Real Mempool Data
```bash
python scripts/main.py --params '{"use_api":true,"network":"ethereum","signal_type":"swap","min_value_usd":100000}'
```

### Fetch Transfers
```bash
python scripts/main.py --params '{"use_api":true,"network":"ethereum","signal_type":"transfer","min_value_usd":500000}'
```

### Analyze Custom Signals
```bash
python scripts/main.py --params '{"network":"polygon","signal_type":"swap","signals":[{"type":"swap","estimated_usd":150000}]}'
```

## Examples

### Example 1: Scan Ethereum Mempool for Swaps
```bash
$ python scripts/main.py --params '{"use_api":true,"network":"ethereum","signal_type":"swap","min_value_usd":100000}'
{
  "ok": true,
  "data": {
    "source": "mempool_api",
    "network": "ethereum",
    "total_pending_txs": 2847,
    "current_gas_gwei": 45.5,
    "signals_detected": 3,
    "signals": [
      {
        "estimated_usd": 250000.0,
        "type": "swap",
        "gas_price_gwei": 48.5
      }
    ]
  }
}
```

### Example 2: Polygon Large Transfers
```bash
$ python scripts/main.py --params '{"use_api":true,"network":"polygon","signal_type":"transfer","min_value_usd":500000}'
{
  "ok": true,
  "data": {
    "source": "mempool_api",
    "network": "polygon",
    "signals_detected": 2
  }
}
```

## Supported Networks

- **ethereum** - Ethereum mainnet
- **polygon** - Polygon mainnet
- **arbitrum** - Arbitrum One
- **optimism** - Optimism mainnet
- **bsc** - Binance Smart Chain

## Signal Types

- **swap** - Uniswap v2/v3, SushiSwap transactions
- **transfer** - Large ERC20 stablecoin transfers
- **all** - Both swaps and transfers
