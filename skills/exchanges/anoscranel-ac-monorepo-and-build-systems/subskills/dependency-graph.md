---
name: dependency-graph
domain: software-engineering/dependency-graph
trigger: "Declaring build inputs so a rebuild happens exactly when they change."
anti_trigger: "Not for package version policy, and not for runtime dependency injection."
scope: "Declared inputs, and why an undeclared one breaks correctness."
status: seedling
---

# Dependency graph

## Standard

A build target declares its inputs and produces outputs, and the graph of those declarations is what allows the build system to decide whether a target is up to date. When the declaration is complete, a rebuild happens exactly when something it depends on changed; when it is missing an input, the target is considered up to date while its output is stale.

Missing inputs are the dangerous failure because they are silent. A build that reads a file it did not declare will succeed on a clean machine and fail on an incremental one, and the developer who sees the difference learns to distrust incremental builds rather than to fix the declaration. The discipline that prevents this is enforcement: the build system should refuse undeclared reads rather than tolerate them.

Primary sources: <https://bazel.build/> and <https://www.cncf.io/>.

## Decision rules

- Record whether the build system enforces declared inputs or merely interprets them.
- Record the granularity of targets: file, package, or module level.
- Record the sandbox or hermeticity mechanism that detects undeclared reads.
- Record the targets whose declarations are known to be incomplete, and the plan for each.
- Record the graph's depth and width, since both affect rebuild cost.
- Record the mechanism that keeps the declaration in step with the code.

## Procedure

1. Record the enforcement regime and its detection mechanism.
2. Choose target granularity and record the reasoning.
3. Enable sandboxing so undeclared reads fail rather than succeed.
4. Audit the targets with the widest input declarations, which are usually the stale ones.
5. Record the mechanism that regenerates declarations from code.
6. Measure rebuild correctness with a clean-machine comparison.

## Anti-patterns

- Declaring the whole repository as an input to every target.
- Tolerating undeclared reads because they only fail sometimes.
- Target granularity so coarse that a one-line change rebuilds everything.
- Hand-maintained declarations with no generation or check.
- Trusting incremental correctness without a clean-build comparison.

## Done checklist

- [ ] Enforcement regime recorded.
- [ ] Granularity recorded.
- [ ] Sandboxing enabled and recorded.
- [ ] Wide declarations audited.
- [ ] Declaration generation recorded.
- [ ] Clean-versus-incremental compared.

The clean-machine comparison is the one measurement that catches an incomplete declaration before a developer does: a build that succeeds incrementally and fails from scratch proves the graph is missing an edge, and running that comparison on a schedule turns a class of intermittent confusion into a reported defect.


## Sources

- Build system documentation: <https://bazel.build/>
- Build and packaging practice: <https://www.cncf.io/>
- Reproducible builds reference: <https://reproducible-builds.org/>
