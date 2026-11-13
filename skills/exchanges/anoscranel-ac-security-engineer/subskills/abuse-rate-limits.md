---
name: abuse-rate-limits
domain: security-hardening/abuse-rate-limits
trigger: "Exposing an endpoint that costs money, sends messages, grants accounts, or runs a business flow: login, signup, OTP, checkout, upload, LLM call."
anti_trigger: "What the log must record when a limit fires (subskills/security-logging.md); the API Top 10 in general (subskills/api-security.md)."
scope: "Rate limits, bot and credential-stuffing defence, quotas"
status: "seedling"
---

# Rate Limiting & Abuse

## Standard

- OWASP **Automated Threat Handbook — Web Applications, v1.30 (17 Mar 2026)**: 21 threats, OAT-001…OAT-021 (OAT-003 now "Cost-Inflation Fraud") (owasp.org automated-threats project).
- OWASP **API4:2023 Unrestricted Resource Consumption**: limit memory, CPU, restarts, file descriptors; cap all inputs; rate-limit per client per timeframe per endpoint; throttle per-operation repeats (OTP, password recovery); validate page-size; **spend limits on third-party APIs** (owasp.org/API-Security/editions/2023).
- ASVS 5.0: **V2.4.1 (L2)** anti-automation against excessive calls (exfiltration, quota exhaustion, DoS, costly resources).
- IETF **RateLimit headers** remain an Internet-Draft (`draft-ietf-httpapi-ratelimit-headers-11`, May 2026), not yet an RFC.
- Bot economics: booter storefronts run from **$19.99/month** — capacity is purchasable by anyone, so the defence is upstream capacity and edge absorption.

## Decision rules

1. Limit per **account** and per **IP** — either alone is bypassed (many IPs per attacker; many accounts per NAT).
2. Tune per endpoint: global limits break the product; per-operation limits stop the abuse. Reset and OTP endpoints are the denial-of-wallet target — a missing limit turns SMS cost into leverage.
3. Allow a burst, then throttle — strict per-request limits punish legitimate clients.
4. Decide the failure mode per endpoint: when the limit store is unreachable, fail open (availability) or fail closed (credential endpoints). ⚠️ House convention — record it in config comments.
5. CAPTCHA is a speed bump, not a control (OAT-009 CAPTCHA Defeat); MFA answers credential stuffing.

## Procedure

1. Inventory cost-bearing and state-changing endpoints: login, signup, password reset, OTP issue/validate, upload, webhook, LLM call, checkout.
2. Assign limits per endpoint per identity (user/API key) and per IP, with bursts; counters live in a shared store, not per-process memory.
3. Throttle **repeats of the same operation**: N password-reset requests per account per hour, regardless of source IP.
4. Bound payloads server-side: max body, array elements, page size, upload size, result size (`subskills/api-security.md`).
5. Add detection beside the limit: failed-login spikes per account and per IP, signup velocity, geographic spread — alert, do not just block; on anomalies, revoke sessions and force re-auth (`subskills/authentication.md`).
6. Put a CDN/edge in front of public HTTP for volumetric absorption (96.62% of measured network-layer attacks stay under 500 Mbps; 90.6% end within ten minutes — Cloudflare H1 2026 ⚠️). L7 floods have no flow field separating abusive from legitimate; the controls are edge cost, challenges, and the per-account limits.

## Anti-patterns

- One global requests-per-minute limit for the whole app; rate limiting only by IP behind a carrier NAT.
- No spend cap on an LLM feature (OWASP LLM10); a retained tool return re-metered once at 14,293× the first call (arXiv:2609.28585).
- "We have a CDN" with the origin IP still resolvable — direct-to-origin bypasses edge controls.

## Done checklist

- [ ] Cost-bearing endpoints inventoried; limited per account and per IP.
- [ ] Failure mode (open/closed) per endpoint; repeat throttles on reset/OTP flows.
- [ ] Same-operation repeat throttles on reset/OTP flows.
- [ ] Payload and page-size caps server-side; spend caps on LLM and third-party APIs.
- [ ] Auth-anomaly alerts wired with first actions; origin protected from direct-to-origin access.

## Sources

- Primary: OWASP Automated Threat Handbook v1.30; API4:2023; ASVS 5.0 V2.4; IETF RateLimit I-D -11; Cloudflare H1 2026 (⚠️); arXiv:2609.28585 (⚠️).
- <https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html>
- <https://owasp.org/Top10/>
