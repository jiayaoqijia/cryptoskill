# Community API Reference

Community endpoints provide insights into trending tokens and topics based on user engagement, discussions, and social activity on CoinMarketCap's community platform.

## Trending Tokens

**Path:** `GET /v1/community/trending/token`

**Description:** Returns tokens that are currently trending based on community activity. This includes mentions, discussions, upvotes, and overall engagement on the CoinMarketCap community platform.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| limit | integer | No | Number of results to return. Default: 10, Max: 100 |
| start | integer | No | Offset for pagination. Default: 1 |
| time_period | string | No | Time period for trending calculation. Options: 24h, 7d, 30d. Default: 24h |

### Response Fields

| Field | Description |
|-------|-------------|
| data | Array of trending token objects |
| data[].id | CMC cryptocurrency ID |
| data[].name | Cryptocurrency name |
| data[].symbol | Cryptocurrency symbol |
| data[].slug | URL-friendly name |
| data[].rank | Current market cap rank |
| data[].trending_rank | Position in trending list |
| data[].trending_score | Calculated trending score |
| data[].mention_count | Number of community mentions |
| data[].post_count | Number of posts about this token |
| data[].engagement_score | Total engagement metric |
| data[].sentiment | Overall sentiment (positive, negative, neutral) |
| data[].sentiment_score | Sentiment score (-100 to 100) |
| data[].logo | URL to token logo |
| data[].quote | Current price data |
| data[].quote.price | Current price in USD |
| data[].quote.percent_change_24h | 24h price change |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/community/trending/token?limit=10&time_period=24h" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Example Response

```json
{
  "status": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": [
    {
      "id": 1,
      "name": "Bitcoin",
      "symbol": "BTC",
      "slug": "bitcoin",
      "rank": 1,
      "trending_rank": 1,
      "trending_score": 98.5,
      "mention_count": 15234,
      "post_count": 3421,
      "engagement_score": 89432,
      "sentiment": "positive",
      "sentiment_score": 72,
      "logo": "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png",
      "quote": {
        "USD": {
          "price": 43250.00,
          "percent_change_24h": 2.35
        }
      }
    },
    {
      "id": 1027,
      "name": "Ethereum",
      "symbol": "ETH",
      "slug": "ethereum",
      "rank": 2,
      "trending_rank": 2,
      "trending_score": 87.3,
      "mention_count": 8945,
      "post_count": 2156,
      "engagement_score": 67234,
      "sentiment": "positive",
      "sentiment_score": 65,
      "logo": "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
      "quote": {
        "USD": {
          "price": 2580.00,
          "percent_change_24h": 1.89
        }
      }
    }
  ]
}
```

---

## Trending Topics

**Path:** `GET /v1/community/trending/topic`

**Description:** Returns topics that are currently trending in community discussions. Topics include themes, events, narratives, and general crypto subjects being discussed.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| limit | integer | No | Number of results to return. Default: 10, Max: 50 |
| start | integer | No | Offset for pagination. Default: 1 |
| time_period | string | No | Time period for trending calculation. Options: 24h, 7d, 30d. Default: 24h |

### Response Fields

| Field | Description |
|-------|-------------|
| data | Array of trending topic objects |
| data[].id | Topic identifier |
| data[].name | Topic name/title |
| data[].slug | URL-friendly topic name |
| data[].description | Brief topic description |
| data[].trending_rank | Position in trending list |
| data[].trending_score | Calculated trending score |
| data[].post_count | Number of posts about this topic |
| data[].comment_count | Number of comments on topic posts |
| data[].engagement_score | Total engagement metric |
| data[].sentiment | Overall sentiment (positive, negative, neutral) |
| data[].related_tokens | Array of related cryptocurrency IDs |
| data[].tags | Array of topic tags |
| data[].created_at | When the topic started trending |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/community/trending/topic?limit=10&time_period=24h" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Example Response

```json
{
  "status": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": [
    {
      "id": "btc-etf-approval",
      "name": "Bitcoin ETF Approval",
      "slug": "bitcoin-etf-approval",
      "description": "Discussion around Bitcoin spot ETF approvals and market impact",
      "trending_rank": 1,
      "trending_score": 95.2,
      "post_count": 5678,
      "comment_count": 23456,
      "engagement_score": 156789,
      "sentiment": "positive",
      "related_tokens": [1, 1027, 825],
      "tags": ["etf", "bitcoin", "regulation", "institutional"],
      "created_at": "2024-01-10T00:00:00.000Z"
    },
    {
      "id": "defi-yields",
      "name": "DeFi Yield Strategies",
      "slug": "defi-yield-strategies",
      "description": "Discussions about DeFi yield farming and staking opportunities",
      "trending_rank": 2,
      "trending_score": 78.6,
      "post_count": 2345,
      "comment_count": 8765,
      "engagement_score": 67890,
      "sentiment": "neutral",
      "related_tokens": [1027, 7083, 5994],
      "tags": ["defi", "yield", "staking", "farming"],
      "created_at": "2024-01-12T00:00:00.000Z"
    }
  ]
}
```

---

## Use Cases

### Social Sentiment Analysis

Track community sentiment for trading insights:
1. Monitor trending tokens for early momentum signals
2. Identify sentiment shifts before price moves
3. Detect hype cycles and FOMO indicators

### Narrative Discovery

Find emerging market narratives:
1. Track trending topics for sector rotations
2. Identify new themes gaining traction
3. Correlate topic trends with token performance

### Research and Due Diligence

Use community data for research:
1. Gauge community interest in projects
2. Compare engagement across similar tokens
3. Identify tokens with growing mindshare

### Alert Systems

Build alerts based on community activity:
1. Notify when a token enters trending list
2. Track sentiment score changes
3. Monitor topic emergence for specific themes

### Content Strategy

For content creators and marketers:
1. Identify hot topics for content creation
2. Track what the community is discussing
3. Find tokens with high engagement for coverage
