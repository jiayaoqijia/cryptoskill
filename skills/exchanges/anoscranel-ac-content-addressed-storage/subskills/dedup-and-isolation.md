---
name: dedup-and-isolation
domain: software-engineering/dedup-and-isolation
trigger: "Reasoning about what deduplication shares and what it must not."
anti_trigger: "Not for cache hit-rate tuning, and not for compression algorithm choice."
scope: "What dedup shares, cross-tenant leakage, and compression's own dedup surprises."
status: seedling
---

# Dedup and isolation

## Standard

Deduplication is the payoff of content addressing: identical content is stored once whatever it was uploaded as. The economics are large — builds and container images repeat layers and dependencies endlessly — and the consequence is shared storage across whatever boundaries the store serves. If two tenants can each reach their own object by digest, and the object is stored once, the store must decide what a digest lookup reveals about the presence of other tenants' content.

The isolation question surfaces in two observable ways. An existence check — does this digest exist? — can reveal that someone else stored that content. And a direct fetch by a guessed digest can succeed without any per-tenant authorization, because the addressing layer authorized the digest, not the requester. Multi-tenant stores handle this at the API layer, and the choice they make is part of the store's security posture, not an implementation detail.

Primary sources: <https://docs.docker.com/registry/spec/api/> and <https://en.wikipedia.org/wiki/Data_deduplication>.

## Decision rules

- Record what dedup crosses: tenancy lines, repository boundaries, or only a single user's uploads.
- Record whether digest-presence checks are visible to unauthorized callers.
- Record whether fetching a known digest requires path-level authorization in addition to ingest.
- Record whether the store's dedup is chunk-level, object-level, or both.
- Record what compression applies and where dedup happens relative to it.
- Record the timing side channel: faster responses for already-present digests reveal prior uploads.

## Procedure

1. Determine the dedup boundary and record it.
2. Test whether an unauthenticated or cross-tenant caller can distinguish existing from missing digests.
3. Check how fetch authorization interacts with deduplicated storage.
4. Record the dedup granularity.
5. Place compression in the pipeline and check whether it happens before or after dedup.
6. Write the isolation assessment with the observable channels named.

## Anti-patterns

- Assuming dedup is per-project when the store serves a global namespace.
- Treating a digest as an authorization token for content.
- Ignoring the timing side channel on upload paths.
- Compressing before chunking when compression is per-file and chunk dedup is cross-file.
- Believing dedup only helps when the store chooses it; layers can be shared automatically.

## Done checklist

- [ ] Dedup boundary recorded.
- [ ] Digest-presence visibility tested.
- [ ] Fetch authorization model recorded.
- [ ] Dedup granularity recorded.
- [ ] Compression ordering recorded.
- [ ] Timing channels named in the isolation assessment.

## Sources

- Registry API and digest behaviour: <https://docs.docker.com/registry/spec/api/>
- Content-addressed layer sharing in build systems: <https://llvm.org/docs/>
- Discussion of deduplication boundaries: <https://en.wikipedia.org/wiki/Data_deduplication>
