---
name: incremental-ci
domain: software-engineering/incremental-ci
trigger: "Making CI run only what a change requires."
anti_trigger: "Not for pipeline wiring, and not for deployment strategy."
scope: "Making CI consume the graph rather than run everything."
status: seedling
---

# Incremental CI

## Standard

A CI pipeline that runs the full suite on every change is correct and increasingly slow, and a pipeline that runs only affected targets is fast and correct only if the graph is complete. The engineering task is to make CI a consumer of the same graph the local build uses, so that the selection in CI and the rebuild locally are derived from one source rather than from two heuristics.

The two failure modes are opposite and both common. A pipeline that selects too little misses a regression and discovers it later; one that selects too much is slow and eventually gets bypassed. The record states the selection rule, the widening conditions, and the full run that provides the backstop.

Primary sources: <https://www.cncf.io/> and <https://bazel.build/>.

## Decision rules

- Record whether CI derives its selection from the build graph or from path filters.
- Record the widening conditions: shared configuration, dependency manifests, and toolchain changes.
- Record the scheduled full run and its cadence.
- Record the per-stage selection: which stages run on affected and which on all.
- Record the cache sharing between local and CI, and its scope.
- Record the time saved and the failures attributable to selection.

## Procedure

1. Record the selection source and its relationship to the build graph.
2. Define widening conditions and record them.
3. Schedule a full run as a backstop.
4. Set per-stage policy: affected or all.
5. Share the remote cache between local and CI and record the scope.
6. Measure duration and selection-caused failures.

## Anti-patterns

- Path filters that approximate the dependency graph.
- No widening for a change to a shared lockfile.
- Treating the affected set as authoritative without a full run.
- A cache scope that lets an untrusted branch poison results.
- Optimising pipeline duration while ignoring what it missed.

## Done checklist

- [ ] Selection source recorded.
- [ ] Widening conditions recorded.
- [ ] Full run scheduled.
- [ ] Per-stage policy recorded.
- [ ] Cache scope recorded.
- [ ] Duration and missed failures measured.

The per-stage policy matters because stages have different cost profiles: a lint stage is cheap enough to run broadly, while an integration stage that takes thirty minutes needs selection, and applying one policy to both either wastes time or takes risk that the cheap stage did not need to take.


## Sources

- Continuous integration practice: <https://www.cncf.io/>
- Build graph documentation: <https://bazel.build/>
- Delivery and release guidance: <https://martinfowler.com/>
