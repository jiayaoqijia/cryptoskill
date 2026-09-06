# API Endpoints

Complete reference for GMX V2 REST and GraphQL APIs.

## Oracle REST API

Base URL pattern: `https://{network}-api.gmxinfra.io`

| Chain | Primary URL |
|-------|------------|
| Arbitrum | `https://arbitrum-api.gmxinfra.io` |
| Avalanche | `https://avalanche-api.gmxinfra.io` |
| Botanix | `https://botanix-api.gmxinfra.io` |

### Endpoints

#### GET /prices/tickers

Returns current min/max prices for all tokens on the chain.

```json
[
  {
    "tokenSymbol": "ETH",
    "tokenAddress": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    "minPrice": "3456789000000000000000000000000000",
    "maxPrice": "3456891000000000000000000000000000",
    "oracleDecimals": 8,
    "updatedAt": 1709500000
  }
]
```

#### GET /prices/candles

OHLC price candles for a token.

**Query params:**
- `tokenSymbol` (required) — e.g., `ETH`, `BTC`, `ARB`
- `period` (required) — `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
- `limit` (optional) — number of candles, default 100

#### GET /signed_prices/latest

Signed oracle prices for order execution. Used internally by keepers.

#### GET /tokens

Token list with metadata. Response is wrapped in a `tokens` key.

```json
{
  "tokens": [
    {
      "symbol": "ETH",
      "address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
      "decimals": 18,
      "isSynthetic": false
    }
  ]
}
```

#### GET /markets

Market configuration listing index, long, and short tokens. Response is wrapped in a `markets` key.

```json
{
  "markets": [
    {
      "name": "ETH/USD [WETH-USDC]",
      "marketToken": "0x70d95587d40A2cdd56BBE18AB51Bbd657434570c",
      "indexToken": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
      "longToken": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
      "shortToken": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
    }
  ]
}
```

#### GET /markets/info

Extended market data including pool sizes, utilization, open interest, and fee factors.

---

## GraphQL (Subsquid)

Base URL pattern: `https://gmx.squids.live/gmx-synthetics-{network}:prod/api/graphql`

| Chain | URL |
|-------|-----|
| Arbitrum | `https://gmx.squids.live/gmx-synthetics-arbitrum:prod/api/graphql` |
| Avalanche | `https://gmx.squids.live/gmx-synthetics-avalanche:prod/api/graphql` |
| Botanix | `https://gmx.squids.live/gmx-synthetics-botanix:prod/api/graphql` |

### Example: Fetch Trade Actions

```graphql
query RecentTrades($account: String!) {
  tradeActions(
    where: { account_eq: $account }
    orderBy: timestamp_DESC
    limit: 20
  ) {
    id
    eventName
    orderType
    orderKey
    marketAddress
    sizeDeltaUsd
    collateralDeltaAmount
    triggerPrice
    acceptablePrice
    executionPrice
    isLong
    timestamp
    transactionHash
  }
}
```

### Example: Fetch Position Increase Events

```graphql
query PositionIncreases($account: String!) {
  tradeActions(
    where: {
      account_eq: $account
      eventName_eq: "OrderExecuted"
      orderType_in: [2, 3, 8]
    }
    orderBy: timestamp_DESC
    limit: 50
  ) {
    id
    orderType
    marketAddress
    sizeDeltaUsd
    executionPrice
    isLong
    timestamp
    transactionHash
  }
}
```

### Pagination

The Subsquid indexer uses cursor-based pagination with a maximum of 500 items per request (`SUBSQUID_PAGINATION_LIMIT`).

```graphql
query PaginatedTrades($cursor: String) {
  tradeActionsConnection(
    orderBy: timestamp_DESC
    first: 500
    after: $cursor
  ) {
    edges {
      node { id, eventName, orderType, timestamp, transactionHash }
      cursor
    }
    pageInfo { hasNextPage, endCursor }
  }
}
```

---

## Fallback URLs

Each chain has primary and fallback oracle endpoints for redundancy.

### Arbitrum

| Priority | URL |
|----------|-----|
| Primary | `https://arbitrum-api.gmxinfra.io` |
| Fallback 1 | `https://arbitrum-api-fallback.gmxinfra.io` |
| Fallback 2 | `https://arbitrum-api-fallback.gmxinfra2.io` |

### Avalanche

| Priority | URL |
|----------|-----|
| Primary | `https://avalanche-api.gmxinfra.io` |
| Fallback 1 | `https://avalanche-api-fallback.gmxinfra.io` |
| Fallback 2 | `https://avalanche-api-fallback.gmxinfra2.io` |

### Botanix

| Priority | URL |
|----------|-----|
| Primary | `https://botanix-api.gmxinfra.io` |
| Fallback 1 | `https://botanix-api-fallback.gmxinfra.io` |
| Fallback 2 | `https://botanix-api-fallback.gmxinfra2.io` |

### Fallback Tracker Configuration

The SDK automatically manages endpoint health using a tracker:

- **Check interval:** 10 seconds
- **Check timeout:** 10 seconds
- **Cache timeout:** 5 minutes
- **Failures before ban:** 3 failures within 60 seconds
- **Ban throttle:** 2 seconds between retries
- **Endpoint rotation throttle:** 5 seconds
