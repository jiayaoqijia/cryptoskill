---
name: cache-policy-record
domain: software-engineering/cache-policy-record
trigger: "Writing the record of a cache's keys, TTLs and invalidation rules."
anti_trigger: "Not for recommending a cache product, and not for query tuning."
scope: "The written record: keys, TTLs, invalidation, and the staleness bound."
status: seedling
---

# Cache policy record

## Standard

The record states what is cached, the key structure, the TTL, the invalidation events, and the resulting staleness bound. It exists because a cache's behaviour is distributed across code, configuration, and infrastructure, and no single place otherwise describes what the system guarantees — which means the guarantee is discovered during an incident rather than read before one.

Its second function is the key taxonomy. The most common cache incident is not a stale value but a key collision or a key that omits part of the context, so a value computed for one tenant or one locale is served to another. Listing the key's components forces that context to be named, and naming it is what prevents the collision.

Primary sources: <https://aws.amazon.com/caching/best-practices/> and <https://osf.io/prereg/>.

## Decision rules

- The record lists every cached entity with its key structure and every component of the key.
- The TTL per entity is recorded, with the resulting worst-case staleness.
- The invalidation events per entity are recorded with their propagation path.
- The negative-cache windows are recorded separately, since they bound a different thing.
- The read-your-own-writes mechanism is recorded where it exists.
- Review triggers are dated: entity schema change, TTL change, new consumer, invalidation failure.

## Procedure

1. List cached entities with their key structures.
2. Record TTLs and the resulting bounds.
3. Record invalidation events and propagation.
4. Record negative-cache windows.
5. Record the read-your-own-writes mechanism.
6. Set review triggers and amend when any of the above changes.

## Anti-patterns

- A key that omits a context component such as tenant or locale.
- Recording the TTL without the resulting staleness bound.
- Omitting invalidation events because they live in another service.
- Leaving the negative cache out of the record.
- No trigger on schema change, so keys silently become wrong.

## Done checklist

- [ ] Entities and key structures listed.
- [ ] TTLs and bounds recorded.
- [ ] Invalidation events recorded.
- [ ] Negative-cache windows recorded.
- [ ] Read-your-own-writes recorded.
- [ ] Triggers dated.

The record should also state who can change the policy and how, because a TTL edited during an incident and not restored is a bound that no longer holds, and the only defence against that is a document that says what the bound is supposed to be.


## Sources

- Caching best practices: <https://aws.amazon.com/caching/best-practices/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- HTTP caching semantics: <https://www.rfc-editor.org/rfc/rfc9111.html>
