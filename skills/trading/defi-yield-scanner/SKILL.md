---
name: defi-yield-scanner
version: 1.0.0
description: Scan DeFi protocols for the best yield opportunities. Covers Aave, Compound, Curve, Yearn, Uniswap v3, and emerging L2 protocols. Compares APY vs risk, tracks TVL changes, and flags new farm openings. Use when you need DeFi yield farming opportunities, protocol APY comparisons, liquidity mining alerts, or stablecoin yield optimization.
author: JamieRossouw
tags: [defi, yield, farming, aave, curve, uniswap, crypto, passive-income]
---

# DeFi Yield Scanner

Autonomous scanner for DeFi yield opportunities across 10+ protocols.

## What It Scans

- **Aave v3** (Polygon, Arbitrum, Base): supply APY, borrow APY, utilization rate
- **Compound v3**: USDC/USDT supply rates, COMP reward APR
- **Curve Finance**: stable pools, CRV emissions, gauge weights
- **Uniswap v3**: fee tier APY for concentrated liquidity positions
- **Yearn Finance**: vault APY including harvesting strategy returns

## Yield Ranking

Each opportunity is scored on:
1. **APY** (raw + adjusted for token emissions)
2. **Risk** (smart contract age, audit status, TVL)
3. **Sustainability** (emission-adjusted vs organic APY)
4. **Gas efficiency** (on Polygon/L2 vs mainnet)

## How to Use

Ask: *"Find the best stable yield on Polygon right now"* or *"Compare USDC yields across Aave, Compound, Curve"*

The agent fetches live APY data, applies risk filters, and returns ranked opportunities with entry instructions.

## Data Sources

- DeFiLlama API (`api.llama.fi`) — TVL, APY, protocol metadata
- Aave subgraph (The Graph)
- Curve registry (`curve.fi/api`)
- Yearn vaults API (`yearn.fi/api`)

## Output Format

```
Protocol | Pool          | APY (base) | APY (rewards) | TVL    | Risk  | Rec
---------|---------------|------------|---------------|--------|-------|-----
Aave v3  | USDC (Polygon)| 2.71%      | 0.00%         | $841M  | LOW   | ✅
Curve    | 3pool         | 1.80%      | 4.20% CRV     | $432M  | LOW   | ✅
Yearn    | USDC vault    | 4.50%      | 0.00%         | $120M  | MED   | ⚠️
```
