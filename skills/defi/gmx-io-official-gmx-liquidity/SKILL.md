---
name: gmx-liquidity
description: Provide liquidity on GMX V2 — deposit into GM pools and GLV vaults, withdraw, shift between pools, and query pool data across Arbitrum, Avalanche, and Botanix.
license: MIT
metadata:
  author: gmx-io
  version: "0.1"
  chains: "arbitrum, avalanche, botanix"
---

# GMX Liquidity Skill

## Overview

GMX V2 has two liquidity layers that back perpetual and spot trading:

- **GM Pools** — Single-market liquidity pools. Each GM pool backs one market (e.g., ETH/USD) and is composed of a long token and short token. Depositing mints GM tokens (LP tokens); withdrawing burns them.
- **GLV Vaults** (GMX Liquidity Vaults) — Multi-market vaults that hold multiple GM tokens and auto-rebalance across constituent pools. Depositing mints GLV tokens; withdrawing burns them.

**Supported chains:**
| Chain | Chain ID | Native Token | GLV Vaults |
|-------|----------|-------------|------------|
| Arbitrum | 42161 | ETH | Yes |
| Avalanche | 43114 | AVAX | Yes |
| Botanix | 3637 | BTC | No (contracts deployed, no vaults configured) |

**Execution model:** All write operations use a two-step async pattern:
1. User creates a request (deposit/withdrawal/shift) via `ExchangeRouter` or `GlvRouter` multicall
2. Keeper executes the request with oracle prices (typically 1–30 seconds later)

The user pays an execution fee (in native token) upfront to cover keeper gas costs. Excess fee is refunded.

**Integration paths:**
- **SDK** (`@gmx-io/sdk`) — Read pool data, balances, and market info. Write operations (deposit/withdraw) are not yet in the SDK.
- **Contract-level** (viem) — Full read + write via `ExchangeRouter.multicall()` and `GlvRouter.multicall()`.

This skill complements [gmx-trading](../gmx-trading/SKILL.md) which covers perpetual trading and swaps.

## GM Pools

Each GM pool is a pair of tokens backing a specific market:
- **Long token** — The asset (e.g., WETH for ETH/USD)
- **Short token** — The stablecoin (e.g., USDC)
- **GM token** — The LP token representing a share of the pool

**Deposits** can be:
- **Balanced** — Deposit both long and short tokens proportionally. Lower fees (helps balance the pool).
- **Single-sided** — Deposit only one token. The protocol swaps a portion internally. Higher fees if it imbalances the pool.

**Withdrawals** burn GM tokens and return the underlying long and short tokens. A withdrawal can specify `minLongTokenAmount` and `minShortTokenAmount` for slippage protection.

**Pricing:** GM token price = pool value / GM token supply. Pool value is the sum of long and short token values at oracle prices plus accrued PnL.

GM pool addresses are dynamic — discover them via `sdk.markets.getMarkets()`.

## GLV Vaults

GLV vaults hold multiple GM tokens and auto-rebalance across markets:

**Known GLV vaults** (source: [`sdk/src/configs/markets.ts`](https://github.com/gmx-io/gmx-interface/blob/release/sdk/src/configs/markets.ts)):
| Chain | Vault | Long Token | Short Token | Address |
|-------|-------|-----------|-------------|---------|
| Arbitrum | GLV [WETH-USDC] | WETH | USDC | `0x528A5bac7E746C9A509A1f4F6dF58A03d44279F9` |
| Arbitrum | GLV [WBTC-USDC] | WBTC | USDC | `0xdF03EEd325b82bC1d4Db8b49c30ecc9E05104b96` |
| Avalanche | GLV [WAVAX-USDC] | WAVAX | USDC | `0x901eE57f7118A7be56ac079cbCDa7F22663A3874` |

**Deposit modes:**
- **Raw tokens** — Deposit long/short tokens. The vault creates a GM deposit into the selected constituent market, then deposits the resulting GM tokens into the GLV.
- **GM tokens** — Deposit existing GM tokens directly (`isMarketTokenDeposit: true`). Skips the intermediate deposit step.

**Withdrawals** burn GLV tokens. The vault withdraws from the specified constituent market and returns the underlying long/short tokens.

## Reading Pool Data (SDK)

Use `sdk.markets.getMarketsInfo()` to query all pool data:

```typescript
const { GmxSdk } = require("@gmx-io/sdk");

const sdk = new GmxSdk({
  chainId: 42161,
  rpcUrl: "https://arb1.arbitrum.io/rpc",
  oracleUrl: "https://arbitrum-api.gmxinfra.io",
  subsquidUrl: "https://gmx.squids.live/gmx-synthetics-arbitrum:prod/api/graphql",
});

const { marketsInfoData, tokensData } = await sdk.markets.getMarketsInfo();

// Find a specific pool
const ethPool = Object.values(marketsInfoData).find(
  (m) => tokensData[m.indexTokenAddress]?.symbol === "WETH" && !m.isSpotOnly
);

// Pool liquidity data
console.log("Long pool:", ethPool.longPoolAmount);       // Long token amount in pool
console.log("Short pool:", ethPool.shortPoolAmount);      // Short token amount in pool
console.log("Pool value (max):", ethPool.poolValueMax);   // Total pool value USD
console.log("Pool value (min):", ethPool.poolValueMin);

// Pool capacity
console.log("Max long:", ethPool.maxLongPoolAmount);      // Max long token capacity
console.log("Max short:", ethPool.maxShortPoolAmount);     // Max short token capacity

// GM token address
console.log("Market token:", ethPool.marketTokenAddress);
```

**Check GM token balances:**

```typescript
const { tokensData } = await sdk.tokens.getTokensBalances();
// GM tokens appear as regular tokens — filter by market token addresses
```

**List all pools:**

```typescript
const { marketsInfoData, tokensData } = await sdk.markets.getMarketsInfo();

for (const market of Object.values(marketsInfoData)) {
  const indexSymbol = tokensData[market.indexTokenAddress]?.symbol ?? "SPOT";
  const longSymbol = tokensData[market.longTokenAddress]?.symbol;
  const shortSymbol = tokensData[market.shortTokenAddress]?.symbol;
  console.log(`${indexSymbol}: ${longSymbol}/${shortSymbol} — Pool: ${market.poolValueMax}`);
}
```

## Reading Pool Data (REST / GraphQL)

**REST API** — Get market info including pool sizes:

```
GET https://arbitrum-api.gmxinfra.io/markets/info
```

Returns extended market data including pool sizes, utilization, open interest, and fee factors.

**GraphQL (Subsquid)** — Query historical deposit/withdrawal events:

| Chain | Endpoint |
|-------|----------|
| Arbitrum | `https://gmx.squids.live/gmx-synthetics-arbitrum:prod/api/graphql` |
| Avalanche | `https://gmx.squids.live/gmx-synthetics-avalanche:prod/api/graphql` |
| Botanix | `https://gmx.squids.live/gmx-synthetics-botanix:prod/api/graphql` |

## Prerequisites for Write Operations

Before calling `ExchangeRouter.multicall()` or `GlvRouter.multicall()`:

**1. Token approvals:**
- For **all operations** (GM and GLV): approve tokens to `SyntheticsRouter`
- This applies to GM deposits/withdrawals/shifts via `ExchangeRouter` and GLV deposits/withdrawals via `GlvRouter`

```typescript
// Approve USDC to SyntheticsRouter (works for both GM and GLV operations)
await usdcContract.write.approve([syntheticsRouterAddress, amount]);
```

**2. Default parameter values:**
```typescript
callbackContract: zeroAddress,   // No callback
callbackGasLimit: 0n,            // No callback gas
dataList: [],                     // Reserved for future use
uiFeeReceiver: zeroAddress,      // No UI fee (set to your address if building a frontend)
```

**3. Native token handling:**
When depositing the wrapped native token (WETH on Arbitrum, WAVAX on Avalanche, PBTC on Botanix) and `shouldUnwrapNativeToken` is true, add the deposit amount to the `sendWnt` call value instead of using `sendTokens`. The `sendWnt` call wraps native token automatically.

```typescript
// If depositing ETH (native) on Arbitrum:
const wntAmount = executionFee + longTokenAmount; // execution fee + deposit amount
// Use sendWnt for the full amount, skip sendTokens for the long token
```

**4. Slippage:**
Apply slippage client-side before passing to the contract:
```typescript
// Apply 0.3% slippage to minimum output
const minMarketTokens = expectedMarketTokens * 997n / 1000n;
```

## Execution Fee Calculation

All operations require an execution fee in native token. The formula is the same for all operations:

```
estimatedGasLimit = (per-operation formula)
oraclePriceCount = (per-operation formula)

// adjustGasLimitForEstimate (mirrors contract logic)
gasLimit = estimatedGasFeeBaseAmount
         + (estimatedGasFeePerOraclePrice × oraclePriceCount)
         + applyFactor(estimatedGasLimit, estimatedFeeMultiplierFactor)

executionFee = gasLimit × gasPrice
```

**Per-operation formulas:**

| Operation | estimatedGasLimit | oraclePriceCount |
|-----------|------------------|-----------------|
| GM Deposit | `depositToken + swaps × singleSwap` | `3 + swapsCount` |
| GM Withdrawal | `withdrawalMultiToken + swaps × singleSwap` | `3 + swapsCount` |
| Shift | `shift` | `4` |
| GLV Deposit (raw tokens) | `glvDepositGasLimit + markets × glvPerMarketGasLimit + depositToken + swaps × singleSwap` | `2 + marketsCount + swapsCount` |
| GLV Deposit (GM tokens) | `glvDepositGasLimit + markets × glvPerMarketGasLimit` | `2 + marketsCount` |
| GLV Withdrawal | `glvWithdrawalGasLimit + markets × glvPerMarketGasLimit + withdrawalMultiToken + swaps × singleSwap` | `2 + marketsCount + swapsCount` |

**Important: `marketsCount` for GLV operations.**
GLV vaults contain many constituent GM markets — GLV [WETH-USDC] on Arbitrum has **40+ markets**. The contract validates the execution fee against the actual constituent count, and reverts with `InsufficientExecutionFee` if too low. The SDK does not expose a method to query the GLV constituent market count. Use these values:

| GLV Vault | Chain | Recommended `marketsCount` |
|-----------|-------|---------------------------|
| GLV [WETH-USDC] | Arbitrum | 53 |
| GLV [WBTC-USDC] | Arbitrum | 53 |
| GLV [WAVAX-USDC] | Avalanche | 20 |

Excess execution fee is always refunded, so overestimating `marketsCount` is safe. GLV execution fees are typically ~0.001 ETH — roughly 10x higher than GM operations (~0.0001 ETH) due to the large number of constituent markets.

**Using the SDK to get gas parameters:**

```typescript
const gasLimits = await sdk.utils.getGasLimits();
const gasPrice = await sdk.utils.getGasPrice();

// --- Per-operation gas limit field names from sdk.utils.getGasLimits() ---
// GM Deposit:       gasLimits.depositToken
// GM Withdrawal:    gasLimits.withdrawalMultiToken
// Shift:            gasLimits.shift
// GLV per-market:   gasLimits.glvPerMarketGasLimit
// GLV Deposit:      gasLimits.glvDepositGasLimit
// GLV Withdrawal:   gasLimits.glvWithdrawalGasLimit
// Swap (per swap):  gasLimits.singleSwap
// Base fee fields:  gasLimits.estimatedGasFeeBaseAmount,
//                   gasLimits.estimatedGasFeePerOraclePrice,
//                   gasLimits.estimatedFeeMultiplierFactor

function calculateExecutionFee(estimatedGasLimit: bigint, oraclePriceCount: bigint): bigint {
  let gasLimit = gasLimits.estimatedGasFeeBaseAmount;
  gasLimit += gasLimits.estimatedGasFeePerOraclePrice * oraclePriceCount;
  gasLimit += estimatedGasLimit * gasLimits.estimatedFeeMultiplierFactor / 10n ** 30n;
  return gasLimit * gasPrice;
}

// Example: GM deposit (no swaps)
const gmDepositFee = calculateExecutionFee(gasLimits.depositToken, 3n);

// Example: GLV deposit (raw tokens, 53 markets, no swaps)
const marketsCount = 53n;
const glvDepositGas = gasLimits.glvDepositGasLimit
  + marketsCount * gasLimits.glvPerMarketGasLimit
  + gasLimits.depositToken;
const glvDepositFee = calculateExecutionFee(glvDepositGas, 2n + marketsCount);
```

## Depositing into GM Pools

Use `ExchangeRouter.multicall()` to batch send tokens + create deposit in one transaction:

```typescript
import { encodeFunctionData, zeroAddress } from "viem";

const exchangeRouterAddress = "0x1C3fa76e6E1088bCE750f23a5BFcffa1efEF6A41"; // Arbitrum
const depositVaultAddress = "0xF89e77e8Dc11691C9e8757e84aaFbCD8A67d7A55";   // Arbitrum

// Step 1: Approve tokens to SyntheticsRouter (one-time)
// await longToken.write.approve([syntheticsRouterAddress, longTokenAmount]);
// await shortToken.write.approve([syntheticsRouterAddress, shortTokenAmount]);

// Step 2: Build multicall
const wntAmount = executionFee; // Add longTokenAmount if depositing native token

const multicall = [
  encodeFunctionData({
    abi: exchangeRouterAbi,
    functionName: "sendWnt",
    args: [depositVaultAddress, wntAmount],
  }),
  encodeFunctionData({
    abi: exchangeRouterAbi,
    functionName: "sendTokens",
    args: [longTokenAddress, depositVaultAddress, longTokenAmount],
  }),
  encodeFunctionData({
    abi: exchangeRouterAbi,
    functionName: "sendTokens",
    args: [shortTokenAddress, depositVaultAddress, shortTokenAmount],
  }),
  encodeFunctionData({
    abi: exchangeRouterAbi,
    functionName: "createDeposit",
    args: [{
      addresses: {
        receiver: account.address,
        callbackContract: zeroAddress,
        uiFeeReceiver: zeroAddress,
        market: marketTokenAddress,         // GM pool address
        initialLongToken: longTokenAddress,
        initialShortToken: shortTokenAddress,
        longTokenSwapPath: [],
        shortTokenSwapPath: [],
      },
      minMarketTokens: minGmTokensOut,      // Apply slippage
      shouldUnwrapNativeToken: false,
      executionFee: executionFee,
      callbackGasLimit: 0n,
      dataList: [],
    }],
  }),
];

// Step 3: Send transaction
const hash = await walletClient.writeContract({
  address: exchangeRouterAddress,
  abi: exchangeRouterAbi,
  functionName: "multicall",
  args: [multicall],
  value: wntAmount,
});
```

**Native token deposits:** If depositing WETH/WAVAX/PBTC with `shouldUnwrapNativeToken: true`, add the deposit amount to `wntAmount` (`executionFee + longTokenAmount`) and skip the `sendTokens` call for that token. The `sendWnt` call wraps native ETH/AVAX/BTC automatically.

## Withdrawing from GM Pools

```typescript
const withdrawalVaultAddress = "0x0628D46b5D145f183AdB6Ef1f2c97eD1C4701C55"; // Arbitrum

// Approve GM tokens to SyntheticsRouter first
// await gmToken.write.approve([syntheticsRouterAddress, marketTokenAmount]);

const multicall = [
  encodeFunctionData({
    abi: exchangeRouterAbi,
    functionName: "sendWnt",
    args: [withdrawalVaultAddress, executionFee], // Only execution fee, no deposit
  }),
  encodeFunctionData({
    abi: exchangeRouterAbi,
    functionName: "sendTokens",
    args: [marketTokenAddress, withdrawalVaultAddress, marketTokenAmount], // GM tokens
  }),
  encodeFunctionData({
    abi: exchangeRouterAbi,
    functionName: "createWithdrawal",
    args: [{
      addresses: {
        receiver: account.address,
        callbackContract: zeroAddress,
        uiFeeReceiver: zeroAddress,
        market: marketTokenAddress,
        longTokenSwapPath: [],
        shortTokenSwapPath: [],
      },
      minLongTokenAmount: minLongOut,       // Apply slippage
      minShortTokenAmount: minShortOut,     // Apply slippage
      shouldUnwrapNativeToken: true,        // Unwrap WETH to ETH on receive
      executionFee: executionFee,
      callbackGasLimit: 0n,
      dataList: [],
    }],
  }),
];

const hash = await walletClient.writeContract({
  address: exchangeRouterAddress,
  abi: exchangeRouterAbi,
  functionName: "multicall",
  args: [multicall],
  value: executionFee,
});
```

## GLV Deposits

Use `GlvRouter.multicall()` (not ExchangeRouter):

```typescript
const glvRouterAddress = "0x7EAdEE2ca1b4D06a0d82fDF03D715550c26AA12F";  // Arbitrum
const glvVaultAddress = "0x393053B58f9678C9c28c2cE941fF6cac49C3F8f9";   // Arbitrum

// Approve tokens to SyntheticsRouter (same as GM operations)

const multicall = [
  encodeFunctionData({
    abi: glvRouterAbi,
    functionName: "sendWnt",
    args: [glvVaultAddress, wntAmount],
  }),
  encodeFunctionData({
    abi: glvRouterAbi,
    functionName: "sendTokens",
    args: [longTokenAddress, glvVaultAddress, longTokenAmount],
  }),
  encodeFunctionData({
    abi: glvRouterAbi,
    functionName: "createGlvDeposit",
    args: [{
      addresses: {
        glv: glvTokenAddress,                // GLV vault address
        market: constituentMarketAddress,    // Which GM market to deposit through
        receiver: account.address,
        callbackContract: zeroAddress,
        uiFeeReceiver: zeroAddress,
        initialLongToken: longTokenAddress,
        initialShortToken: shortTokenAddress,
        longTokenSwapPath: [],
        shortTokenSwapPath: [],
      },
      minGlvTokens: minGlvTokensOut,        // Note: minGlvTokens, not minMarketTokens
      executionFee: executionFee,
      callbackGasLimit: 0n,
      shouldUnwrapNativeToken: false,
      isMarketTokenDeposit: false,           // true if depositing GM tokens directly
      dataList: [],
    }],
  }),
];

const hash = await walletClient.writeContract({
  address: glvRouterAddress,
  abi: glvRouterAbi,
  functionName: "multicall",
  args: [multicall],
  value: wntAmount,
});
```

**Depositing GM tokens directly:** Set `isMarketTokenDeposit: true` and send GM tokens to `GlvVault` instead of long/short tokens. This skips the intermediate GM deposit step and uses less gas.

## GLV Withdrawals

```typescript
// Approve GLV tokens to SyntheticsRouter first

const multicall = [
  encodeFunctionData({
    abi: glvRouterAbi,
    functionName: "sendWnt",
    args: [glvVaultAddress, executionFee],
  }),
  encodeFunctionData({
    abi: glvRouterAbi,
    functionName: "sendTokens",
    args: [glvTokenAddress, glvVaultAddress, glvTokenAmount], // GLV tokens
  }),
  encodeFunctionData({
    abi: glvRouterAbi,
    functionName: "createGlvWithdrawal",
    args: [{
      addresses: {
        receiver: account.address,
        callbackContract: zeroAddress,
        uiFeeReceiver: zeroAddress,
        market: constituentMarketAddress,    // Which GM market to withdraw from
        glv: glvTokenAddress,
        longTokenSwapPath: [],
        shortTokenSwapPath: [],
      },
      minLongTokenAmount: minLongOut,
      minShortTokenAmount: minShortOut,
      shouldUnwrapNativeToken: true,
      executionFee: executionFee,
      callbackGasLimit: 0n,
      dataList: [],
    }],
  }),
];

const hash = await walletClient.writeContract({
  address: glvRouterAddress,
  abi: glvRouterAbi,
  functionName: "multicall",
  args: [multicall],
  value: executionFee,
});
```

## Shift Operations

Shifts move GM tokens from one pool to another atomically — without withdrawing first. Lower fees than manual withdraw + deposit.

```typescript
const shiftVaultAddress = "0xfe99609C4AA83ff6816b64563Bdffd7fa68753Ab"; // Arbitrum

// Approve from-market GM tokens to SyntheticsRouter first

const multicall = [
  encodeFunctionData({
    abi: exchangeRouterAbi,
    functionName: "sendWnt",
    args: [shiftVaultAddress, executionFee],
  }),
  encodeFunctionData({
    abi: exchangeRouterAbi,
    functionName: "sendTokens",
    args: [fromMarketTokenAddress, shiftVaultAddress, fromMarketTokenAmount],
  }),
  encodeFunctionData({
    abi: exchangeRouterAbi,
    functionName: "createShift",
    args: [{
      addresses: {
        receiver: account.address,
        callbackContract: zeroAddress,
        uiFeeReceiver: zeroAddress,
        fromMarket: fromMarketTokenAddress,
        toMarket: toMarketTokenAddress,
      },
      minMarketTokens: minToMarketTokens,  // Apply slippage
      executionFee: executionFee,
      callbackGasLimit: 0n,
      dataList: [],
    }],
  }),
];

const hash = await walletClient.writeContract({
  address: exchangeRouterAddress,
  abi: exchangeRouterAbi,
  functionName: "multicall",
  args: [multicall],
  value: executionFee,
});
```

Note: `CreateShiftParams` does not have a `shouldUnwrapNativeToken` field (unlike deposit/withdrawal).

## Cancelling Pending Operations

If a request hasn't been executed by a keeper yet, the creator can cancel it using the request key (bytes32) returned by the create function:

**Via ExchangeRouter:**
```typescript
await walletClient.writeContract({
  address: exchangeRouterAddress,
  abi: exchangeRouterAbi,
  functionName: "cancelDeposit",    // or cancelWithdrawal, cancelShift
  args: [requestKey],
});
```

**Via GlvRouter:**
```typescript
await walletClient.writeContract({
  address: glvRouterAddress,
  abi: glvRouterAbi,
  functionName: "cancelGlvDeposit",  // or cancelGlvWithdrawal
  args: [requestKey],
});
```

Cancellation refunds tokens to the receiver address. Only the account that created the request can cancel it.

## Fees

**Deposit/withdrawal fees:** Same balancing incentive model as swap fees. Deposits that balance the pool (move it closer to 50/50) pay lower fees. Deposits that imbalance the pool pay higher fees. The fee is deducted from the minted GM/GLV tokens.

**Execution fees:** Paid in native token upfront. Covers keeper gas costs. Calculated using the formula in the [Execution Fee Calculation](#execution-fee-calculation) section. Excess fee is refunded to the receiver.

## Limitations

- **SDK write operations:** `@gmx-io/sdk` does not yet expose convenience methods for deposit/withdraw/shift. Use contract-level multicall as shown above.
- **APY:** Not directly exposed via API. Derived client-side from trading fees, borrowing rates, and funding rates flowing through each pool.
- **GLV on Botanix:** GLV contracts are deployed on Botanix but no vaults are configured yet. GM pool operations work on all three chains.
- **Multichain deposits:** Cross-chain deposits (from a different chain via LayerZero) are not covered in this skill.
- **Atomic withdrawals:** `ExchangeRouter.executeAtomicWithdrawal()` exists but requires oracle price params — intended for advanced/keeper use.

## References

- [Liquidity Operations Reference](references/liquidity-operations.md) — Contract structs, flows, gas formulas, GLV addresses
- [Contract Addresses](../gmx-trading/references/contract-addresses.md) — All deployed contracts per chain (shared with gmx-trading)
- [SDK Reference](../gmx-trading/references/sdk-reference.md) — SDK module and method documentation (shared with gmx-trading)
- [API Endpoints](../gmx-trading/references/api-endpoints.md) — Oracle, OpenAPI, and GraphQL endpoints (shared with gmx-trading)
- [GMX Documentation](https://docs.gmx.io) — Official protocol documentation
- [GMX App — Pools](https://app.gmx.io/#/pools) — GM pool interface
- [GMX App — Vaults](https://app.gmx.io/#/vaults) — GLV vault interface
- [`@gmx-io/sdk` on npm](https://www.npmjs.com/package/@gmx-io/sdk) — SDK package
