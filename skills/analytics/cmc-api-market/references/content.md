# Content API Reference

Content endpoints provide access to news articles, Alexandria educational content, and community posts on CoinMarketCap.

## Table of Contents

1. [Latest Content](#latest-content)
2. [Post Comments](#post-comments)
3. [Latest Posts](#latest-posts)
4. [Top Posts](#top-posts)
5. [Use Cases](#use-cases)

---

## Latest Content

**Path:** `GET /v1/content/latest`

**Description:** Returns the latest news articles and Alexandria content from CoinMarketCap. Alexandria is CMC's educational and research platform featuring in-depth articles and analysis.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| limit | integer | No | Number of results to return. Default: 10, Max: 100 |
| start | integer | No | Offset for pagination. Default: 1 |
| content_type | string | No | Filter by content type. Options: news, alexandria, all. Default: all |
| category | string | No | Filter by category (e.g., bitcoin, ethereum, defi, nft, regulation) |
| language | string | No | Filter by language code (e.g., en, zh, es). Default: en |
| slug | string | No | Filter by cryptocurrency slug to get related content |
| id | string | No | Filter by cryptocurrency ID to get related content |

### Response Fields

| Field | Description |
|-------|-------------|
| data | Array of content objects |
| data[].id | Content unique identifier |
| data[].title | Article title |
| data[].subtitle | Article subtitle or summary |
| data[].slug | URL-friendly content slug |
| data[].content_type | Type: news or alexandria |
| data[].category | Content category |
| data[].author | Author name |
| data[].source | Source publication (for news) |
| data[].source_url | Original source URL |
| data[].cover_image | URL to cover image |
| data[].published_at | Publication timestamp |
| data[].updated_at | Last update timestamp |
| data[].language | Content language code |
| data[].tags | Array of content tags |
| data[].related_coins | Array of related cryptocurrency IDs |
| data[].views | View count |
| data[].likes | Like count |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/content/latest?limit=10&content_type=news" \
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
      "id": "news-123456",
      "title": "Bitcoin Surges Past $45,000 Amid ETF Optimism",
      "subtitle": "Market sentiment improves as institutional adoption grows",
      "slug": "bitcoin-surges-past-45000-amid-etf-optimism",
      "content_type": "news",
      "category": "bitcoin",
      "author": "John Smith",
      "source": "CoinMarketCap",
      "source_url": "https://coinmarketcap.com/news/...",
      "cover_image": "https://cdn.coinmarketcap.com/content/123456.jpg",
      "published_at": "2024-01-15T09:00:00.000Z",
      "updated_at": "2024-01-15T09:30:00.000Z",
      "language": "en",
      "tags": ["bitcoin", "etf", "price"],
      "related_coins": [1],
      "views": 15234,
      "likes": 892
    }
  ]
}
```

---

## Post Comments

**Path:** `GET /v1/content/posts/comments`

**Description:** Returns comments for a specific community post. Useful for analyzing community reactions and discussions around specific content.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| post_id | string | Yes | The ID of the post to get comments for |
| limit | integer | No | Number of results to return. Default: 20, Max: 100 |
| start | integer | No | Offset for pagination. Default: 1 |
| sort | string | No | Sort order. Options: newest, oldest, top. Default: newest |

### Response Fields

| Field | Description |
|-------|-------------|
| data | Array of comment objects |
| data[].id | Comment unique identifier |
| data[].post_id | Parent post ID |
| data[].user | Comment author information |
| data[].user.id | User ID |
| data[].user.username | User display name |
| data[].user.avatar | User avatar URL |
| data[].content | Comment text content |
| data[].created_at | Comment creation timestamp |
| data[].updated_at | Last edit timestamp |
| data[].likes | Number of likes |
| data[].replies_count | Number of replies to this comment |
| data[].parent_comment_id | ID of parent comment (for nested replies) |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/content/posts/comments?post_id=abc123&limit=20&sort=top" \
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
      "id": "comment-789",
      "post_id": "abc123",
      "user": {
        "id": "user-456",
        "username": "CryptoTrader",
        "avatar": "https://cdn.coinmarketcap.com/avatars/user-456.jpg"
      },
      "content": "Great analysis! I agree with the bullish outlook.",
      "created_at": "2024-01-15T08:30:00.000Z",
      "updated_at": "2024-01-15T08:30:00.000Z",
      "likes": 45,
      "replies_count": 3,
      "parent_comment_id": null
    }
  ]
}
```

---

## Latest Posts

**Path:** `GET /v1/content/posts/latest`

**Description:** Returns the latest community posts from CoinMarketCap users. These are user-generated posts including analysis, opinions, and discussions.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| limit | integer | No | Number of results to return. Default: 20, Max: 100 |
| start | integer | No | Offset for pagination. Default: 1 |
| id | string | No | Filter by cryptocurrency ID for related posts |
| slug | string | No | Filter by cryptocurrency slug for related posts |
| post_type | string | No | Filter by post type. Options: analysis, prediction, news, general |
| language | string | No | Filter by language code. Default: en |

### Response Fields

| Field | Description |
|-------|-------------|
| data | Array of post objects |
| data[].id | Post unique identifier |
| data[].user | Post author information |
| data[].user.id | User ID |
| data[].user.username | User display name |
| data[].user.avatar | User avatar URL |
| data[].user.verified | Whether user is verified |
| data[].title | Post title |
| data[].content | Post text content |
| data[].post_type | Type of post |
| data[].created_at | Post creation timestamp |
| data[].updated_at | Last edit timestamp |
| data[].likes | Number of likes |
| data[].comments_count | Number of comments |
| data[].shares_count | Number of shares |
| data[].views | View count |
| data[].images | Array of image URLs |
| data[].related_coins | Array of related cryptocurrency IDs |
| data[].tags | Array of post tags |
| data[].sentiment | Post sentiment if tagged (bullish, bearish, neutral) |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/content/posts/latest?limit=20&id=1" \
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
      "id": "post-abc123",
      "user": {
        "id": "user-123",
        "username": "BTCAnalyst",
        "avatar": "https://cdn.coinmarketcap.com/avatars/user-123.jpg",
        "verified": true
      },
      "title": "Bitcoin Technical Analysis: Key Levels to Watch",
      "content": "Looking at the 4H chart, BTC is approaching major resistance...",
      "post_type": "analysis",
      "created_at": "2024-01-15T07:00:00.000Z",
      "updated_at": "2024-01-15T07:00:00.000Z",
      "likes": 234,
      "comments_count": 56,
      "shares_count": 23,
      "views": 5678,
      "images": ["https://cdn.coinmarketcap.com/posts/chart-123.png"],
      "related_coins": [1],
      "tags": ["bitcoin", "technical-analysis", "trading"],
      "sentiment": "bullish"
    }
  ]
}
```

---

## Top Posts

**Path:** `GET /v1/content/posts/top`

**Description:** Returns the top-ranked community posts based on engagement metrics. These are the most popular and highly engaged posts.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| limit | integer | No | Number of results to return. Default: 20, Max: 100 |
| start | integer | No | Offset for pagination. Default: 1 |
| id | string | No | Filter by cryptocurrency ID for related posts |
| slug | string | No | Filter by cryptocurrency slug for related posts |
| time_period | string | No | Time period for ranking. Options: 24h, 7d, 30d, all. Default: 24h |
| post_type | string | No | Filter by post type. Options: analysis, prediction, news, general |

### Response Fields

| Field | Description |
|-------|-------------|
| data | Array of post objects (same structure as latest posts) |
| data[].ranking_score | Score used for ranking |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/content/posts/top?limit=10&time_period=24h" \
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
      "id": "post-xyz789",
      "user": {
        "id": "user-789",
        "username": "CryptoInsider",
        "avatar": "https://cdn.coinmarketcap.com/avatars/user-789.jpg",
        "verified": true
      },
      "title": "ETF Approval Impact Analysis",
      "content": "Breaking down what the ETF approval means for the market...",
      "post_type": "analysis",
      "created_at": "2024-01-14T18:00:00.000Z",
      "updated_at": "2024-01-14T18:00:00.000Z",
      "likes": 1567,
      "comments_count": 423,
      "shares_count": 234,
      "views": 45678,
      "images": [],
      "related_coins": [1, 1027],
      "tags": ["etf", "market-analysis", "institutional"],
      "sentiment": "bullish",
      "ranking_score": 98.5
    }
  ]
}
```

---

## Use Cases

### News Aggregation

Build a crypto news feed:
1. Fetch latest news with `/content/latest?content_type=news`
2. Filter by category or cryptocurrency
3. Display with cover images and summaries

### Community Sentiment

Analyze community opinions:
1. Get top posts for a specific token
2. Review sentiment tags on posts
3. Aggregate bullish vs bearish ratios

### Research Platform

Build research tools:
1. Fetch Alexandria content for educational material
2. Track popular analysis posts
3. Monitor high-engagement discussions

### Social Signals

Use community data for trading signals:
1. Track posts with high engagement spikes
2. Monitor comment activity on trending topics
3. Identify viral content early
