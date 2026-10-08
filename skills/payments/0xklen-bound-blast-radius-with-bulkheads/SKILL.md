---
name: bound-blast-radius-with-bulkheads
description: Use when one slow or failing dependency, tenant or operation class could exhaust a shared pool and take the whole service down — partitions resources so a fault stays inside one compartment.
---

# Bound blast radius with bulkheads

A single shared thread pool, connection pool or worker queue means any one dependency that stalls consumes every slot, and a healthy peer starts failing too. Partition the resources so a fault in one compartment cannot starve the others.

## Procedure

1. List the shared pools and every class of work that draws from them: outbound HTTP clients, DB connections, background workers, per-tenant jobs. Each shared pool is a shared fate.

2. Partition by the axis that actually fails independently — usually the *dependency* for outbound calls and the *tenant* for inbound work. Give each compartment its own bounded pool:
       var pools = map[string]chan struct{}{
         "payments":  make(chan struct{}, 40),  // slow peer, low concurrency
         "catalog":   make(chan struct{}, 120),
         "search":    make(chan struct{}, 60),
       }

3. Size each compartment from that dependency's own latency ceiling, not from total capacity. If `payments` p99 is 800 ms and you can tolerate 5 s of queueing, 40 slots is the ceiling regardless of how many slots `catalog` gets. Budget the sum to about 80% of the process limit (`ulimit -n`, DB `max_connections`).

4. Acquire before dispatch and release in `defer`, and *fail fast* when full rather than blocking behind a stalled compartment:
       select {
       case pools["payments"] <- struct{}{}:
         defer func() { <-pools["payments"] }()
       case <-time.After(200 * time.Millisecond):
         return errPoolSaturated  // shed, do not queue unbounded
       }

5. Apply the same split at the platform layer: separate Kubernetes deployments (not just containers in one pod) per tenant tier, `resources.requests`/`limits` per pod so an OOM in one does not evict a neighbour, and node pools for heavy batch work.

6. Give each compartment its own circuit breaker and timeout so a broken peer trips its own breaker without touching peers:
       breaker := gobreaker.NewCircuitBreaker(gobreaker.Settings{Name: "payments", Timeout: 30 * time.Second, ReadyToTrip: func(c gobreaker.Counts) bool { return c.ConsecutiveFailures > 5 }})

7. For inbound HTTP, cap per-tenant concurrent requests in middleware and return `429` with `Retry-After`, so one noisy caller cannot occupy the global accept loop.

## Pitfalls

- One pool shared across a fast in-memory cache and a slow third-party API: the slow calls fill the pool and the cache reads queue behind them.
- Sizing every compartment from the *peak* of the same dependency, so the sum exceeds the DB connection limit and the bulkheads collectively re-create a global bottleneck.
- A bulkhead with no timeout: a caller blocks forever waiting for a slot that never frees because the peer is hung.
- Reaching for a new deployment per tenant below ~10 tenants — the operational overhead outweighs the isolation until tenant count justifies it.

## Verification

    # inject a 30s stall into one compartment and confirm peers keep serving
    curl -s -o /dev/null -w '%{http_code} %{time_total}\n' localhost:8080/payments
    curl -s -o /dev/null -w '%{http_code} %{time_total}\n' localhost:8080/catalog
    # payments returns 503 fast; catalog stays 200 under its normal latency
    curl -s localhost:9090/metrics | grep -E 'pool_in_use\{pool='

Report: the compartments defined, each pool's cap and evidence it was sized from that dependency's own p99, and a fault-injection result where the stalled compartment sheds while peers stay within latency SLO.
