---
name: origin-shielding
domain: software-engineering/origin-shielding
trigger: "Controlling how many requests reach the origin when a cache misses."
anti_trigger: "Not for application-level stampede control, and not for queue backpressure."
scope: "Controlling origin load and stampede at the edge."
status: seedling
---

# Origin shielding

## Standard

A cache miss at one edge location becomes a request to the origin. With many locations, a popular object expiring everywhere at once becomes a synchronized wave of identical misses — the thundering herd at the origin, caused by the cache layer that was meant to prevent it. An origin shield sits between the edges and the origin as a second, shared cache: the edges miss, the shield collapses the herd into one origin request, and the rest are served from the shield as it fills.

The shield is a concurrency decision expressed as cache topology. The collapse is what the shield exists for — the origin sees one request for the object rather than one per location — and the settings that matter are the shield's own expiry behaviour and whether it performs request coalescing. Without coalescing, a shield multiplies the herd by one instead of collapsing it.

Primary source: <https://www.rfc-editor.org/rfc/rfc9111>.

## Decision rules

- Record whether a shield is enabled and which edge locations route through it.
- Record coalescing behaviour and the conditions under which parallel requests still pass through.
- Record the shield's expiry relative to the edge caches, and its miss behaviour.
- Record collapse behaviour under load as observed, not as documented.
- Measure the effect: origin request rate with and without the shield for a expiring popular object.
- Record the failure mode: a shield that also misses is a second hop the origin pays for.

## Procedure

1. Record the shield topology and which content classes pass through it.
2. Confirm coalescing settings.
3. Record shield expiry relative to the edge.
4. Expire a popular object and observe the origin request rate.
5. Compare against the same expiry with the shield off.
6. Record the measured collapse ratio and the settings that produced it.

## Anti-patterns

- A shield without request coalescing, adding a hop without collapsing the herd.
- Assuming the shield helps without measuring origin rate.
- Shield expiry longer than edge, so the shield serves stale after the edge refreshed.
- Storing uncacheable responses on the shield path.
- Treating the shield as the fix for an origin too slow to serve even collapsed requests.

## Done checklist

- [ ] Shield topology recorded.
- [ ] Coalescing confirmed.
- [ ] Expiry relationships recorded.
- [ ] Collapse measured with a real expiry.
- [ ] With/without comparison recorded.
- [ ] Failure mode documented.

## Sources

- RFC 9111, HTTP caching: <https://www.rfc-editor.org/rfc/rfc9111>
- Shared and proxy cache behaviour: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching>
- Load management practice: <https://sre.google/sre-book/handling-overload/>
