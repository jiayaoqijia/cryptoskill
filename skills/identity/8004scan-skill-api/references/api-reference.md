# 8004scan Public API — Full Reference

Base URL: `https://8004scan.io/api/v1/public`

OpenAPI spec: `https://8004scan.io/api/v1/public/docs/openapi.json`

---

## GET /agents

List agents with pagination, filtering, and sorting.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number (1-indexed) |
| `limit` | integer | 20 | Results per page (1-100) |
| `chainId` | integer | — | Filter by blockchain network |
| `ownerAddress` | string | — | Filter by owner wallet (0x...) |
| `search` | string | — | Search by name, description, or agent ID |
| `protocol` | string | — | Filter by protocol type (`MCP`, `A2A`, `OASF`, `Web`, `Email`) |
| `sortBy` | string | `created_at` | Sort field (`created_at`, `stars`, `name`, `token_id`, `total_score`) |
| `sortOrder` | string | desc | Sort direction (asc, desc) |
| `isTestnet` | boolean | — | Filter by testnet/mainnet |

### Response

```json
{
  "success": true,
  "data": [
    {
      "chain_id": 8453,
      "token_id": 17,
      "name": "Agent Name",
      "description": "What it does",
      "owner_address": "0x...",
      "active": true,
      "supported_protocols": ["MCP", "A2A"],
      "total_score": 85,
      "star_count": 12,
      "total_feedbacks": 12,
      "created_at": "2026-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "version": "1.0.0",
    "timestamp": "2026-03-16T00:00:00Z",
    "requestId": "uuid",
    "pagination": { "page": 1, "limit": 20, "total": 500, "hasMore": true }
  }
}
```

---

## GET /agents/{chainId}/{tokenId}

Retrieve full details for a specific agent.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `chainId` | integer | Blockchain network chain ID |
| `tokenId` | integer | Agent token ID on the Identity Registry |

### Response

Returns the complete agent profile including:
- Identity: name, description, image, agentURI, owner
- Services: MCP, A2A, ENS, DID, email, web endpoints
- Reputation: `total_score`, `star_count`, `total_feedbacks`
- Metadata: skills, domains, x402, custom fields
- On-chain: chain ID, token ID, owner, creation timestamp

---

## GET /agents/search

Semantic and keyword search for agents.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | **required** | Search query |
| `limit` | integer | 20 | Results per page (1-100) |
| `chainId` | integer | — | Filter by chain |
| `semanticWeight` | float | 0.5 | Balance between keyword (0) and semantic (1) search |

### Notes

- `semanticWeight=0` → pure keyword matching
- `semanticWeight=1` → pure semantic/embedding search
- `semanticWeight=0.5` → balanced (default)

---

## GET /accounts/{address}/agents

List agents owned by a wallet address.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `address` | string | Wallet address matching `^0x[a-fA-F0-9]{40}$` |

### Response

Array of agent summaries owned by the address. Same structure as `/agents` list items.

Query parameters: `page`, `limit`, `sortBy`, `sortOrder`.

---

## GET /stats

Global platform statistics.

### Response

```json
{
  "success": true,
  "data": {
    "total_agents": 5000,
    "total_users": 1200,
    "total_feedbacks": 15000,
    "total_validations": 30
  }
}
```

---

## GET /chains

List all blockchain networks supported by 8004scan.

The frontend OpenAPI schema describes `data` as an array. Current live responses may also wrap the list under `data.chains` (or `data.data.chains` if an extra response envelope is present). Use a defensive selector when scripting:

```bash
jq '.data.chains // .data.data.chains // .data'
```

### Response

```json
{
  "success": true,
  "data": [
    {
      "chain_id": 1,
      "name": "Ethereum Mainnet",
      "is_testnet": false,
      "explorer_url": "https://etherscan.io"
    }
  ]
}
```

---

## GET /feedbacks

Paginated list of feedback entries.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number (1-indexed) |
| `limit` | integer | 20 | Results per page (1-100) |
| `chainId` | integer | — | Filter by chain ID |
| `tokenId` | integer | — | Filter by token ID (requires chainId) |
| `minScore` | integer | — | Minimum score filter (0-5) |
| `maxScore` | integer | — | Maximum score filter (0-5) |

---

## Error Responses

All errors follow a consistent format:

```json
{
  "success": false,
  "error": {
    "code": "BadRequest",
    "message": "Invalid chainId parameter",
    "details": { "param": "chainId", "received": "abc" }
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|------------|-------------|
| `BadRequest` | 400 | Invalid parameters |
| `NotFound` | 404 | Agent/resource not found |
| `RateLimitExceeded` | 429 | Rate limit hit |
| `InternalError` | 500 | Server error |
