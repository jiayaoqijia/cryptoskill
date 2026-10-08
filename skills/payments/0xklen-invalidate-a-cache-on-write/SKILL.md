---
name: invalidate-a-cache-on-write
description: Use when a cached value can go stale after a write — prove the invalidation path with a read-after-write test and a TTL bound instead of trusting a manual purge.
---

# Invalidate a cache on write

A cache is a second copy of the truth; every write must invalidate or version the key it affects. Prove it with a read-after-write assertion, not with a delete you remembered to call.

## Procedure

1. Enumerate every write path that touches cached data:
```
grep -rn "cache.set\|cache.setex\|redis.set\|@lru_cache\|@cache(" src/
```
2. List the exact keys each write invalidates. A write with no `cache.delete(...)` on the same path is a bug until proven otherwise.
3. Make invalidation part of the write, or switch to versioned keys which need no delete:
```python
key = f"user:{uid}:v{version}"     # bump version on write
```
4. Write a read-after-write test that fails if the cache is stale:
```python
def test_profile_updates_immediately(client, cache):
    client.put("/users/1", json={"name": "new"})
    assert client.get("/users/1").json()["name"] == "new"   # served via cache
    assert cache.get("user:1:profile") is None               # or version bumped
```
5. Prove the test catches staleness by deleting the invalidation line and confirming red (see `poison-a-fixture-to-prove-a-detector`).
6. Set a TTL as a backstop even with correct invalidation: `cache.setex(key, 300, val)`. Max acceptable staleness equals the TTL — state it so readers know the bound.
7. For distributed caches, invalidate by version bump published over pub/sub, not by deleting the key on one node — other nodes keep their copy otherwise.

## Pitfalls

- `@lru_cache` on a function reading mutable state never invalidates; call `fn.cache_clear()` on write or drop the decorator.
- Deleting the key *before* the write commits lets a concurrent read repopulate stale data. Invalidate after commit.
- Key collisions from `str(obj)` mean two objects share a slot. Hash a stable tuple, not `repr`.
- Cache-aside with no TTL turns a transient bug into permanent staleness. Always bound the TTL.

## Verification

```
pytest tests/test_profile_updates_immediately.py -q && redis-cli ttl user:1:profile
```
Passes = test green and `ttl` returns a positive integer not exceeding the configured max. Report: "read-after-write green; removing invalidation made the test red; TTL=300s bounds staleness."
