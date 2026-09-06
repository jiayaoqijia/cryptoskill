---
name: swap-integration
slug: pcs-swap-integration
description: Integrate PancakeSwap swaps into applications. Use when user says "integrate swaps", "pancakeswap", "smart router", "add swap functionality", "build a swap frontend", "create a swap script", "smart contract swap integration", "use Universal Router", or mentions swapping tokens via PancakeSwap.
homepage: https://github.com/pancakeswap/pancakeswap-ai
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(npm:*), Bash(npx:*), Bash(yarn:*), Bash(curl:*), WebFetch, Task(subagent_type:swap-integration-expert)
model: opus
license: MIT
metadata:
  author: pancakeswap
  version: '1.0.0'
  openclaw:
    homepage: https://github.com/pancakeswap/pancakeswap-ai
    os:
      - macos
      - linux
    requires:
      bins:
        - curl
        - jq
      anyBins:
        - cast
        - python3
        - node
        - open
        - xdg-open
    install:
      - kind: brew
        formula: curl
        bins: [curl]
      - kind: brew
        formula: jq
        bins: [jq]
      - kind: brew
        formula: foundry
        bins: [cast]
---

# Swap Integration

Integrate PancakeSwap swaps into frontends, backends, and smart contracts.

## Quick Decision Guide

| Building...                                | Use This Method                                                                |
| ------------------------------------------ | ------------------------------------------------------------------------------ |
| Quick quote or prototype                   | PancakeSwap Routing API (Method 1)                                             |
| Frontend with React/Next.js                | Smart Router SDK + Universal Router (Method 2)                                 |
| Backend script or trading bot              | Smart Router SDK + Universal Router (Method 2)                                 |
| Simple V2 swap, smart contract             | Direct V2 Router contract calls (Method 3)                                     |
| Need exact Universal Router encoding       | Universal Router SDK directly (Method 2)                                       |
| Swap through Infinity (v4) CL or Bin pools | Routing API (Method 1) or Smart Router SDK with Infinity pool types (Method 2) |

### Protocol Types

| Protocol     | Description                                                                                      | Fee Tiers (bps)         | Chains        |
| ------------ | ------------------------------------------------------------------------------------------------ | ----------------------- | ------------- |
| V2           | Classic AMM (xy=k), constant product formula                                                     | 25 (0.25%)              | BSC only      |
| V3           | Concentrated liquidity (Uniswap V3-compatible)                                                   | 1, 5, 25, 100 (0.01–1%) | All chains    |
| StableSwap   | Low-slippage for correlated/pegged assets                                                        | 1, 4 (0.01–0.04%)       | BSC only      |
| Infinity CL  | Concentrated liquidity in the v4 singleton PoolManager; supports hooks for custom logic          | Same tiers as V3        | BSC, Base     |
| Infinity Bin | Fixed-price-bin liquidity (similar to Trader Joe v2); tight ranges, predictable bin-level prices | Configurable            | BSC, Base     |
| Mixed        | Split route across any combination of the above protocols                                        | N/A (composite)         | BSC primarily |

## Supported Chains

| Chain                   | Chain ID | V2  | V3  | StableSwap | Infinity CL | Infinity Bin | RPC                                                                      |
| ----------------------- | -------- | --- | --- | ---------- | ----------- | ------------ | ------------------------------------------------------------------------ |
| BNB Smart Chain         | 56       | ✅  | ✅  | ✅         | ✅          | ✅           | `https://bsc-dataseed1.binance.org`                                      |
| BNB Smart Chain Testnet | 97       | ✅  | ❌  | ❌         | ❌          | ❌           | `https://bsc-testnet-rpc.publicnode.com or https://bsc-testnet.drpc.org` |
| Ethereum                | 1        | ❌  | ✅  | ❌         | ❌          | ❌           | `https://cloudflare-eth.com`                                             |
| Arbitrum One            | 42161    | ❌  | ✅  | ❌         | ❌          | ❌           | `https://arb1.arbitrum.io/rpc`                                           |
| Base                    | 8453     | ❌  | ✅  | ❌         | ✅          | ✅           | `https://mainnet.base.org`                                               |
| Polygon                 | 137      | ❌  | ✅  | ❌         | ❌          | ❌           | `https://polygon-rpc.com`                                                |
| zkSync Era              | 324      | ❌  | ✅  | ❌         | ❌          | ❌           | `https://mainnet.era.zksync.io`                                          |
| Linea                   | 59144    | ❌  | ✅  | ❌         | ❌          | ❌           | `https://rpc.linea.build`                                                |
| opBNB                   | 204      | ❌  | ✅  | ❌         | ❌          | ❌           | `https://opbnb-mainnet-rpc.bnbchain.org`                                 |

> **For testing**: Use **BSC Testnet (chain ID 97)**. Get free testnet BNB from <https://testnet.bnbchain.org/faucet-smart>.
> The Smart Router SDK does not index testnet pools — use **Method 3 (Direct V2 Router)** on testnet.

## Key Token Addresses

### BSC Mainnet (Chain ID: 56)

| Token | Address                                      |
| ----- | -------------------------------------------- |
| WBNB  | `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c` |
| BUSD  | `0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56` |
| USDT  | `0x55d398326f99059fF775485246999027B3197955` |
| USDC  | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` |
| CAKE  | `0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82` |
| ETH   | `0x2170Ed0880ac9A755fd29B2688956BD959F933F8` |
| BTCB  | `0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c` |

### BSC Testnet (Chain ID: 97)

| Token    | Address                                      | Notes               |
| -------- | -------------------------------------------- | ------------------- |
| WBNB     | `0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd` |                     |
| CAKE     | `0xFa60D973f7642b748046464E165A65B7323b0C73` |                     |
| BUSD     | `0xeD24FC36d5Ee211Ea25A80239Fb8C4Cfd80f12Ee` |                     |
| V2Router | `0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3` | PancakeSwap testnet |

### Universal Router Addresses

| Chain           | Chain ID | Universal Router Address                     |
| --------------- | -------- | -------------------------------------------- |
| BNB Smart Chain | 56       | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` |
| Ethereum        | 1        | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` |
| Arbitrum        | 42161    | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` |
| Base            | 8453     | `0x198EF79F1F515F02dFE9e3115eD9fC07183f02fC` |
| Polygon         | 137      | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` |
| zkSync Era      | 324      | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` |
| Linea           | 59144    | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` |
| opBNB           | 204      | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` |

---

## Method 1: PancakeSwap Routing API (Simplest)

Best for: Quick quotes, prototypes, and situations where you don't want to manage on-chain pool data yourself. No SDK installation required.

**Base URL**: `https://router.pancakeswap.finance/v0/quote`

### Get a Quote

```bash
# Exact input: 1 BNB → CAKE on BSC
curl -s "https://router.pancakeswap.finance/v0/quote?\
tokenInAddress=BNB\
&tokenInChainId=56\
&tokenOutAddress=0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82\
&tokenOutChainId=56\
&amount=1000000000000000000\
&type=exactIn\
&maxHops=3\
&maxSplits=4" | jq '{
  amountOut: .trade.outputAmount,
  priceImpact: .trade.priceImpact,
  route: [.trade.routes[].type]
}'
```

### API Parameters

| Parameter         | Type   | Description                                         |
| ----------------- | ------ | --------------------------------------------------- |
| `tokenInAddress`  | string | Input token address or `"BNB"` / `"ETH"` for native |
| `tokenInChainId`  | number | Input chain ID                                      |
| `tokenOutAddress` | string | Output token address                                |
| `tokenOutChainId` | number | Output chain ID                                     |
| `amount`          | string | Amount in raw units (wei for 18-decimal tokens)     |
| `type`            | string | `"exactIn"` or `"exactOut"`                         |
| `maxHops`         | number | Max hops per route (default: 3)                     |
| `maxSplits`       | number | Max route splits (default: 4)                       |

> **Infinity (v4) support**: The Routing API automatically considers Infinity CL and Infinity Bin pools on BSC and Base alongside V2/V3/StableSwap. No extra parameters are needed — the router selects the best route across all pool types.

### TypeScript Fetch Example

```typescript
interface PancakeRouteQuote {
  trade: {
    inputAmount: string
    outputAmount: string
    priceImpact: string
    routes: Array<{ type: 'V2' | 'V3' | 'STABLE' | 'MIXED'; pools: unknown[] }>
    blockNumber: number
  }
}

async function getQuote(params: {
  tokenIn: string
  tokenOut: string
  chainId: number
  amount: bigint
  type: 'exactIn' | 'exactOut'
}): Promise<PancakeRouteQuote> {
  const url = new URL('https://router.pancakeswap.finance/v0/quote')
  url.searchParams.set('tokenInAddress', params.tokenIn)
  url.searchParams.set('tokenInChainId', String(params.chainId))
  url.searchParams.set('tokenOutAddress', params.tokenOut)
  url.searchParams.set('tokenOutChainId', String(params.chainId))
  url.searchParams.set('amount', String(params.amount))
  url.searchParams.set('type', params.type)
  url.searchParams.set('maxHops', '3')
  url.searchParams.set('maxSplits', '4')

  const res = await fetch(url.toString())
  if (!res.ok) throw new Error(`Routing API error: ${res.status} ${await res.text()}`)
  return res.json()
}

// Usage
const quote = await getQuote({
  tokenIn: 'BNB',
  tokenOut: '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82', // CAKE
  chainId: 56,
  amount: BigInt('1000000000000000000'), // 1 BNB
  type: 'exactIn',
})

console.log('Output:', quote.trade.outputAmount, 'CAKE (raw)')
console.log('Price impact:', quote.trade.priceImpact, '%')
```

> **Quote freshness**: Re-fetch if the quote is more than ~15 seconds old before broadcasting. Stale quotes frequently fail with `INSUFFICIENT_OUTPUT_AMOUNT`.

---

## Method 2: Smart Router SDK + Universal Router SDK

Best for: Frontends and backends that need full programmatic control over routing and transaction encoding. Operates entirely on-chain — no external API dependency.

### Installation

```bash
npm install @pancakeswap/smart-router @pancakeswap/sdk @pancakeswap/v3-sdk @pancakeswap/universal-router-sdk viem@2.37.13
```

### Package Roles

| Package                             | Role                                              |
| ----------------------------------- | ------------------------------------------------- |
| `@pancakeswap/smart-router`         | Pool fetching + best route finding                |
| `@pancakeswap/sdk`                  | Core types: Token, CurrencyAmount, Percent, etc.  |
| `@pancakeswap/v3-sdk`               | V3-specific types: FeeAmount, pool encoding       |
| `@pancakeswap/universal-router-sdk` | Encode calldata for the Universal Router contract |
| `viem@2.37.13`                      | Ethereum client (reads, writes, signing) — pin to this version for PancakeSwap compatibility |

### Step 1: Set Up Viem Clients

```typescript
import { createPublicClient, createWalletClient, http } from 'viem'
import { bsc } from 'viem/chains'
import { privateKeyToAccount } from 'viem/accounts'

const publicClient = createPublicClient({
  chain: bsc,
  transport: http('https://bsc-dataseed1.binance.org'),
})

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`)
const walletClient = createWalletClient({
  account,
  chain: bsc,
  transport: http('https://bsc-dataseed1.binance.org'),
})
```

### Step 2: Define Tokens

```typescript
import { ChainId, Token } from '@pancakeswap/sdk'
import { Native } from '@pancakeswap/swap-sdk-evm'

const chainId = ChainId.BSC // 56

// Native BNB (no address)
const BNB = Native.onChain(chainId)

// ERC-20 tokens
const CAKE = new Token(
  chainId,
  '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82',
  18,
  'CAKE',
  'PancakeSwap Token',
)

const USDT = new Token(
  chainId,
  '0x55d398326f99059fF775485246999027B3197955',
  18,
  'USDT',
  'Tether USD',
)
```

### Step 3: Fetch Candidate Pools

```typescript
import { SmartRouter, PoolType } from '@pancakeswap/smart-router'
import { TradeType } from '@pancakeswap/sdk'
import { CurrencyAmount } from '@pancakeswap/swap-sdk-core'

const amountIn = CurrencyAmount.fromRawAmount(
  BNB,
  BigInt('1000000000000000000'), // 1 BNB
)

// Fetch all relevant pool types in parallel
const [v2Pools, v3Pools, stablePools] = await Promise.all([
  SmartRouter.getV2CandidatePools({
    onChainProvider: () => publicClient,
    currencyA: BNB,
    currencyB: CAKE,
  }),
  SmartRouter.getV3CandidatePools({
    onChainProvider: () => publicClient,
    subgraphProvider: undefined, // optional — speeds up pool discovery
    currencyA: BNB,
    currencyB: CAKE,
  }),
  SmartRouter.getStableCandidatePools({
    onChainProvider: () => publicClient,
    currencyA: BNB,
    currencyB: CAKE,
  }),
])

const pools = [...v2Pools, ...v3Pools, ...stablePools]
```

> **Performance tip**: If you're building a UI, consider caching pools for 30–60 seconds and only re-fetching when the user changes tokens or chain.

> **Infinity (v4) pool access**: The Smart Router SDK's Infinity pool integration is still evolving. For reliable Infinity CL and Infinity Bin pool access today, use **Method 1 (Routing API)** — it automatically considers all pool types including Infinity on BSC and Base with no extra setup required.

### Step 4: Find Best Trade

```typescript
const trade = await SmartRouter.getBestTrade(amountIn, CAKE, TradeType.EXACT_INPUT, {
  gasPriceWei: () => publicClient.getGasPrice(),
  maxHops: 3,
  maxSplits: 4,
  poolProvider: SmartRouter.createStaticPoolProvider(pools),
  quoteProvider: SmartRouter.createQuoteProvider({
    onChainProvider: () => publicClient,
  }),
  allowedPoolTypes: [PoolType.V2, PoolType.V3, PoolType.STABLE],
})

// Always check price impact before proceeding
if (parseFloat(trade.priceImpact.toSignificant(4)) > 2) {
  console.warn(`⚠️  High price impact: ${trade.priceImpact.toSignificant(4)}%`)
}

console.log('Output:', trade.outputAmount.toSignificant(6), CAKE.symbol)
console.log('Route:', trade.routes.map((r) => r.type).join(' + '))
```

### Step 5: Approve Tokens

> Skip this step if the input currency is native BNB/ETH — native currency does not need approval.

```typescript
import { erc20Abi } from 'viem'
import {
  PancakeSwapUniversalRouter,
  getUniversalRouterAddress,
} from '@pancakeswap/universal-router-sdk'

const PERMIT2_ADDRESS = '0x000000000022D473030F116dDEE9F6B43aC78BA3' as const

async function ensureTokenApproved(
  tokenAddress: `0x${string}`,
  owner: `0x${string}`,
  chainId: number,
) {
  // Step 1: Approve Permit2 contract (one-time per token, per wallet)
  const permit2Allowance = await publicClient.readContract({
    address: tokenAddress,
    abi: erc20Abi,
    functionName: 'allowance',
    args: [owner, PERMIT2_ADDRESS],
  })

  const MAX_UINT256 = BigInt('0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
  if (permit2Allowance < MAX_UINT256 / 2n) {
    const hash = await walletClient.writeContract({
      address: tokenAddress,
      abi: erc20Abi,
      functionName: 'approve',
      args: [PERMIT2_ADDRESS, MAX_UINT256],
    })
    await publicClient.waitForTransactionReceipt({ hash })
    console.log('✅ Permit2 approved')
  }

  // Step 2: Approve the Universal Router via Permit2 (per-swap, via signature OR transaction)
  // The Universal Router SDK handles this via inputTokenPermit in options.
  // For simplicity, approve the Universal Router directly instead:
  const routerAddress = getUniversalRouterAddress(chainId) as `0x${string}`
  const routerAllowance = await publicClient.readContract({
    address: tokenAddress,
    abi: erc20Abi,
    functionName: 'allowance',
    args: [owner, routerAddress],
  })

  if (routerAllowance < MAX_UINT256 / 2n) {
    const hash = await walletClient.writeContract({
      address: tokenAddress,
      abi: erc20Abi,
      functionName: 'approve',
      args: [routerAddress, MAX_UINT256],
    })
    await publicClient.waitForTransactionReceipt({ hash })
    console.log('✅ Universal Router approved')
  }
}
```

### Step 6: Encode and Send the Transaction

```typescript
import {
  PancakeSwapUniversalRouter,
  getUniversalRouterAddress,
} from '@pancakeswap/universal-router-sdk'
import { Percent } from '@pancakeswap/sdk'

const slippage = new Percent(50, 10000) // 0.5%
const deadline = BigInt(Math.floor(Date.now() / 1000) + 60 * 20) // 20 min

// Encode the swap calldata
const { calldata, value } = PancakeSwapUniversalRouter.swapERC20CallParameters(trade, {
  slippageTolerance: slippage,
  recipient: account.address,
  deadlineOrPreviousBlockhash: deadline,
})

// Send the transaction
const hash = await walletClient.sendTransaction({
  to: getUniversalRouterAddress(chainId) as `0x${string}`,
  data: calldata as `0x${string}`,
  value: BigInt(value), // Non-zero only when input is native BNB/ETH
  gas: 400000n, // Overestimate — unspent gas is refunded
})

const receipt = await publicClient.waitForTransactionReceipt({ hash })
if (receipt.status === 'reverted') {
  throw new Error(`Swap reverted: ${receipt.transactionHash}`)
}
console.log('✅ Swap confirmed:', receipt.transactionHash)
```

### Exact Output Swaps

To swap for a precise output amount (e.g., "I want exactly 100 USDT"):

```typescript
const amountOut = CurrencyAmount.fromRawAmount(
  USDT,
  BigInt('100000000000000000000'), // 100 USDT (18 decimals)
)

const trade = await SmartRouter.getBestTrade(
  amountOut,
  BNB, // currencyIn — note: swapped argument order for EXACT_OUTPUT
  TradeType.EXACT_OUTPUT,
  {
    gasPriceWei: () => publicClient.getGasPrice(),
    maxHops: 3,
    maxSplits: 4,
    poolProvider: SmartRouter.createStaticPoolProvider(pools),
    quoteProvider: SmartRouter.createQuoteProvider({ onChainProvider: () => publicClient }),
  },
)

console.log('Max BNB to spend:', trade.inputAmount.toSignificant(6))

// Encode with maximumAmountIn applied automatically via slippageTolerance
const { calldata, value } = PancakeSwapUniversalRouter.swapERC20CallParameters(trade, {
  slippageTolerance: new Percent(50, 10000),
  recipient: account.address,
  deadlineOrPreviousBlockhash: deadline,
})
```

---

## Method 3: Direct V2 Router Contract

Best for: Simple BSC swaps, Solidity integrations, or when you want zero SDK dependencies. Only supports V2 pools — no V3 or StableSwap.

### V2 Router Address (BSC Mainnet)

```
0x10ED43C718714eb63d5aA57B78B54704E256024E
```

### V2 Router ABI (subset)

```typescript
const PANCAKE_V2_ROUTER_ABI = [
  {
    name: 'swapExactETHForTokens',
    type: 'function',
    stateMutability: 'payable',
    inputs: [
      { name: 'amountOutMin', type: 'uint256' },
      { name: 'path', type: 'address[]' },
      { name: 'to', type: 'address' },
      { name: 'deadline', type: 'uint256' },
    ],
    outputs: [{ name: 'amounts', type: 'uint256[]' }],
  },
  {
    name: 'swapExactTokensForETH',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'amountIn', type: 'uint256' },
      { name: 'amountOutMin', type: 'uint256' },
      { name: 'path', type: 'address[]' },
      { name: 'to', type: 'address' },
      { name: 'deadline', type: 'uint256' },
    ],
    outputs: [{ name: 'amounts', type: 'uint256[]' }],
  },
  {
    name: 'swapExactTokensForTokens',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'amountIn', type: 'uint256' },
      { name: 'amountOutMin', type: 'uint256' },
      { name: 'path', type: 'address[]' },
      { name: 'to', type: 'address' },
      { name: 'deadline', type: 'uint256' },
    ],
    outputs: [{ name: 'amounts', type: 'uint256[]' }],
  },
  // Fee-on-transfer variant (SafeMoon-style tokens)
  {
    name: 'swapExactTokensForTokensSupportingFeeOnTransferTokens',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'amountIn', type: 'uint256' },
      { name: 'amountOutMin', type: 'uint256' },
      { name: 'path', type: 'address[]' },
      { name: 'to', type: 'address' },
      { name: 'deadline', type: 'uint256' },
    ],
    outputs: [],
  },
  {
    name: 'getAmountsOut',
    type: 'function',
    stateMutability: 'view',
    inputs: [
      { name: 'amountIn', type: 'uint256' },
      { name: 'path', type: 'address[]' },
    ],
    outputs: [{ name: 'amounts', type: 'uint256[]' }],
  },
] as const

const V2_ROUTER = '0x10ED43C718714eb63d5aA57B78B54704E256024E' as const
const WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c' as const
const CAKE = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82' as const
```

### V2 Swap Example (BNB → CAKE)

```typescript
import { parseEther } from 'viem'

const slippageBps = 50n // 0.5%
const deadline = BigInt(Math.floor(Date.now() / 1000) + 60 * 20)

// 1. Get quote
const amounts = await publicClient.readContract({
  address: V2_ROUTER,
  abi: PANCAKE_V2_ROUTER_ABI,
  functionName: 'getAmountsOut',
  args: [parseEther('0.1'), [WBNB, CAKE]],
})
const expectedOut = amounts[1]
const minOut = (expectedOut * (10000n - slippageBps)) / 10000n

// 2. Approve router for the input token (skip for BNB input)

// 3. Execute
const hash = await walletClient.writeContract({
  address: V2_ROUTER,
  abi: PANCAKE_V2_ROUTER_ABI,
  functionName: 'swapExactETHForTokens',
  args: [minOut, [WBNB, CAKE], account.address, deadline],
  value: parseEther('0.1'),
})
```

### Multi-hop V2 (BNB → USDT → CAKE)

```typescript
// Simply extend the path array
const amounts = await publicClient.readContract({
  address: V2_ROUTER,
  abi: PANCAKE_V2_ROUTER_ABI,
  functionName: 'getAmountsOut',
  args: [parseEther('0.1'), [WBNB, USDT_BSC, CAKE]],
})
```

---

## Token Approval Reference

| Scenario                        | What to Approve            | Where                    |
| ------------------------------- | -------------------------- | ------------------------ |
| Smart Router / Universal Router | Token → Permit2            | One-time per token       |
| Smart Router / Universal Router | Permit2 → Universal Router | Per session (or use sig) |
| Direct V2 Router                | Token → V2 Router          | One-time per token       |
| Native BNB/ETH input            | No approval needed         | —                        |

---

## V3 Fee Tiers

```typescript
import { FeeAmount } from '@pancakeswap/v3-sdk'

FeeAmount.LOWEST // 100   bps = 0.01%  — stablecoin pairs (USDT/USDC)
FeeAmount.LOW // 500   bps = 0.05%  — stable-ish pairs
FeeAmount.MEDIUM // 2500  bps = 0.25%  — most standard pairs (default)
FeeAmount.HIGH // 10000 bps = 1%     — exotic or highly volatile pairs
```

---

## Critical Implementation Notes

### TypeScript Import Conventions

Use `import type` (or inline `type` modifier) for any import that is only used as a TypeScript type — never at runtime. This keeps bundles clean and avoids circular-dependency issues.

```typescript
// ✅ Correct — Currency is only used in a type annotation
import { type Currency, TradeType, Percent } from '@pancakeswap/sdk'
import type { SmartRouterTrade } from '@pancakeswap/smart-router'

// ❌ Wrong — Currency is only a type, don't import it as a value
import { Currency, TradeType, Percent } from '@pancakeswap/sdk'
```

### Slippage Guidelines

| Token Type                          | Recommended Slippage |
| ----------------------------------- | -------------------- |
| Stablecoins (USDT/USDC/BUSD pairs)  | 0.01–0.1%            |
| Large caps (CAKE, BNB, ETH)         | 0.3–0.5%             |
| Mid/small caps                      | 0.5–2%               |
| Fee-on-transfer / reflection tokens | 5–12%                |
| New meme tokens                     | 5–15%                |

**Never set 0% slippage in production.** Every block's price movement will cause the transaction to revert.

### Native BNB/ETH Handling

- Pass `Native.onChain(chainId)` as the currency — the Smart Router and Universal Router handle `WRAP_ETH` / `UNWRAP_WETH` commands automatically.
- For direct V2 calls: use `swapExactETHForTokens` with `value: amountIn`.
- `value` in the encoded calldata will be non-zero only when the input is native. Always pass it when sending the transaction.

### Fee-on-Transfer Tokens (Reflection Tokens)

- These tokens deduct a fee on every transfer, so the router receives less than `amountIn`.
- On V2: use `swapExactTokensForTokensSupportingFeeOnTransferTokens` or `swapExactETHForTokensSupportingFeeOnTransferTokens`.
- The Smart Router detects these automatically and routes accordingly.
- Always set slippage ≥ the token's transfer fee (e.g., 5% token fee → use ≥5% slippage).

### Quote Staleness

- Re-fetch the trade quote if it is more than **15–30 seconds old** before sending.
- Stale quotes frequently revert with `INSUFFICIENT_OUTPUT_AMOUNT`.

### Gas Estimates

| Swap Type              | Approx. Gas      |
| ---------------------- | ---------------- |
| V2 single-hop          | ~150,000         |
| V3 single-hop          | ~180,000         |
| V2+V3 two-hop          | ~300,000         |
| Mixed 3-hop            | ~400,000–600,000 |
| With Permit2 signature | +~40,000         |

Always use `publicClient.estimateGas()` in production; hard-coded values can under-estimate on complex routes.

---

## Error Handling

### Common Revert Reasons

| Error String                    | Cause                                   | Fix                                         |
| ------------------------------- | --------------------------------------- | ------------------------------------------- |
| `INSUFFICIENT_OUTPUT_AMOUNT`    | Slippage exceeded (price moved)         | Increase `slippageTolerance` or re-quote    |
| `EXCESSIVE_INPUT_AMOUNT`        | Slippage exceeded for exact-output swap | Increase `slippageTolerance` or re-quote    |
| `EXPIRED`                       | `deadline` timestamp is in the past     | Re-fetch quote with a fresh deadline        |
| `TRANSFER_FAILED`               | Fee-on-transfer token, incorrect method | Use `SupportingFeeOnTransferTokens` variant |
| `STF` (SafeTransferFrom failed) | Token not approved to router or Permit2 | Run `ensureTokenApproved()` first           |
| `TransactionExecutionError`     | General on-chain failure                | Decode with `publicClient.call()` below     |

### Debugging a Revert

```typescript
// Simulate the transaction to get the revert reason
try {
  await publicClient.call({
    to: getUniversalRouterAddress(chainId) as `0x${string}`,
    data: calldata as `0x${string}`,
    value: BigInt(value),
    account: account.address,
  })
} catch (err: unknown) {
  // viem throws with the decoded revert reason
  console.error('Revert reason:', (err as Error).message)
}
```

---

## Frontend Integration (React + wagmi)

For React frontends, use wagmi hooks alongside the Smart Router SDK:

```bash
npm install wagmi@2.17.5 viem@2.37.13 @tanstack/react-query
```


```typescript
import { useWalletClient, usePublicClient, useChainId } from 'wagmi'
import { useMutation } from '@tanstack/react-query'
import { type Currency, TradeType, Percent } from '@pancakeswap/sdk'
import { CurrencyAmount } from '@pancakeswap/swap-sdk-core'
import { SmartRouter } from '@pancakeswap/smart-router'
import {
  PancakeSwapUniversalRouter,
  getUniversalRouterAddress,
} from '@pancakeswap/universal-router-sdk'

type SwapVariables = { amountIn: bigint; tokenIn: Currency; tokenOut: Currency }

function useSwap() {
  const chainId = useChainId()
  const { data: walletClient } = useWalletClient()
  const publicClient = usePublicClient()

  return useMutation<`0x${string}`, Error, SwapVariables>({
    mutationFn: async ({ amountIn, tokenIn, tokenOut }) => {
      if (!walletClient || !publicClient) throw new Error('Wallet not connected')

      // 1. Fetch pools
      const pools = await fetchPancakePools(publicClient, tokenIn, tokenOut, chainId)

      // 2. Get best trade
      const trade = await SmartRouter.getBestTrade(
        CurrencyAmount.fromRawAmount(tokenIn, amountIn),
        tokenOut,
        TradeType.EXACT_INPUT,
        {
          gasPriceWei: () => publicClient.getGasPrice(),
          maxHops: 3,
          maxSplits: 4,
          poolProvider: SmartRouter.createStaticPoolProvider(pools),
          quoteProvider: SmartRouter.createQuoteProvider({ onChainProvider: () => publicClient }),
        },
      )
      if (!trade) throw new Error('No route found for this token pair')

      // 3. Encode
      const { calldata, value } = PancakeSwapUniversalRouter.swapERC20CallParameters(trade, {
        slippageTolerance: new Percent(50, 10000),
        recipient: walletClient.account.address,
        deadlineOrPreviousBlockhash: BigInt(Math.floor(Date.now() / 1000) + 1200),
      })

      // 4. Send
      return walletClient.sendTransaction({
        to: getUniversalRouterAddress(chainId) as `0x${string}`,
        data: calldata as `0x${string}`,
        value: BigInt(value),
      })
    },
  })
}
```

---

## Complete Working Example: BNB → CAKE

```typescript
import { createPublicClient, createWalletClient, http } from 'viem'
import { bsc } from 'viem/chains'
import { privateKeyToAccount } from 'viem/accounts'
import { ChainId, Token, TradeType, Percent } from '@pancakeswap/sdk'
import { Native } from '@pancakeswap/swap-sdk-evm'
import { CurrencyAmount } from '@pancakeswap/swap-sdk-core'
import { SmartRouter, PoolType } from '@pancakeswap/smart-router'
import {
  PancakeSwapUniversalRouter,
  getUniversalRouterAddress,
} from '@pancakeswap/universal-router-sdk'

const chainId = ChainId.BSC
const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`)

const publicClient = createPublicClient({
  chain: bsc,
  transport: http('https://bsc-dataseed1.binance.org'),
})
const walletClient = createWalletClient({
  account,
  chain: bsc,
  transport: http('https://bsc-dataseed1.binance.org'),
})

const BNB = Native.onChain(chainId)
const CAKE = new Token(chainId, '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82', 18, 'CAKE')

async function swapBNBforCAKE(bnbAmountWei: bigint) {
  const amountIn = CurrencyAmount.fromRawAmount(BNB, bnbAmountWei)

  // 1. Fetch candidate pools (V2 + V3; stable not relevant for BNB/CAKE)
  const [v2Pools, v3Pools] = await Promise.all([
    SmartRouter.getV2CandidatePools({
      onChainProvider: () => publicClient,
      currencyA: BNB,
      currencyB: CAKE,
    }),
    SmartRouter.getV3CandidatePools({
      onChainProvider: () => publicClient,
      subgraphProvider: undefined,
      currencyA: BNB,
      currencyB: CAKE,
    }),
  ])

  // 2. Find best route
  const trade = await SmartRouter.getBestTrade(amountIn, CAKE, TradeType.EXACT_INPUT, {
    gasPriceWei: () => publicClient.getGasPrice(),
    maxHops: 3,
    maxSplits: 4,
    poolProvider: SmartRouter.createStaticPoolProvider([...v2Pools, ...v3Pools]),
    quoteProvider: SmartRouter.createQuoteProvider({ onChainProvider: () => publicClient }),
    allowedPoolTypes: [PoolType.V2, PoolType.V3],
  })

  const impact = parseFloat(trade.priceImpact.toSignificant(4))
  if (impact > 2) console.warn(`⚠️  High price impact: ${impact}%`)

  console.log(
    `Swapping ${amountIn.toSignificant(4)} BNB → ~${trade.outputAmount.toSignificant(4)} CAKE`,
  )

  // 3. Encode calldata
  const { calldata, value } = PancakeSwapUniversalRouter.swapERC20CallParameters(trade, {
    slippageTolerance: new Percent(50, 10000), // 0.5%
    recipient: account.address,
    deadlineOrPreviousBlockhash: BigInt(Math.floor(Date.now() / 1000) + 1200),
  })

  // 4. Send (no token approval needed — input is native BNB)
  const hash = await walletClient.sendTransaction({
    to: getUniversalRouterAddress(chainId) as `0x${string}`,
    data: calldata as `0x${string}`,
    value: BigInt(value),
    gas: 400000n,
  })

  const receipt = await publicClient.waitForTransactionReceipt({ hash })
  if (receipt.status === 'reverted') throw new Error(`Swap reverted: ${hash}`)

  console.log('✅ Confirmed:', receipt.transactionHash)
  return receipt
}

await swapBNBforCAKE(BigInt('100000000000000000')) // 0.1 BNB
```
