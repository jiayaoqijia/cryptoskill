---
name: hermetic-builds
domain: software-engineering/hermetic-builds
trigger: "Making a build reproducible across machines and time."
anti_trigger: "Not for deployment environment parity, and not for container hygiene."
scope: "Undeclared dependencies, environment leakage, and reproducibility."
status: seedling
---

# Hermetic builds

## Standard

A hermetic build reads only its declared inputs and produces byte-identical outputs from identical inputs, regardless of the machine, the clock, or the network. That property is what makes a cache sound and an incremental build trustworthy, and it is what allows a build to be reproduced months later when a defect needs investigating.

Non-hermeticity enters through narrow doors: a build that downloads a dependency at compile time, reads a timestamp into a generated file, iterates a directory in filesystem order, or picks up a local tool from the path. Each is small, each is invisible on the machine where it was introduced, and each produces a build that cannot be reproduced elsewhere.

Primary sources: <https://reproducible-builds.org/> and <https://bazel.build/>.

## Decision rules

- Record the sandbox mechanism and what it restricts: filesystem, network, and environment.
- Record any build step that fetches at compile time, and how the fetched content is pinned.
- Record sources of nondeterminism: timestamps, ordering, randomness, and locale.
- Record the verification that two builds of the same source produce identical output.
- Record the toolchain's provenance and how it is pinned.
- Record the exceptions where hermeticity is not achieved, and the reason.

## Procedure

1. Record the sandbox and the restrictions it enforces.
2. Disable network access during the build and record the failures it reveals.
3. Pin every fetched artifact by digest.
4. Remove or normalise timestamps and ordering in generated output.
5. Verify reproducibility by building twice in different directories.
6. Record the remaining exceptions.

## Anti-patterns

- Fetching dependencies during compilation.
- Embedding the build time in a version string.
- Iterating a directory without sorting.
- Assuming a build is reproducible because it passed once.
- A toolchain resolved from the path rather than pinned.

## Done checklist

- [ ] Sandbox and restrictions recorded.
- [ ] Network disabled and results recorded.
- [ ] Fetched artifacts pinned by digest.
- [ ] Nondeterminism sources normalised.
- [ ] Reproducibility verified across directories.
- [ ] Exceptions recorded.

The network-disabled build is the single most informative experiment in this skill: it turns every undeclared fetch into an immediate failure rather than a silent difference between machines, and the list of failures it produces is a precise inventory of the build's hidden inputs.


The reproducibility check should be run from a clean checkout in a different path, because a second build in the same directory reuses outputs and can pass on a build that would fail elsewhere; the difference between the two runs is exactly the environment leakage the check is meant to find.


## Sources

- Reproducible builds project: <https://reproducible-builds.org/>
- Build tool documentation: <https://bazel.build/>
- Supply chain integrity guidance: <https://www.cncf.io/>
