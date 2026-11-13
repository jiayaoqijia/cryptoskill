---
name: stampede-and-herd
domain: software-engineering/stampede-and-herd
trigger: "Bounding the load spike when a hot cache entry expires."
anti_trigger: "Not for cache product selection, and not for general load shedding."
scope: "What happens when a hot key expires, and the controls that bound it."
status: seedling
---

# Stampede and herd

## Standard

When a cache entry serving a large share of traffic expires, every concurrent request misses at once and each goes to the source. The source, sized for the cached read rate, receives the full uncached rate in a burst and can fail, which turns an expiry into an outage — and the failure repeats when the entry expires again.

The controls are structural rather than tuning. A per-key lock lets one request rebuild while the others wait or serve the stale value. A probabilistic early refresh spreads rebuilds before expiry instead of after it. A stale-while-revalidate window serves the old value while one worker refreshes. And a request coalescing layer collapses identical in-flight misses into one source call. Each bounds the burst; none removes the underlying dependency.

Primary sources: <https://aws.amazon.com/caching/best-practices/> and <https://www.rfc-editor.org/rfc/rfc5861.html>.

## Decision rules

- Record the hot keys and the share of traffic each serves.
- Record the source's capacity relative to the uncached read rate.
- Record the control in place: lock, coalescing, early refresh, or stale-while-revalidate.
- Record what a waiting request does: block, serve stale, or fail.
- Record the worst case at simultaneous expiry of several hot keys.
- Record the timeout on the lock or coalescing window, so a stuck rebuild does not deadlock.

## Procedure

1. Identify hot keys and their traffic share.
2. Record source capacity against the uncached rate.
3. Record the control and the waiting behaviour.
4. Compute the burst at simultaneous expiry.
5. Record lock timeouts and failure paths.
6. Write the analysis with the bound stated.

## Anti-patterns

- Assuming a TTL staggered across keys is sufficient protection.
- Blocking all waiting requests with no timeout.
- Adding a lock without a stale-serve path, so a slow rebuild becomes an outage.
- Ignoring the case where many hot keys expire together.
- Sizing the source for the cached rate and relying on the cache holding.

## Done checklist

- [ ] Hot keys and traffic share recorded.
- [ ] Source capacity recorded.
- [ ] Control and waiting behaviour recorded.
- [ ] Simultaneous-expiry burst computed.
- [ ] Timeouts recorded.
- [ ] Bound stated.

The measurement worth keeping is the source's observed load immediately after an expiry, compared with its capacity: that ratio is the real margin, and it is the number that decides whether a single hot key expiring can take the source down. Recording it makes the risk concrete rather than theoretical.


## Sources

- Caching best practices: <https://aws.amazon.com/caching/best-practices/>
- Stale-while-revalidate specification: <https://www.rfc-editor.org/rfc/rfc5861.html>
- Cache implementation guidance: <https://redis.io/docs/manual/client-side-caching/>
