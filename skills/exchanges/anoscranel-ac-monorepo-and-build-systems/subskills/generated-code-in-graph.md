---
name: generated-code-in-graph
domain: software-engineering/generated-code-in-graph
trigger: "Putting code generation inside the build graph."
anti_trigger: "Not for runtime code generation, and not for template design."
scope: "Codegen as a graph node, and the stale-output traps."
status: seedling
---

# Generated code in the graph

## Standard

Generated code is a build output like any other, and it belongs in the graph with declared inputs and a declared output. When it is committed instead, the repository carries artifacts that can drift from the generator; when it is generated outside the graph, the build can consume a stale copy without knowing it.

The traps are specific. A generator that reads its inputs from the filesystem rather than from declared dependencies will not rerun when they change. An output written to a path the build also reads as source creates an ordering dependency that may not be declared. And a generator whose output depends on its own previous output will produce different results on the first run and on subsequent ones.

Primary sources: <https://bazel.build/> and <https://reproducible-builds.org/>.

## Decision rules

- Record which generated artifacts are committed and which are produced in the build.
- Record each generator's declared inputs and outputs.
- Record whether the generator is deterministic across runs.
- Record the ordering dependency between generation and consumption.
- Record the mechanism that prevents a stale committed copy being read.
- Record the review process for a generated diff, which is often unreadable.

## Procedure

1. Classify artifacts as committed or generated.
2. Declare inputs and outputs for each generator.
3. Verify determinism by running the generator twice.
4. Declare the ordering between generation and consumption.
5. Add a check that fails when a committed artifact differs from generated output.
6. Record the review approach for generated diffs.

## Anti-patterns

- Committing generated artifacts with no check that they match the generator.
- A generator reading undeclared files.
- Writing output into a source directory without declaring the dependency.
- A generator that is not idempotent.
- Reviewing a large generated diff as if it were hand-written.

## Done checklist

- [ ] Artifacts classified.
- [ ] Generator inputs and outputs declared.
- [ ] Determinism verified.
- [ ] Ordering declared.
- [ ] Stale-artifact check in place.
- [ ] Review approach recorded.

The check that a committed artifact matches its generator is worth running in CI rather than locally, because the failure is a drift that accumulates: a generator change that was not followed by a regeneration leaves a repository that builds correctly until someone regenerates, at which point an unrelated diff appears in the change.


## Sources

- Build graph documentation: <https://bazel.build/>
- Reproducible builds reference: <https://reproducible-builds.org/>
- Code review practice: <https://martinfowler.com/>
