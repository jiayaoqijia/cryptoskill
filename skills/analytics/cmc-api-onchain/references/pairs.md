# DEX Pairs APIs

## Pairs Quotes Latest

**Path:** `GET /v4/dex/pairs/quotes/latest`

**Description:** Get the latest quote data for a specific DEX trading pair. Returns price, volume, liquidity, and recent price changes.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | Yes* | Network identifier (e.g., ethereum, solana, bsc) |
| platform_crypto_id | integer | Yes* | Alternative to network_slug, use platform's CMC ID |
| contract_address | string | Yes | Pool/pair contract address |
| base_address | string | No | Base token address (for direction) |
| quote_address | string | No | Quote token address (for direction) |

*One of network_slug or platform_crypto_id is required.

### Response Fields

| Field | Description |
|-------|-------------|
| pair_address | Pool/pair contract address |
| dex_name | DEX name (Uniswap V3, Raydium, etc.) |
| dex_slug | DEX identifier |
| network_slug | Network of the pair |
| base_token | Base token information |
| base_token.name | Base token name |
| base_token.symbol | Base token symbol |
| base_token.address | Base token contract address |
| quote_token | Quote token information |
| quote_token.name | Quote token name |
| quote_token.symbol | Quote token symbol |
| quote_token.address | Quote token contract address |
| price | Current price (base in terms of quote) |
| price_usd | Price in USD |
| price_quote | Price in quote token |
| percent_change_1h | 1-hour price change % |
| percent_change_24h | 24-hour price change % |
| percent_change_7d | 7-day price change % |
| volume_24h | 24-hour trading volume in USD |
| volume_24h_base | 24-hour volume in base token |
| volume_24h_quote | 24-hour volume in quote token |
| liquidity | Total liquidity in USD |
| liquidity_base | Liquidity in base token |
| liquidity_quote | Liquidity in quote token |
| fee_tier | Pool fee percentage (e.g., 0.3%) |
| txns_24h | Number of transactions in 24h |
| buys_24h | Number of buy transactions |
| sells_24h | Number of sell transactions |
| makers_24h | Unique makers in 24h |
| last_updated | Timestamp of last update |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v4/dex/pairs/quotes/latest?network_slug=ethereum&contract_address=0x11b815efb8f581194ae79006d24e0d814b7697f6" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Spot Pairs Latest

**Path:** `GET /v4/dex/spot-pairs/latest`

**Description:** Get a listing of DEX spot trading pairs with filtering and sorting options. Useful for discovering trading pairs on specific DEXs or networks.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | No | Filter by network |
| platform_crypto_id | integer | No | Alternative network filter |
| dex_slug | string | No | Filter by DEX (uniswap-v3, raydium, pancakeswap) |
| base_address | string | No | Filter pairs with this base token |
| quote_address | string | No | Filter pairs with this quote token |
| start | integer | No | Pagination offset (default: 1) |
| limit | integer | No | Results per page (default: 100, max: 1000) |
| sort | string | No | Sort field (volume_24h, liquidity, price_change_24h) |
| sort_dir | string | No | Sort direction (asc, desc) |
| min_liquidity | number | No | Minimum liquidity in USD |
| min_volume_24h | number | No | Minimum 24h volume in USD |

### Response Fields

| Field | Description |
|-------|-------------|
| pairs | Array of trading pair objects |
| pairs[].pair_address | Pool/pair contract address |
| pairs[].dex_name | DEX name |
| pairs[].dex_slug | DEX identifier |
| pairs[].network_slug | Network identifier |
| pairs[].base_token | Base token info (name, symbol, address) |
| pairs[].quote_token | Quote token info (name, symbol, address) |
| pairs[].price | Current price |
| pairs[].price_usd | USD price |
| pairs[].percent_change_24h | 24-hour change % |
| pairs[].volume_24h | 24-hour volume |
| pairs[].liquidity | Total liquidity |
| pairs[].fee_tier | Pool fee % |
| pairs[].created_at | Pair creation timestamp |
| total_count | Total pairs matching filters |

### Example

```bash
# Get top Uniswap V3 pairs by volume
curl -X GET "https://pro-api.coinmarketcap.com/v4/dex/spot-pairs/latest?network_slug=ethereum&dex_slug=uniswap-v3&sort=volume_24h&sort_dir=desc&limit=20" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

```bash
# Get all pairs for a specific token
curl -X GET "https://pro-api.coinmarketcap.com/v4/dex/spot-pairs/latest?network_slug=ethereum&base_address=0x6982508145454Ce325dDbE47a25d4ec3d2311933&min_liquidity=10000" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

```bash
# Get Solana Raydium pairs
curl -X GET "https://pro-api.coinmarketcap.com/v4/dex/spot-pairs/latest?network_slug=solana&dex_slug=raydium&sort=liquidity&sort_dir=desc&limit=50" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```
