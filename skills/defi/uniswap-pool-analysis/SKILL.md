---
name: uniswap-pool-analysis
description: Analyze Uniswap pool data including liquidity distribution, fee tiers, tick ranges, and TVL. Use when the user asks about pool metrics, liquidity analysis, or wants to query on-chain pool state.
---

# Uniswap Pool Analysis

## Overview

This skill covers querying and analyzing Uniswap v3/v4 pool state on-chain using viem.

## Key Concepts

- **sqrtPriceX96**: Encoded price format used by Uniswap v3/v4. Convert with `price = (sqrtPriceX96 / 2^96)^2`
- **Ticks**: Discrete price points defining liquidity ranges. Tick spacing depends on fee tier.
- **Liquidity**: The `L` value representing active liquidity at the current tick.

## Fee Tiers (v3)

| Fee (bps)   | Tick Spacing | Typical Use      |
| ----------- | ------------ | ---------------- |
| 1 (0.01%)   | 1            | Stablecoin pairs |
| 5 (0.05%)   | 10           | Correlated pairs |
| 30 (0.30%)  | 60           | Standard pairs   |
| 100 (1.00%) | 200          | Exotic pairs     |

## Querying Pool State

Use the Uniswap v3 Pool ABI to read on-chain state:

```typescript
import { createPublicClient, http } from "viem";
import { mainnet } from "viem/chains";

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.ETHEREUM_RPC_URL),
});

// Read slot0 for current price and tick
const [
  sqrtPriceX96,
  tick,
  observationIndex,
  observationCardinality,
  observationCardinalityNext,
  feeProtocol,
  unlocked,
] = await client.readContract({
  address: poolAddress,
  abi: poolAbi,
  functionName: "slot0",
});

// Read liquidity
const liquidity = await client.readContract({
  address: poolAddress,
  abi: poolAbi,
  functionName: "liquidity",
});
```

## Price Conversion

```typescript
function sqrtPriceX96ToPrice(
  sqrtPriceX96: bigint,
  decimals0: number,
  decimals1: number,
): number {
  const price = Number(sqrtPriceX96) / 2 ** 96;
  return (price * price * 10 ** decimals0) / 10 ** decimals1;
}

function tickToPrice(
  tick: number,
  decimals0: number,
  decimals1: number,
): number {
  return (1.0001 ** tick * 10 ** decimals0) / 10 ** decimals1;
}
```

## Liquidity Distribution

To analyze liquidity distribution across ticks:

1. Query `tickBitmap` to find initialized ticks
2. For each initialized tick, read `ticks(tickIndex)` to get `liquidityNet`
3. Walk from `MIN_TICK` to `MAX_TICK`, accumulating net liquidity changes
4. Plot cumulative liquidity vs price for the distribution

## Multi-chain Support

Always accept a `chainId` parameter. Use the shared chain config from `packages/common/` to resolve:

- RPC URL
- Pool factory address
- Quoter address
- Subgraph endpoint (if available)
