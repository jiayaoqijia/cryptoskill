---
name: position-manager
description: This skill should be used when the user asks to "check my positions", "show my liquidity positions", "list my LP positions", "view my pools", "position status", "show open positions", "show closed positions", "my DeFi positions", "portfolio positions", "position performance", "how are my positions doing", "unclaimed fees", "position APR", "position earnings", or wants to view, monitor, or analyze their DeFi liquidity positions. Queries the KyberSwap Earn Service API to display position details, APR, earnings, unclaimed fees, and portfolio summary across multiple chains and protocols.
metadata:
  tags:
    - defi
    - kyberswap
    - positions
    - liquidity
    - portfolio
    - evm
    - concentrated-liquidity
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Position Manager Skill

Query and display DeFi liquidity positions. View in-range, out-of-range, and closed positions with APR, earnings, unclaimed fees, and portfolio analytics.

## Input Parsing

The user will provide input like:
- `show my positions for 0xAbc123...`
- `check positions on ethereum for 0xAbc123...`
- `show open positions for 0xAbc123...`
- `show closed positions on arbitrum for 0xAbc123...`
- `how are my positions doing for 0xAbc123...`
- `show my unclaimed fees for 0xAbc123...`
- `position performance for 0xAbc123...`

Extract these fields:
- **wallet** (required) — the wallet address to query
- **chain** (optional) — filter by chain; if omitted, show all chains
- **status** (optional) — position status filter; default: in-range + out-of-range (active positions)
- **keyword** (optional) — filter by token symbol or pool address
- **sort** (optional) — sort order; default: `valueUsd:desc`
- **page** (optional) — page number; default: 1
- **pageSize** (optional) — results per page; default: 10

**If the wallet address is not provided, ask the user for it before proceeding.** Do not guess or use a placeholder address.

**Wallet address validation — reject or warn before proceeding:**
- **Must not be the zero address** (`0x0000000000000000000000000000000000000000`) — this is an invalid address and the query will return no results.
- **Must not be the native token sentinel** (`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`) — this is a placeholder for native tokens, not a real account.
- **Must match the format** `^0x[a-fA-F0-9]{40}$` — reject malformed addresses.
- **Warn if it matches a known contract address** (e.g., a token address or a router address) — querying positions for a contract is unusual and likely a mistake. Ask the user to confirm.

## Supported Chains

All chains supported by the KyberSwap Earn Service. The API accepts any chain ID. Common ones:

| Chain | Chain ID |
|---|---|
| Ethereum | `1` |
| BNB Smart Chain | `56` |
| Arbitrum | `42161` |
| Polygon | `137` |
| Optimism | `10` |
| Base | `8453` |
| Avalanche | `43114` |
| Linea | `59144` |
| Scroll | `534352` |
| zkSync | `324` |
| Sonic | `146` |
| Berachain | `80094` |
| Ronin | `2020` |

When the user specifies a chain by name, map it to the corresponding chain ID. When viewing positions across all chains, leave the `chainIds` parameter as an empty string.

## Workflow

### Step 1: Build Query Parameters

Map user input to API query parameters:

| User says | API `statuses` value |
|---|---|
| "open positions" / "active positions" (or no filter specified) | `PositionStatusInRange,PositionStatusOutRange` |
| "in-range positions" | `PositionStatusInRange` |
| "out-of-range positions" | `PositionStatusOutRange` |
| "closed positions" | `PositionStatusClosed` |
| "all positions" | `PositionStatusInRange,PositionStatusOutRange,PositionStatusClosed` |

Additional parameter mappings:
- Specific chain → `chainIds={chainId}` (use chain ID number, not slug)
- All chains → `chainIds=` (empty)
- Token keyword → `keyword={symbol}`
- Sort → `sorts=valueUsd:desc` (default)
- Page → `page=1` (default, 1-indexed)
- Page size → `pageSize=10` (default)

### Step 2: Fetch Positions

Make the request using **WebFetch**:

```
URL: https://earn-service.kyberswap.com/api/v1/positions?wallet={wallet}&chainIds={chainIds}&protocols={protocols}&statuses={statuses}&keyword={keyword}&sorts={sorts}&page={page}&pageSize={pageSize}
Prompt: Return the full JSON response body exactly as received.
```

Add the `X-Client-Id: ai-agent-skills` header.

### Step 3: Handle Errors

Check the response for errors before proceeding:

| Scenario | Quick Fix |
|---|---|
| No positions found | Wallet has no positions matching the specified filters. Try broadening filters (e.g., "all positions") or verify the wallet address. |
| Invalid wallet address | Validate format: `^0x[a-fA-F0-9]{40}$`. Ensure it is not the zero address or native token sentinel. |
| API error (500) | Retry. The Earn Service may be temporarily unavailable. |
| Rate limited (429) | Wait and retry with exponential backoff. |
| Empty response | The API returned no data. Verify the wallet address and try again. |

For any error not listed here, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.

### Step 4: Parse and Calculate

Extract the following from the response:

**From top-level `data.stats`:**
- Total positions: `stats.totalItems`
- Total portfolio value: `stats.totalValueUsd`
- Total unclaimed fees: `stats.totalUnclaimedFeeUsd`
- Total earned fees: `stats.totalEarnedFeeUsd`
- Total claimed fees: `stats.totalClaimedFeeUsd`
- Total unclaimed rewards: `stats.totalUnclaimedRewardUsd`
- Total claimed rewards: `stats.totalClaimedRewardUsd`
- Total pending rewards: `stats.totalPendingRewardUsd`

**For each position in `data.positions[]`:**
- Token pair: `currentAmounts[0].token.symbol` / `currentAmounts[1].token.symbol`
- Position value: `valueInUSD`
- Current amounts: `currentAmounts[].amount.usdValue` and human amount (`amount / 10^decimals`)
- Provided amounts (initial deposit): `providedAmounts[].amount.usdValue`
- PnL: `sum(currentAmounts usdValue) + sum(unclaimed fee usdValue) - sum(providedAmounts usdValue)`
- Unclaimed fees: `stats.earning.fee.unclaimed[].amount.usdValue`
- APR: `stats.apr.all.30d` (use 30d as default display)
- LP APR: `stats.apr.lp.30d`
- Reward APR: `stats.apr.reward.lm` or `stats.apr.reward.eg` (30d values)
- Earnings: `stats.earning.totalUsd` (24h, 7d, 30d)
- Protocol: `pool.protocol.name`
- Pool address: `pool.address`
- Price range: `extra.priceRange.min` to `extra.priceRange.maxPrice`
- Current pool price: `pool.price`
- Chain: `chain.name` (chain ID: `chain.id`)
- Token ID: `tokenId`
- Token address (NFT manager): `tokenAddress`
- Status: `status`
- Created: `createdAtTime` (unix timestamp)
- Last updated: `lastUpdatedAt` (unix timestamp)

**Status mapping:**
- `PositionStatusInRange` → In Range
- `PositionStatusOutRange` → Out of Range
- `PositionStatusClosed` → Closed

### Step 5: Display Results

**Portfolio Summary (always show first):**

```
## Liquidity Position Portfolio for `{wallet}`

| Metric | Value |
|---|---|
| Total Positions | {totalItems} |
| Total Value | ${totalValueUsd} |
| Total Unclaimed Fees | ${totalUnclaimedFeeUsd} |
| Total Earned Fees | ${totalEarnedFeeUsd} |
```

**Positions Table:**

```
## Active Positions

| # | Chain | Pool | Protocol | Value | APR (30d) | Unclaimed Fees | Status |
|---|---|---|---|---|---|---|---|
| 1 | {chain} | {token0}/{token1} | {protocol} | ${value} | {apr}% | ${fees} | In Range |
| 2 | {chain} | {token0}/{token1} | {protocol} | ${value} | {apr}% | ${fees} | Out of Range |
```

**Detailed position view (when user asks about a specific position or wants details):**

```
## Position #{tokenId} -- {token0}/{token1} on {Chain}

| Detail | Value |
|---|---|
| Protocol | {protocol.name} |
| Pool | `{pool.address}` |
| Token ID | #{tokenId} |
| Status | {status} |
| Value | ${valueInUSD} |
| APR (30d) | {apr.all.30d}% (LP: {apr.lp.30d}% + Rewards: {apr.reward}%) |

### Current Amounts
| Token | Amount | USD Value | Price |
|---|---|---|---|
| {token0} | {amount0} | ${usdValue0} | ${priceUsd0} |
| {token1} | {amount1} | ${usdValue1} | ${priceUsd1} |

### Provided Amounts (Initial Deposit)
| Token | Amount | USD Value |
|---|---|---|
| {token0} | {provided0} | ${providedUsd0} |
| {token1} | {provided1} | ${providedUsd1} |

### Unclaimed Fees
| Token | Amount | USD Value |
|---|---|---|
| {token0} | {fee0} | ${feeUsd0} |
| {token1} | {fee1} | ${feeUsd1} |

### Price Range
| | Value |
|---|---|
| Current Price | {pool.price} |
| Min Range | {extra.priceRange.min} |
| Max Range | {extra.priceRange.maxPrice} |
| In Range | {yes/no} |

### Earnings (30d)
| Period | Earned |
|---|---|
| 24h | ${earning.24h} |
| 7d | ${earning.7d} |
| 30d | ${earning.30d} |
```

If more than 10 positions are returned, note pagination: *"Showing {count} of {total} positions. Use 'show positions page 2' for more."*

### Structured JSON Output

After the markdown tables, always include a JSON code block so other plugins or agents can consume the result programmatically:

````
```json
{
  "type": "kyberswap-position-manager",
  "wallet": "{wallet}",
  "summary": {
    "totalPositions": {totalItems},
    "totalValueUsd": {totalValueUsd},
    "totalUnclaimedFeeUsd": {totalUnclaimedFeeUsd},
    "totalEarnedFeeUsd": {totalEarnedFeeUsd}
  },
  "positions": [
    {
      "tokenId": {tokenId},
      "chain": "{chain}",
      "chainId": {chainId},
      "pool": "{poolAddress}",
      "protocol": "{protocolName}",
      "token0": "{token0Symbol}",
      "token1": "{token1Symbol}",
      "status": "{status}",
      "valueUsd": {valueInUSD},
      "apr30d": {apr},
      "unclaimedFeesUsd": {feeUsd},
      "priceRange": {
        "min": {min},
        "max": {max},
        "current": {currentPrice}
      }
    }
  ]
}
```
````

This JSON block enables downstream agents or plugins to parse the position data without scraping the markdown tables.

### Step 6: Actionable Suggestions

After displaying positions, suggest relevant actions based on position state:

**For out-of-range positions:**
> "Position #{tokenId} is out of range and not earning fees. Consider migrating to a new range: `/zap migrate position #{tokenId} ...`"

**For positions with significant unclaimed fees (> $1 USD):**
> "You have ${fees} in unclaimed fees on position #{tokenId}. Consider zapping out to collect: `/zap out position #{tokenId} on {chain} from {wallet}`"

**For adding more liquidity:**
> "To add more liquidity: `/zap 1 ETH into {pool} on {chain} from {wallet}`"

**For checking token prices:**
> "Check current prices with `/token-info {token0} {token1} on {chain}`"

## API Reference

### Endpoint

```
GET https://earn-service.kyberswap.com/api/v1/positions
```

### Query Parameters

| Parameter | Required | Description |
|---|---|---|
| `wallet` | Yes | Wallet address |
| `chainIds` | No | Comma-separated chain IDs (empty = all chains) |
| `protocols` | No | Filter by protocol |
| `statuses` | No | Comma-separated status values: `PositionStatusInRange`, `PositionStatusOutRange`, `PositionStatusClosed` |
| `keyword` | No | Search by token symbol or pool address |
| `sorts` | No | Sort order, e.g. `valueUsd:desc`, `valueUsd:asc` |
| `page` | No | Page number (1-indexed, default: 1) |
| `pageSize` | No | Results per page (default: 10) |

### Position Object Key Fields

| Field | Type | Description |
|---|---|---|
| `chain` | `{ name, logo, id }` | Chain information |
| `tokenId` | number | NFT token ID |
| `tokenAddress` | string | NFT manager contract address |
| `positionId` | string | Position identifier |
| `wallet` | string | Owner wallet address |
| `liquidity` | string | Liquidity amount |
| `status` | string | `PositionStatusInRange`, `PositionStatusOutRange`, or `PositionStatusClosed` |
| `valueInUSD` | number | Position value in USD |
| `createdAtTime` | number | Unix timestamp of creation |
| `createAtBlock` | number | Block number at creation |
| `lastUpdatedAt` | number | Unix timestamp of last update |
| `stats.apr.all` | `{ 24h, 7d, 30d }` | Combined APR |
| `stats.apr.lp` | `{ 24h, 7d, 30d }` | LP fee APR |
| `stats.apr.reward.lm` | `{ 24h, 7d, 30d }` | Liquidity mining reward APR |
| `stats.apr.reward.eg` | `{ 24h, 7d, 30d }` | Elastic reward APR |
| `stats.earning.totalUsd` | `{ 24h, 7d, 30d }` | Total earnings in USD |
| `stats.earning.fee.unclaimed[]` | array | Unclaimed fee tokens with `{ amount: { usdValue, priceUsd, amount }, token: { logo, symbol, name, decimals, address } }` |
| `stats.earning.fee.claimed[]` | array | Claimed fee tokens (same structure) |
| `currentAmounts[]` | array | Current token amounts in the position |
| `providedAmounts[]` | array | Initial deposit amounts |
| `pool` | object | Pool details: `{ id, address, price, tokenAmounts[], fees[], tickSpacing, protocol: { type, logo, name }, category, hooks }` |
| `extra.priceRange` | `{ min, maxPrice }` | Position price range |
| `id` | number | Internal position ID |

### Response Stats (Top-Level)

| Field | Description |
|---|---|
| `data.stats.totalItems` | Total number of matching positions |
| `data.stats.totalValueUsd` | Sum of all position values |
| `data.stats.totalEarnedFeeUsd` | Total fees earned (all time) |
| `data.stats.totalClaimedFeeUsd` | Total fees claimed |
| `data.stats.totalUnclaimedFeeUsd` | Total unclaimed fees |
| `data.stats.totalClaimedRewardUsd` | Total claimed rewards |
| `data.stats.totalUnclaimedRewardUsd` | Total unclaimed rewards |
| `data.stats.totalPendingRewardUsd` | Total pending rewards |

## Important Notes

- This is a **read-only skill** -- no transactions are built or submitted.
- To add liquidity, use the **zap** skill (`${CLAUDE_PLUGIN_ROOT}/skills/zap/SKILL.md`).
- To remove liquidity, use the **zap** skill's zap-out workflow.
- To migrate positions, use the **zap** skill's migrate workflow.
- Position values and APRs are estimates provided by the KyberSwap Earn Service and may differ slightly from on-chain values.
- Unclaimed fees must be collected via a zap-out or collect transaction.
- Default to showing active (in-range + out-of-range) positions sorted by value if no filter is specified.
- When viewing positions across all chains, the `chainIds` parameter should be an empty string.
- If the user doesn't specify a chain, query all chains.
- Never guess wallet addresses. Always ask the user if not provided.

## Additional Resources

### Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`** -- Token addresses and decimals by chain
- **`${CLAUDE_PLUGIN_ROOT}/references/api-reference.md`** -- Full API specification, error codes, rate limiting

### Related Skills

- **`${CLAUDE_PLUGIN_ROOT}/skills/zap/SKILL.md`** -- Zap in, zap out, and migrate positions
- **`${CLAUDE_PLUGIN_ROOT}/skills/token-info/SKILL.md`** -- Token price and information lookup

### External Documentation

- **KyberSwap Earn:** https://kyberswap.com/earn

## Troubleshooting

| Issue | Resolution |
|---|---|
| No positions found | Verify the wallet address owns liquidity positions. Try "all positions" to include closed ones. Check the wallet on the KyberSwap Earn UI. |
| Missing APR data | Some positions (especially newly created or low-liquidity ones) may not have APR data yet. The Earn Service calculates APR periodically. |
| Stale position data | Position data is indexed periodically. Recent on-chain changes (deposits, withdrawals) may take a few minutes to appear. |
| Chain not showing positions | Verify the chain ID is correct. Try querying all chains (omit `chainIds`) to see if positions exist on a different chain. |
| Rate limited | The Earn Service may rate-limit requests. Wait and retry. |

For error codes not covered above, or for advanced debugging, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.
