---
name: token-info
description: This skill should be used when the user asks to "check token price", "get token info", "token details", "what is the price of", "current price of", "look up token", "token lookup", "market cap of", "is this token safe", or wants to know the current price, market cap, safety status, or contract address of a token before placing a limit order, swapping, or zapping into a pool. Fetches token metadata and live USD price from KyberSwap APIs across 18 EVM chains.
metadata:
  tags:
    - defi
    - kyberswap
    - token
    - price
    - evm
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Token Info Skill

Fetch token metadata (address, decimals, safety, market cap) and live USD price for any token on supported chains. Useful as reference before limit orders or zap operations.

## Input Parsing

The user will provide input like:
- `price of ETH on ethereum`
- `token info WBTC on arbitrum`
- `is USDe safe on ethereum`
- `check price of LINK, UNI, AAVE on ethereum` (multi-token)
- `what is the price of SOL` (default chain: ethereum)

Extract these fields:
- **token(s)** — one or more token symbols
- **chain** — the chain slug (default: `ethereum`)

## Workflow

### Step 1: Resolve Token Address

Read the token registry at `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`.

Look up each token symbol for the specified chain. Match case-insensitively. Note the **decimals** for each token.

**Aliases to handle:**
- "ETH" on Ethereum/Arbitrum/Optimism/Base/Linea/Unichain -> native token address
- "MATIC" or "POL" on Polygon -> native token address
- "BNB" on BSC -> native token address
- "AVAX" on Avalanche -> native token address
- "MNT" on Mantle -> native token address
- "S" on Sonic -> native token address
- "BERA" on Berachain -> native token address
- "RON" on Ronin -> native token address
- "XTZ" on Etherlink -> native token address
- "MON" on Monad -> native token address

**If a token is not found in the registry:**
Use the KyberSwap Token API fallback:

```
GET https://token-api.kyberswap.com/api/v1/public/tokens?chainIds={chainId}&name={symbol}&isWhitelisted=true
Header: X-Client-Id: ai-agent-skills
```

Via **WebFetch**. Pick the result whose `symbol` matches exactly with the highest `marketCap`. If no whitelisted match, retry without `isWhitelisted` (only trust verified or market-cap tokens). If still nothing, browse `page=1&pageSize=100` (try up to 3 pages).

If the Token API also returns no results, ask the user to provide the contract address. Never guess or fabricate addresses.

### Step 2: Get Token Metadata

If the token was resolved from the registry, fetch additional metadata from the Token API:

```
GET https://token-api.kyberswap.com/api/v1/public/tokens?chainIds={chainId}&name={symbol}
Header: X-Client-Id: ai-agent-skills
```

Via **WebFetch**. Extract these fields from the matching result:
- `address` — the token contract address
- `symbol` — the token ticker
- `name` — the full token name
- `decimals` — the number of decimal places
- `marketCap` — the token market cap in USD
- `cmcRank` — the CoinMarketCap rank
- `isVerified` — whether the token is verified
- `isWhitelisted` — whether the token is whitelisted on KyberSwap
- `isStable` — whether the token is a stablecoin
- `isFOT` — whether the token has fee-on-transfer
- `isHoneypot` — whether the token is flagged as a honeypot
- `logoURL` — the token logo URL

If metadata was already fetched during the Token API fallback in Step 1, reuse it and skip this step.

### Step 3: Check Token Safety

For any token **not** in the built-in registry and **not** a native token, check the honeypot/FOT API:

```
GET https://token-api.kyberswap.com/api/v1/public/tokens/honeypot-fot-info?chainId={chainId}&address={tokenAddress}
Header: X-Client-Id: ai-agent-skills
```

Via **WebFetch**, check each token:
- If `isHoneypot: true` — **warn the user prominently** that this token is flagged as a honeypot (cannot be sold after buying). Display the warning with a caution indicator.
- If `isFOT: true` — warn the user that this token has a fee-on-transfer (tax: `{tax}%`). Any swap or transfer will lose a percentage to the tax.

### Step 4: Get Live USD Price

Use the KyberSwap Aggregator routes endpoint to get the live price by quoting 1 unit of the token against USDC:

```
GET https://aggregator-api.kyberswap.com/{chain}/api/v1/routes?tokenIn={tokenAddress}&tokenOut={usdcAddress}&amountIn={oneUnitInWei}&source=ai-agent-skills
```

Via **WebFetch**.

**Key details:**
- For native tokens, use the native token sentinel `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` as `tokenIn`.
- For `usdcAddress`, use the USDC address from the token registry for the given chain.
- For `oneUnitInWei`, convert 1 unit of the token to wei using its decimals:
  ```
  oneUnitInWei = 1 * 10^(token decimals)
  ```
  Example: 1 ETH (18 decimals) = `1000000000000000000`, 1 WBTC (8 decimals) = `100000000`
- Convert the `amountOut` from wei (6 decimals for USDC) to get the USD price:
  ```
  priceUsd = amountOut / 10^6
  ```

**Fallback:** If the route fails (e.g., no USDC liquidity on that chain), try USDT as the quote token instead. Use the USDT address from the token registry for the given chain.

If both USDC and USDT routes fail, report "Price unavailable" but still show all available metadata from Steps 2 and 3.

### Step 5: Format the Output

**Single token — detailed table:**

```
## Token Info — {symbol} on {Chain}

| Detail | Value |
|---|---|
| Name | {name} |
| Symbol | {symbol} |
| Address | `{address}` |
| Decimals | {decimals} |
| Price (USD) | ${price} |
| Market Cap | ${marketCap} |
| CMC Rank | #{cmcRank} |
| Verified | {isVerified} |
| Whitelisted | {isWhitelisted} |
| Stablecoin | {isStable} |
| Honeypot | {isHoneypot} (if true, add warning) |
| Fee-on-Transfer | {isFOT} (tax: {tax}%) |
```

**Multi-token — summary comparison table:**

```
## Token Prices on {Chain}

| Token | Price (USD) | Market Cap | Verified | Safe |
|---|---|---|---|---|
| {symbol1} | ${price1} | ${marketCap1} | Yes/No | Yes/Warning |
| {symbol2} | ${price2} | ${marketCap2} | Yes/No | Yes/Warning |
```

For multi-token queries, also include the individual detailed tables for each token below the summary.

### Structured JSON Output

After the markdown table, always include a JSON code block so other plugins or agents can consume the result programmatically:

````
```json
{
  "type": "kyberswap-token-info",
  "chain": "{chain}",
  "tokens": [
    {
      "symbol": "{symbol}",
      "name": "{name}",
      "address": "{address}",
      "decimals": {decimals},
      "priceUsd": "{price}",
      "marketCap": {marketCap},
      "cmcRank": {cmcRank},
      "isVerified": {isVerified},
      "isWhitelisted": {isWhitelisted},
      "isStable": {isStable},
      "isHoneypot": {isHoneypot},
      "isFOT": {isFOT},
      "tax": {tax}
    }
  ]
}
```
````

This JSON block enables downstream agents or plugins to parse the token info result without scraping the markdown table.

## Important Notes

- Always read both `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md` and `${CLAUDE_PLUGIN_ROOT}/references/api-reference.md` before making API calls.
- Never guess token addresses. Always verify from the registry or via the Token API.
- If the user doesn't specify a chain, default to `ethereum`.
- Price is derived from live Aggregator quotes, not cached. Prices may vary slightly from exchange prices.
- This skill is read-only — no transactions are built or submitted.
- Use this skill to provide context before limit orders (compare target price vs current price) or zap operations (understand token values).

## Additional Resources

### Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/references/api-reference.md`** — Full API specification, error codes, rate limiting
- **`${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`** — Token addresses and decimals by chain

## Troubleshooting

**Token not found in registry or API?**
- Verify the symbol spelling. Try alternative names (e.g., "WETH" instead of "ETH" for the ERC-20 version).
- The token may not be listed on KyberSwap. Ask the user for the contract address.

**Price unavailable?**
- The token may not have a USDC or USDT liquidity pool on the specified chain.
- Try a different chain if the token is multi-chain.
- For very new or low-liquidity tokens, price quotes may not be available.

**Safety check returns unexpected results?**
- The honeypot/FOT API may not have data for very new tokens. Absence of data does not guarantee safety.
- For high-value operations, always verify token contracts independently.

For error codes not covered above, or for advanced debugging, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.
