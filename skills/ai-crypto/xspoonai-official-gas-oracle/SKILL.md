---
name: gas-oracle
description: Analyze gas price history and predict optimal transaction fees.
version: 1.0.0
author: SpoonOS Contributor
tags: [web3, gas, ethereum, optimization, cost-saving]
---

# Gas Price Oracle

A data intelligence skill that analyzes blockchain gas fee history to recommend optimal gas prices. It helps agents decide whether to execute a transaction now or wait for lower fees.

## Quick Start

```python
# Check if gas is low enough to transact
gas_report = await agent.run_tool(
    "gas_tracker",
    action="check_status",
    threshold_gwei=20
)
print(gas_report)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [gas_tracker.py](scripts/gas_tracker.py) | Fetches `eth_feeHistory` and calculates percentiles |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WEB3_RPC_URL` | Yes | RPC URL to fetch fee history |

## Best Practices

1. Use before high-cost interactions (like contract deployment).
2. Set `maxPriorityFeePerGas` based on the 'fast' recommendation for urgent txs.
