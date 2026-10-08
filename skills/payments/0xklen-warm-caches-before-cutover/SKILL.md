---
name: warm-caches-before-cutover
description: Use when a fresh instance or new cache starts cold and its first minutes are slow — pre-populate hot keys and gate readiness on warmup before taking traffic.
---

# Warm caches before cutover

A newly started instance is slower than a warm one: no JIT, an empty in-process cache, a cold page cache, an empty connection pool. If you route traffic the moment the process is up, the first requests pay every cold cost at once — and a rolling deploy repeats it per instance.

## Procedure

1. Enumerate what is cold on startup: in-process caches and LRU, the database buffer cache, JIT or interpreted warmup, connection pools, and lazily loaded config.
2. Load a warm set of hot keys before the instance is marked ready, and fail readiness until warmup completes so no traffic arrives early:
```
/warmup  -> replays the top-N keys from a recorded access log
/healthz -> liveness only; OK as soon as the process runs
/readyz  -> 503 until /warmup reports done
```
3. Prime the pool by opening `pool_size` connections during warmup instead of lazily on first request.
4. Warm the JIT for hot paths with a few hundred representative calls against a scratch route that mutates nothing.
5. Derive the hot set from real traffic, not a guess: top keys by hit count from the cache's own stats or an access log, refreshed periodically.
6. Warm the shared tier on a schedule too, so a shared key expiry never lands during peak.
7. Stagger per-instance warmup across a rolling deploy so the warmup load does not itself hammer the origin.

## Pitfalls

- Serving traffic before warmup finishes, so the cold cost lands on users instead of the deploy.
- Warming with synthetic keys that never appear in real traffic — warming the wrong thing.
- A warmup that itself stampedes the origin; warm from the shared cache, not the database, and bound its concurrency.
- A readiness probe that passes on process start rather than on warm completion.
- Warming once at deploy while normal TTLs expire the keys minutes later.
- Warming such a huge set that startups take minutes and the rollout stalls.

## Verification

    curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/readyz   # 503 until warm
    redis-cli dbsize; redis-cli info stats | grep keyspace_hits
    # pass: the first user request after cutover shows warm-path latency, not cold p99

Report what is warmed, the hot-set source, the readiness gate, and the p99 of the first 60s after cutover versus steady state.
