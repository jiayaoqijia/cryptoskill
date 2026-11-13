---
name: registry-resolution
domain: software-engineering/registry-resolution
trigger: "Understanding how tools resolve names to digests in a registry."
anti_trigger: "Not for choosing a registry vendor, and not for signing manifests."
scope: "Tags as moving pointers, digest pinning, resumability, and concurrent manifest publication."
status: seedling
---

# Registry resolution

## Standard

A registry pairs immutable digests with mutable names. A tag like `latest` or `1.2` is a pointer that an operator can retarget; the digest beneath it cannot change. Every resolution is therefore a two-step event: translate the human name to a digest, then act on the digest. Tools that cache or pin at the first step behave differently from tools that re-resolve, and the difference is observable in which bytes a build actually consumes.

The operation most worth reading carefully is manifest publication. Uploading layers is resumable and idempotent because layers are addressed by content; publishing the manifest is the single point at which a tag moves, and concurrent publishes produce a last-writer-wins outcome that can interleave components that were never validated together. Registries mitigate with tag immutability options and digest references; readers mitigate by pinning digests rather than names whenever the choice exists.

Primary sources: <https://docs.docker.com/registry/spec/api/> and <https://opencontainers.org/>.

## Decision rules

- Record which names resolve at fetch time versus which are pinned at build or deploy time.
- Record the tag-movement policy: mutable, immutable once pushed, or frozen per channel.
- Record whether a manifest can mix components produced at different times.
- Record the resumability behaviour for interrupted layer uploads.
- Record whether the store's clients verify digests on fetch or trust the registry's lookup.
- Record how tag history is retained, if at all, for rollback.

## Procedure

1. Enumerate the names in play and where each resolution happens.
2. State the tag mutability policy.
3. Check the publication path for concurrent-push behaviour.
4. Test an interrupted upload's resumption.
5. Determine whether fetch verifies content against the digest.
6. Write the resolution policy with the pinning points named.

## Anti-patterns

- Pinning a mutable tag and expecting reproducible fetches.
- Assuming a manifest's components were all present and validated at one instant.
- Re-pushing a moved tag during an incident and losing the prior manifest.
- Treating digest-equals-trust: verification of bytes against digest is a separate act.
- Ignoring tag history and losing the ability to name the previous good build.

## Done checklist

- [ ] Resolution points enumerated.
- [ ] Tag mutability policy stated.
- [ ] Concurrent publication behaviour recorded.
- [ ] Resumability tested.
- [ ] Fetch verification behaviour recorded.
- [ ] Tag history and rollback story written.

## Sources

- Registry specification and digest semantics: <https://docs.docker.com/registry/spec/api/>
- OCI image and manifest specification: <https://opencontainers.org/>
