# API key prefix index

## Verified in practice (2026-08)

| Prefix | Provider | Read-only verification endpoint |
|--------|----------|--------------------------------|
| `sk-or-v1-` | OpenRouter | GET `https://openrouter.ai/api/v1/auth/key` → label, is_management_key, limit (spend cap, USD), usage (lifetime/daily/weekly/monthly), is_free_tier, expires_at, creator_user_id. Also GET `https://openrouter.ai/api/v1/credits` → total_credits, total_usage (no account email in the 2026-08 response). Bearer auth. |

## UUID-format keys (no telltale prefix)

A bare UUIDv4 (`91c31ab9-…`) is *not* an identifier for nothing — several search/retrieval APIs use UUID keys (Exa is one). Do not conclude "unknown provider" from the absence of a prefix; ask or probe candidate providers' auth with a single cheap call.

| Format | Provider | Verification |
|--------|----------|--------------|
| UUIDv4 | Exa | `curl -s -o /tmp/k.json -w '%{http_code}' -X POST https://api.exa.ai/search -H "x-api-key: $KEY" -H 'Content-Type: application/json' -d '{"query":"test","numResults":1,"type":"lite"}'` → 200 = live, 401 = invalid/revoked. Header is `x-api-key`, not Bearer. There is NO usable metadata/credits endpoint on the normal key: `GET /usage`, `/teams`, `/whoami` all 404. Balance lives behind the admin API (`https://admin-api.exa.ai/team-management/api-keys/{id}/usage`), which needs a service-account key the team owner must create — say you cannot read the balance rather than guessing it. |

## Widely documented formats (confirm against provider docs before relying)

| Prefix | Provider |
|--------|----------|
| `sk-ant-` | Anthropic |
| `sk-proj-` / `sk-svcacct-` | OpenAI (project / service-account keys) |
| `sk-` bare (48+ chars, no suffix) | OpenAI (legacy) — ambiguous, verify |
| `ghp_` / `gho_` / `github_pat_` | GitHub (classic PAT / OAuth / fine-grained PAT) |
| `xai-` | xAI |
| `gsk_` | Groq |
| `AIza...` | Google (API key) |

Generic `sk-` prefixes are shared by many providers — prefix alone is never
identity; always confirm with the provider's metadata endpoint when one
exists.
