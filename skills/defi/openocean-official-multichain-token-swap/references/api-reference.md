# OpenOcean Aggregator API Reference

> Source: [OpenOcean API Docs — Swap API V4](https://apis.openocean.finance/developer/apis/swap-api/api-v4)

## Base URL

```
https://open-api.openocean.finance/v4
```

## Rate Limiting

- **Public Plan**: 2 RPS (20 requests / 10 seconds)
- Exceeding the limit may result in rate limiting or temporary blocking
- **Enterprise Plan**: For higher RPS or business collaboration, contact OpenOcean through the appropriate request channel

## Supported Chains

OpenOcean supports 40+ chains including both EVM and non-EVM networks (Solana, Sui, etc.).

### EVM Chains (Partial List)
| Chain | Path Slug | Chain ID |
|---|---|---|
| Ethereum | `1` or `ethereum` | `1` |
| BNB Smart Chain | `56` or `bsc` | `56` |
| Arbitrum | `42161` or `arbitrum` | `42161` |
| Polygon | `137` or `polygon` | `137` |
| Optimism | `10` or `optimism` | `10` |
| Base | `8453` or `base` | `8453` |
| Avalanche | `43114` or `avalanche` | `43114` |
| Linea | `59144` or `linea` | `59144` |
| Mantle | `5000` or `mantle` | `5000` |

**Note**: The `chain` parameter accepts either a chain ID (number) or a chain name (string). Use lowercase for names, such as `ethereum`, `arbitrum`, `polygon`, `base`, `bsc`, and `optimism`.

**Chain slug examples:** `1` or `ethereum`, `42161` or `arbitrum`, `137` or `polygon`, `8453` or `base`, `56` or `bsc`, `10` or `optimism`. Full list: [Supported Chains](https://apis.openocean.finance/developer/apis/supported-chains).

**Deprecated parameters (do not use):** OpenOcean is deprecating `amount` and `gasPrice`. Use **`amountDecimals`** (token amount in base units as integer string) and **`gasPriceDecimals`** (gas price in wei as integer string) for all requests.

---

## Endpoints

### GET `/:chain/quote`

Get the best swap quote for a token pair.

**Query Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chain` | string | Yes | Chain ID or chain name (e.g., `1`, `ethereum`, `56`, `bsc`) |
| `inTokenAddress` | string | Yes | Input token address. Use `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` for native token |
| `outTokenAddress` | string | Yes | Output token address. Same native token format as above |
| `amountDecimals` | string | Yes | Token amount expressed in base units as an integer string. For example, if the input is 1 USDT, use `1000000` (`1 * 10^6`) |
| `gasPriceDecimals` | string | Yes | Gas price in wei, expressed as an integer string |
| `slippage` | string | No | Acceptable slippage level (0.05 to 50). Default: `1` (1%) |
| `disabledDexIds` | string | No | Comma-separated DEX index numbers to disable |
| `enabledDexIds` | string | No | Comma-separated DEX index numbers to enable (higher priority than disabledDexIds) |

**Example Request**

```
GET https://open-api.openocean.finance/v4/1/quote?inTokenAddress=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE&outTokenAddress=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&amountDecimals=1000000000000000000&gasPriceDecimals=1000000000
```

**Response Schema**

```json
{
  "code": 200,
  "data": {
    "inToken": {
      "address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
      "decimals": 18,
      "symbol": "ETH",
      "name": "Ethereum",
      "usd": "2345.67",
      "volume": 2345.67
    },
    "outToken": {
      "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "decimals": 6,
      "symbol": "USDC",
      "name": "USD Coin",
      "usd": "1.00",
      "volume": 2345.67
    },
    "inAmount": "1000000000000000000",
    "outAmount": "2345670000",
    "estimatedGas": "129211",
    "dexes": [
      {
        "dexIndex": 0,
        "dexCode": "UniswapV3",
        "swapAmount": "1000000000000000000"
      }
    ],
    "path": {
      "from": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
      "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "parts": 10,
      "routes": [...]
    },
    "save": -0.0018,
    "price_impact": "0.01%",
    "exchange": "0x6352a56caadC4F1E25CD6c75970Fa768A3304e64"
  }
}
```

**Key response fields:**
- `data.inToken` / `data.outToken` — Token information including decimals, symbol, USD price
- `data.inAmount` — Input amount in wei
- `data.outAmount` — Output amount in wei
- `data.estimatedGas` — Estimated gas units
- `data.dexes` — Array of DEXes used in the route
- `data.path` — Detailed route path
- `data.save` — Savings compared to market price (negative means worse)
- `data.price_impact` — Price impact percentage
- `data.exchange` — OpenOcean router contract address

**Important (price_impact):** The `price_impact` field indicates estimated price deviation relative to market. OpenOcean does not enforce execution blocks based on price impact; it is the **integrator's responsibility** to evaluate this value and implement checks (e.g. abort if above a threshold) before submitting transactions. See [API v4](https://apis.openocean.finance/developer/apis/swap-api/api-v4).

---

### GET `/:chain/reverseQuote` (Optional)

Reverse quote: user wants to **receive** a fixed amount of the "in" token; the API returns how much of the "out" token is needed to sell.

- In the request, **inToken** = token the user wants to receive, **outToken** = token the user will pay; **amount** = target amount of inToken to receive (with decimals).
- Same query parameters as `/quote` (chain, inTokenAddress, outTokenAddress, amountDecimals, gasPriceDecimals, slippage, etc.).
- Response includes `reverseAmount` (required outToken amount). See [API v4 ReverseQuote](https://apis.openocean.finance/developer/apis/swap-api/api-v4).

---

### GET `/:chain/swap`

Get swap quote with transaction calldata.

**Query Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chain` | string | Yes | Chain ID or chain name |
| `inTokenAddress` | string | Yes | Input token address |
| `outTokenAddress` | string | Yes | Output token address |
| `amountDecimals` | string | Yes | Token amount expressed in base units as an integer string |
| `gasPriceDecimals` | string | Yes | Gas price in wei, expressed as an integer string |
| `slippage` | string | No | Slippage percentage (0.05 to 50). Default: `1` |
| `account` | string | Yes* | User's wallet address. Required for calldata generation |
| `referrer` | string | No | Referrer wallet address for fee sharing |
| `referrerFee` | number | No | Referrer fee percentage (0.01 to 5) |
| `enabledDexIds` | string | No | Comma-separated DEX index numbers to enable |
| `disabledDexIds` | string | No | Comma-separated DEX index numbers to disable |
| `sender` | string | No | Caller address (if different from account); when set, sender = caller and account = receiver |
| `minOutput` | string | No | Minimum output amount in base units (integer string, e.g. 9.9 USDC with 6 decimals = `9900000`). **Supported chains:** Base, BNB, ETH only |

*Note: If `account` is not provided, the response returns quote data only and does not include calldata.

**Example Request**

```
GET https://open-api.openocean.finance/v4/1/swap?inTokenAddress=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE&outTokenAddress=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&amountDecimals=1000000000000000000&gasPriceDecimals=1000000000&slippage=1&account=0xYourAddress
```

**Response Schema**

```json
{
  "code": 200,
  "data": {
    "inToken": {...},
    "outToken": {...},
    "inAmount": "1000000000000000000",
    "outAmount": "2345670000",
    "estimatedGas": 516812,
    "minOutAmount": "2322213300",
    "from": "0xYourAddress",
    "to": "0x6352a56caadC4F1E25CD6c75970Fa768A3304e64",
    "value": "1000000000000000000",
    "gasPrice": "1000000000",
    "data": "0x90411a32...",
    "chainId": 1,
    "price_impact": "0.01%"
  }
}
```

**Key response fields for transaction building:**
- `data.data` — Encoded calldata for transaction
- `data.to` — Router contract address (send transaction to this address)
- `data.value` — Transaction value in wei (non-zero for native token input)
- `data.from` — Sender address
- `data.gasPrice` — Gas price in **wei** (use this value when sending the transaction so it matches the quote)
- `data.estimatedGas` — Estimated gas limit (reference only; OpenOcean recommends recalculating or using e.g. `eth_estimateGas * 1.25`–2.5 for safety)
- `data.minOutAmount` — Minimum output amount after slippage
- `data.chainId` — Chain ID for transaction

**price_impact:** Returned in the response; same integrator responsibility as for `/quote` (evaluate and enforce thresholds before submitting).

---

### GET `/:chain/tokenList`

Get list of tokens for a specific chain.

**Query Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chain` | string | Yes | Chain ID or chain name |

**Example Request**

```
GET https://open-api.openocean.finance/v4/1/tokenList
```

**Response Schema**

```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "code": "eth",
      "name": "Ethereum",
      "address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
      "decimals": 18,
      "symbol": "ETH",
      "icon": "https://...",
      "chain": "ethereum",
      "usd": "2345.67"
    },
    ...
  ]
}
```

---

### GET `/:chain/dexList`

Get list of supported DEXes for a specific chain.

**Query Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chain` | string | Yes | Chain ID or chain name |

**Example Request**

```
GET https://open-api.openocean.finance/v4/1/dexList
```

**Response Schema**

```json
{
  "code": 200,
  "data": [
    {
      "index": 1,
      "code": "UniswapV3",
      "name": "Uniswap V3"
    },
    ...
  ]
}
```

---

### GET `/:chain/gasPrice`

Get current gas price for a chain.

**Query Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chain` | string | Yes | Chain ID or chain name |

**Example Request**

```
GET https://open-api.openocean.finance/v4/1/gasPrice
```

**Response Schema (Ethereum)**

`data` contains gas values **in wei** (integer). Use `data.standard.legacyGasPrice` or `data.base` for legacy transactions.

```json
{
  "code": 200,
  "data": {
    "base": 605865956,
    "standard": {
      "legacyGasPrice": 605865956,
      "maxPriorityFeePerGas": 500000000,
      "maxFeePerGas": 1366388318,
      "waitTimeEstimate": 45000
    },
    "fast": {...},
    "instant": {...},
    "low": {...}
  },
  "without_decimals": {
    "base": 0.605865956,
    "standard": {
      "legacyGasPrice": 0.605865956,
      ...
    },
    ...
  }
}
```

**Response (other EVM chains)**

Some chains return a flat structure; values are **in wei**:

```json
{
  "code": 200,
  "data": {
    "standard": 1000000000,
    "fast": 1000000000,
    "instant": 1000000000
  }
}
```

**Important:** Always use the **wei** values from `data` (not `without_decimals`) when passing `gasPriceDecimals` to `/quote` or `/swap`. For Ethereum use `.data.standard.legacyGasPrice` or `.data.base`; for other EVM use `.data.standard` if `.standard.legacyGasPrice` is absent.

---

## Error Handling

Common error codes:

| Code | Meaning | Action |
|---|---|---|
| 200 | Success | Continue with response data |
| 400 | Bad Request | Check parameter formats and values |
| 429 | Rate Limited | Wait and retry later |
| 500 | Internal Server Error | Retry or contact support |

For detailed error handling, refer to `skills/error-handling/SKILL.md`.

---

## Wei Conversion Reference

Tokens use different decimal places. To convert a human-readable amount to wei:

```
wei = amount * 10^decimals
```

| Decimals | Multiply by | Common tokens |
|---|---|---|
| 18 | 1000000000000000000 | ETH, WETH, most ERC-20s |
| 8 | 100000000 | WBTC (Ethereum), renBTC |
| 6 | 1000000 | USDC, USDT |

**Examples:**
- 1 ETH (18 decimals) = `1000000000000000000`
- 1 USDC (6 decimals) = `1000000`
- 0.5 WBTC (8 decimals) = `50000000`
- 100 USDC (6 decimals) = `100000000`

**Important:** The `amountDecimals` parameter must be a plain decimal string. Never use scientific notation.

---

## Native Token Address

For native tokens (ETH, BNB, MATIC, etc.), use the special address:
```
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
```

## Slippage Calculation

**API parameter:** `slippage` is a **percentage** (0.05 to 50). Example: `1` = 1%, `0.5` = 0.5%.  
If your UI uses basis points (bps), convert: `slippage_api = bps / 100` (e.g. 100 bps → 1, 50 bps → 0.5).

When `slippage` = 1%:
```
minOutAmount = outAmount * (1 - slippage/100)
```

Example: If `outAmount` = 1000000 and `slippage` = 1:
```
minOutAmount = 1000000 * (1 - 1/100) = 990000
```

## Gas Price Units

Gas price must be provided **in wei** for `gasPriceDecimals` (`1 Gwei = 1,000,000,000 wei`).

Example: 10 Gwei = `10000000000`

**Critical for display:** If you show gas price in Gwei or compute gas fee in ETH, use:
- **Gas price in Gwei** = `gasPriceWei / 10^9` (do not use the raw wei value as Gwei).
- **Gas fee in wei** = `gasLimit × gasPriceWei`
- **Gas fee in ETH** = `gasFeeWei / 10^18`

---

## Troubleshooting / Fallback

If this reference is outdated or endpoints return unexpected errors, consult the official OpenOcean API documentation:

**Official API documentation:** https://apis.openocean.finance/developer/apis/swap-api/api-v4

The official docs are the single source of truth for endpoint specs, error codes, supported chains, and parameter definitions.

**Other API v4 endpoints** (not used by the current skills; see official docs for params and responses): `GET /:chain/getTransaction`, `GET /:chain/decodeInputData` (and POST variant).