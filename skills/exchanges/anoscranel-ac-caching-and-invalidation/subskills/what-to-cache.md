---
name: what-to-cache
domain: software-engineering/what-to-cache
trigger: "Deciding whether a data source is worth caching at all."
anti_trigger: "Not for choosing a cache product, and not for query tuning."
scope: "Read-write ratio, cost of a miss, and the hit-rate arithmetic."
status: seedling
---

# What to cache

## Standard

A cache is worth its complexity when the read cost it avoids exceeds the cost of being sometimes wrong. That comparison has three inputs: the read-to-write ratio, the cost of a miss in latency and in load on the source, and the consequences of serving stale data. A read-heavy source whose misses are cheap is a poor candidate; a write-heavy source is usually a worse one, because invalidation dominates.

The arithmetic is simple enough to state and is often skipped. If a source serves a hundred thousand reads a second and the cache hits ninety percent, the source sees ten thousand — a real saving. If the cache hits fifty percent, the source sees fifty thousand and the cache has added a network hop, a failure mode, and a consistency problem for a halving. The hit rate needed to justify the complexity is higher than intuition suggests.

Primary sources: <https://aws.amazon.com/caching/best-practices/> and <https://redis.io/docs/manual/client-side-caching/>.

## Decision rules

- Record the source's read rate and write rate.
- Record the cost of a miss: latency added, and load added to the source.
- Record the staleness the consumers can tolerate, in seconds or as an event.
- Compute the source load at the expected hit rate.
- Record what a cache outage does, since that is the failure the cache introduces.
- Record the key cardinality, which sets the cache's working set size.

## Procedure

1. Record read and write rates for the source.
2. Record the miss cost in latency and load.
3. Record the tolerable staleness.
4. Compute source load at the expected hit rate.
5. Record the outage behaviour.
6. Write the decision with the arithmetic shown.

## Anti-patterns

- Adding a cache before measuring the source's load.
- Assuming a hit rate without knowing the key distribution.
- Caching a write-heavy source and fighting invalidation forever.
- Ignoring what happens when the cache is unavailable.
- Treating a cache as free because the product is managed.

## Done checklist

- [ ] Read and write rates recorded.
- [ ] Miss cost recorded.
- [ ] Tolerable staleness recorded.
- [ ] Source load at expected hit rate computed.
- [ ] Outage behaviour recorded.
- [ ] Decision written with arithmetic.

The last input is worth stating plainly: a cache that is not measured is a cache whose benefit is assumed. Recording the hit rate before and after, against the same traffic, is the only way to know whether the complexity bought anything, and the measurement is cheap compared with the cache itself.


## Sources

- Caching best practices: <https://aws.amazon.com/caching/best-practices/>
- Client-side caching documentation: <https://redis.io/docs/manual/client-side-caching/>
- HTTP caching specification: <https://www.rfc-editor.org/rfc/rfc9111.html>
