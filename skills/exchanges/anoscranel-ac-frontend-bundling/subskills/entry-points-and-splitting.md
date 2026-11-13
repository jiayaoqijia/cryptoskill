---
name: entry-points-and-splitting
domain: software-engineering/entry-points-and-splitting
trigger: "Deciding what loads at start and what loads on demand."
anti_trigger: "Not for runtime performance measurement, and not for choosing a router."
scope: "Entry points, chunks, and what loads when."
status: seedling
---

# Entry points and splitting

## Standard

An entry point is what the browser asks for first; everything reachable from it without a dynamic import ships in the initial load. Splitting moves code out of that reachable set by making it reachable only through a dynamic import — a separate request issued when the code is actually needed. The decision for each module is therefore binary in effect: does it load at start, or does it wait?

The common failure is splitting by file rather than by need. A chunk split at an arbitrary boundary does not help if the application still requests it immediately, and a split point placed at a route boundary helps only if users reach that route. The productive question is which interactions each chunk can wait for, and the honest answer usually puts the modal, the settings panel, and the rarely-visited route behind dynamic imports and leaves the shell eager.

Primary source: <https://web.dev/learn>.

## Decision rules

- Record the initial entry points and what each ships eagerly.
- Record each dynamic import and the interaction that triggers its chunk.
- Prefer route boundaries and interaction boundaries as split points.
- Measure the eager payload after each split to confirm the reduction.
- Watch for chunks that every route requests — they belong in the entry or in a shared cache group.
- Record the chunk-loading failure path: what the user sees if a chunk request fails.

## Procedure

1. List entry points and generate the build manifest.
2. Record the eager set and its total size.
3. List dynamic imports and their triggers.
4. Move candidates behind interactions and re-measure the eager set.
5. Inspect chunks requested on every route; merge or inline as needed.
6. Record the chunk error path and the fallback behaviour.

## Anti-patterns

- Splitting by file size rather than by need.
- A dynamic import the application issues on page load anyway.
- Hundreds of tiny chunks, each paying a request cost.
- No failure handling for a chunk that fails to load after a deploy.
- Splitting a module whose data is still fetched eagerly.

## Done checklist

- [ ] Entry points and eager set recorded.
- [ ] Dynamic imports and triggers recorded.
- [ ] Eager payload measured after splits.
- [ ] Every-route chunks identified and handled.
- [ ] Chunk failure path recorded.
- [ ] Split rationale documented.

## Sources

- Code splitting guide: <https://web.dev/learn>
- Dynamic import proposal: <https://tc39.es/proposal-dynamic-import/>
- HTTP caching guidance for assets: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching>
