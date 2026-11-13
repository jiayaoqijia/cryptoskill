---
name: remote-cache-keys
domain: software-engineering/remote-cache-keys
trigger: "Designing or auditing a build cache key."
anti_trigger: "Not for application-level caching, and not for CDN configuration."
scope: "What must be in the key for a cache hit to be safe."
status: seedling
---

# Remote cache keys

## Standard

A build cache returns a previous output when the key matches, so the key's completeness is the cache's correctness. The key must cover every input that can change the output: source files, their contents, the declared dependencies' outputs, the compiler and tool versions, the environment variables the build reads, and the platform it targets.

A key that omits an input produces a wrong hit, which is worse than a miss because it is silent and it produces an artifact that does not correspond to the source. The common omissions are the toolchain version, environment variables that leak into compilation, and a dependency's transitive outputs which are hashed only at their own level.

Primary sources: <https://bazel.build/> and <https://reproducible-builds.org/>.

## Decision rules

- Record exactly which inputs are hashed into the key.
- Record the toolchain and its version in the key, not in the environment.
- Record the environment variables the build reads, which must be declared and hashed.
- Record whether the key includes the platform and target architecture.
- Record the cache's scope: per-branch, shared, or public, and the isolation that implies.
- Record the hit rate and the wrong-hit incidents, since a hit rate alone rewards looseness.

## Procedure

1. Enumerate the inputs the build reads and record them.
2. Verify each is hashed into the key.
3. Record the toolchain identification in the key.
4. Declare and hash environment variables.
5. Record the cache scope and isolation.
6. Measure hit rate alongside correctness checks.

## Anti-patterns

- Keying on file paths rather than contents.
- Omitting the compiler or toolchain version.
- Allowing the build to read environment variables that are not in the key.
- A shared public cache with no isolation between untrusted branches.
- Optimising the hit rate without verifying that hits are correct.

## Done checklist

- [ ] Hashed inputs enumerated.
- [ ] Toolchain version in the key.
- [ ] Environment variables declared and hashed.
- [ ] Platform recorded.
- [ ] Cache scope and isolation recorded.
- [ ] Hit rate and correctness measured together.

The wrong-hit incident log is worth keeping even when the count is zero, because it demonstrates that correctness is being checked rather than inferred from a hit rate, and a cache whose only metric is its hit rate is a cache that will be loosened until it produces a wrong artifact.


## Sources

- Build cache documentation: <https://bazel.build/>
- Reproducible builds reference: <https://reproducible-builds.org/>
- Supply chain security guidance: <https://www.cncf.io/>
