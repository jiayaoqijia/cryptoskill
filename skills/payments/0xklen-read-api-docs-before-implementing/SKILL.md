---
name: read-api-docs-before-implementing
description: Use when integrating an unfamiliar API. Read the reference for auth, pagination, rate limits, error taxonomy, and deprecations before writing the first request.
---

# Read the API docs before implementing

Guessing an API's shape from one sample response produces code that breaks on page two, the
first 429, or the first nullable field. Extract the contract from the reference first.

## Procedure

1. Pull the machine-readable spec, not just the HTML page. OpenAPI is the contract:
   ```bash
   curl -s "$BASE/openapi.json" -o /tmp/api.json
   jq '.paths | keys' /tmp/api.json
   ```
2. Read six sections in order and write each down: auth scheme, base URL per environment, pagination style, rate limits, error format, deprecation policy.
3. Read pagination literally. Record cursor (`next_cursor`, opaque), offset/limit, or link-header. You cannot design the loop without this.
4. Note the stated quota and the headers that report it (`X-RateLimit-Remaining`, `Retry-After`).
5. Run one real example request against the sandbox before writing code:
   ```bash
   curl -s -H "Authorization: Bearer $TOKEN" "$SANDBOX_BASE/v1/ping" | jq .
   ```
6. Grep the spec for `deprecated` and versioned paths (`/v1/`, `/v2/`) so you build on the current version.
7. List every field not in `required` and every `nullable: true` field — those crash naive parsers.
8. Record the docs URL and spec hash in the module docstring so the next reader knows the target contract.

## Pitfalls

- SDK README examples are often the oldest, not the newest; the spec is authoritative on fields.
- "1000/hour" without a burst number misleads — the burst is what trips the first 429.
- Cursor tokens are opaque: never parse, sort, or construct them. Treat as `str` only.
- A field you saw in one response is not contract; it can vanish without a major bump.
- A docs URL saying v2 and a spec `version: 1.0.0` can disagree; trust the spec `version`.

## Verification

    jq -e '.paths and .components.securitySchemes' /tmp/api.json >/dev/null && echo "spec parsed"

Report the base URLs per environment, the pagination style, the stated quota, and the docs URL/hash you built against.
