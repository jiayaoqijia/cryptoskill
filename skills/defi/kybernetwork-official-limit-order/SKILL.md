---
name: limit-order
description: This skill should be used when the user asks to "create a limit order", "place a limit order", "set a target price order", "limit buy", "limit sell", "cancel limit order", "check my orders", "query limit orders", or wants to trade tokens at a specific price. Creates, queries, and cancels gasless limit orders via KyberSwap Limit Order API across 17 EVM chains.
metadata:
  tags:
    - defi
    - kyberswap
    - limit-order
    - evm
    - gasless
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Limit Order Skill

Create, query, and cancel gasless limit orders via the KyberSwap Limit Order API. Orders are signed off-chain using EIP-712 and settled on-chain when a taker fills them. No gas is required to create or gasless-cancel an order.

**This skill supports three operations:**
1. **Create** a limit order (sign-message, user signs, submit order)
2. **Query** existing orders (by maker address)
3. **Cancel** an order (gasless cancel or hard cancel)

## Input Parsing

The user will provide input like:
- `limit sell 1000 USDC for ETH at 0.00035 on arbitrum from 0xAbc123...`
- `limit buy 0.5 ETH with USDC at 3200 on ethereum from 0xAbc123...`
- `place a limit order to sell 100 LINK for USDC at 15.50 on polygon from 0xAbc123...`
- `check my limit orders on ethereum for 0xAbc123...`
- `cancel limit order {orderId} on arbitrum from 0xAbc123...`

### Create Order — Extract These Fields

- **makerAsset** (tokenIn) — the token the maker is selling
- **takerAsset** (tokenOut) — the token the maker wants to receive
- **makingAmount** — the human-readable amount of makerAsset to sell
- **targetPrice** — the price per unit of makerAsset denominated in takerAsset
- **chain** — the chain slug (default: `ethereum`)
- **maker** — the address creating the order (**required**)
- **expiry** — order expiry duration (e.g., "1 hour", "1 day", "7 days", "1 week", "30 days"). Default: **7 days**
- **recipient** — the address to receive taker tokens (default: same as maker)

Derive the **takingAmount** from the user's input based on order direction:

**Limit-sell** (user sells `makerAsset` to receive `takerAsset`):
```
takingAmount = makingAmount × targetPrice
```
*Example: Sell 1 ETH at 3200 USDC/ETH → makerAsset=WETH, makingAmount=1, takerAsset=USDC, takingAmount=3200*

**Limit-buy** (user wants to buy `takerAsset` by spending `makerAsset`):
```
makerAsset  = token being spent
takerAsset  = token being bought
makingAmount = desiredBuyAmount × targetPrice   (amount of makerAsset to spend)
takingAmount = desiredBuyAmount                  (amount of takerAsset to receive)
```
*Example: Buy 1 ETH at 3200 USDC/ETH → makerAsset=USDC, makingAmount=3200, takerAsset=WETH, takingAmount=1*

> **Important:** The formula `takingAmount = makingAmount × targetPrice` is correct for limit-sell only. For limit-buy the direction inverts — always confirm whether the user is selling or buying before computing amounts.

### Query Orders — Extract These Fields

- **maker** — the address to query orders for (**required**)
- **chain** — the chain slug (default: `ethereum`)
- **status** — filter by order status: `active`, `filled`, `cancelled`, `expired` (default: `active`)

### Cancel Order — Extract These Fields

- **orderId** (or orderIds) — the order ID(s) to cancel (**required**)
- **maker** — the address that created the order (**required**)
- **chain** — the chain slug (default: `ethereum`)
- **cancelType** — `gasless` (default) or `hard`

**If the maker address is not provided, ask the user for it before proceeding.** Do not guess or use a placeholder address.

**Maker address validation:** See `${CLAUDE_PLUGIN_ROOT}/references/address-validation.md` for validation rules. Reject zero address, native token sentinel, and warn on contract addresses.

## Supported Chains (17)

See `${CLAUDE_PLUGIN_ROOT}/references/supported-chains.md` for the full chain list with chain IDs. All Aggregator chains except MegaETH are supported.

> **Note:** Limit orders are not supported on megaeth. If the user requests megaeth, inform them and suggest using a swap instead.

## Create Order Workflow

### Step 1: Resolve Token Addresses

Read the token registry at `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`.

Look up `makerAsset` and `takerAsset` for the specified chain. Match case-insensitively. Note the **decimals** for each token.

**Aliases to handle — IMPORTANT: Limit orders require ERC-20 tokens.** The native token sentinel (`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`) is NOT valid for `makerAsset` or `takerAsset`. When the user specifies a native token alias, automatically convert it to the wrapped ERC-20 equivalent. See `${CLAUDE_PLUGIN_ROOT}/references/wrapped-tokens.md` for the complete mapping table.

When auto-converting, display a note to the user: *"Native {TOKEN} converted to W{TOKEN} for limit orders — the Limit Order API requires ERC-20 tokens, not native token addresses."*

**If a token is not found in the registry:**
Use the fallback sequence described at the bottom of `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`:
1. **KyberSwap Token API** (preferred) — search whitelisted tokens first: `https://token-api.kyberswap.com/api/v1/public/tokens?chainIds={chainId}&name={symbol}&isWhitelisted=true` via WebFetch. Pick the result whose `symbol` matches exactly with the highest `marketCap`. If no whitelisted match, retry without `isWhitelisted` (only trust verified or market-cap tokens). If still nothing, browse `page=1&pageSize=100` (try up to 3 pages).
2. **CoinGecko API** (secondary fallback) — search CoinGecko for verified contract addresses if the Token API doesn't have it.
3. **Ask user manually** (final fallback) — if CoinGecko also fails, ask the user to provide the contract address. Never guess or fabricate addresses.

### Step 2: Check Token Safety

For any token **not** in the built-in registry and **not** a native token, check the honeypot/FOT API:

```
GET https://token-api.kyberswap.com/api/v1/public/tokens/honeypot-fot-info?chainId={chainId}&address={tokenAddress}
```

Via **WebFetch**, check both `makerAsset` and `takerAsset`:
- If `isHoneypot: true` — **refuse the order** and warn the user that this token is flagged as a honeypot (cannot be sold after buying).
- If `isFOT: true` — warn the user that this token has a fee-on-transfer (tax: `{tax}%`). The actual received amount will be less than expected. Proceed only if the user acknowledges the tax.

### Step 2a: Price Reference Check

Before creating the order, fetch the current market price to help the user evaluate their target price. Use the KyberSwap Aggregator to quote 1 unit of makerAsset against takerAsset:

```
GET https://aggregator-api.kyberswap.com/{chain}/api/v1/routes?tokenIn={makerAssetAddress}&tokenOut={takerAssetAddress}&amountIn={oneUnitMakerInWei}&source=ai-agent-skills
```

Via **WebFetch**. For native tokens in the quote, use the native token sentinel `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`. For limit orders where tokens are wrapped (WETH, WPOL, etc.), use the wrapped token address.

**Calculate the current market price:**
```
currentMarketPrice = amountOut / 10^(takerAsset decimals)
```

**Compare target price vs market price:**
```
deviationPercent = ((targetPrice - currentMarketPrice) / currentMarketPrice) * 100
```

**Display price context in the confirmation step (Step 6a):**

Add a "Price Context" row to the confirmation table:

| Detail | Value |
|---|---|
| Current market price | 1 {makerAsset} = {currentMarketPrice} {takerAsset} |
| Target price | 1 {makerAsset} = {targetPrice} {takerAsset} |
| Deviation | {deviationPercent}% {above/below} market |

**Warning thresholds — warn prominently if the target price is unfavorable:**

For **limit-sell** orders (selling makerAsset):
- Target price **below** market by > 5% → **WARN**: *"Your target price is {deviationPercent}% below the current market price. You would receive less than the current market rate. Are you sure this is intentional?"*
- Target price **above** market → Informational: *"Your target price is {deviationPercent}% above the current market price. The order will fill when the market reaches your target."*

For **limit-buy** orders (buying takerAsset):
- Target price **above** market by > 5% → **WARN**: *"Your target price is {deviationPercent}% above the current market price. You would pay more than the current market rate. Are you sure this is intentional?"*
- Target price **below** market → Informational: *"Your target price is {deviationPercent}% below the current market price. The order will fill when the market reaches your target."*

**If the Aggregator route fails** (no liquidity for the pair), skip the price check and note: *"Could not fetch current market price for this pair. Unable to compare target price with market. Proceed with caution."*

> **Tip:** Use the `token-info` skill for more detailed token information including market cap and safety status.

### Step 3: Convert Amounts to Wei

```
makingAmountWei = makingAmount * 10^(makerAsset decimals)
takingAmountWei = takingAmount * 10^(takerAsset decimals)
```

Both results must be plain integer strings with no decimals, no scientific notation, and no separators.

**Use deterministic conversion** — compute via `python3` or `bc`, never mental math:

```bash
python3 -c "print(int({makingAmount} * 10**{makerDecimals}))"
python3 -c "print(int({takingAmount} * 10**{takerDecimals}))"
```

### Step 4: Get the Contract Address

Fetch the DSLOProtocol contract address for the chain:

```
GET https://limit-order.kyberswap.com/read-ks/api/v1/configs/contract-address?chainId={chainId}
```

Via **WebFetch**. The contract address is typically `0xcab2FA2eeab7065B45CBcF6E3936dDE2506b4f6C` on all supported chains, but always verify.

### Step 5: Compute Expiry Timestamp

Convert the user's expiry duration to a Unix timestamp:

```bash
# Example: 7 days from now
echo $(($(date +%s) + 7 * 86400))
```

Common durations:
| Duration | Seconds |
|---|---|
| 1 hour | 3600 |
| 1 day | 86400 |
| 7 days | 604800 |
| 30 days | 2592000 |

### Step 6: Get EIP-712 Sign Message

Use `Bash(curl)` for this POST request:

```bash
curl -s --connect-timeout 10 --max-time 30 \
  -X POST "https://limit-order.kyberswap.com/write/api/v1/orders/sign-message" \
  -H "Content-Type: application/json" \
  -H "X-Client-Id: ai-agent-skills" \
  -d '{
    "chainId": "{chainId}",
    "makerAsset": "{makerAssetAddress}",
    "takerAsset": "{takerAssetAddress}",
    "maker": "{makerAddress}",
    "allowedSenders": ["0x0000000000000000000000000000000000000000"],
    "makingAmount": "{makingAmountWei}",
    "takingAmount": "{takingAmountWei}",
    "expiredAt": {expiryTimestamp}
  }'
```

The response contains the EIP-712 typed data that the user must sign.

### Step 6a: Display Order Summary and Request Confirmation

**CRITICAL: Always show order details and ask for confirmation before requesting a signature.**

Present the order details:

```
## Limit Order — Confirmation Required

**Sell {makingAmount} {makerAsset} for {takingAmount} {takerAsset}** on {Chain}

| Detail | Value |
|---|---|
| You sell | {makingAmount} {makerAsset} |
| You receive | {takingAmount} {takerAsset} |
| Target price | 1 {makerAsset} = {targetPrice} {takerAsset} |
| Expires | {expiryDate} ({expiryDuration} from now) |
| Chain | {chain} (Chain ID: {chainId}) |

### Addresses

| Field | Value |
|---|---|
| Maker | `{maker}` |
| Recipient | `{recipient}` |
| Maker Asset | `{makerAssetAddress}` |
| Taker Asset | `{takerAssetAddress}` |
| Contract | `{contractAddress}` |

### Fee Structure

Limit order fees are deducted from the taker amount upon fill:

| Token Category | Fee Rate |
|---|---|
| Super Stable | 0.01% |
| Stable | 0.02% |
| Normal | 0.1% |
| Exotic | 0.3% |
| High Volatility | 0.5% |
| Super High Volatility | 1% |

### Warnings

- **Signing an EIP-712 message authorizes the limit order contract to spend your {makerAsset} when a taker fills the order.**
- Review the target price and amounts carefully before signing.
- The order will remain active until filled, cancelled, or expired.

**Do you want to proceed with signing this limit order?** (yes/no)
```

**Wait for the user to explicitly confirm with "yes", "confirm", "proceed", or similar affirmative response before requesting the signature.**

If the user says "no", "cancel", or similar, abort and inform them the order was not created. Do NOT proceed to Step 7.

### Step 7: User Signs the EIP-712 Message

Present the EIP-712 typed data from Step 6 to the user for signing. The user must sign this message with their wallet.

```
### EIP-712 Signature Required

Please sign the following EIP-712 message with your wallet:

{EIP-712 typed data JSON from sign-message response}

Provide the signature (0x-prefixed hex string) after signing.
```

**Wait for the user to provide the signature before proceeding.**

### Step 8: Create the Order

Once the user provides the signature, submit the order using `Bash(curl)`:

```bash
curl -s --connect-timeout 10 --max-time 30 \
  -X POST "https://limit-order.kyberswap.com/write/api/v1/orders" \
  -H "Content-Type: application/json" \
  -H "X-Client-Id: ai-agent-skills" \
  -d '{
    "chainId": "{chainId}",
    "makerAsset": "{makerAssetAddress}",
    "takerAsset": "{takerAssetAddress}",
    "maker": "{makerAddress}",
    "allowedSenders": ["0x0000000000000000000000000000000000000000"],
    "makingAmount": "{makingAmountWei}",
    "takingAmount": "{takingAmountWei}",
    "expiredAt": {expiryTimestamp},
    "signature": "{userSignature}",
    "salt": "{saltFromSignMessage}",
    "interactions": "{interactionsFromSignMessage}"
  }'
```

Include all fields returned from the sign-message response (`salt`, `interactions`, etc.) along with the user's signature.

### Step 8a: Handle Create Errors

| Scenario | Quick Fix |
|---|---|
| Invalid signature | Ensure the user signed the exact EIP-712 message. Re-request signing if needed. |
| Expired timestamp | The `expiredAt` is in the past. Recompute with a future timestamp. |
| Invalid token address | Verify token addresses for the correct chain. |
| Insufficient maker balance | The maker must hold enough makerAsset when the order is filled. |
| Order already exists | The same order parameters with same salt already submitted. |

### Step 9: Format the Output

Present the results:

```
## Limit Order Created

**Sell {makingAmount} {makerAsset} for {takingAmount} {takerAsset}** on {Chain}

| Detail | Value |
|---|---|
| Order ID | `{orderId}` |
| Status | Active |
| You sell | {makingAmount} {makerAsset} |
| You receive | {takingAmount} {takerAsset} |
| Target price | 1 {makerAsset} = {targetPrice} {takerAsset} |
| Expires | {expiryDate} |
| Chain | {chain} (Chain ID: {chainId}) |

> **Next steps:**
> - Your order is now live and will be filled when the market reaches your target price.
> - To check order status: "check my limit orders on {chain} for {maker}"
> - To cancel: "cancel limit order {orderId} on {chain} from {maker}"
```

### Step 10: ERC-20 Approval Reminder

If `makerAsset` is **not** the native token, remind the user about token approval. See `${CLAUDE_PLUGIN_ROOT}/references/approval-guide.md` (ERC-20 section) for the approval template. Use:

- **Token contract:** `{makerAsset address}`
- **Spender (DSLOProtocol):** `{contractAddress}`
- **Amount:** `{makingAmountWei}`

### Structured JSON Output

After the markdown table, always include a JSON code block so other plugins or agents can consume the result programmatically:

````
```json
{
  "type": "kyberswap-limit-order",
  "operation": "create",
  "chain": "{chain}",
  "chainId": {chainId},
  "orderId": "{orderId}",
  "makerAsset": {
    "symbol": "{makerAsset}",
    "address": "{makerAssetAddress}",
    "decimals": {makerAssetDecimals},
    "amount": "{makingAmount}",
    "amountWei": "{makingAmountWei}"
  },
  "takerAsset": {
    "symbol": "{takerAsset}",
    "address": "{takerAssetAddress}",
    "decimals": {takerAssetDecimals},
    "amount": "{takingAmount}",
    "amountWei": "{takingAmountWei}"
  },
  "targetPrice": "{targetPrice}",
  "maker": "{maker}",
  "recipient": "{recipient}",
  "expiredAt": {expiryTimestamp},
  "contract": "{contractAddress}"
}
```
````

## Query Orders Workflow

### Step 1: Query Maker Orders

Use **WebFetch** for this GET request:

```
URL: https://limit-order.kyberswap.com/read-ks/api/v1/orders?chainId={chainId}&maker={makerAddress}&status={status}
Prompt: Return the full JSON response body exactly as received.
```

Add the `X-Client-Id: ai-agent-skills` header.

### Step 2: Display Results

Present the orders in a table:

```
## Your Limit Orders on {Chain}

Showing {count} {status} order(s) for `{maker}`

| # | Sell | Buy | Target Price | Filled | Expires | Order ID |
|---|---|---|---|---|---|---|
| 1 | {makingAmount} {makerAsset} | {takingAmount} {takerAsset} | 1 {makerAsset} = {price} {takerAsset} | {filledPercent}% | {expiryDate} | `{orderId}` |
| ... | ... | ... | ... | ... | ... | ... |
```

Convert amounts from wei to human-readable using the token decimals.

### Structured JSON Output

````
```json
{
  "type": "kyberswap-limit-order",
  "operation": "query",
  "chain": "{chain}",
  "chainId": {chainId},
  "maker": "{maker}",
  "status": "{status}",
  "count": {count},
  "orders": [
    {
      "orderId": "{orderId}",
      "makerAsset": "{makerAssetSymbol}",
      "takerAsset": "{takerAssetSymbol}",
      "makingAmount": "{makingAmount}",
      "takingAmount": "{takingAmount}",
      "filledPercent": "{filledPercent}",
      "expiredAt": {expiredAt},
      "status": "{status}"
    }
  ]
}
```
````

## Gasless Cancel Workflow

**Gasless cancellation is free but not instant — it takes up to 90 seconds.** During this window, the order may still be filled by a taker.

### Step 1: Request Cancel Signature

Use `Bash(curl)` for this POST request:

```bash
curl -s --connect-timeout 10 --max-time 30 \
  -X POST "https://limit-order.kyberswap.com/write/api/v1/orders/cancel-sign" \
  -H "Content-Type: application/json" \
  -H "X-Client-Id: ai-agent-skills" \
  -d '{
    "chainId": "{chainId}",
    "maker": "{makerAddress}",
    "orderIds": [{orderIds}]
  }'
```

### Step 2: Display Cancel Confirmation

```
## Gasless Cancel — Confirmation Required

You are about to cancel the following order(s):

| Order ID | Sell | Buy |
|---|---|---|
| `{orderId}` | {makingAmount} {makerAsset} | {takingAmount} {takerAsset} |

### Warnings

- **Gasless cancellation is not instant — it takes up to 90 seconds. During this window, the order may still be filled.**
- If you need immediate cancellation, use **hard cancel** instead (requires gas).

Please sign the cancellation message with your wallet and provide the signature.
```

### Step 3: User Signs Cancellation Message

Present the cancellation data from Step 1 to the user for signing. Wait for the signature.

### Step 4: Execute Gasless Cancel

Use `Bash(curl)`:

```bash
curl -s --connect-timeout 10 --max-time 30 \
  -X POST "https://limit-order.kyberswap.com/write/api/v1/orders/cancel" \
  -H "Content-Type: application/json" \
  -H "X-Client-Id: ai-agent-skills" \
  -d '{
    "chainId": "{chainId}",
    "maker": "{makerAddress}",
    "orderIds": [{orderIds}],
    "signature": "{userSignature}"
  }'
```

### Step 5: Format Output

```
## Limit Order Cancellation Submitted

| Detail | Value |
|---|---|
| Cancel type | Gasless |
| Order ID(s) | `{orderIds}` |
| Status | Cancellation submitted |
| ETA | Up to 90 seconds |

> **Note:** The cancellation has been submitted to the operator. It may take up to 90 seconds to take effect. During this window, the order could still be filled.
```

## Hard Cancel Workflow

**Hard cancellation is immediate but requires an on-chain transaction and costs gas.**

**IMPORTANT: Always confirm with the user before fetching hard-cancel calldata.**

Display the order details (from the query in the preceding step) and ask:
```
You have requested a hard cancel for order(s): {orderIds}
This requires an on-chain transaction and will cost gas.

Do you want to build hard-cancel calldata for these order(s)? (yes/no)
```
Wait for explicit confirmation. If the user says "no" or similar, abort and do not call the encode API.

### Option A: Cancel Specific Orders

Use `Bash(curl)`:

```bash
curl -s --connect-timeout 10 --max-time 30 \
  -X POST "https://limit-order.kyberswap.com/read-ks/api/v1/encode/cancel-batch-orders" \
  -H "Content-Type: application/json" \
  -H "X-Client-Id: ai-agent-skills" \
  -d '{
    "chainId": "{chainId}",
    "orderIds": [{orderIds}]
  }'
```

### Option B: Cancel All Orders (Increase Nonce)

Use `Bash(curl)`:

```bash
curl -s --connect-timeout 10 --max-time 30 \
  -X POST "https://limit-order.kyberswap.com/read-ks/api/v1/encode/increase-nonce" \
  -H "Content-Type: application/json" \
  -H "X-Client-Id: ai-agent-skills" \
  -d '{
    "chainId": "{chainId}",
    "maker": "{makerAddress}"
  }'
```

Both options return encoded calldata. Present it to the user:

```
## Hard Cancel — Transaction Required

| Detail | Value |
|---|---|
| Cancel type | Hard (on-chain) |
| Order ID(s) | `{orderIds}` (or "All active orders" for nonce increase) |

### Transaction Details

| Field | Value |
|---|---|
| To (DSLOProtocol) | `{contractAddress}` |
| Data | `{encodedCalldata}` |
| Value | `0` |
| Sender | `{maker}` |

> **WARNING:** Hard cancellation requires an on-chain transaction and costs gas. Review the transaction details carefully before submitting. This skill does NOT submit the transaction — it only builds the calldata.
```

### Structured JSON Output (Cancel)

````
```json
{
  "type": "kyberswap-limit-order",
  "operation": "cancel",
  "cancelType": "{gasless|hard}",
  "chain": "{chain}",
  "chainId": {chainId},
  "maker": "{maker}",
  "orderIds": ["{orderId}"],
  "status": "{submitted|calldata-ready}",
  "tx": {
    "to": "{contractAddress}",
    "data": "{encodedCalldata}",
    "value": "0"
  }
}
```
````

The `tx` field is only present for hard cancellations. For gasless cancellations, omit the `tx` field.

## Error Handling

### Common Error Scenarios

| Scenario | Cause | Quick Fix |
|---|---|---|
| Invalid chain ID | Chain not supported for limit orders | Check the 17 supported chains. megaeth is not supported. |
| Invalid token address | Token does not exist on the specified chain | Verify token address via token registry or Token API. |
| Invalid maker address | Address is zero address or malformed | Validate address format: `^0x[a-fA-F0-9]{40}$` |
| Signature mismatch | User signed wrong data or with wrong account | Ensure the user signs the exact EIP-712 message with the maker address. |
| Order not found | Order ID does not exist or belongs to a different maker | Verify the order ID and maker address. Query orders first. |
| Expired order | Cannot cancel an already expired order | The order has already expired. No action needed. |
| Already cancelled | Order was already cancelled | The order is already cancelled. No action needed. |
| Already filled | Order was already filled by a taker | The order has been filled. No action needed. |
| Insufficient allowance | Maker has not approved makerAsset to DSLOProtocol | Approve the contract to spend makerAsset before the order can be filled. |
| TakerAsset/MakerAsset invalid (4004) | Native token sentinel (`0xEeee...`) used as makerAsset or takerAsset | Limit orders require ERC-20 tokens. Use the wrapped version (e.g., WETH instead of ETH). See the alias table in Step 1. |
| Rate limit | Too many requests | Wait and retry. Space requests by at least 1 second. |

### HTTP Error Codes

| Code | Meaning | Action |
|---|---|---|
| 400 | Bad request | Check request body format, required fields, and data types. |
| 401 | Unauthorized | Verify the signature and maker address. |
| 404 | Not found | Check endpoint URL and chain ID. |
| 429 | Rate limited | Wait and retry with exponential backoff. |
| 500 | Internal server error | Retry after a brief delay. If persistent, the service may be down. |

For any error not listed here, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.

## Important Notes

- Always read `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md` before resolving token addresses.
- Never guess token addresses or maker addresses.
- If the user doesn't specify a chain, default to `ethereum`.
- If the user specifies a chain not in the 17 supported chains, inform them that limit orders are not supported on that chain.
- **Limit orders require ERC-20 tokens.** The native token sentinel (`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`) is rejected by the API (error 4004). Always resolve native token aliases (ETH, BNB, MATIC, etc.) to their wrapped ERC-20 equivalents (WETH, WBNB, WPOL, etc.).
- Slippage is **not** relevant for limit orders — users set exact target prices.
- Orders are gasless to create (signed off-chain). Gas is only needed for hard cancellation and token approval.
- **Signing an EIP-712 message authorizes the limit order contract to spend your tokens when a taker fills the order.** Always warn the user.
- **Gasless cancellation is not instant — it takes up to 90 seconds. During this window, the order may still be filled.** Always warn the user.
- **Hard cancellation requires an on-chain transaction and costs gas.** Always warn the user.
- The DSLOProtocol contract address is typically `0xcab2FA2eeab7065B45CBcF6E3936dDE2506b4f6C` on all chains, but always verify via the contract-address endpoint.
- Native token address: `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`

## Additional Resources

### Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/references/api-reference.md`** — Full API specification, error codes, rate limiting
- **`${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`** — Token addresses and decimals by chain

### Documentation

- **Create Limit Order:** https://docs.kyberswap.com/kyberswap-solutions/limit-order/developer-guides/create-limit-order
- **Gasless Cancel:** https://docs.kyberswap.com/kyberswap-solutions/limit-order/developer-guides/gasless-cancel
- **Hard Cancel:** https://docs.kyberswap.com/kyberswap-solutions/limit-order/developer-guides/hard-cancel
- **Fill Limit Order:** https://docs.kyberswap.com/kyberswap-solutions/limit-order/developer-guides/fill-limit-order

## Troubleshooting

**Order not being filled?**
- Verify the target price is realistic relative to current market price.
- Ensure the maker has sufficient makerAsset balance.
- Ensure the DSLOProtocol contract has been approved to spend makerAsset.
- Check that the order has not expired.

**Gasless cancel didn't work?**
- Gasless cancellation takes up to 90 seconds. Wait and re-query the order status.
- If the order was filled during the 90-second window, cancellation will fail. The order is already complete.
- Use hard cancel for immediate, guaranteed cancellation.

**Signature errors?**
- Ensure the user is signing with the exact wallet address specified as `maker`.
- Ensure the EIP-712 message is passed to the wallet exactly as returned by the sign-message endpoint.
- Some wallets may not support EIP-712 signing. Check wallet compatibility.

For error codes not covered above, or for advanced debugging, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.
