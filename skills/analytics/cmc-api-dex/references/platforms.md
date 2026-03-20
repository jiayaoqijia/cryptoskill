# DEX Platform APIs

## Platform List

**Path:** `GET /v1/dex/platform/list`

**Description:** Get a list of all supported blockchain platforms/networks for DEX data. Use this to get valid network_slug and platform_crypto_id values for other endpoints.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start | integer | No | Pagination offset (default: 1) |
| limit | integer | No | Results per page (default: 100, max: 500) |
| sort | string | No | Sort field (name, dex_count) |
| sort_dir | string | No | Sort direction (asc, desc) |

### Response Fields

| Field | Description |
|-------|-------------|
| platforms | Array of platform objects |
| platforms[].id | Platform CMC ID (use as platform_crypto_id) |
| platforms[].name | Platform name (e.g., Ethereum, Solana) |
| platforms[].slug | Platform slug (use as network_slug) |
| platforms[].symbol | Native token symbol (ETH, SOL) |
| platforms[].token_count | Number of tracked tokens |
| platforms[].dex_count | Number of DEXs on platform |
| platforms[].total_liquidity | Total liquidity across all DEXs |
| platforms[].volume_24h | 24-hour volume across all DEXs |
| platforms[].logo | Platform logo URL |
| total_count | Total platforms available |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/platform/list?limit=50&sort=total_liquidity&sort_dir=desc" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Platform Detail

**Path:** `GET /v1/dex/platform/detail`

**Description:** Get detailed information about a specific blockchain platform including all DEXs operating on it.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | Yes* | Network identifier (e.g., ethereum) |
| platform_crypto_id | integer | Yes* | Alternative to network_slug |

*One of network_slug or platform_crypto_id is required.

### Response Fields

| Field | Description |
|-------|-------------|
| id | Platform CMC ID |
| name | Platform name |
| slug | Platform slug |
| symbol | Native token symbol |
| description | Platform description |
| logo | Platform logo URL |
| website | Official website |
| explorer | Block explorer URL |
| token_count | Number of tracked tokens |
| pair_count | Number of trading pairs |
| total_liquidity | Total liquidity in USD |
| volume_24h | 24-hour trading volume |
| dexes | Array of DEX objects on this platform |
| dexes[].name | DEX name |
| dexes[].slug | DEX slug |
| dexes[].logo | DEX logo |
| dexes[].liquidity | DEX liquidity |
| dexes[].volume_24h | DEX 24h volume |
| dexes[].pair_count | Number of pairs on DEX |
| dexes[].website | DEX website |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/platform/detail?network_slug=ethereum" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/platform/detail?platform_crypto_id=5426" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Search

**Path:** `GET /v1/dex/search`

**Description:** Search for DEX tokens and trading pairs by keyword. Useful for finding contract addresses when you only know the token name or symbol.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| keyword | string | Yes | Search term (token name, symbol, or partial address) |
| network_slug | string | No | Filter by network |
| platform_crypto_id | integer | No | Alternative network filter |
| search_type | string | No | Filter results (token, pair, all) |
| start | integer | No | Pagination offset (default: 1) |
| limit | integer | No | Results per page (default: 20, max: 100) |

### Response Fields

| Field | Description |
|-------|-------------|
| tokens | Array of matching token objects |
| tokens[].id | Token CMC DEX ID |
| tokens[].name | Token name |
| tokens[].symbol | Token symbol |
| tokens[].contract_address | Contract address |
| tokens[].network_slug | Network identifier |
| tokens[].network_name | Network name |
| tokens[].price | Current price |
| tokens[].volume_24h | 24-hour volume |
| tokens[].liquidity | Total liquidity |
| tokens[].logo | Token logo URL |
| tokens[].verified | Whether token is verified |
| pairs | Array of matching pair objects |
| pairs[].pair_address | Pool contract address |
| pairs[].dex_name | DEX name |
| pairs[].network_slug | Network identifier |
| pairs[].base_token | Base token info |
| pairs[].quote_token | Quote token info |
| pairs[].liquidity | Pair liquidity |
| pairs[].volume_24h | 24-hour volume |
| total_tokens | Total matching tokens |
| total_pairs | Total matching pairs |

### Example

```bash
# Search for PEPE token
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/search?keyword=PEPE&limit=10" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

```bash
# Search for tokens on Solana only
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/search?keyword=bonk&network_slug=solana&search_type=token" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

```bash
# Search by partial contract address
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/search?keyword=0x6982508&network_slug=ethereum" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```
