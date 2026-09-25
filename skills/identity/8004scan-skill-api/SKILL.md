---
name: 8004scan-skill-api
description: Query the 8004scan public API to discover, search, and analyze ERC-8004 AI agents registered on the blockchain. Covers agent listing, semantic search, agent details, account lookups, platform statistics, supported chains, and feedback queries. Consult this skill when the user wants to search for agents, browse the agent registry, check agent details on 8004scan, get platform stats, look up agents by owner address, query feedback scores, or integrate with the 8004scan API programmatically.
version: 1.0.0
allowed-tools: "Bash(curl:*) Bash(jq:*)"
tags:
  - 8004scan
  - erc-8004
  - api
  - identity
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - jq
      env:
        - EIGHTSCAN_API_KEY
    primaryEnv: EIGHTSCAN_API_KEY
    emoji: "🔍"
    homepage: https://8004scan.io/developers
---

# 8004scan — Agent Discovery API Skill

8004scan is the definitive platform for discovering and interacting with ERC-8004 compliant AI agents. This skill wraps the **8004scan Public API** for programmatic agent discovery, search, and analytics.

## Reference Map

| File | When to read |
|------|-------------|
| `{baseDir}/references/api-reference.md` | Full endpoint documentation, parameters, response schemas |
| `{baseDir}/references/authentication.md` | API key setup, rate limit tiers, headers |
| `{baseDir}/references/examples.md` | curl examples for every endpoint |

---

## Base URL

```
https://8004scan.io/api/v1/public
```

## Authentication

Optional `X-API-Key` header for elevated rate limits. Without a key, requests use anonymous tier (10 req/min, 100/day).

| Tier | Requests/Min | Daily Limit |
|------|-------------|-------------|
| Anonymous | 10 | 100 |
| Free API Key | 30 | 1,000 |
| Basic | 100 | 10,000 |
| Pro | 500 | 100,000 |
| Enterprise | 2,000 | Unlimited |

Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

If `EIGHTSCAN_API_KEY` is set, include it: `-H "X-API-Key: $EIGHTSCAN_API_KEY"`.

---

## Request Classification

1. **Search query** ("find agents that do X", "search for code review agents") → Search Agents endpoint.
2. **Agent detail** ("show agent 8453:17", "get agent details") → Get Agent endpoint.
3. **Browse query** ("list all agents", "agents on Base") → List Agents endpoint.
4. **Account query** ("what agents does 0x... own?") → Account Agents endpoint.
5. **Stats query** ("how many agents are registered?", "platform stats") → Stats endpoint.
6. **Chain query** ("which chains does 8004scan support?") → Chains endpoint.
7. **Feedback query** ("recent feedback", "feedback scores") → Feedbacks endpoint.
8. **Integration query** ("how to use the API?", "rate limits?") → Read `references/api-reference.md`.

---

## Endpoints Quick Reference

### 1. List Agents

```bash
curl -s "https://8004scan.io/api/v1/public/agents?limit=20&page=1" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .
```

**Parameters**: `page` (1-indexed, default 1), `limit` (1-100, default 20), `chainId`, `ownerAddress`, `search`, `protocol`, `sortBy`, `sortOrder`, `isTestnet`.

### 2. Get Agent Details

```bash
curl -s "https://8004scan.io/api/v1/public/agents/{chainId}/{tokenId}" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .
```

Returns full agent profile: name, description, endpoints, metadata, reputation, owner.

### 3. Search Agents

```bash
curl -s "https://8004scan.io/api/v1/public/agents/search?q=code+review&limit=10" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .
```

**Parameters**: `q` (search query), `limit`, `chainId`, `semanticWeight` (0-1, balance keyword vs semantic).

### 4. Account Agents

```bash
curl -s "https://8004scan.io/api/v1/public/accounts/{address}/agents" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .
```

Address format: `^0x[a-fA-F0-9]{40}$`. Returns agents owned by the wallet.

### 5. Platform Stats

```bash
curl -s "https://8004scan.io/api/v1/public/stats" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .
```

Global statistics: total agents, chains, feedbacks, recent activity.

### 6. Supported Chains

```bash
curl -s "https://8004scan.io/api/v1/public/chains" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq '.data.chains // .data.data.chains // .data'
```

Returns all blockchain networks supported by 8004scan.

### 7. Feedbacks

```bash
curl -s "https://8004scan.io/api/v1/public/feedbacks?limit=20" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .
```

**Parameters**: `page`, `limit`, `chainId`, `tokenId`, `minScore` (0-5), `maxScore` (0-5).

---

## Response Format

All responses follow a consistent structure:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "version": "1.0",
    "timestamp": "2026-03-16T00:00:00Z",
    "requestId": "uuid",
    "pagination": { "page": 1, "limit": 20, "total": 100, "hasMore": true }
  }
}
```

**Error responses**:
```json
{
  "success": false,
  "error": {
    "code": "RateLimitExceeded",
    "message": "Rate limit exceeded",
    "details": { ... }
  }
}
```

---

## Standard Patterns

### Pagination

List endpoints use 1-indexed `page` + `limit`. Default limit: 20, max: 100. To iterate:

```bash
# Page 1
curl -s "https://8004scan.io/api/v1/public/agents?limit=100&page=1" | jq .
# Page 2
curl -s "https://8004scan.io/api/v1/public/agents?limit=100&page=2" | jq .
```

### Filtering by Chain

Most endpoints accept `chainId` parameter to scope results to a specific network:

```bash
# Only Base Mainnet agents
curl -s "https://8004scan.io/api/v1/public/agents?chainId=8453" | jq .
```

### Combining Search with Filters

```bash
# Semantic search on Ethereum mainnet
curl -s "https://8004scan.io/api/v1/public/agents/search?q=defi+trading&chainId=1&semanticWeight=0.7" | jq .
```

### Error Handling

- **400 BadRequest** — Check query parameters
- **404 NotFound** — Verify chainId and tokenId exist
- **429 RateLimitExceeded** — Wait for `X-RateLimit-Reset`, or upgrade API tier
- **500 InternalError** — Retry after brief delay

---

## Examples

**Example 1: Discover agents**
User: "Find AI agents that do code review"
```bash
curl -s "https://8004scan.io/api/v1/public/agents/search?q=code+review&limit=10" | jq '.data'
```
→ Show results as table: Agent ID, Name, Chain, Description.

**Example 2: Agent details**
User: "Show me agent 8453:17"
```bash
curl -s "https://8004scan.io/api/v1/public/agents/8453/17" | jq '.data'
```
→ Display full profile with endpoints, reputation, owner.

**Example 3: Platform overview**
User: "How many agents are registered?"
```bash
curl -s "https://8004scan.io/api/v1/public/stats" | jq '.data'
```
→ Report total agents, active chains, feedback count.

**Example 4: Owner lookup**
User: "What agents does 0x1234...abcd own?"
```bash
curl -s "https://8004scan.io/api/v1/public/accounts/0x1234...abcd/agents" | jq '.data'
```
→ List all agents owned by the wallet address.

**Example 5: Chain exploration**
User: "Which chains does 8004scan support?"
```bash
curl -s "https://8004scan.io/api/v1/public/chains" | jq '.data.chains // .data.data.chains // .data'
```
→ List all supported blockchain networks with chain IDs.
