# Info API Reference

## Cryptocurrency Info

**Path:** `GET /v2/cryptocurrency/info`

**Description:** Returns static metadata for one or more cryptocurrencies including logo, description, website URLs, social links, technical documentation, and contract addresses. This data changes infrequently and should be cached.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Conditional | One or more comma-separated CMC IDs (e.g., 1,1027) |
| slug | string | Conditional | One or more comma-separated slugs (e.g., bitcoin,ethereum) |
| symbol | string | Conditional | One or more comma-separated symbols (e.g., BTC,ETH) |
| address | string | Conditional | One or more comma-separated contract addresses |
| skip_invalid | boolean | No | Skip invalid IDs instead of erroring. Default: false |
| aux | string | No | Additional fields: urls, logo, description, tags, platform, date_added, notice, status. Default: all |

**Note:** At least one of `id`, `slug`, `symbol`, or `address` is required.

### Response Fields

| Field | Description |
|-------|-------------|
| data[id].id | CMC cryptocurrency ID |
| data[id].name | Cryptocurrency name |
| data[id].symbol | Cryptocurrency symbol |
| data[id].slug | URL slug |
| data[id].category | Category (coin or token) |
| data[id].description | Full description text |
| data[id].logo | URL to logo image |
| data[id].subreddit | Subreddit name |
| data[id].notice | Any notices about the crypto |
| data[id].tags | Array of tags |
| data[id].tag-names | Human-readable tag names |
| data[id].tag-groups | Tag groupings |
| data[id].date_added | Date added to CMC |
| data[id].date_launched | Official launch date |
| data[id].is_hidden | Hidden from CMC listings |
| data[id].platform | Platform details for tokens |
| data[id].platform.id | Platform CMC ID |
| data[id].platform.name | Platform name |
| data[id].platform.symbol | Platform symbol |
| data[id].platform.slug | Platform slug |
| data[id].platform.token_address | Contract address |
| data[id].contract_address | Array of contract addresses |
| data[id].contract_address[].contract_address | Contract address |
| data[id].contract_address[].platform.name | Platform name |
| data[id].contract_address[].platform.coin.id | Platform coin ID |
| data[id].self_reported_circulating_supply | Self-reported supply |
| data[id].self_reported_market_cap | Self-reported market cap |
| data[id].self_reported_tags | Self-reported tags |
| data[id].infinite_supply | Has infinite supply |
| data[id].urls | Object containing URL arrays |
| data[id].urls.website | Official website URLs |
| data[id].urls.technical_doc | Whitepaper/docs URLs |
| data[id].urls.twitter | Twitter profile URLs |
| data[id].urls.reddit | Reddit URLs |
| data[id].urls.message_board | Forum URLs |
| data[id].urls.announcement | Announcement URLs |
| data[id].urls.chat | Chat/Discord URLs |
| data[id].urls.explorer | Blockchain explorer URLs |
| data[id].urls.source_code | Source code URLs |

### Example

```bash
# Get info by ID
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info?id=1,1027" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get info by symbol
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info?symbol=BTC,ETH" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get info by contract address
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info?address=0xdac17f958d2ee523a2206206994597c13d831ec7" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Example Response

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": {
    "1": {
      "id": 1,
      "name": "Bitcoin",
      "symbol": "BTC",
      "slug": "bitcoin",
      "category": "coin",
      "description": "Bitcoin (BTC) is a cryptocurrency launched in 2009. Users are able to generate BTC through the process of mining. Bitcoin has a current supply of 19,590,000. The last known price of Bitcoin is 42,567.89 USD and is down -1.23 over the last 24 hours.",
      "logo": "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png",
      "subreddit": "bitcoin",
      "notice": null,
      "tags": ["mineable", "pow", "sha-256", "store-of-value"],
      "date_added": "2010-07-13T00:00:00.000Z",
      "date_launched": "2009-01-03T00:00:00.000Z",
      "platform": null,
      "contract_address": [],
      "self_reported_circulating_supply": null,
      "self_reported_market_cap": null,
      "infinite_supply": false,
      "urls": {
        "website": ["https://bitcoin.org/"],
        "technical_doc": ["https://bitcoin.org/bitcoin.pdf"],
        "twitter": ["https://twitter.com/bitcoin"],
        "reddit": ["https://reddit.com/r/bitcoin"],
        "message_board": ["https://bitcointalk.org"],
        "announcement": [],
        "chat": [],
        "explorer": [
          "https://blockchain.info/",
          "https://blockchair.com/bitcoin",
          "https://btc.com/"
        ],
        "source_code": ["https://github.com/bitcoin/bitcoin"]
      }
    },
    "1027": {
      "id": 1027,
      "name": "Ethereum",
      "symbol": "ETH",
      "slug": "ethereum",
      "category": "coin",
      "description": "Ethereum (ETH) is a cryptocurrency launched in 2015...",
      "logo": "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
      "subreddit": "ethereum",
      "notice": null,
      "tags": ["pos", "smart-contracts", "ethereum-ecosystem"],
      "date_added": "2015-08-07T00:00:00.000Z",
      "platform": null,
      "contract_address": [],
      "infinite_supply": true,
      "urls": {
        "website": ["https://www.ethereum.org/"],
        "technical_doc": ["https://ethereum.org/whitepaper/"],
        "twitter": ["https://twitter.com/ethereum"],
        "reddit": ["https://reddit.com/r/ethereum"],
        "message_board": [],
        "announcement": [],
        "chat": [],
        "explorer": [
          "https://etherscan.io/",
          "https://ethplorer.io/"
        ],
        "source_code": ["https://github.com/ethereum/go-ethereum"]
      }
    }
  }
}
```

### Important Notes

1. **Response structure**: Unlike list endpoints, this returns data keyed by ID in an object, not an array.

2. **Symbol lookups**: When using `symbol`, multiple cryptocurrencies may match. The response will include all matches keyed by their IDs.

3. **Caching**: This metadata changes infrequently. Cache results for 24 hours or more.

4. **Logo URLs**: Logo URLs follow the pattern `https://s2.coinmarketcap.com/static/img/coins/64x64/{id}.png`. Sizes available: 64x64, 128x128, 200x200.

5. **Contract addresses**: Tokens exist on multiple chains. Check the `contract_address` array for all deployments.
