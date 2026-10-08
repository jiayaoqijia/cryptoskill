---
name: shed-load-before-saturation
description: Use when overload slows every request including healthy ones — reject or degrade the lowest-value work early with admission control instead of queueing it all.
---

# Shed load before saturation

When demand exceeds capacity, admitting every request means everyone waits: p99 runs away and even trivial requests time out. Rejecting a fraction early keeps the served requests fast. Shedding is a feature, not a failure.

## Procedure

1. Classify cheap versus expensive work: health checks, static assets, and cached reads must never be shed; expensive uncached queries, report generation, and fan-outs are shed first.
2. Add admission control on the scarce resource (in-flight count or a token bucket), not on global request rate:
```python
try:
    await asyncio.wait_for(SEM.acquire(), timeout=0.001)
except asyncio.TimeoutError:
    return Response(status_code=503, headers={"Retry-After": "1"})
```
3. Set the limit from measured capacity: the concurrency at which p99 crosses the SLO under normal load, minus margin.
4. Return a fast, honest failure — `503` with `Retry-After`, never a slow `200` or an indefinite wait — so clients with retry/backoff reduce pressure automatically.
5. Prefer priority shedding to random shedding: tag requests by class (interactive vs batch) and shed batch first, keeping a small reserve for critical traffic.
6. Degrade before shedding where possible: serve a cached or partial response, drop a non-essential section, skip personalization — cheaper than refusing outright.
7. Fault-inject the shed path; a branch that has never run will carry a bug when it first does.

## Pitfalls

- Shedding on rate without a concurrency cap, so a burst of slow requests still overwhelms.
- Returning an upstream's 5xx as your own without shedding, propagating overload downstream.
- Shedding health checks or load-balancer probes, so the orchestrator marks the instance unhealthy and removes it, making things worse.
- No `Retry-After` or a zero backoff, so clients retry immediately and amplify the storm.
- A hard limit set above the true knee, so shedding never triggers before collapse.
- Shedding without a metric, so the operator cannot see how much traffic is being refused.

## Verification

    hey -z 60s -c 200 -q 200 http://localhost:8080/expensive
    curl -s localhost:9090/metrics | grep -E "shed_total|inflight_requests"
    # pass: sheddable requests get fast 503s; non-sheddable p99 stays within SLO

Report the admission limit, which work is subject to shedding, the response code and `Retry-After`, and the p99 of non-sheddable traffic under overload.
