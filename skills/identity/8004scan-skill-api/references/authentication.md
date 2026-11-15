# 8004scan API Authentication & Rate Limits

## Authentication

The 8004scan public API uses optional API key authentication. All endpoints work without a key (anonymous tier) but with reduced rate limits.

### API Key Header

```
X-API-Key: your-api-key-here
```

### Environment Variable

Set `EIGHTSCAN_API_KEY` and include in requests:

```bash
curl -s "https://8004scan.io/api/v1/public/agents" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY"
```

### Getting an API Key

Visit https://8004scan.io/developers to obtain API keys for different tiers.

## Rate Limit Tiers

| Tier | Requests/Min | Daily Limit | Use Case |
|------|-------------|-------------|----------|
| **Anonymous** | 10 | 100 | Quick testing, one-off queries |
| **Free API Key** | 30 | 1,000 | Development, prototyping |
| **Basic** | 100 | 10,000 | Small applications, bots |
| **Pro** | 500 | 100,000 | Production applications |
| **Enterprise** | 2,000 | Unlimited | High-volume integrations |

## Rate Limit Headers

Every response includes rate limit information:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests allowed in the current window |
| `X-RateLimit-Remaining` | Requests remaining in the current window |
| `X-RateLimit-Reset` | Unix timestamp when the limit resets |

## Rate Limit Exceeded

When the limit is hit, the API returns HTTP 429:

```json
{
  "success": false,
  "error": {
    "code": "RateLimitExceeded",
    "message": "Rate limit exceeded. Please wait or upgrade your plan.",
    "details": {
      "limit": 10,
      "remaining": 0,
      "resetAt": "2026-03-16T12:05:00Z"
    }
  }
}
```

### Handling Rate Limits

1. Check `X-RateLimit-Remaining` before making requests
2. If remaining is 0, wait until `X-RateLimit-Reset`
3. For batch operations, add delays between requests
4. Consider upgrading tier for production use

## Response Metadata

Every successful response includes `meta`:

```json
{
  "meta": {
    "version": "1.0",
    "timestamp": "2026-03-16T12:00:00Z",
    "requestId": "550e8400-e29b-41d4-a716-446655440000",
    "pagination": {
      "limit": 20,
      "page": 1,
      "limit": 20,
      "total": 500,
      "hasMore": true
    }
  }
}
```

Use `requestId` when reporting issues to 8004scan support.
