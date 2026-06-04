# 8004scan API — curl Examples

All examples use `jq` for JSON formatting. Set `EIGHTSCAN_API_KEY` for authenticated requests.

## List Agents

```bash
# List first 20 agents (default)
curl -s "https://8004scan.io/api/v1/public/agents" | jq .

# With API key
curl -s "https://8004scan.io/api/v1/public/agents" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Filter by chain (Base Mainnet)
curl -s "https://8004scan.io/api/v1/public/agents?chainId=8453&limit=50" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Filter by owner
curl -s "https://8004scan.io/api/v1/public/agents?ownerAddress=0x1234567890abcdef1234567890abcdef12345678" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Sort by most recent
curl -s "https://8004scan.io/api/v1/public/agents?sortBy=created_at&sortOrder=desc&limit=10" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Sort by highest reputation
curl -s "https://8004scan.io/api/v1/public/agents?sortBy=total_score&sortOrder=desc&limit=10" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Paginate (page 2)
curl -s "https://8004scan.io/api/v1/public/agents?limit=20&page=2" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .
```

## Get Agent Details

```bash
# Agent on Ethereum Mainnet (chain 1, token 42)
curl -s "https://8004scan.io/api/v1/public/agents/1/42" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Agent on Base (chain 8453, token 17)
curl -s "https://8004scan.io/api/v1/public/agents/8453/17" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Agent on Sepolia testnet
curl -s "https://8004scan.io/api/v1/public/agents/11155111/7" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .
```

## Search Agents

```bash
# Keyword search
curl -s "https://8004scan.io/api/v1/public/agents/search?q=code+review" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Semantic search (weight toward meaning)
curl -s "https://8004scan.io/api/v1/public/agents/search?q=help+me+debug+python&semanticWeight=0.8" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Keyword-only search
curl -s "https://8004scan.io/api/v1/public/agents/search?q=defi+trading&semanticWeight=0" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Search on specific chain
curl -s "https://8004scan.io/api/v1/public/agents/search?q=translation&chainId=8453&limit=5" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Extract just names and descriptions
curl -s "https://8004scan.io/api/v1/public/agents/search?q=code+review" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq '.data[] | {name, description, chain_id, token_id}'
```

## Account Agents

```bash
# List all agents owned by a wallet
curl -s "https://8004scan.io/api/v1/public/accounts/0x1234567890abcdef1234567890abcdef12345678/agents" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .
```

## Platform Stats

```bash
# Global statistics
curl -s "https://8004scan.io/api/v1/public/stats" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# Extract specific stats
curl -s "https://8004scan.io/api/v1/public/stats" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq '.data | {total_agents, total_users, total_feedbacks, total_validations}'
```

## Supported Chains

```bash
# List all supported chains
curl -s "https://8004scan.io/api/v1/public/chains" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# List chain names and IDs
curl -s "https://8004scan.io/api/v1/public/chains" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq '(.data.chains // .data.data.chains // .data)[] | {name, chain_id, is_testnet}'
```

## Feedbacks

```bash
# Recent feedbacks
curl -s "https://8004scan.io/api/v1/public/feedbacks?limit=10" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .

# High-rated feedbacks only
curl -s "https://8004scan.io/api/v1/public/feedbacks?minScore=4&limit=20" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq .
```

## Scripting Patterns

```bash
# Count agents per chain
curl -s "https://8004scan.io/api/v1/public/chains" \
  -H "X-API-Key: $EIGHTSCAN_API_KEY" | \
  jq -r '(.data.chains // .data.data.chains // .data)[].chain_id' | while read cid; do
    total=$(curl -s "https://8004scan.io/api/v1/public/agents?chainId=$cid&limit=1&page=1" \
      -H "X-API-Key: $EIGHTSCAN_API_KEY" | jq '.meta.pagination.total')
    echo "Chain $cid: $total agents"
  done

# Export all agents to JSONL
page=1
while true; do
  batch=$(curl -s "https://8004scan.io/api/v1/public/agents?limit=100&page=$page" \
    -H "X-API-Key: $EIGHTSCAN_API_KEY")
  echo "$batch" | jq -c '.data[]'
  total=$(echo "$batch" | jq '.meta.pagination.total')
  limit=$(echo "$batch" | jq '.meta.pagination.limit')
  has_more=$(echo "$batch" | jq -r '.meta.pagination.hasMore')
  [ "$has_more" != "true" ] && break
  page=$((page + 1))
  sleep 1  # Respect rate limits
done > agents.jsonl
```
