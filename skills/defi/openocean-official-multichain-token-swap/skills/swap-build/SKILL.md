---
name: swap-build
description: This skill should be used when the user asks to "build a swap", "prepare swap transaction", "get swap calldata", or wants to create a transaction for a token trade. Builds full swap transaction with calldata from OpenOcean Aggregator.
metadata:
  tags:
    - defi
    - openocean
    - swap
    - transaction
    - evm
    - aggregator
  provider: OpenOcean
  homepage: https://openocean.finance
---

# OpenOcean Swap Build Skill

Build a complete swap transaction with calldata using the OpenOcean aggregator. Given a token pair, amount, and sender address, fetch the best route and prepare the data required for on-chain execution.

## Read Before Execution (Agent Checklist)

1. **Paths**: Resolve reference files with glob first (do not read fixed paths first).
   - Run: `**/token-registry.md` and `**/api-reference.md`.
   - Use the unique matched path and continue.
   - Report error only when no unique match exists.
2. **API**: Use **mcp_web_fetch** to call the `gasPrice` and `swap` endpoints. The `swap` request must include `account={sender}` in order to receive calldata.
3. **Slippage**: A user may say `slippage 100` to mean 1% (100 bps). The API expects a **percentage** value, where `1 = 1%`. Convert with `slippage_api = slippage_bps / 100`.
4. **Amount**: `amountDecimals` must be an integer string with no scientific notation.
5. **Chain Normalization**: Normalize user chain names to OpenOcean-supported `Chain Code` before calling APIs (for example `ethereum` -> `eth`), or keep numeric chain ID as-is.

## Input Parsing

The user will provide input like:
- `100 USDC to ETH on arbitrum from 0xYourAddress`
- `1 ETH to USDC on ethereum from 0xYourAddress slippage 100`
- `0.5 WBTC to DAI on polygon from 0xYourAddress`

Extract these fields:
- **amount** — the human-readable amount to swap
- **tokenIn** — the input token symbol
- **tokenOut** — the output token symbol
- **chain** — the chain slug or ID
- **sender** — the sender wallet address (after "from")
- **slippage** — optional, in **basis points** (default: 100 = 1%). Convert it to a percentage before sending it to the API: `slippage_api = slippage_bps / 100`.

## Workflow

### Step 1: Resolve Token Addresses

Read the token registry at `references/token-registry.md`.

Look up `tokenIn` and `tokenOut` for the specified chain. Match case-insensitively. Note the **decimals** for each token.

**Native Token Address:**
For native tokens (ETH, BNB, MATIC, etc.), use:
```
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
```

**If a token is not found in the registry:**
Follow the fallback sequence in `references/token-registry.md`.

### Step 2: Get Current Gas Price

Fetch current gas price:
```
GET https://open-api.openocean.finance/v4/:chain/gasPrice
```

Use the `standard` gas price from the response. **Values in `data` are already in wei** (use `data.standard.legacyGasPrice` or `data.standard` on non-Ethereum chains); pass them directly as `gasPriceDecimals` to swap.

### Step 3: Convert Amount to Wei

```
amountInWei = amount * 10^(tokenIn decimals)
```

Use deterministic conversion:
```bash
python3 -c "print(int(AMOUNT * 10**DECIMALS))"
```

### Step 4: Call the Swap API (GET request)

Use **mcp_web_fetch** with this URL format:

```
https://open-api.openocean.finance/v4/{chain}/swap?inTokenAddress={tokenInAddress}&outTokenAddress={tokenOutAddress}&amountDecimals={amountInWei}&gasPriceDecimals={gasPriceWei}&slippage={slippage_api}&account={sender}
```

- `slippage_api`: percentage value from 0.05 to 50, where `1 = 1%`. If the user says `slippage 100`, pass `1`; if they say `slippage 50`, pass `0.5`.
- `account`: the user's wallet address. This field is required in order to receive calldata.

### Step 5: Verify Response

Check `code` = 200 and ensure `data.data` field exists (contains calldata).

If `code` is not `200`, handle the error according to the error-handling skill.

### Step 6: Present Quote Details for Confirmation

Before returning calldata, show the user:

```
## OpenOcean Swap Build - Review Before Proceeding

**{amount} {tokenIn} → {minOutAmount} {tokenOut}** on {Chain}

| Detail | Value |
|---|---|
| Input | {amount} {tokenIn} (~${amountInUsd}) |
| Expected Output | {outAmount} {tokenOut} (~${amountOutUsd}) |
| Minimum Output | {minOutAmount} {tokenOut} (after {slippage}% slippage) |
| Gas estimate | {estimatedGas} units |
| Gas price | {gasPrice} wei (display in Gwei as gasPrice ÷ 10^9) |
| Price impact | {price_impact} |
| Router | `{to}` |

### Transaction Details
- **To**: `{to}` (OpenOcean router)
- **Value**: {value} wei (0 for ERC-20, >0 for native token)
- **Chain ID**: {chainId}
- **From**: `{from}`

⚠️ **Important:**
1. This builds the transaction but does NOT execute it
2. Minimum output is protected by contract
3. Gas costs are estimates only
4. Prices may change before execution

Do you want to proceed with building this swap? (Yes/No)
```

### Step 7: If User Confirms, Return Calldata

If user confirms "Yes", return the complete transaction data:

```
## OpenOcean Swap Transaction Built

Transaction data ready for signing and broadcasting.

### Raw Transaction
```json
{
  "from": "{from}",
  "to": "{to}",
  "value": "{value}",
  "data": "{data}",
  "gas": "{estimatedGas}",
  "gasPrice": "{gasPrice}",
  "chainId": {chainId}
}
```

### Calldata (for manual construction)
```
Data: {data}
```

### Next Steps
1. Sign this transaction with your wallet
2. Broadcast to the network
3. Or use `/swap-execute` to execute directly (requires Foundry)

**Transaction hash will be available after broadcasting.**
```

### Step 8: If User Declines, Cancel

If user says "No" or cancels:
```
## Swap Build Cancelled

No transaction data was generated. You can:
- Adjust parameters and try again
- Use `/quote` to check prices first
- Contact support if you have questions
```

## Important Notes

### Safety Checks
1. **Slippage Protection**: Minimum output is enforced by contract
2. **Gas Estimates**: Are estimates only, actual may vary
3. **Price Validity**: Quotes expire quickly, execute promptly
4. **Token Approvals**: ERC-20 tokens require approval before swapping

### Parameter Guidelines
- **Slippage:**
  - 0.1% (10 bps) for stablecoin ↔ stablecoin
  - 0.5% (50 bps) for common pairs
  - 1-2% (100-200 bps) for volatile tokens
- **Gas Price**: Use current market rates from gasPrice endpoint. For the built transaction, use **data.gasPrice from the swap response** (wei) so the tx matches the quote. When displaying, gas price in Gwei = gasPrice ÷ 10^9 (never use the wei value as Gwei).
- **Deadline**: OpenOcean uses default 20-minute deadline

### Native vs ERC-20
- **Native token input**: `value` > 0, no approval needed
- **ERC-20 input**: `value` = 0, approval required before swap
- **Always check**: Token approvals before attempting swap

## Error Handling

Common issues:

1. **Insufficient Balance**: Check user has enough tokenIn + gas
2. **Insufficient Allowance**: ERC-20 needs approval first
3. **Rate Limited**: Wait and retry
4. **No Route**: Token pair may have no liquidity

For detailed error codes, see `skills/error-handling/SKILL.md`.

## Example Usage

```
/swap-build 1 ETH to USDC on ethereum from 0x742d35Cc6634C0532925a3b844Bc9e90F1b6fB28 slippage 50
```

This will:
1. Get ETH → USDC quote on Ethereum
2. Show details for confirmation
3. If confirmed, return transaction calldata
4. User can then sign and broadcast

## Next Steps After Build

After getting calldata, user can:
1. **Manual Execution**: Sign and broadcast using their wallet
2. **`/swap-execute`**: Use Foundry cast to execute (requires setup)
3. **`/swap-execute-fast`**: Build and execute in one step (dangerous)

**Remember**: Built transactions are not submitted until they are broadcast on-chain.
