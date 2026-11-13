---
name: dns-and-propagation
domain: software-engineering/dns-and-propagation
trigger: "Planning a DNS change and how fast it takes effect everywhere."
anti_trigger: "Not for internal service discovery, and not for DNS security extensions."
scope: "Resolution order, TTLs, and how fast a change becomes universal."
status: seedling
---

# DNS and propagation

## Standard

DNS is a distributed cache with no push. A resolver that has answered a query keeps the answer for the record's time-to-live, and it serves that answer until the TTL expires, no matter what the authoritative zone says in the meantime. A change therefore becomes universal only as cached answers expire, and the slowest cached answer anywhere on the internet is the real propagation time — which the changer does not control.

The practical sequence follows from that. Lower the TTL well before the change so caches hold short answers; make the change; confirm the authoritative answer; then wait for the world to age out the old one. Reversing the order — changing first and lowering later — guarantees a window in which resolvers hold the old answer for the old long TTL, and rolling back does not reclaim that window.

Primary source: <https://www.iana.org/>.

## Decision rules

- Record the current TTL for each record being changed, before touching it.
- Lower the TTL at least one old-TTL ahead of the change window.
- Make changes with a short TTL active, and raise it back only after stability.
- Confirm at the authoritative servers first, then at public resolvers, then in the regions users come from.
- Treat negative answers as cached too; a record's absence has its own TTL.
- Record the fallback: the old address must stay serving until the last plausible cache expires.

## Procedure

1. Record current record set and TTLs.
2. Lower TTLs to a short value and wait one old-TTL.
3. Confirm the new TTL is what resolvers see.
4. Make the change at the authoritative zone.
5. Verify the authoritative answer, then public resolvers in the user's regions.
6. Serve both old and new through the expiry window; raise TTLs after.

## Anti-patterns

- Changing a record with a long TTL still active.
- Treating TTL as a delay of the change rather than of the cache.
- Only verifying the authoritative answer, not what resolvers return.
- Taking an old address down as soon as the change is made.
- Ignoring negative-caching TTLs when removing records.

## Done checklist

- [ ] Existing TTLs recorded.
- [ ] TTL lowered one old-TTL ahead.
- [ ] Change made at the authoritative source.
- [ ] Verified at resolvers in user regions.
- [ ] Both addresses served through expiry.
- [ ] TTLs raised after stability.

## Sources

- DNS root and TLD operations: <https://www.iana.org/>
- RFC 1034, domain names concepts: <https://www.rfc-editor.org/rfc/rfc1034>
- RFC 1035, implementation and TTL semantics: <https://www.rfc-editor.org/rfc/rfc1035>
