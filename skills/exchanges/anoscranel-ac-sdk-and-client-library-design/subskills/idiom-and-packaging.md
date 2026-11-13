---
name: idiom-and-packaging
domain: software-engineering/idiom-and-packaging
trigger: "Making a client library feel native in its language."
anti_trigger: "Not for package registry operations, and not for build configuration."
scope: "Following the language's conventions rather than importing another's."
status: seedling
---

# Idiom and packaging

## Standard

A library that behaves like its language is easier to adopt than one that behaves like the API it wraps. Callers expect the language's naming conventions, its error mechanism, its resource cleanup pattern, and its concurrency primitives; a library that returns a promise in a callback ecosystem, or throws where the language returns a result, forces every caller to write an adapter.

Packaging is the second half. The dependency footprint matters because it becomes the caller's: a library that pulls in a large framework for a small feature imposes that cost indefinitely. The distribution should also respect the ecosystem's conventions for optional dependencies, so that a caller using only one transport does not install three.

Primary sources: <https://semver.org/> and <https://www.w3.org/>.

## Decision rules

- Record the error mechanism used and whether it matches the language's convention.
- Record the naming conventions followed, which should not mirror the wire format.
- Record the resource cleanup pattern, since a client holding connections needs one.
- Record the dependency footprint and the reason for each dependency.
- Record optional dependencies and how they are gated.
- Record the concurrency model and whether the client is safe to share across threads or tasks.

## Procedure

1. Record the language's conventions for errors, naming, and cleanup.
2. Compare the design against each and record deviations.
3. Record the dependency list and justification.
4. Record optional dependencies and gating.
5. Record the concurrency safety guarantee.
6. Write the idiom summary with deviations explained.

## Anti-patterns

- Exposing wire-format names in the public API.
- A client that requires explicit cleanup with no integration into the language's mechanism.
- A heavy dependency included for convenience.
- Optional features that install their dependencies unconditionally.
- A shared client that is not safe to share, with no documentation of that.

## Done checklist

- [ ] Error mechanism recorded.
- [ ] Naming conventions recorded.
- [ ] Cleanup pattern recorded.
- [ ] Dependency footprint recorded.
- [ ] Optional dependencies recorded.
- [ ] Concurrency safety recorded.

The concurrency guarantee deserves a sentence even when the answer is unfavourable: a client that is not safe to share must say so, because the default assumption in most ecosystems is that a client can be shared, and a caller who shares an unsafe client discovers it as intermittent corruption rather than as an error.


## Sources

- Library and packaging conventions: <https://semver.org/>
- Interface design context: <https://www.w3.org/>
- Release practice: <https://www.rfc-editor.org/rfc/rfc9110>
