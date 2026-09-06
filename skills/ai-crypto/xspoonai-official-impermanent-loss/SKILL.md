---
name: impermanent-loss
description: Calculate Impermanent Loss (IL) for Liquidity Provider positions.
version: 1.0.0
author: SpoonOS Contributor
tags: [web3, defi, finance, calculator, yield-farming]
---

# Impermanent Loss Calculator

A financial utility that helps agents quantify the risk of providing liquidity. It calculates the divergence loss experienced when the price ratio of pooled tokens changes.

## Quick Start

```python
# Calculate IL if one token doubles in price (200% or 2.0x ratio change)
il_data = await agent.run_tool(
    "il_calc",
    price_change_ratio=2.0
)
print(il_data)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [il_calc.py](scripts/il_calc.py) | Mathematical calculator for IL scenarios |

## Best Practices

1. Use to audit active LP positions.
2. Combine with 'Yield Calculator' to see if trading fees cover the IL.
