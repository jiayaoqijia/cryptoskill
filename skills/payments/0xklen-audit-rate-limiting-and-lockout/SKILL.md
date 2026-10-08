---
name: audit-rate-limiting-and-lockout
description: Use when login, OTP, password-reset, or search endpoints may be brute-forced or abused. Checks per-account and per-IP limits, spoofable client IPs, and enumeration leaks, then sets thresholds.
---

# Audit rate limiting and lockout

Rate limiting protects credentials, one-time codes, and expensive endpoints from being hammered.
The usual failure is a limit that exists but keys on a spoofable value, or a lockout that reveals
which accounts exist.

## Procedure

1. Identify the sensitive endpoints: login, OTP verify, password reset, registration, search, and
   any endpoint that calls a paid upstream.

       rg -n "def (login|verify_otp|reset_password|register|search)|/login|/otp|/reset" src/

2. Measure the current behaviour with a burst and read the status codes:

       for i in $(seq 1 30); do \
         curl -s -o /dev/null -w '%{http_code} ' -X POST https://app.example.com/login \
           -d 'user=victim@example.com&pass=wrong'$i; \
       done; echo

   Expect a shift to 429 after the configured threshold — not 30 consecutive 401s.

3. Find how the limiter keys the request. A limiter on `X-Forwarded-For` is bypassable if the app
   trusts the header from the client:

       curl -s -X POST https://app.example.com/login \
         -H 'X-Forwarded-For: 1.2.3.4' -d 'user=victim&pass=x' -o /dev/null -w '%{http_code}\n'

   Rotating that header must not reset the counter. Trust `XFF` only from the known proxy, and key
   limits on the resolved client IP plus the account.

4. Rate-limit per account (not only per IP) so a botnet with many IPs cannot spray one account.

5. Use exponential backoff or a token bucket rather than a hard lockout that an attacker can trigger
   to lock out real users (denial of service by lockout).

6. Check the reset/OTP flows for enumeration: differing responses or timing for "user exists" vs
   "does not". Compare response bytes and latency:

       for u in real@example.com missing@example.com; do \
         curl -s -o /dev/null -w "$u %{http_code} %{time_total}\n" \
           -X POST https://app.example.com/forgot -d "user=$u"; \
       done

7. Cap OTP attempts (e.g. 5 per code) and expire codes (e.g. 10 min); invalidate on success.

## Pitfalls

- A limit keyed only on IP lets one attacker burn a shared NAT IP and block legitimate users.
- Returning 200 "reset email sent" but a different body/timing still leaks account existence.
- In-memory counters reset on every deploy and are per-instance, so they never fire on a fleet.
- `Retry-After` missing forces clients to guess and hammer harder.
- A hard credential lockout is itself a DoS vector against known usernames.
- Limiting the POST but not the GET confirmation link leaves the token brute-forceable.

## Verification

    n=$(for i in $(seq 1 50); do curl -s -o /dev/null -w '%{http_code}\n' \
          -X POST https://app.example.com/login -H "X-Forwarded-For: 9.9.9.$i" \
          -d 'user=victim&pass=x'; done | rg -c '^429'); echo "429s under IP rotation: $n"

Pass: 429s appear even when `X-Forwarded-For` is rotated, and the "exists" vs "missing" cases are
indistinguishable in status, body, and timing. Report thresholds chosen, the key used, and the
enumeration result.
