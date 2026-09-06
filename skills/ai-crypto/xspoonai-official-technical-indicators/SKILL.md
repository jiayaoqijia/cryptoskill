---
name: technical-indicators
description: Calculate trading indicators (RSI, SMA, EMA) from price data.
version: 1.0.0
author: SpoonOS Contributor
tags: [web3, trading, finance, analysis, market]
---

# Technical Indicators

Gives SpoonOS agents the ability to perform Technical Analysis (TA). It takes raw price arrays (which can be fetched via other skills) and computes standard indicators like Relative Strength Index (RSI) and Moving Averages.

## Quick Start

```python
# Calculate RSI for a price history
indicators = await agent.run_tool(
    "calc_indicators",
    prices=[100, 102, 101, 105, 110, ...]
)
print(f"RSI: {indicators['rsi']}")
```

## Scripts

| Script | Purpose |
|--------|---------|
| [indicators.py](scripts/indicators.py) | Math engine for trading signals |

## Best Practices

1. Use consistent timeframes (e.g., all 1-hour candle closes) for the input list.
2. Combine multiple indicators (e.g., RSI < 30 AND Price > SMA) for stronger signals.
