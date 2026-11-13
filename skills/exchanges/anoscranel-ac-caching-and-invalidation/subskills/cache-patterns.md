---
name: cache-patterns
domain: software-engineering/cache-patterns
trigger: "Choosing who populates and updates the cache."
anti_trigger: "Not for cache product selection, and not for query tuning."
scope: "Cache-aside, read-through, write-through, and who owns population."
status: seedling
---

# Cache patterns

## Standard

The patterns differ in who is responsible for the cache. In cache-aside the application checks the cache, and on a miss reads the source and populates the entry itself; the cache knows nothing about the source. In read-through the cache is configured with a loader and performs the read on a miss, so the application always sees the same interface.

The write side has the matching pair. Write-through updates the cache and the source together, which keeps them close at the cost of write latency. Write-behind updates the cache and defers the source write, which is fast and risks losing data if the cache fails before flushing. Cache-aside with a write-invalidate on the source is the most common combination, and its hazard is the race where a read repopulates a stale value just after a write invalidated it.

Primary sources: <https://aws.amazon.com/caching/best-practices/> and <https://redis.io/docs/manual/client-side-caching/>.

## Decision rules

- Record which pattern is used for reads and which for writes.
- Record who populates a miss, since that decides where the loader logic lives.
- Record the write path: invalidate, update, or defer.
- Record the race between a read repopulating and a write invalidating, and the mitigation.
- Record the failure behaviour when the cache write succeeds and the source write fails.
- Record whether the cache is authoritative, which it should never be.

## Procedure

1. Record the read pattern and who populates.
2. Record the write pattern and its ordering.
3. Identify the interleaving that produces a stale entry.
4. Record the mitigation, such as a per-key lock or a version in the key.
5. Record the partial-failure behaviour.
6. Write the pattern summary with the race named.

## Anti-patterns

- Mixing patterns without stating which applies where.
- Treating a write-behind cache as durable.
- Ignoring the read-repopulate race after a write invalidation.
- Putting loader logic in two places for the same key.
- Assuming the cache is the source of truth.

## Done checklist

- [ ] Read pattern recorded.
- [ ] Write pattern recorded.
- [ ] Stale interleaving identified.
- [ ] Mitigation recorded.
- [ ] Partial-failure behaviour recorded.
- [ ] Race named in writing.

The choice also fixes where the failure is observed: with cache-aside the application's own code holds the miss path, so an error there is a bug in the service; with read-through the loader is part of the cache's configuration, so the same error looks like a cache fault and is debugged by a different team. Naming which team owns the miss path is part of choosing the pattern.


## Sources

- Caching patterns guidance: <https://aws.amazon.com/caching/best-practices/>
- Client-side caching documentation: <https://redis.io/docs/manual/client-side-caching/>
- HTTP caching semantics: <https://www.rfc-editor.org/rfc/rfc9111.html>
