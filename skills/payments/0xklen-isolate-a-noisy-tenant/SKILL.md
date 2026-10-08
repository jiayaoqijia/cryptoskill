---
name: isolate-a-noisy-tenant
description: Use when one customer's traffic or jobs slow or starve everyone else on shared infrastructure — applies per-tenant quotas, fair queuing and caps so one tenant cannot consume the shared pool.
---

# Isolate a noisy tenant

On shared infrastructure, the tenant that sends the most requests sets the latency for everyone. Fairness does not emerge on its own; it has to be enforced with per-tenant limits and a scheduler that cannot let one key monopolise a worker.

## Procedure

1. Attribute load before limiting: tag every request and job with `tenant_id` at the edge and propagate it through logs and metrics. Without attribution, "the site is slow" is unactionable. Confirm with a query:
       sum by (tenant) (rate(http_requests_total[5m])) / on() group_left sum(rate(http_requests_total[5m]))

2. Set two limits per tenant — a *rate* (requests/second) and a *burst* (concurrent in-flight) — using a token bucket keyed by tenant:
       bucket = f"rl:{tenant}:{route}"
       if redis.eval(token_bucket_lua, [bucket], [rate, burst, now]) == 0 { return 429, Retry-After }

3. Make queues fair with a *round-robin or weighted* scheduler over tenant queues, not one FIFO. A single FIFO lets one tenant with 100k enqueued jobs delay every other tenant behind them. Weight tiers (enterprise 8, free 1) so priority is explicit.

4. Cap the heavy jobs, not just HTTP: per-tenant concurrency for background work and per-tenant CPU/memory via Kubernetes `ResourceQuota` so a tenant's batch job cannot evict neighbours:
       apiVersion: v1; kind: ResourceQuota; spec: {hard: {requests.cpu: "4"}}

5. Give the largest tenants dedicated shards or deployments when the shared path cannot be made fair — isolation is cheaper than a scheduler that keeps a whale and a minnow apart.

6. Return `429` with `Retry-After` and a clear body ("rate limit: acme exceeded 100 req/s"), never a `500`. Throttling is a capacity statement, not a fault, and clients should back off rather than retry hard.

7. Alert on the *share* a single tenant takes of a shared resource (a top-N metric), so you see the noisy neighbour before it becomes an incident rather than after.

## Pitfalls

- A global rate limit with no per-tenant split: the tenant that floods is unaffected while everyone else is throttled by a limit they never hit.
- Limiting requests but not concurrency, so 10 slow requests per second from one tenant still occupy every worker slot.
- A FIFO work queue that lets one tenant's backlog delay all others — the classic noisy-neighbour in disguise.
- Returning `500` for a throttled request, which counts against the error SLO and sends clients into an aggressive retry loop.

## Verification

    # blast one tenant and confirm others stay within latency SLO
    hey -z 60s -c 200 -H 'X-Tenant: acme'  http://localhost:8080/api/search > /dev/null &
    curl -s -o /dev/null -w '%{http_code} %{time_total}\n' -H 'X-Tenant: globex' http://localhost:8080/api/search
    # acme gets 429s; globex stays 200 under its normal latency
    curl -s localhost:9090/metrics | grep 'http_429_total{tenant="acme"}'

Report: the per-tenant rate and concurrency caps, the scheduler fairness policy, and a load test where one tenant is throttled while a peer keeps its latency.
