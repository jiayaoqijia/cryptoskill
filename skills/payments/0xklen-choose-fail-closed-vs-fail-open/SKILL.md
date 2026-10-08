---
name: choose-fail-closed-vs-fail-open
description: Use when a guard, authz check or feature gate can error, and you must decide per call site whether an error denies the action or allows it — because the default picks the failure mode for you.
---

# Choose fail-closed vs fail-open

When a policy service, config fetch or feature-flag lookup errors, the code does *something*. If that something is not a deliberate choice, you have chosen the dangerous branch by accident. Decide per call site, write the decision down, and make the fallback explicit.

## Procedure

1. Enumerate every place a check can fail: auth/authz middleware, key lookups, schema validation, rate-limit counters, feature flags, secrets fetch. For each, ask what the worst case is if it wrongly *allows* versus wrongly *denies*.

2. Fail **closed** when allowing the action is hard or impossible to reverse and denying merely degrades a feature: authentication, authorisation, payments, destructive writes, data exports, admin endpoints. Return `403`, not `200`, when the policy engine is unreachable:
       allowed, err := policy.Check(ctx, principal, action)
       if err != nil {
         return errFailClosed   // never `return true` on error
       }

3. Fail **open** only when denying breaks the core path and allowing exposes nothing new: cached read replicas, a non-critical recommendation panel, telemetry, a cosmetic flag. Serve the previously-known-good value and record a metric:
       v, err := flag.Get(ctx, "new-ui")
       if err != nil { v = lastKnownGood; metrics.Inc("flag.fetch_error") }

4. Write the decision into the code as a named constant so reviewers can see it, and never let a language default decide. A bare `if err != nil { allowed = true }` is the classic accidental fail-open — the reviewer cannot tell if it was intended.

5. For secrets and keys, always fail closed *and refuse to start*. A service that boots with an empty signing key and signs nothing valid is worse than one that refuses to boot:
       if len(signingKey) == 0 { log.Fatal("SIGNING_KEY missing; refusing to start") }

6. Add a timeout to every check so "fail closed" cannot become "hang forever": `ctx, cancel := context.WithTimeout(ctx, 250*time.Millisecond)`. A check that blocks holds the request open and turns a policy outage into a site-wide latency outage.

7. Record the fallback path in metrics and logs with a distinct reason (`policy_unreachable`, `flag_stale`) so you can tell a real deny from an infrastructure failure during an incident.

## Pitfalls

- Treating all checks as the same: one fail-open helper reused for both a rate limiter (safe to open) and an authz gate (must close).
- Fail-closed on a hot read path with no timeout, so the policy outage propagates as a full latency outage.
- Caching a *deny* from a transient policy failure for the full TTL, locking out legitimate users long after the policy service recovered.
- A feature flag reader that panics on a missing flag instead of returning the coded default — a config typo becomes a crash loop.

## Verification

    # kill the policy service, then probe each guarded endpoint
    docker stop policy-svc
    curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/admin/export   # expect 403 / 503
    curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/recommend     # expect 200 (fail-open)
    grep -R "err != nil" internal/authz | grep -n "true"                    # expect no accidental allow

Report: a table of each check, its chosen failure mode, the code path that implements it, and a live probe showing the guard denies (403/503) with the policy service down while the cosmetic path still serves.
