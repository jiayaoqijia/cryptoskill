---
name: directory-services
domain: software-engineering/directory-services
trigger: "Choosing between computing placement and looking it up."
anti_trigger: "Not for service discovery of processes, and not for configuration storage."
scope: "Computed placement versus a lookup layer, and the trade each makes."
status: seedling
---

# Directory services

## Standard

There are exactly two ways to find where a key lives: compute it, or look it up. Computed placement — hash modulo, ring walk, range boundaries — is deterministic, requires no shared state, and changes only when the formula's inputs change. A directory service replaces the formula with a mapping: the key is looked up, the answer is authoritative, and the cost is a lookup layer's availability, freshness, and cache story.

The trade is control versus dependence. Computed placement cannot express exceptions — a physically-special node, a tenant that must be pinned, a temporary quarantine — because the formula applies to all keys equally. A directory expresses everything, including mistakes: a stale entry routes to the wrong owner, and an unavailable directory routes nowhere unless clients cache. Production systems frequently hybridise: compute the default, store the exceptions.

Primary sources: <https://dataintensive.net/> and <https://martinfowler.com/articles/patterns-of-distributed-systems/>.

## Decision rules

- Record which path answers location: computed, directory, or hybrid.
- Record the directory's consistency model: how stale an answer can be.
- Record the client's behaviour when the directory is unreachable.
- Record the exception surface the directory supports that the formula cannot.
- Record who can change mappings and how the change propagates.
- Record the mapping's audit history — moves are events, and they should be traceable.

## Procedure

1. State where each lookup class is answered.
2. Measure or bound the mapping's staleness window.
3. Test client behaviour on directory unavailability, including cached answers' lifetime.
4. Enumerate the exceptions that motivated the directory's existence.
5. Walk the change path: from a mapping edit to a client acting on it.
6. Write the routing design with the failure path stated.

## Anti-patterns

- Treating a directory as always consistent; stale answers misroute silently.
- No client-side cache, making the directory a hard dependency.
- Storing in the directory what the formula already computes, adding drift surface.
- No history, so a wrong routing cannot be attributed.
- Changing mappings by hand directly against the store.

## Done checklist

- [ ] Lookup path per class stated.
- [ ] Staleness window bounded.
- [ ] Unavailability behaviour tested.
- [ ] Exception surface enumerated.
- [ ] Change propagation path walked.
- [ ] Mapping audit history verified.

The hybrid also has a drift failure worth naming: when the exception set grows, each entry is a special case that a formula change later invalidates, so the record should carry the exception count and a scheduled review of which exceptions the formula can now absorb.

## Sources

- Request routing designs: <https://dataintensive.net/>
- Distributed systems patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
- Distributed hash table background: <https://en.wikipedia.org/wiki/Distributed_hash_table>
