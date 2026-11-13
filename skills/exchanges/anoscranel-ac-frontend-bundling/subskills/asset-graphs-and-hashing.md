---
name: asset-graphs-and-hashing
domain: software-engineering/asset-graphs-and-hashing
trigger: "Referencing assets so browsers can cache them safely."
anti_trigger: "Not for server cache configuration, and not for image optimisation choices."
scope: "Referencing assets so caches can be trusted."
status: seedling
---

# Asset graphs and hashing

## Standard

A front-end build produces more than scripts: images, fonts, styles, and media, each referenced from the application. If those references are stable names, the browser cannot know when a file's content changed, so a cache either holds the old version forever or is told to hold nothing. Content hashing solves this: each output file's name includes a digest of its content, so a change changes the name, and a stable name guarantees stable content.

The rule that makes hashing work is that references travel with the graph. The bundle and the styles must reference the hashed name, and the hashed name must be computed from the exact bytes served. A hand-written URL that bypasses the graph breaks the guarantee in both directions — a changed file keeps an old name, or an unchanged file gets a new one, and the cache becomes unreliable in the one place it was supposed to be safe.

Primary source: <https://web.dev/learn>.

## Decision rules

- Hash every immutable output asset by content, and record the hash length and placement in the name.
- Reference assets through the build graph, not by hand-written absolute URLs.
- Set long cache lifetimes only on hashed assets; unhashed paths must revalidate.
- Record the fingerprint placement — in the filename, not the query string, so intermediaries cooperate.
- Verify that a content change produces a new name and that a no-op build produces identical names.
- Record font loading behaviour, which interacts with caching through preload decisions.

## Procedure

1. Record the build's asset naming and hashing configuration.
2. Grep for hand-written asset URLs that bypass the graph.
3. Set cache-control headers appropriate to hashed and unhashed outputs.
4. Build twice with no source change and compare output names — they must be identical.
5. Change one asset and confirm only names that depend on it change.
6. Record the naming scheme and the verified behaviour.

## Anti-patterns

- Hash in a query parameter, which some caches ignore.
- A no-op rebuild that renames everything, defeating every cache.
- Hand-written URLs with manual version suffixes.
- Long cache lifetimes on an index file that references hashed assets.
- Copying assets outside the build graph, so the served bytes are not the hashed bytes.

## Done checklist

- [ ] Hashing configuration recorded.
- [ ] Hand-written asset URLs found and routed through the graph.
- [ ] Cache-control policy set per output class.
- [ ] No-op rebuild verified name-stable.
- [ ] Content change verified name-changing.
- [ ] Naming scheme documented.

## Sources

- HTTP caching reference: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching>
- Web asset delivery guide: <https://web.dev/learn>
- Cache-Control directive definitions: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control>
