---
name: design-a-multi-layer-cache
description: Use when every read hits the same remote cache and latency or cost is high — layer an in-process and a shared cache by lifetime, and name which layer owns invalidation.
---

# Design a multi-layer cache

An in-process cache answers in nanoseconds but lives per instance; Redis answers in a millisecond but is shared. Layering them correctly means choosing each layer's TTL from the data's change rate and accepting that the outermost layer sets the staleness bound.

## Procedure

1. Classify data by change rate and blast radius: static config (minutes to hours), reference data (seconds), user state (invalidate on write). Assign a TTL per class, not one global TTL.
2. L1 = in-process LRU per worker, L2 = shared Redis/Memcached, L3 = origin. Read L1 → L2 → origin; on an L2 miss populate both layers.
3. Keep L1 small and bounded (`lru_cache(maxsize=10000)`); a large L1 across many pods is N copies that can disagree, so give anything mutable a 1-5s L1 TTL.
4. State the staleness bound explicitly: `max_staleness = ttl(L1) + ttl(L2)`. If it is user-visible, put it in the response contract.
5. Jitter TTLs on both layers so keys never expire in lockstep:
```python
ttl = base + random.randint(0, base // 10)
```
6. Decide who invalidates. On write, delete L2 and publish an invalidation message so every L1 drops the key — or version the key so no delete is needed.
7. Emit a per-layer hit-rate metric; a layer with a 5% hit rate is costing memory and a hop for nothing.

## Pitfalls

- Identical TTLs on every key, so the entire cache expires in the same second.
- L1 with no cross-pod invalidation: one pod serves stale for the whole L1 TTL while others are fresh.
- Caching errors or `None` and counting them as hits, so an outage gets cached.
- Caching per-user data under a key that omits the user id — a cross-user data leak.
- A cache larger than the working set, evicting hot keys continuously (thrashing).
- Measuring hit rate without the byte cost per hit; a high-hit, huge-value layer can still be a net loss.

## Verification

    redis-cli info stats | grep -E "keyspace_hits|keyspace_misses"
    curl -s localhost:9090/metrics | grep -E "cache_l1_hit|cache_l2_hit"
    # pass: p99 read latency drops, L2 hit rate > 0.8, no growth in stale-serve alerts

Report per-layer TTLs and hit rates, the resulting max staleness, and who owns invalidation for each data class.
