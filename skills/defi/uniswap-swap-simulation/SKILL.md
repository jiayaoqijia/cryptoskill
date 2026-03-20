---
name: uniswap-swap-simulation
description: Simulate and analyze Uniswap swaps including price impact, slippage, optimal routing, and gas estimation. Use when the user asks about swap execution, routing, price impact, or MEV considerations.
---

# Uniswap Swap Simulation

## Overview

This skill covers simulating Uniswap swaps, calculating price impact, and analyzing routing decisions.

## Key Concepts

- **Price Impact**: The change in pool price caused by a swap. Larger swaps have higher impact.
- **Slippage**: Difference between expected and executed price, including price movement between submission and execution.
- **Routing**: Finding the optimal path across pools and protocols for best execution.

## Simulating a Swap

Use the Quoter contract to simulate swaps without executing:

```typescript
import { createPublicClient, http, encodeFunctionData } from "viem";

// QuoterV2 for v3 pools
const quote = await client.readContract({
  address: quoterV2Address,
  abi: quoterV2Abi,
  functionName: "quoteExactInputSingle",
  args: [
    {
      tokenIn,
      tokenOut,
      amountIn,
      fee,
      sqrtPriceLimitX96: 0n,
    },
  ],
});

// Returns: [amountOut, sqrtPriceX96After, initializedTicksCrossed, gasEstimate]
```

## Price Impact Calculation

```typescript
function calculatePriceImpact(
  amountIn: bigint,
  amountOut: bigint,
  marketPrice: number, // token1/token0
  decimals0: number,
  decimals1: number,
): number {
  const executionPrice =
    Number(amountOut) / 10 ** decimals1 / (Number(amountIn) / 10 ** decimals0);
  return Math.abs(1 - executionPrice / marketPrice);
}
```

## Slippage Tolerance

- **Stablecoin pairs**: 0.01% - 0.05%
- **Major pairs** (ETH/USDC): 0.1% - 0.5%
- **Volatile pairs**: 0.5% - 1.0%
- **Low liquidity**: 1% - 5%

Calculate minimum amount out:

```typescript
const minAmountOut = (amountOut * (10000n - BigInt(slippageBps))) / 10000n;
```

## Multi-hop Routing

For tokens without direct pools, route through intermediary tokens:

```typescript
// ETH -> USDC -> DAI (two hops)
const path = encodePacked(
  ["address", "uint24", "address", "uint24", "address"],
  [WETH, 3000, USDC, 100, DAI],
);

const quote = await client.readContract({
  address: quoterV2Address,
  abi: quoterV2Abi,
  functionName: "quoteExactInput",
  args: [path, amountIn],
});
```

## Gas Estimation

Typical gas costs by swap complexity:

- Single hop: ~130,000 gas
- Two hops: ~200,000 gas
- Three hops: ~270,000 gas

Always add a 15-20% buffer to gas estimates.

## MEV Considerations

When building swap tools:

- Recommend private RPCs (Flashbots Protect) for large swaps
- Warn users about sandwich attack risk for high-impact swaps
- Suggest using deadline parameters to limit exposure
