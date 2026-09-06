---
name: order-manager
description: This skill should be used when the user asks to "check my orders", "show my limit orders", "list open orders", "order status", "order history", "show filled orders", "view partially filled orders", "order fill history", "how much has been filled", "order summary", "order portfolio", or wants to view, monitor, or analyze their KyberSwap limit orders across any status. Queries the KyberSwap Limit Order API to display order details, fill progress, and transaction history across 17 EVM chains.
metadata:
  tags:
    - defi
    - kyberswap
    - limit-order
    - orders
    - portfolio
    - evm
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Order Manager Skill

Query, display, and analyze limit orders. View open, partially filled, filled, cancelled, and expired orders with fill progress and transaction history.

## Input Parsing

The user will provide input like:
- `show my orders on ethereum for 0xAbc123...`
- `check open orders on arbitrum for 0xAbc123...`
- `show filled orders on base for 0xAbc123...`
- `order status on ethereum for 0xAbc123...` (shows all active statuses)
- `show all orders for 0xAbc123...` (all statuses, all chains)

Extract these fields:
- **maker** — the address to query orders for (**required**)
- **chain** — the chain slug (default: `ethereum`)
- **status** — filter by order status (default: show `open` + `partially_filled`)

**If the maker address is not provided, ask the user for it before proceeding.** Do not guess or use a placeholder address.

**Maker address validation — reject or warn before proceeding:**
- **Must not be the zero address** (`0x0000000000000000000000000000000000000000`) — this is an invalid address and the query will return no meaningful results.
- **Must not be the native token sentinel** (`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`) — this is a placeholder for native tokens, not a real account.
- **Warn if it matches a known contract address** (e.g., a token address or the DSLOProtocol contract) — querying orders for a contract address is unusual and likely a mistake. Ask the user to confirm.

### Status Values

| Status | Description |
|---|---|
| `open` | Order is active and waiting to be filled |
| `partially_filled` | Order has been partially filled by one or more takers |
| `filled` | Order has been completely filled |
| `cancelled` | Order was cancelled (gasless or hard cancel) |
| `expired` | Order expired without being fully filled |

**Default behavior:**
- No status specified → query `open` and `partially_filled` (active orders)
- "all orders" or "order summary" → query all five statuses in sequence
- Specific status named → query only that status

## Supported Chains (17)

ethereum (1), bsc (56), arbitrum (42161), polygon (137), optimism (10), avalanche (43114), base (8453), linea (59144), mantle (5000), sonic (146), berachain (80094), ronin (2020), unichain (130), hyperevm (999), plasma (9745), etherlink (42793), monad (143)

> **Note:** Limit orders are not supported on megaeth. If the user requests megaeth, inform them and suggest using a swap instead.

## Workflow

### Step 1: Query Orders

Use **WebFetch** for this GET request:

```
URL: https://limit-order.kyberswap.com/read-ks/api/v1/orders?chainId={chainId}&maker={makerAddress}&status={status}
Prompt: Return the full JSON response body exactly as received.
```

Add the `X-Client-Id: ai-agent-skills` header.

If the user asks for "all orders" or "order summary", query multiple statuses in sequence: `open`, `partially_filled`, `filled`, `cancelled`, `expired`.

If no status specified, default to showing `open` and `partially_filled` (active orders).

### Step 2: Parse and Calculate

For each order in the response, extract and compute:

**Order object fields:**
- `id`, `chainId`, `nonce`, `makerAsset`, `takerAsset`, `contractAddress`, `orderHash`
- `makerAssetSymbol`, `takerAssetSymbol`, `makerAssetLogoURL`, `takerAssetLogoURL`
- `makerAssetDecimals`, `takerAssetDecimals`
- `makingAmount`, `takingAmount` (wei strings)
- `filledMakingAmount`, `filledTakingAmount` (wei strings)
- `status`, `createdAt`, `expiredAt`
- `transactions[]` array with: `id`, `txHash`, `txTime`, `makingAmount`, `takingAmount`, `makingAmountUSD`, `takingAmountUSD`

**Calculations:**

1. **Human-readable amounts** — convert wei strings using the correct decimals:
   ```bash
   python3 -c "print({amount_wei} / 10**{decimals})"
   ```

2. **Fill percentage:**
   ```
   fillPercent = filledMakingAmount / makingAmount * 100
   ```

3. **Remaining amounts:**
   ```
   remainingMaking = makingAmount - filledMakingAmount
   remainingTaking = takingAmount - filledTakingAmount
   ```

4. **Target price** (what the maker set):
   ```
   targetPrice = takingAmount / makingAmount
   ```

5. **Effective price** (actual execution price, for partially/fully filled orders):
   ```
   effectivePrice = filledTakingAmount / filledMakingAmount
   ```

6. **Time since creation** — human-readable duration from `createdAt` to now.

7. **Time until expiry** — human-readable duration from now to `expiredAt`, or "Expired" if in the past.

**Use `python3` for all wei conversions — never mental math.**

### Step 3: Display Results

**For active orders (open + partially_filled):**

```
## Active Limit Orders on {Chain}

Showing {count} active order(s) for `{maker}`

| # | Pair | Side | Making | Taking | Target Price | Filled | Status | Expires |
|---|---|---|---|---|---|---|---|---|
| 1 | {makerSymbol}/{takerSymbol} | Sell {makerSymbol} | {makingAmount} {makerSymbol} | {takingAmount} {takerSymbol} | 1 {makerSymbol} = {price} {takerSymbol} | {fillPercent}% | {status} | {expiryDate} |
```

**For a single order with detail (when user asks about a specific order):**

Show detailed view with fill history:

```
## Order #{orderId} — {makerSymbol} → {takerSymbol}

| Detail | Value |
|---|---|
| Status | {status} |
| Pair | {makerSymbol} / {takerSymbol} |
| Making | {makingAmount} {makerSymbol} |
| Taking | {takingAmount} {takerSymbol} |
| Target price | 1 {makerSymbol} = {price} {takerSymbol} |
| Filled | {fillPercent}% ({filledMaking} / {makingAmount} {makerSymbol}) |
| Remaining | {remainingMaking} {makerSymbol} |
| Created | {createdDate} |
| Expires | {expiryDate} |
| Chain | {chain} (ID: {chainId}) |
| Order hash | `{orderHash}` |

### Fill History

| # | Time | Sold | Received | USD Value | Tx |
|---|---|---|---|---|---|
| 1 | {txTime} | {makingAmt} {makerSymbol} | {takingAmt} {takerSymbol} | ~${usdValue} | `{txHash}` |
```

**For portfolio summary (all statuses):**

```
## Order Summary for `{maker}`

| Status | Count | Total Making (USD) | Total Taking (USD) |
|---|---|---|---|
| Open | {count} | ~${value} | ~${value} |
| Partially Filled | {count} | ~${value} | ~${value} |
| Filled | {count} | -- | -- |
| Cancelled | {count} | -- | -- |
| Expired | {count} | -- | -- |
```

### Step 4: Actionable Suggestions

After displaying orders, suggest relevant actions:

- **For open orders:** "To cancel: `cancel limit order {orderId} on {chain} from {maker}`"
- **For partially filled orders:** Show remaining amount and suggest cancelling if price has moved significantly. Example: "This order is {fillPercent}% filled with {remainingMaking} {makerSymbol} remaining. To cancel the remaining portion: `cancel limit order {orderId} on {chain} from {maker}`"
- **For expired orders:** "This order expired without being filled. Consider creating a new order with updated price: `limit sell {amount} {makerSymbol} for {takerSymbol} at {newPrice} on {chain} from {maker}`"
- **For all views:** Suggest using the `token-info` skill to check current price vs target price: "To compare target price with current market: `price {makerSymbol} on {chain}`"

### Structured JSON Output

After the markdown table, always include a JSON code block so other plugins or agents can consume the result programmatically:

````
```json
{
  "type": "kyberswap-order-manager",
  "chain": "{chain}",
  "chainId": {chainId},
  "maker": "{maker}",
  "summary": {
    "open": {count},
    "partiallyFilled": {count},
    "filled": {count},
    "cancelled": {count},
    "expired": {count}
  },
  "orders": [
    {
      "orderId": {id},
      "status": "{status}",
      "makerAsset": "{makerSymbol}",
      "takerAsset": "{takerSymbol}",
      "makingAmount": "{makingAmount}",
      "takingAmount": "{takingAmount}",
      "filledPercent": "{fillPercent}",
      "targetPrice": "{targetPrice}",
      "effectivePrice": "{effectivePrice}",
      "remainingMaking": "{remaining}",
      "createdAt": {timestamp},
      "expiredAt": {timestamp},
      "fillCount": {txCount}
    }
  ]
}
```
````

## Error Handling

### Common Error Scenarios

| Scenario | Cause | Quick Fix |
|---|---|---|
| No orders found | Maker has no orders with the specified status on this chain | Try a different status or chain. Use "show all orders" to check all statuses. |
| Invalid chain | Chain not supported for limit orders | Check the 17 supported chains. megaeth is not supported. |
| Invalid maker address | Address is zero address or malformed | Validate address format: `^0x[a-fA-F0-9]{40}$` |
| Rate limited | Too many requests | Wait and retry. Space requests by at least 1 second. |

### HTTP Error Codes

| Code | Meaning | Action |
|---|---|---|
| 400 | Bad request | Check query parameters: `chainId`, `maker`, `status`. |
| 404 | Not found | Check endpoint URL and chain ID. |
| 429 | Rate limited | Wait and retry with exponential backoff. |
| 500 | Internal server error | Retry after a brief delay. If persistent, the service may be down. |

For any error not listed here, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.

## Important Notes

- This is a **read-only skill** — no orders are created, modified, or cancelled.
- To create orders, use the `limit-order` skill.
- To cancel orders, use the `limit-order` skill's cancel workflow.
- Always convert wei amounts to human-readable using the correct decimals from the order object (`makerAssetDecimals`, `takerAssetDecimals`).
- **Use `python3` for wei conversions — never mental math.**
- Default to showing active orders (`open` + `partially_filled`) if no status specified.
- If the user doesn't specify a chain, default to `ethereum`.
- If the user specifies a chain not in the 17 supported chains, inform them that limit orders are not supported on that chain.
- Suggest checking current token price via `token-info` skill when viewing orders to compare target vs market price.
- Native token address: `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`

## Additional Resources

### Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`** — Token addresses and decimals by chain
- **`${CLAUDE_PLUGIN_ROOT}/references/api-reference.md`** — Full API specification, error codes, rate limiting

### Documentation

- **Limit Order API:** https://docs.kyberswap.com/kyberswap-solutions/limit-order/limit-order-api-specification/maker-apis

## Troubleshooting

**No orders showing up?**
- Verify the maker address is correct and is the address that created the orders.
- Try querying all statuses: "show all orders for {maker} on {chain}".
- Orders are chain-specific — ensure you're querying the correct chain.
- If orders were created recently, they may take a few seconds to appear.

**Fill percentage seems wrong?**
- Fill amounts are in wei. Always use `makerAssetDecimals` for conversion.
- Partial fills accumulate — `filledMakingAmount` is the total filled across all transactions.

**Order shows as expired but was partially filled?**
- An order can expire while partially filled. The filled portion is settled; the remaining portion is no longer available.
- Check the `transactions[]` array for the fill history of what was executed before expiry.

For error codes not covered above, or for advanced debugging, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.
