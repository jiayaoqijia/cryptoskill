---
name: api-security
domain: security-hardening/api-security
trigger: "Hardening an HTTP or GraphQL API against the OWASP API Security Top 10: object authorisation, authentication, consumption limits, inventory and unsafe consumption."
anti_trigger: "Access logic in general (subskills/authorization.md); token design and verification (subskills/sessions-tokens.md); outbound SSRF (subskills/ssrf.md)."
scope: "API Security Top 10 2023: BOLA, mass assignment, resource consumption"
status: "seedling"
---

# API Security

## Standard

- OWASP API Security Top 10 **2023** is the current and only official edition — no 2024/25/26 edition exists (https://owasp.org/API-Security/editions/2023/en/0x04-release-notes). Any "API Top 10 2025" is vendor commentary.
- RFC 9700 (BCP 240, Jan 2025): PKCE on every authorization-code flow, exact redirect-URI matching, no implicit or ROPC grants. Service-to-service: mTLS (RFC 8705) or per-service scoped tokens, never a shared root key.
- OWASP GraphQL Cheat Sheet: disable introspection and GraphiQL in production; cap query depth and amount; cost analysis, timeouts and rate limiting; watch batching attacks.
- Standard Webhooks for inbound integrations (signature over the raw body, timestamped, deduplicated).

## Decision rules

1. API1 BOLA: per-object policy check on every ID-based access (subskills/authorization.md) — the same root cause as Top 10 A01.
2. API4 Unrestricted Resource Consumption: nothing in IT is limitless. Put a cap on every input (string length, array elements, upload size) and every behaviour.
3. Rate-limit per client and per timeframe, tuned per endpoint; throttle per-operation repeats (OTP validation, password recovery) — these are the denial-of-wallet endpoints.
4. Validate page-size and record-count parameters server-side; never trust a client-requested limit.
5. Set spending limits (or billing alerts) on paid third-party APIs.
6. API9 inventory: one source of truth (the OpenAPI spec), version in the path, a sunset date for every old version. Shadow endpoints are the ones with no auth and no limit.
7. API10: treat third-party responses and webhook bodies as untrusted input (subskills/input-output.md).

## Procedure

1. Inventory every endpoint from the OpenAPI spec; flag undocumented routes.
2. Per route: authentication, then server-side authorisation, then input schema, then consumption limits.
3. Add rate limits per client (IP and account) with a burst allowance, strictest on auth, reset and OTP endpoints.
4. Cap payloads, page sizes and array counts; return a clear 4xx on violation.
5. For GraphQL: disable introspection and GraphiQL in production, cap depth and amount, add cost analysis and timeouts.
6. For webhooks: verify the signature over the raw body, reject replays by timestamp, dedupe on the event ID, then parse.
7. For outbound calls to third parties: per-integration scoped credentials, response validation, spending caps.

## Anti-patterns

- Unlimited endpoints, especially password reset and OTP validation.
- Client-supplied page size honoured without a server cap.
- One long-lived shared API key for every integration.
- A GraphQL endpoint with introspection, unlimited depth and no cost analysis in production.

## Done checklist

- [ ] Every endpoint inventoried from the spec; shadow routes removed or documented.
- [ ] Auth, authorisation, input schema and limits defined per route.
- [ ] Rate limits per client and account, tightest on auth flows.
- [ ] Payload, page-size and array caps enforced.
- [ ] GraphQL: introspection off, depth/amount/cost/timeout limits on.
- [ ] Webhooks signature-verified before parsing; replays rejected.
- [ ] Third-party API spending capped or alerted.

## Sources

- Primary: OWASP API Security Top 10 2023 (API1, API4, API9, API10); RFC 9700; RFC 8705; OWASP GraphQL Cheat Sheet; Standard Webhooks.
- <https://owasp.org/API-Security/>
- <https://cheatsheetseries.owasp.org>
