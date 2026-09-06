---
name: pool-info
description: This skill should be used when the user asks to "check pool info", "get pool details", "pool TVL", "pool volume", "pool APR", "find pools", "search pools", "best pool for", "which pool", "pool address info", "what DEX is this pool", "identify pool", "pool stats", or wants to look up pool metadata (DEX, fee tier, tokens, TVL, volume, APR) before zapping into a pool. Also used internally by zap skills for DEX auto-detection when the user provides a pool address without specifying the DEX.
metadata:
  tags:
    - defi
    - kyberswap
    - pool
    - liquidity
    - evm
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Pool Info Skill

Look up pool metadata (DEX, fee tier, tokens, TVL, volume, APR) using the KyberSwap Earn Service API. Supports both pool address lookup and token pair search across all indexed DEXes and chains.

**Primary use cases:**
1. **Pool lookup** — Get details for a specific pool address (or V4 pool ID)
2. **Pool search** — Find the best pools for a token pair by TVL, volume, or APR
3. **DEX auto-detection** — Identify which DEX a pool belongs to (used by zap skills)

## API Endpoint

```
GET https://earn-service.kyberswap.com/api/v1/explorer/pools
```

### Parameters

| Parameter | Required | Description | Example |
|---|---|---|---|
| `chainIds` | Yes | Chain ID(s), comma-separated | `42161`, `1,42161,8453` |
| `q` | No | Search query — pool address or token symbols | `0xc696...`, `ETH USDC` |
| `protocol` | No | DEX filter (matches `exchange` field in response) | `uniswapv3`, `uniswap-v4`, `pancake-v3` |
| `page` | No | Page number (default: 1) | `1` |
| `limit` | No | Results per page (default: 10) | `10` |
| `interval` | No | Stats interval (default: `24h`) | `24h`, `7d` |
| `sortBy` | No | Sort field | `tvl`, `volume`, `apr`, `earnFee` |
| `orderBy` | No | Sort order | `DESC`, `ASC` |
| `userAddress` | No | User wallet address (for position context) | `0xeF8A...` |

### Response Fields (per pool)

| Field | Type | Description |
|---|---|---|
| `address` | string | Pool address (20-byte) or pool ID (32-byte for V4) |
| `exchange` | string | DEX identifier — e.g. `uniswapv3`, `uniswap-v4`, `pancake-v3` |
| `feeTier` | number | Fee tier as percentage (e.g. `0.05` = 0.05%) |
| `tvl` | number | Total value locked in USD |
| `volume` | number | Trading volume in USD (for the `interval`) |
| `apr` | number | Total APR (percentage) |
| `lpApr` | number | LP APR from trading fees only |
| `kemApr` | number | KyberSwap Elastic Mining APR (external rewards) |
| `earnFee` | number | Fees earned in USD (for the `interval`) |
| `tokens[]` | array | Token objects: `address`, `symbol`, `logoURI` |
| `chain` | object | Chain info: `id`, `name`, `logoUrl` |

### Exchange to ZaaS DEX ID Mapping

The `exchange` field in the API response maps to the ZaaS API `dex` parameter:

| `exchange` value | ZaaS `dex` parameter |
|---|---|
| `uniswapv3` | `DEX_UNISWAPV3` |
| `uniswap-v4` | `DEX_UNISWAP_V4` |
| `pancake-v3` | `DEX_PANCAKESWAPV3` |
| `sushiswap-v3` | `DEX_SUSHISWAPV3` |
| `aerodrome-cl` | `DEX_AERODROMECL` |
| `camelot-v3` | `DEX_CAMELOTV3` |
| `quickswap-v3-uni` | `DEX_QUICKSWAPV3UNI` |
| `quickswap-v3-algebra` | `DEX_QUICKSWAPV3ALGEBRA` |
| `metavault-v3` | `DEX_METAVAULTV3` |
| `thruster-v3` | `DEX_THRUSTERV3` |

**General rule:** Uppercase the exchange value, replace `-` with `_`, and prefix with `DEX_`. Special cases exist — when in doubt, cross-reference with `${CLAUDE_PLUGIN_ROOT}/references/dex-identifiers.md`.

## Input Parsing

The user will provide input like:
- `pool info 0xc6962004f452be9203591991d15f6b388e09e8d0 on arbitrum`
- `find ETH/USDC pools on arbitrum`
- `best pool for WBTC/ETH on ethereum by TVL`
- `what DEX is pool 0xc696... on arbitrum`
- `top 5 uniswapv3 pools on base by volume`
- `pool APR for 0x7fcd... on arbitrum`

Extract these fields:
- **query** — pool address/ID or token pair (e.g. `ETH USDC`)
- **chain** — the chain slug (default: `ethereum`)
- **protocol** — optional DEX filter (e.g. `uniswapv3`, `uniswap-v4`)
- **sortBy** — sort field (default: `tvl`)
- **limit** — number of results (default: `5` for search, `1` for address lookup)

## Workflow

### Step 1: Resolve Chain ID

Map the chain slug to chain ID using `${CLAUDE_PLUGIN_ROOT}/references/supported-chains.md`.

### Step 2: Query the API

Via **WebFetch**:

**For pool address lookup:**
```
GET https://earn-service.kyberswap.com/api/v1/explorer/pools?chainIds={chainId}&page=1&limit=1&interval=24h&q={poolAddress}
```

**For token pair search:**
```
GET https://earn-service.kyberswap.com/api/v1/explorer/pools?chainIds={chainId}&page=1&limit={limit}&interval=24h&sortBy={sortBy}&orderBy=DESC&q={token0}+{token1}
```

**For DEX-filtered search:**
```
GET https://earn-service.kyberswap.com/api/v1/explorer/pools?chainIds={chainId}&page=1&limit={limit}&interval=24h&sortBy={sortBy}&orderBy=DESC&protocol={protocol}&q={searchQuery}
```

Add the `X-Client-Id: ai-agent-skills` header.

### Step 3: Handle Empty Results

If the API returns 0 results:
- For address lookup: "Pool `{address}` not found on {chain}. It may not be indexed by KyberSwap, or the chain may be wrong."
- For token pair search: "No pools found for {token0}/{token1} on {chain}. Try a different chain or check token symbols."
- Suggest the user try without the `protocol` filter if one was applied.

### Step 4: Format the Output

**Single pool (address lookup):**

```
## Pool Info — {token0}/{token1} on {Chain}

| Detail | Value |
|---|---|
| Pool Address | `{address}` |
| DEX | {exchange} |
| Fee Tier | {feeTier}% |
| Token 0 | {token0.symbol} (`{token0.address}`) |
| Token 1 | {token1.symbol} (`{token1.address}`) |
| TVL | ${tvl} |
| 24h Volume | ${volume} |
| APR | {apr}% |
| LP APR | {lpApr}% |
| 24h Fees Earned | ${earnFee} |
```

**Multiple pools (search):**

```
## {token0}/{token1} Pools on {Chain} (sorted by {sortBy})

| # | DEX | Fee | TVL | 24h Volume | APR | Pool Address |
|---|---|---|---|---|---|---|
| 1 | {exchange} | {feeTier}% | ${tvl} | ${volume} | {apr}% | `{address}` |
| 2 | ... | ... | ... | ... | ... | ... |
```

### Structured JSON Output

After the markdown table, include a JSON block:

````
```json
{
  "type": "kyberswap-pool-info",
  "chain": "{chain}",
  "chainId": {chainId},
  "query": "{query}",
  "pools": [
    {
      "address": "{address}",
      "exchange": "{exchange}",
      "dex": "{DEX_IDENTIFIER}",
      "feeTier": {feeTier},
      "token0": {"symbol": "{symbol}", "address": "{address}"},
      "token1": {"symbol": "{symbol}", "address": "{address}"},
      "tvl": {tvl},
      "volume": {volume},
      "apr": {apr},
      "lpApr": {lpApr},
      "earnFee": {earnFee}
    }
  ]
}
```
````

## DEX Auto-Detection (for zap skills)

When a zap skill receives a pool address without a DEX identifier, use this API to detect the DEX:

```
GET https://earn-service.kyberswap.com/api/v1/explorer/pools?chainIds={chainId}&page=1&limit=1&interval=24h&q={poolAddress}
```

Extract the `exchange` field and map it to the ZaaS `dex` parameter using the [Exchange to ZaaS DEX ID Mapping](#exchange-to-zaas-dex-id-mapping) table above.

**If the pool is not indexed** (0 results), fall back to asking the user to specify the DEX.

## Error Handling

### HTTP Error Codes

| Code | Meaning | Action |
|---|---|---|
| 400 | Bad request | Check query parameters: `chainIds`, `q`, `protocol`. |
| 404 | Not found | Check endpoint URL and chain ID. |
| 429 | Rate limited | Wait and retry with exponential backoff. |
| 500 | Internal server error | Retry after a brief delay. If persistent, the service may be down. |

For any error not listed here, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.

## Important Notes

- This skill is **read-only** — no transactions are built or submitted.
- The API indexes pools across many DEXes. Not all pools are indexed — very new or low-liquidity pools may be missing.
- V4 pools use 32-byte pool IDs as the `address` field (e.g. `0x864a...03a8`).
- The `feeTier` is a percentage (e.g. `0.05` means 0.05%), not basis points.
- APR values are annualized from the selected `interval` — 24h APR can be volatile.
- Use `sortBy=tvl` for the most liquid pools, `sortBy=apr` for highest yield, `sortBy=volume` for most active.

## Troubleshooting

| Issue | Resolution |
|---|---|
| Pool not found | Pool may not be indexed. Try without chain filter or verify the address on a block explorer. |
| Wrong DEX returned | The `exchange` field is authoritative. If it doesn't match expectations, the pool may have been deployed by a different DEX. |
| Stale data | APR and volume are based on the `interval` parameter. Use `7d` for more stable averages. |
| V4 pool not found by ID | V4 pool indexing may lag. Try searching by token pair with `protocol=uniswap-v4` instead. |
