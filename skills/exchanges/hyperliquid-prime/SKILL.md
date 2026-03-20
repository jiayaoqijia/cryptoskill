---
name: hyperliquid-prime
description: Trade on Hyperliquid's perp markets (native + HIP-3) with intelligent order routing and cross-market splitting. Use when the user wants to trade crypto, stocks, or commodities on Hyperliquid, get best execution across fragmented markets, split large orders across multiple venues, compare funding rates, view aggregated orderbooks, or manage positions across multiple collateral types. Routes across both native HL perps (ETH, BTC) and HIP-3 deployer markets. Handles collateral swaps (USDC→USDH/USDT0) automatically during execution when the best liquidity requires it.
---

# Hyperliquid Prime

A TypeScript SDK that acts as a **prime broker layer** on top of Hyperliquid's perp markets — both native (ETH, BTC) and HIP-3 deployer markets. Automatically discovers all markets for an asset, compares liquidity/funding/cost, and routes to the best execution — or splits across multiple venues for optimal fills with automatic collateral swaps.

## When to Use This Skill

- Trading crypto, stocks (AAPL, NVDA, TSLA), indexes, or commodities (GOLD, SILVER) on Hyperliquid
- Need best execution across multiple perp markets (native + HIP-3) for the same asset
- Splitting large orders across venues for better fills and lower price impact
- Comparing funding rates across different collateral types
- Aggregated orderbook view across fragmented markets
- Managing positions that may be spread across multiple collateral types
- Automatic collateral swaps (USDC → USDH, USDT0) when non-USDC markets offer better prices

## Quick Start

### Installation

```bash
npm install hyperliquid-prime
```

### Read-Only Usage (no wallet needed)

```typescript
import { HyperliquidPrime } from 'hyperliquid-prime'

const hp = new HyperliquidPrime({ testnet: true })
await hp.connect()

// Get all perp markets for an asset (native + HIP-3)
const markets = hp.getMarkets('ETH') // or 'TSLA', 'BTC', etc.

// Get routing quote for best execution
const quote = await hp.quote('TSLA', 'buy', 50)
const quoteWithLev = await hp.quote('TSLA', 'buy', 50, { leverage: 5, isCross: true })

// Aggregated orderbook
const book = await hp.getAggregatedBook('TSLA')

// Funding rate comparison
const funding = await hp.getFundingComparison('TSLA')

await hp.disconnect()
```

### Trading (wallet required)

```typescript
const hp = new HyperliquidPrime({
  privateKey: '0x...',
  testnet: true,
})
await hp.connect()

// Quote then execute (recommended)
const quote = await hp.quote('TSLA', 'buy', 50, { leverage: 5, isCross: true })
const receipt = await hp.execute(quote.plan)

// One-step convenience
const receipt2 = await hp.long('TSLA', 50, { leverage: 5 })
const receipt3 = await hp.short('TSLA', 25, { leverage: 3, isCross: false })

// Split across multiple markets for better fills
const splitQuote = await hp.quoteSplit('TSLA', 'buy', 200, { leverage: 4 })
const splitReceipt = await hp.executeSplit(splitQuote.splitPlan)
// Or one-step: await hp.longSplit('TSLA', 200)

// Unified position view
const positions = await hp.getGroupedPositions()

await hp.disconnect()
```

### CLI

```bash
# Show all perp markets for an asset (native + HIP-3)
hp markets ETH
hp markets TSLA

# Aggregated orderbook
hp book TSLA

# Compare funding rates
hp funding TSLA

# Get routing quote
hp quote TSLA buy 50
hp quote TSLA buy 50 --leverage 5
hp quote TSLA buy 50 --leverage 3 --isolated

# Execute trades
HP_PRIVATE_KEY=0x... hp long TSLA 50
HP_PRIVATE_KEY=0x... hp short TSLA 25
HP_PRIVATE_KEY=0x... hp long TSLA 50 --leverage 5
HP_PRIVATE_KEY=0x... hp short TSLA 25 --leverage 3 --isolated

# View positions and balance
HP_PRIVATE_KEY=0x... hp positions
HP_PRIVATE_KEY=0x... hp balance

# Use testnet
hp markets TSLA --testnet
```

## Important: Fees & Automatic Actions

**Builder Fee**: A 1 basis point (0.01%) builder fee is charged by default on all SDK-executed orders via Hyperliquid's native builder fee mechanism. On the first trading order from a wallet, the SDK sends an on-chain approval transaction to authorize this fee. To disable entirely, set `builder: null` in the config.

**Collateral Swaps (Split Orders Only)**: When `executeSplit()` routes orders to non-USDC collateral markets, the SDK automatically:
1. Enables DEX abstraction on the user's account
2. Transfers USDC from the perp account to the spot account
3. Places a spot order to swap USDC into the required collateral token (e.g., USDH, USDT0)
4. A 1% buffer is added to swap amounts to account for slippage

These actions only occur during split order execution and only when the best liquidity requires non-USDC collateral.

**Read-Only Operations**: Quotes, orderbooks, funding comparisons, and market discovery require no wallet, no fees, and perform no on-chain actions.

**Credentials**: Trading operations require a private key via `HP_PRIVATE_KEY` environment variable or the `privateKey` config option. The key is used to sign transactions sent to the Hyperliquid API. Source code is available for audit at <https://github.com/mehranhydary/hl-prime>.

**User Confirmation Flow**: The SDK uses a quote-then-execute pattern as the confirmation mechanism:
1. `quote()` / `quoteSplit()` are **read-only** — they return an execution plan with estimated prices, markets, and costs. No on-chain actions are taken.
2. The caller reviews the plan (programmatically or via CLI output).
3. `execute()` / `executeSplit()` must be **explicitly called** to perform on-chain actions (place orders, approve fees, swap collateral).
4. One-step convenience methods (`long()`, `short()`, `longSplit()`, `shortSplit()`) combine both steps — use quote-then-execute for explicit control.

**Implementation Note**: This skill bundle contains instructions only (SKILL.md). The SDK implementation must be installed separately via `npm install hyperliquid-prime`. The source code is open-source and available for audit at the GitHub repository before installation.

## How Routing Works

When you call `hp.quote("TSLA", "buy", 50)`, the router:

1. **Fetches** the orderbook for every TSLA market
2. **Simulates** walking each book to estimate average fill price and price impact
3. **Scores** each market using:
   - **Price impact** (dominant) — cost in basis points to fill
   - **Funding rate** (secondary) — prefers favorable funding direction
   - **Collateral swap cost** (penalty) — estimated cost to swap into the required collateral
4. **Selects** the lowest-score market and builds an execution plan

For split orders (`quoteSplit`), the router merges all orderbooks, walks the combined book greedily to consume the cheapest liquidity first across all venues, and builds split execution legs. Collateral requirements and swaps are estimated and executed at `executeSplit(...)` time using live balances. If leverage is included in the quote options, execution applies that leverage per market leg before order placement.

For single-market orders, leverage included in `quote(...)` is carried into the execution plan and applied before the order is sent.

## Configuration

```typescript
interface HyperliquidPrimeConfig {
  privateKey?: `0x${string}` // Required for trading
  walletAddress?: string       // Derived from privateKey if not provided
  testnet?: boolean            // Default: false
  defaultSlippage?: number     // Default: 0.01 (1%)
  logLevel?: 'debug' | 'info' | 'warn' | 'error' | 'silent'
  prettyLogs?: boolean         // Default: false
  builder?: BuilderConfig | null // Builder fee (default: 1 bps, null to disable)
}
```

### Builder Fee

A 1 basis point (0.01%) builder fee is included by default on all SDK-executed orders via Hyperliquid's native builder fee mechanism. The fee is auto-approved on the trader's first order. Set `builder: null` to disable, or provide a custom `{ address, feeBps }` to override.

## Key Methods

### Read-Only
- `getMarkets(asset)` — All perp markets for an asset (native + HIP-3)
- `getAggregatedMarkets()` — Asset groups with multiple markets
- `getAggregatedBook(asset)` — Merged orderbook across all markets
- `getFundingComparison(asset)` — Funding rates compared across markets
- `quote(asset, side, size, options?)` — Routing quote for single best market
- `quoteSplit(asset, side, size, options?)` — Split quote across multiple markets

### Trading (wallet required)
- `execute(plan)` — Execute a single-market quote
- `executeSplit(plan)` — Execute a split quote (handles collateral swaps)
- `long(asset, size, options?)` — Quote + execute a long on best market
- `short(asset, size, options?)` — Quote + execute a short on best market
- `longSplit(asset, size, options?)` — Split quote + execute a long across markets
- `shortSplit(asset, size, options?)` — Split quote + execute a short across markets
- `close(asset)` — Close all positions for an asset

### Trade Options
- `leverage?: number` — Positive number, e.g. `5` for 5x.
- `isCross?: boolean` — Default `true` (cross); set `false` for isolated.
- `isCross` requires `leverage`. If leverage is omitted, no leverage-setting API call is made.

### Position & Balance
- `getPositions()` — All positions with market metadata
- `getGroupedPositions()` — Positions grouped by base asset
- `getBalance()` — Account margin summary

## Repository

<https://github.com/mehranhydary/hl-prime>

## License

MIT
