---
name: quote
description: This skill should be used when the user asks to "get a swap quote", "check swap price", "compare token rates", "see exchange rates", "how much would I get for", "price check", or wants to know the expected output for a token trade. Fetches the best route from OpenOcean Aggregator across 40+ chains.
metadata:
  tags:
    - defi
    - openocean
    - swap
    - quote
    - evm
    - aggregator
  provider: OpenOcean
  homepage: https://openocean.finance
---

# OpenOcean Quote Skill

Fetch a swap quote from the OpenOcean aggregator. Given a token pair and amount, return the best route along with the expected output, exchange rate, and gas cost.

## Read Before Execution (Agent Checklist)

1. **Paths**: All referenced files in this project are relative to the **workspace root**.
   - Always run glob first (do not read fixed paths first): `**/token-registry.md` and `**/api-reference.md`.
   - Read the unique matched path directly.
   - Only fail when no unique match can be found.
2. **API Requests**: Use **mcp_web_fetch** (or an equivalent GET request tool) to call OpenOcean. Never fabricate response data.
3. **Amount**: `amountDecimals` must be an **integer string** with no decimal point and no scientific notation.
4. **Chain**: The `chain` field accepts either a chain code or chain ID. Always normalize user input to OpenOcean-supported `Chain Code` (or keep numeric chain ID). Example: `ethereum` -> `eth`.

## Input Parsing

The user will provide input like:
- `1 ETH to USDC on ethereum`
- `100 USDC to WBTC on arbitrum`
- `0.5 WBTC to DAI on polygon`
- `1000 USDT to ETH` (default chain: ethereum)

Extract these fields:
- **amount** — the human-readable amount to swap
- **tokenIn** — the input token symbol
- **tokenOut** — the output token symbol
- **chain** — the chain slug or ID (default: `ethereum`)

## Workflow

### Step 1: Resolve Token Addresses

Read the token registry at `references/token-registry.md`.

Look up `tokenIn` and `tokenOut` for the specified chain. Match case-insensitively. Note the **decimals** for each token.

**Native Token Address:**
For native tokens (ETH, BNB, MATIC, etc.), use:
```
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
```

**Aliases to handle:**
- "ETH" on Ethereum/Arbitrum/Optimism/Base → native token address
- "MATIC" on Polygon → native token address
- "BNB" on BSC → native token address
- "AVAX" on Avalanche → native token address

**If a token is not found in the registry:**
Use the fallback sequence described at the bottom of `references/token-registry.md`:
1. **OpenOcean Token API** — request `https://open-api.openocean.finance/v4/{chain}/tokenList` (for example with `mcp_web_fetch`), then match by symbol within the returned JSON `data` array.
2. **Chain Explorer APIs** — secondary fallback for verified tokens
3. **Ask user manually** (final fallback) — if automated lookup fails, ask the user to provide the contract address. Never guess or fabricate addresses.

### Step 2: Get Current Gas Price

Before getting a quote, fetch current gas price:
```
GET https://open-api.openocean.finance/v4/:chain/gasPrice
```

Use the `standard` gas price from the response. **Values in `data` are already in wei** (use `data.standard.legacyGasPrice` or `data.standard` on non-Ethereum chains); pass them directly as `gasPriceDecimals` to quote/swap.

### Step 3: Convert Amount to Wei

```
amountInWei = amount * 10^(tokenIn decimals)
```

The result must be a plain integer string with no decimals, no scientific notation, and no separators.

**For wei conversion, use a deterministic method:**
```bash
python3 -c "print(int(AMOUNT * 10**DECIMALS))"
# or
echo "AMOUNT * 10^DECIMALS" | bc
```

**Verify known reference values:**
- 1 ETH (18 decimals) = `1000000000000000000`
- 1 USDC (6 decimals) = `1000000`
- 0.5 WBTC (8 decimals) = `50000000`

### Step 4: Call the Quote API (GET request)

Read the API reference at `references/api-reference.md` for the full specification.

Use **mcp_web_fetch** with this URL format:

```
https://open-api.openocean.finance/v4/{chain}/quote?inTokenAddress={tokenInAddress}&outTokenAddress={tokenOutAddress}&amountDecimals={amountInWei}&gasPriceDecimals={gasPriceWei}
```
Optional: `&slippage=1` means 1%. `amountDecimals` must not use scientific notation.

### Step 5: Handle Errors

Check the `code` field in the JSON response:

| Code | Meaning | Action |
|---|---|---|
| 200 | Success | Continue with response |
| 400 | Bad Request | Check parameter formats |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Retry or contact support |

For detailed error handling, refer to **`skills/error-handling/SKILL.md`**.

### Step 6: Format the Output

Present the results in this format:

```
## OpenOcean Quote

**{amount} {tokenIn} → {amountOut} {tokenOut}** on {Chain}

| Detail | Value |
|---|---|
| Input | {amount} {tokenIn} (~${amountInUsd}) |
| Output | {amountOut} {tokenOut} (~${amountOutUsd}) |
| Rate | 1 {tokenIn} = {rate} {tokenOut} |
| Gas estimate | {estimatedGas} units |
| Price impact | {price_impact} |
| Savings | {save}% |

### Route
{For each dex in data.dexes, show: dexCode: {swapAmount} {tokenOut}}
```

**Calculating the output amount:**
Convert `outAmount` from wei back to human-readable using tokenOut's decimals:
```
humanAmountOut = outAmount / 10^(tokenOut decimals)
```

**Calculating the rate:**
```
rate = humanAmountOut / amount
```

Display rates with appropriate precision (up to 6 significant digits).

### Structured JSON Output

After the markdown table, include a JSON code block for programmatic consumption:

````
```json
{
  "type": "openocean-quote",
  "chain": "{chain}",
  "tokenIn": {
    "symbol": "{tokenIn}",
    "address": "{tokenInAddress}",
    "decimals": {tokenInDecimals},
    "amount": "{amount}",
    "amountWei": "{amountInWei}",
    "amountUsd": "{amountInUsd}"
  },
  "tokenOut": {
    "symbol": "{tokenOut}",
    "address": "{tokenOutAddress}",
    "decimals": {tokenOutDecimals},
    "amount": "{amountOut}",
    "amountWei": "{outAmount}",
    "amountUsd": "{amountOutUsd}"
  },
  "rate": "{rate}",
  "estimatedGas": "{estimatedGas}",
  "priceImpact": "{price_impact}",
  "savings": "{save}",
  "routerAddress": "{exchange}"
}
```
````

## Important Notes

- Always read both `references/token-registry.md` and `references/api-reference.md` before making API calls.
- Never guess token addresses. Always verify from the registry or via the Token API.
- If the user doesn't specify a chain, default to `ethereum`.
- The quote is informational only — no transaction is built or submitted.
- OpenOcean supports 40+ chains including Solana and Sui (non-EVM).

## Additional Resources

### Reference Files

- **`references/api-reference.md`** — Full API specification
- **`references/token-registry.md`** — Token addresses and decimals

### Example Files

- **`skills/quote/references/basic-quote.md`** — Simple ETH to USDC quote on Ethereum

## Troubleshooting

For error codes not covered above, or for advanced debugging, refer to **`skills/error-handling/SKILL.md`**.
