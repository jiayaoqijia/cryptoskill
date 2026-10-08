---
name: prevent-cache-stampede-with-single-flight
description: Use when a popular key expires and every request rebuilds it at once — collapse concurrent misses into one load with a lock, plus a stale-while-revalidate fallback.
---

# Prevent a cache stampede

When a hot key expires, every concurrent request misses and races to recompute it. A thousand callers recompute the same value and the origin takes a thousand hits — exactly the load the cache existed to prevent. Collapse the herd to a single loader.

## Procedure

1. Recognise the shape: an origin QPS spike that coincides with a key's TTL boundary, with p99 rising while the key is rebuilt.
2. Single-flight in-process: coalesce concurrent loads for the same key into one. Go's `golang.org/x/sync/singleflight`, Node's `p-memoize`, or a per-key promise map:
```python
inflight = {}
async def get(key):
    if key not in inflight:
        inflight[key] = asyncio.create_task(load(key))
    return await inflight.pop(key)
```
3. Across processes, take a short distributed lock before recomputing; losers wait briefly then re-read the now-populated key:
```python
if redis.set(f"lock:{key}", 1, nx=True, ex=10):
    val = load(key); redis.setex(key, 300, val)
else:
    await asyncio.sleep(0.05); return await get(key)
```
4. Prefer stale-while-revalidate over blocking: serve the expired value and refresh in the background, with `stale-if-error` covering an origin outage.
5. Jitter every TTL so keys never expire together: `ttl = 300 + random.randint(0, 30)`.
6. Pre-warm the hottest keys on deploy or on a schedule, before the boundary rather than after it.
7. Bound the wait: a crashed lock holder must release via the key's `ex` TTL, never via a manual unlock that can deadlock.

## Pitfalls

- A lock with no TTL — a crashed holder blocks the key forever.
- Serving stale for a security-critical value (auth token, balance) where staleness is not acceptable.
- Single-flight keyed by a lossy key (`user`) so unrelated tenants collide.
- Refreshing in the background but never logging failures, so the stale value is served indefinitely.
- Collapsing the herd and still exceeding a rate-limited upstream's quota on the one reload.
- A per-process lock only, so N pods still produce N origin calls.

## Verification

    redis-cli monitor | grep -c "lock:"      # one lock and one origin load per key
    for i in $(seq 1 200); do curl -s localhost:8080/hot >/dev/null & done; wait
    grep -c "origin_call" app.log            # pass: ~1, not ~200

Report the collapse mechanism, the origin call count for N concurrent misses of a cold key, and the TTL jitter range used.
