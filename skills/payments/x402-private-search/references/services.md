# Known x402 Services

## Web Search (SearXNG)

- **URL**: `https://nicholas-hopefully-plumbing-troubleshooting.trycloudflare.com`
- **Endpoint**: `GET /web/search?q=<query>&count=<1-20>&offset=<n>`
- **Price**: $0.001 USDC per query
- **Network**: Base Sepolia (`eip155:84532`)
- **Response**: Brave Search API compatible JSON
- **Free endpoints**: `GET /health`, `GET /routes`

> ⚠️ This URL is a quick Cloudflare tunnel and may change on service restart. Check `/health` to verify availability.

### Response format

```json
{
  "query": { "original": "search terms" },
  "type": "search",
  "web": {
    "type": "search",
    "results": [
      {
        "title": "Result Title",
        "url": "https://example.com",
        "description": "Snippet text...",
        "age": "2026-02-14"
      }
    ],
    "family_friendly": true
  }
}
```

### Discovery

Any x402 service returns payment requirements when you hit a paid endpoint without payment. Call `GET /routes` on any x402 gateway to list available endpoints and prices.
