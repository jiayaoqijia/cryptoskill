---
name: budget-retries-across-a-request-chain
description: Use when a request fans out through several services or a service mesh and retries multiply, turning one slow dependency into a traffic storm. Give the whole chain one deadline and one retry budget instead of retrying independently at every hop.
---

# Budget retries across a request chain

Independent retries compose multiplicatively. Three hops each retrying three times is 27 attempts at
the tail, and every one inherits the original timeout — a small failure becomes an overload. Bound the
chain, not each hop.

## Procedure

1. Define one end-to-end deadline at the entry point and pass the remaining budget downstream:
   ```python
   deadline = time.monotonic() + 2.0        # total for the whole chain
   remaining = max(0, deadline - time.monotonic())
   resp = client.get(url, timeout=remaining)
   ```
2. Propagate the deadline as a header so downstream hops inherit it:
   ```bash
   curl -H 'X-Request-Deadline: 1699999999' https://svc.internal/v1/work
   ```
   Each hop computes `max(0, deadline - now)` and uses that for its own calls.
3. Allow retries only at the layer closest to the caller, never at every hop:
   - Only the edge retries; internal services return the error up.
   - If an internal hop must retry, it re-checks the deadline first and gives up when the budget is spent.
4. Cap retries per request, not per hop, and use one timeout value shared across the chain:
   ```yaml
   # envoy: retry budget instead of unbounded retries
   retry_policy:
     retry_on: "5xx,reset"
     num_retries: 2
     per_try_timeout: 0.5s
     retry_budget: { budget_percent: { value: 20 } }
   ```
5. Never retry non-idempotent calls (POST that charges a card) without an idempotency key.
6. Measure amplification: total backend attempts / total frontend requests. It should stay near 1.
   ```bash
   # compare request counts across tiers in Prometheus
   rate(http_requests_total{service="backend"}[5m]) / rate(http_requests_total{service="edge"}[5m])
   ```
7. Shed load when the budget is exhausted rather than queueing: return `503` immediately.

## Pitfalls

- Nested timeout constants stack: each hop's `timeout=30s` means the chain can exceed 90 s while the client gave up at 5 s.
- Retrying at every hop multiplies load exactly when the dependency is already struggling.
- A retry that ignores the deadline keeps firing after the caller has gone, wasting capacity.
- Retries without jitter synchronise and create thundering-herd bursts (see the backoff skills).
- Retrying 5xx without checkout of idempotency double-charges or double-creates.
- A service mesh's default `num_retries: 3` applies silently to every route and is easy to forget.
- Retrying the request that timed out at the *client* while the server still processes it duplicates work.

## Verification

    # amplification should hover near 1.0, not 3.0
    rate(http_requests_total{service="backend"}[5m]) / rate(http_requests_total{service="edge"}[5m])

Pass means amplification stays under ~1.3 under normal load and the chain fails fast when the deadline
expires. Report: "single 2 s deadline propagated; retries only at edge; amplification 1.05."
