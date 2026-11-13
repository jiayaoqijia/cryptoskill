---
name: negative-caching
domain: software-engineering/negative-caching
trigger: "Caching the absence of a record and the correctness trap it sets."
anti_trigger: "Not for cache product selection, and not for query tuning."
scope: "Caching absence, and the correctness trap it sets."
status: seedling
---

# Negative caching

## Standard

Caching a miss protects the source from repeated lookups of something that does not exist — a common pattern when a large share of requests ask for records that were never created or were deleted. Without it, an attacker or a bad client can drive load on the source simply by asking for absent keys, and the cost per request is paid again every time.

The trap is creation. An entry recording that a key is absent must be invalidated when the record appears, and the invalidation path for a create is often different from the path for an update, which means it is the one that gets missed. A short TTL on negative entries is the usual mitigation, and the TTL is the deliberate cap on how long a newly created record can appear missing.

Primary sources: <https://aws.amazon.com/caching/best-practices/> and <https://www.rfc-editor.org/rfc/rfc9111.html>.

## Decision rules

- Record which absent-key lookups are cached and the expected share of traffic.
- Record the TTL on negative entries, which bounds how long a created record can appear missing.
- Record the invalidation path for creation and verify it exists.
- Record whether the negative entry is distinguishable from a cached empty result.
- Record the interaction with authorisation, since caching absence can leak existence.
- Record the cost of a false absence to the user, which may exceed the load saved.

## Procedure

1. Record the absent-key traffic share.
2. Record the negative TTL and the false-absence window it creates.
3. Verify the creation path invalidates the negative entry.
4. Check the distinction between absent and empty.
5. Check the authorisation interaction.
6. Write the policy with the window stated.

## Anti-patterns

- Caching absence without an invalidation on create.
- Using a long TTL on negative entries for a high-creation workload.
- Conflating a cached absence with a cached empty list.
- Caching absence across permission boundaries and leaking existence.
- Adding negative caching before measuring how much traffic is absent-key.

## Done checklist

- [ ] Absent-key share recorded.
- [ ] Negative TTL and window recorded.
- [ ] Creation invalidation verified.
- [ ] Absent versus empty distinguished.
- [ ] Authorisation interaction checked.
- [ ] Policy written with the window.

A further check is the enumeration case: caching absence per key protects a lookup but not a listing, and an attacker enumerating keys still drives one request each, so the protection has to be paired with a rate limit or a per-client budget rather than relied on alone.


## Sources

- Caching best practices: <https://aws.amazon.com/caching/best-practices/>
- HTTP caching semantics for error responses: <https://www.rfc-editor.org/rfc/rfc9111.html>
- Cache implementation guidance: <https://redis.io/docs/manual/client-side-caching/>
