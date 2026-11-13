---
name: sessions-tokens
domain: security-hardening/sessions-tokens
trigger: "Managing authenticated state over time: session IDs and cookies, JWT design and verification, OAuth/OIDC flows, API keys and webhook signatures."
anti_trigger: "Choosing or verifying the user's authentication factor (subskills/authentication.md); deciding what the user may access (subskills/authorization.md)."
scope: "Session IDs, JWT/OAuth tokens, expiry, rotation, logout"
status: "seedling"
---

# Sessions and Tokens

## Standard

- OWASP Session Management Cheat Sheet: cookies set `Secure`, `HttpOnly`, `SameSite=Strict` (Lax acceptable; never `None` without `Secure`); `__Host-` prefix; idle timeout 2–5 minutes for high-value applications, 15–30 for low-risk; absolute timeout 4–8 hours; regenerate the session ID after any privilege-level change, above all at login; ≥64 bits entropy from a CSPRNG, ≥128 recommended.
- OWASP JSON Web Token Cheat Sheet opens with a "Not using JWTs" section: server-side sessions with opaque tokens for browser apps, because JWTs are hard to revoke.
- OAuth 2.1 (`draft-ietf-oauth-v2-1-13`, May 2025) removes the implicit and Resource-Owner-Password-Credentials grants; RFC 9700 (BCP 240, Jan 2025) makes PKCE and exact redirect-URI matching normative.
- Standard Webhooks (standardwebhooks.com): verify the signature over the raw body, `webhook-id`, `webhook-timestamp`, `webhook-signature` (`v1,<HMAC-SHA256>` over `id.timestamp.body`), 5-minute tolerance, constant-time compare, dedupe on `webhook-id`.
- ASVS 5.0 V7 Session Management, V9 Self-contained Tokens, V10 OAuth & OIDC.

## Decision rules

1. Default to opaque tokens plus a server-side lookup for browser sessions: revocation is free.
2. Use JWTs only where stateless verification is genuinely required; treat them as signed but not confidential (JWE when the payload is secret).
3. Verify every JWT: signature, an algorithm allow-list, `iss`, `aud`, `exp`. Never trust `jku`/`jwk`/`kid` header material.
4. API keys: high-entropy, hashed at rest, scoped, prefixed for detection, rotatable, revocable. One key per service and environment.
5. OAuth/OIDC: exact callback URLs (no wildcards), PKCE everywhere, `state`/`nonce` validated, ID token's signature, issuer, audience, expiry and nonce checked server-side.
6. A `localStorage` token is an XSS-readable token; prefer an `HttpOnly` cookie.

## Procedure

1. Use the framework's session middleware; set the three cookie flags and the `__Host-` prefix.
2. Regenerate the session ID at login, password change and any role change; destroy the old ID.
3. Set idle and absolute timeouts to the cheat-sheet figures; never set custom timeouts higher.
4. For JWTs, pin `algorithms` in verification, e.g. `jwt.verify(token, key, { algorithms: ['RS256'] })`; rotate keys on schedule.
5. Register exact redirect URIs; adopt a maintained OIDC library (or a managed IdP) rather than hand-rolling the flow.
6. Verify webhook signatures over the raw body before parsing; reject replays by timestamp; dedupe on the event ID.

## Anti-patterns

- Storing access tokens in `localStorage`/`sessionStorage`.
- Accepting `alg: none` or trusting the token's named key material.
- Wildcard or loosely-matched redirect URIs — open redirectors that leak codes and tokens.
- Checking token expiry only on the client.
- Trusting an unsigned webhook body, or parsing JSON before verifying the signature.

## Done checklist

- [ ] Session cookies carry `Secure`, `HttpOnly`, `SameSite` and the `__Host-` prefix.
- [ ] Session ID regenerated at every privilege change.
- [ ] Idle and absolute timeouts set to the guidance.
- [ ] JWT verification pins the algorithm and checks `iss`/`aud`/`exp`.
- [ ] OAuth callbacks are exact; PKCE and `state`/`nonce` enforced.
- [ ] Webhook signatures verified over the raw body with replay rejection.

## Sources

- Primary: OWASP Session Management, JSON Web Token, OAuth2 Cheat Sheets; OAuth 2.1 draft-13; RFC 9700; RFC 8705; Standard Webhooks; OWASP ASVS 5.0 V7/V9/V10.
- <https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>
- <https://pages.nist.gov/800-63-3/sp800-63b.html>
