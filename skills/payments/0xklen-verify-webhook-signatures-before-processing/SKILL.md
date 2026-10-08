---
name: verify-webhook-signatures-before-processing
description: Use when you receive webhooks. Verify the HMAC signature over the exact raw body with a constant-time compare and reject replays — an unverified webhook is an unauthenticated write.
---

# Verify webhook signatures before processing

A webhook endpoint is a public URL that triggers writes. Without signature verification, anyone
who learns the URL can forge events. Verify first, process second.

## Procedure

1. Capture the raw request body bytes before any JSON parsing; re-serialising changes whitespace and breaks the signature.
2. Read the signature header per provider: Stripe `Stripe-Signature`, GitHub `X-Hub-Signature-256`, generic `X-Signature`.
3. Compute HMAC-SHA256 over the raw body and compare in constant time:
   ```python
   import hmac, hashlib
   expected = hmac.new(SECRET, raw_body, hashlib.sha256).hexdigest()
   if not hmac.compare_digest(expected, got):
       return Response(status=401)
   ```
4. Support the provider's timestamp scheme (Stripe `t=...,v1=...`) and reject events older than a tolerance (~5 min) to block replay.
5. Use `hmac.compare_digest`, never `==`.
6. Confirm the secret is the endpoint's signing secret, not the API key.
7. Return 2xx fast and process asynchronously; a slow handler makes the provider retry.

## Pitfalls

- Parsing JSON then re-encoding to verify changes key order and always fails; verify the raw bytes.
- `==` on strings is timing-attackable; use `compare_digest`.
- Skipping the timestamp check lets an attacker replay an old, valid event.
- Accepting the request before verifying (verifying later) is a race; verify first.
- During secret rotation try both secrets, then treat a match on either as valid.

## Verification

    curl -s -X POST localhost:3000/hook -H "X-Signature: deadbeef" -d '{}' -o /dev/null -w '%{http_code}\n'

Expect 401 for a bad signature and 200 for a correctly signed body. Report: "Rejected 3 unsigned deliveries; 42 signed events processed."
