---
name: yield-calc
description: Project future returns based on APY and compounding.
version: 1.0.0
author: SpoonOS Contributor
tags: [web3, defi, investment, planning, compound-interest]
---

# Yield Calculator

A forecasting skill for DeFi agents. It converts APR to APY, handles compounding frequency, and projects the future value of a crypto investment.

## Quick Start

```python
# Project returns for $1000 at 50% APR for 1 year
projection = await agent.run_tool(
    "calc_yield",
    principal=1000,
    apr_percent=50,
    days=365
)
print(projection)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [yield_projector.py](scripts/yield_projector.py) | Investment forecasting engine |

## Best Practices

1. Use to compare DeFi pools (e.g., "Pool A vs Pool B").
2. Remember that DeFi rates fluctuate; this provides a theoretical projection.
