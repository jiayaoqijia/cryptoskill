---
name: gas-spike-monitor
track: web3-data-intelligence
version: 0.1.0
summary: Monitor gas price spikes across blockchain networks with real-time RPC data
---

## Description

Monitor gas price spikes across blockchain networks including Ethereum, Polygon, Arbitrum, Optimism, and BSC. Compares current gas prices against baseline values and triggers alerts when spikes exceed configured thresholds with live RPC integration.

## Inputs

```json
{
  "network": "ethereum",
  "current_gas_gwei": 85,
  "baseline_gas_gwei": 30,
  "spike_threshold_percentage": 50,
  "use_live_prices": false
}
```

## Inputs (Live Mode)

```json
{
  "network": "ethereum",
  "baseline_gas_gwei": 30,
  "spike_threshold_percentage": 50,
  "use_live_prices": true
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "network": "ethereum",
    "current_gas_gwei": 85.0,
    "baseline_gas_gwei": 30.0,
    "spike_percentage": 183.33,
    "spike_threshold_percentage": 50,
    "is_spike": true,
    "status": "critical",
    "alert_triggered": true,
    "price_source": "provided",
    "recommendation": "⚠️ CRITICAL: Gas prices extremely high. Wait for network congestion to clear.",
    "check_timestamp": "2026-02-07T08:30:00Z"
  }
}
```

## Usage

### With Provided Prices
```bash
python scripts/main.py --params '{"network":"ethereum","current_gas_gwei":85,"baseline_gas_gwei":30,"spike_threshold_percentage":50}'
```

### With Live RPC Fetching
```bash
python scripts/main.py --params '{"network":"ethereum","baseline_gas_gwei":30,"use_live_prices":true,"spike_threshold_percentage":50}'
```

## Examples

### Example 1: Ethereum Spike Detection
```bash
$ python scripts/main.py --params '{"network":"ethereum","current_gas_gwei":120,"baseline_gas_gwei":30,"spike_threshold_percentage":50}'
{
  "ok": true,
  "data": {
    "network": "ethereum",
    "current_gas_gwei": 120.0,
    "baseline_gas_gwei": 30.0,
    "spike_percentage": 300.0,
    "status": "critical",
    "is_spike": true,
    "alert_triggered": true,
    "price_source": "provided",
    "recommendation": "⚠️ CRITICAL: Gas prices extremely high. Wait for network congestion to clear.",
    "check_timestamp": "2026-02-07T08:30:00Z"
  }
}
```

### Example 2: Polygon Normal Conditions
```bash
$ python scripts/main.py --params '{"network":"polygon","current_gas_gwei":45,"baseline_gas_gwei":50,"spike_threshold_percentage":25}'
{
  "ok": true,
  "data": {
    "network": "polygon",
    "current_gas_gwei": 45.0,
    "baseline_gas_gwei": 50.0,
    "spike_percentage": -10.0,
    "status": "normal",
    "is_spike": false,
    "alert_triggered": false,
    "price_source": "provided",
    "recommendation": "✓ Normal: Gas prices within acceptable range.",
    "check_timestamp": "2026-02-07T08:30:00Z"
  }
}
```

### Example 3: Live Ethereum Price Check
```bash
$ python scripts/main.py --params '{"network":"ethereum","baseline_gas_gwei":40,"use_live_prices":true,"spike_threshold_percentage":75}'
{
  "ok": true,
  "data": {
    "network": "ethereum",
    "current_gas_gwei": 52.5,
    "baseline_gas_gwei": 40.0,
    "spike_percentage": 31.25,
    "status": "elevated",
    "is_spike": false,
    "alert_triggered": false,
    "price_source": "live_rpc",
    "recommendation": "⚠️ ELEVATED: Gas prices above normal. Consider batching transactions or using L2.",
    "check_timestamp": "2026-02-07T08:30:00Z"
  }
}
```

## Error Handling

When an error occurs, the skill returns:

```json
{
  "ok": false,
  "error": "Error description",
  "details": "Additional context"
}
```

## Supported Networks

- **ethereum**: Ethereum mainnet
- **polygon**: Polygon PoS
- **arbitrum**: Arbitrum One
- **optimism**: Optimism mainnet
- **bsc**: Binance Smart Chain
