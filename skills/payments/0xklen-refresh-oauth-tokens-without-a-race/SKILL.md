---
name: refresh-oauth-tokens-without-a-race
description: Use when a client holds OAuth access tokens. Refresh before expiry behind a lock, persist rotated refresh tokens atomically, and handle the 401-then-retry path exactly once.
---

# Refresh OAuth tokens without a race

A token refresh implemented naively misfires three ways: it fires once per concurrent request,
it loses a rotated refresh token, or it loops forever on a dead grant.

## Procedure

1. Store expiry as absolute UTC `expires_at`, not a countdown, and refresh when `now >= expires_at - 60s`.
2. Single-flight the refresh so N concurrent 401s trigger one token request, not N:
   ```python
   import threading, time
   _lock, _access, _expiry = threading.Lock(), None, 0.0
   def token():
       with _lock:
           if time.time() < _expiry - 60: return _access
           return _refresh()  # sets _access/_expiry
   ```
3. When the provider rotates refresh tokens (returns a new `refresh_token`), persist the new one before dropping the old — the old dies immediately on rotation.
4. On a business-call 401: refresh once and retry that call once. A second 401 means the grant is dead — surface it, do not loop.
5. Store tokens at `chmod 600 ~/.config/app/token.json` or in a secret store, never in logs or the repo.
6. Treat `invalid_grant` (re-auth required, human) distinctly from 5xx (retry with backoff).

## Pitfalls

- Two processes each refreshing a rotating token invalidate each other; coordinate via the store's advisory lock.
- Comparing local naive time to a server `expires_in` across timezones shifts expiry; do all maths in UTC.
- Retrying every request N times on 401 turns an auth outage into a self-inflicted burst.
- `expires_in` is usually seconds but some providers send milliseconds — check the unit.
- Logging the token on a refresh failure leaks credentials into your log aggregator.

## Verification

    curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $ACCESS" "$API/v1/me"

200 means the token path works; a persistent 401 means the refresh logic is broken. Report the token's `expires_at` and that a 401 cycle refreshed exactly once.
