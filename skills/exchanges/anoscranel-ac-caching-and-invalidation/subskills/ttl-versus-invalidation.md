---
name: ttl-versus-invalidation
domain: software-engineering/ttl-versus-invalidation
trigger: "Choosing between time-based expiry and explicit invalidation."
anti_trigger: "Not for cache product selection, and not for query tuning."
scope: "Time-based expiry against event-driven eviction, and the window each leaves."
status: seedling
---

# TTL versus invalidation

## Standard

A TTL bounds staleness by time: the entry is served until it expires, so the worst case is the TTL length. Explicit invalidation bounds it by event: the entry is removed when the underlying data changes, so the worst case is the propagation delay of that event, which is usually much shorter but is not zero and can fail.

The two fail differently, and that is the choosing criterion. A TTL is self-healing: a missed invalidation costs at most the TTL, and the system recovers without intervention. An explicit invalidation is precise but fragile: a dropped event leaves a stale entry indefinitely, and the failure is silent. Combining them — invalidate on event, keep a TTL as a backstop — is the common resolution, and the TTL then becomes the stated worst case rather than the primary mechanism.

Primary sources: <https://aws.amazon.com/caching/best-practices/> and <https://www.rfc-editor.org/rfc/rfc9111.html>.

## Decision rules

- Record the TTL and the worst-case staleness it implies.
- Record the invalidation events and their propagation path.
- Record what happens when an invalidation is lost, since that is the failure mode.
- Record whether a TTL backstop exists and its length.
- Record the consumers that can observe staleness and what they must tolerate.
- Record the cost of an invalidation storm when a broad key set changes at once.

## Procedure

1. Record the TTL and the staleness bound it sets.
2. Record the invalidation events and how they propagate.
3. State the consequence of a lost event.
4. Decide on a backstop and its length.
5. Record the invalidation storm case.
6. Write the policy with both bounds stated.

## Anti-patterns

- Relying on explicit invalidation with no TTL backstop.
- Assuming an invalidation event always arrives.
- Setting a TTL long enough that the bound is meaningless.
- Invalidating a broad key set at once and causing a stampede.
- Describing the policy without the worst-case staleness.

## Done checklist

- [ ] TTL and staleness bound recorded.
- [ ] Invalidation events and path recorded.
- [ ] Lost-event consequence stated.
- [ ] Backstop decided.
- [ ] Storm case recorded.
- [ ] Both bounds written.

The combination also needs a rule for which wins when they disagree: if an invalidation arrives and a concurrent read repopulates from a stale replica, the entry's TTL restarts with old data and the precise mechanism has made things worse than no invalidation at all. The rule should say which source the repopulation is allowed to read from.


## Sources

- Caching best practices: <https://aws.amazon.com/caching/best-practices/>
- HTTP caching semantics: <https://www.rfc-editor.org/rfc/rfc9111.html>
- Cache implementation guidance: <https://redis.io/docs/manual/client-side-caching/>
