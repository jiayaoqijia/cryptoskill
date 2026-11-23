---
name: api-key-verification
description: "Identify pasted API keys by prefix and verify liveness."
---

# API Key Identification & Verification

Use when: the user pastes an API key/token and asks "what is this?", "is this valid?", "whose account is this?". Goal: identify the provider from the key's prefix, verify it is live, and report usage/limits/ownership — without printing the secret.

## Steps

1. Identify the provider from the key prefix. Index: `references/providers.md`. Prefix alone is not identity for generic prefixes (many providers use `sk-`); confirm with a metadata call.
2. Probe the provider's read-only metadata/credits endpoint with the key as a Bearer token. These calls have no side effects — never "test" a key against a state-mutating endpoint (no setWebhook-style calls just to check). When no metadata endpoint exists, verify with the single cheapest metered call the provider sells (Exa: `type: lite`, `numResults: 1`, one query), say what that probe cost, and read 401 vs 200 — see `references/providers.md`.
3. Report: valid? label, expiry, spend limit, usage, remaining credits, creator id. Never echo the full key in your reply — it is already in the transcript, don't amplify it; refer to it as `<prefix>…<last4>`. When the balance is unreadable (service-key-only admin API), say so plainly instead of inventing a number.
4. Warn when a live credential was pasted into chat: it is now also in the session store (`~/.hermes/state.db`) and the agent log (`~/.hermes/logs/agent.log`), not just the shell history — offer to scrub those rows or to rotate the key at the provider's keys page.

## Pitfalls

- A default/masked label (the key itself truncated) means the owner never named the key — not that it's fake.
- No prefix is not "no provider": bare UUIDs are real keys for search/retrieval APIs (Exa), and the auth header may be `x-api-key` rather than `Bearer` — check the vendor's own curl sample before concluding the key is malformed.
- Google API keys are not always `AIza…`: the current Stitch/Studio key format is `AQ.…` and is sent as
  the `X-Goog-Api-Key` header, never as a Bearer token. Probe `https://stitch.googleapis.com/mcp` with a
  JSON-RPC `initialize` + `tools/list` POST to prove it live.
- Read the Google error code as state, not as invalidity: `403 API has not been used in project N … or
  it is disabled` means the key is **valid** for that project and only the API is off — say that, and
  name the project number. `401 Request had invalid authentication credentials` when the same key is
  sent as `Authorization: Bearer` means you used the wrong header, not that the key is dead.
- Never store the key yourself by echoing it back into a command line that a log or shell history will keep; write it to the credential file from a variable and confirm only with a masked check (`grep -c '^KEY_NAME='`, `stat -c '%A'`).
- Usage figures are in USD.
- 401 from the metadata endpoint = invalid or revoked. Say so; don't retry-hammer.
- `limit: null` = no spend cap set; `expires_at: null` = no expiry. Both are normal, not anomalies.

## Verified example: OpenRouter (`sk-or-v1-`)

```bash
curl -s https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $KEY"
# → label, is_management_key, limit, usage (lifetime/daily/weekly/monthly, USD),
#   is_free_tier, expires_at, creator_user_id
curl -s https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $KEY"
# → total_credits, total_usage  (no account email in the 2026-08 response)
```

Prefix index for other providers: `references/providers.md`.
