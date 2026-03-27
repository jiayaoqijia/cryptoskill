---
name: yield-strategies
description: Guide for querying DeFi yield and APY data using get_yield_pools. Covers pool filtering by token, chain, protocol, category, stablecoin-only mode, and capacity assessment. Explains APY conventions, lending vs borrowing rates, and sort options. Use when users ask about yields, APY, lending rates, borrowing costs, best pools, or DeFi yield strategies.
---

# DeFi Yield Strategies

## APY Convention

APY values are **already percentages**: `apy = 2.32` means 2.32%.

Do NOT multiply by 100. This is the most common mistake when working with yield data.

## Tool: `defillama:get_yield_pools`

### Filtering Guide

| Want | Parameter | Example |
|------|-----------|---------|
| Pools with specific token | `token` | `"coingecko:ethereum"` |
| Pools on specific chain | `chain` | `"ethereum"` |
| Pools from specific protocol | `protocol` | `"aave"` |
| Pools from protocol category | `category` | `"Lending"`, `"DEXes"` |
| Only stablecoin pools | `stablecoin_only` | `true` |
| Minimum APY threshold | `min_apy` | `5` (= 5%) |
| Minimum TVL | `min_tvl` | `1000000` (= $1M) |
| Include borrow-side data | `include_borrow` | `true` |

### Key Distinction

- **"ETH pools"** = **token** filter: `token: "coingecko:ethereum"`
- **"Pools on Ethereum"** = **chain** filter: `chain: "ethereum"`

### Token Family Matching

The `token` param expects canonical token keys (e.g., `coingecko:ethereum`) and uses `dim.pool_set()` for family resolution. `coingecko:ethereum` finds pools containing ETH, wETH, stETH, cbETH, and all other variants in the ETH family -- not just native ETH.

### Sort Options

`sort_by` accepts strings like: `"apy desc"`, `"tvl desc"`, `"apy_base desc"`, `"apy_reward desc"`

### Returned Columns

Each result includes: `symbol`, `protocol` (sub-protocol slug), `parent_protocol`, `category`, `chain`, `apy`, `apy_base`, `apy_reward`, `apy_base_borrow`, `apy_reward_borrow`, `tvl`, `total_supply`, `total_borrow`

### Historical Data & Volatility

- Use `period` param (`7d`, `30d`, `90d`, `180d`, `365d`) for daily APY/TVL time-series history
- Use `include_volatility: true` to add APY volatility stats (`apy_avg_30d`, `apy_median_30d`, `apy_std_30d`, `cv_30d`) — current queries only
- Use `start_date` / `end_date` for custom date ranges (overrides `period`)

## Borrowing Costs

For lending protocols, borrowing rate data is available:

- `apy_base_borrow`: Base borrowing cost (what you pay)
- `apy_reward_borrow`: Reward offset on borrowing (incentives you earn)
- Net borrow cost = `apy_base_borrow - apy_reward_borrow`

Use `include_borrow: true` to ensure borrow columns are populated.

## Capacity Assessment

When allocating capital, check pool TVL. Allocating more than 10% of a pool's TVL may cause significant rate impact or slippage. Larger pools absorb capital more easily.

## Examples

**Example 1:**
User: "Best stablecoin lending yields"
Tool call: `defillama:get_yield_pools(stablecoin_only: true, category: "Lending", sort_by: "apy desc")`

**Example 2:**
User: "Top ETH yield pools with over $1M TVL"
Tool call: `defillama:get_yield_pools(token: "coingecko:ethereum", min_tvl: 1000000, sort_by: "apy desc")`

**Example 3:**
User: "Cheapest borrowing rates for stablecoins on Arbitrum"
Tool call: `defillama:get_yield_pools(stablecoin_only: true, chain: "arbitrum", category: "Lending", include_borrow: true, sort_by: "apy_base_borrow asc")`

**Example 4:**
User: "Where can I earn yield on USDC?"
Tool call: `defillama:get_yield_pools(token: "coingecko:usd-coin", sort_by: "apy desc", min_tvl: 100000)`

**Example 5:**
User: "Aave yields on Ethereum"
Tool call: `defillama:get_yield_pools(protocol: "aave", chain: "ethereum", sort_by: "apy desc")`
