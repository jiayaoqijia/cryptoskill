# x402 Endpoint Reference

Full parameter reference for all x402 endpoints. These endpoints mirror the standard CMC Pro API.

Base URL: `https://pro.coinmarketcap.com`

---

## Cryptocurrency Quotes Latest

**Path:** `GET /x402/v3/cryptocurrency/quotes/latest`

Returns the latest market quote for one or more cryptocurrencies.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Conditional | Comma-separated CMC IDs (e.g., 1,1027) |
| slug | string | Conditional | Comma-separated slugs (e.g., bitcoin,ethereum) |
| symbol | string | Conditional | Comma-separated symbols (e.g., BTC,ETH) |
| convert | string | No | Quote currency (default: USD) |
| convert_id | string | No | CMC ID of currency to convert to |
| aux | string | No | Additional fields to include |
| skip_invalid | boolean | No | Skip invalid IDs instead of erroring |

At least one of `id`, `slug`, or `symbol` is required.

### Example

```
GET https://pro.coinmarketcap.com/x402/v3/cryptocurrency/quotes/latest?id=1,1027
GET https://pro.coinmarketcap.com/x402/v3/cryptocurrency/quotes/latest?symbol=BTC,ETH
```

### Returns

Price, market cap, volume, circulating supply, percent changes (1h, 24h, 7d, 30d, 60d, 90d), market cap dominance, fully diluted market cap.

---

## Cryptocurrency Listings Latest

**Path:** `GET /x402/v3/cryptocurrency/listing/latest`

Returns a paginated list of all active cryptocurrencies ranked by market cap.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start | integer | No | Offset for pagination (default: 1) |
| limit | integer | No | Number of results (default: 100, max: 5000) |
| price_min | number | No | Filter by minimum price |
| price_max | number | No | Filter by maximum price |
| market_cap_min | number | No | Filter by minimum market cap |
| market_cap_max | number | No | Filter by maximum market cap |
| volume_24h_min | number | No | Filter by minimum 24h volume |
| volume_24h_max | number | No | Filter by maximum 24h volume |
| convert | string | No | Quote currency (default: USD) |
| sort | string | No | Sort field: market_cap, name, symbol, date_added, price, volume_24h, percent_change_24h (default: market_cap) |
| sort_dir | string | No | Sort direction: asc, desc (default: desc) |
| cryptocurrency_type | string | No | Filter: all, coins, tokens (default: all) |

### Example

```
GET https://pro.coinmarketcap.com/x402/v3/cryptocurrency/listing/latest?start=1&limit=10
GET https://pro.coinmarketcap.com/x402/v3/cryptocurrency/listing/latest?limit=100&sort=volume_24h
```

### Returns

Ranked list with id, name, symbol, rank, circulating supply, total supply, max supply, price, volume, market cap, and percent changes for each cryptocurrency.

---

## DEX Search

**Path:** `GET /x402/v1/dex/search`

Search for DEX tokens and trading pairs by keyword.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| q | string | Yes | Search keyword (token name, symbol, or contract address) |
| network_slug | string | No | Filter by network (ethereum, solana, bsc, base, arbitrum, polygon) |
| platform_crypto_id | integer | No | Alternative to network_slug |
| search_type | string | No | Filter: token, pair, all |
| start | integer | No | Pagination offset (default: 1) |
| limit | integer | No | Results per page (default: 20, max: 100) |

### Example

```
GET https://pro.coinmarketcap.com/x402/v1/dex/search?q=pepe
GET https://pro.coinmarketcap.com/x402/v1/dex/search?q=bonk&network_slug=solana
```

### Returns

Matching tokens (id, name, symbol, contract_address, network, price, volume, liquidity) and matching pairs (pair_address, dex_name, base/quote tokens, liquidity, volume).

---

## DEX Pairs Quotes Latest

**Path:** `GET /x402/v4/dex/pairs/quotes/latest`

Get the latest quotes and trading data for specific DEX trading pairs.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| pair_address | string | Yes | DEX pair/pool contract address |
| network_slug | string | No | Network identifier (ethereum, solana, bsc, base, arbitrum, polygon) |
| platform_crypto_id | integer | No | Alternative to network_slug |
| base_address | string | No | Base token address |
| quote_address | string | No | Quote token address |

### Example

```
GET https://pro.coinmarketcap.com/x402/v4/dex/pairs/quotes/latest?pair_address=0x...
GET https://pro.coinmarketcap.com/x402/v4/dex/pairs/quotes/latest?pair_address=0x...&network_slug=ethereum
```

### Returns

Pair address, DEX name, base/quote token info, price, price_usd, percent changes (1h, 24h, 7d), volume_24h, liquidity, fee tier, transaction counts, maker counts.
