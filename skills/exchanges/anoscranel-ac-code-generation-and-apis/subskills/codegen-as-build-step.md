---
name: codegen-as-build-step
domain: software-engineering/codegen-as-build-step
trigger: "Wiring codegen into a build so it runs when it must."
anti_trigger: "Not for the build's caching and graph mechanics."
scope: "Inputs, outputs, freshness, and who owns the step."
status: seedling
---

# Codegen as a build step

## Standard

A generation step turns inputs into source files, and the build has three ways to treat the output: generate fresh every build, generate on demand when output is absent, or commit the output and regenerate by hand. Each is a freshness policy, and each fails differently — every-build hides a broken generator inside a broken everything; on-demand lets stale output ship; committed output drifts silently until something consumes a truth that no longer exists.

The decision that matters most is ownership. A generated file has an owner (the step) and a rule (hands off), and both must be machine-enforced — a lint rule, a header line, a review guard — because the person who edits a generated file is usually not the person who generated it, and the edit survives until the next run reverts it.

Primary source: <https://www.openapis.org/>.

## Decision rules

- Record the step's inputs, its outputs, and its freshness policy.
- Mark every generated output with a header identifying the generator and forbidding edits.
- Enforce the no-edit rule mechanically, not by convention.
- Make the step fail loudly when its input is missing, rather than emitting empty output.
- Record whether output is committed, and if so, the drift check that detects a stale artifact.
- Record who owns the step's configuration and who can change its inputs.

## Procedure

1. List the generators, their inputs, and their outputs.
2. Choose a freshness policy per generator and justify it.
3. Add headers to outputs and a mechanical no-edit guard.
4. Add a missing-input failure to the step.
5. If output is committed, add a CI drift check: regenerate and diff.
6. Record owners for configuration and inputs.

## Anti-patterns

- Editing a generated file to fix a build.
- Silent fallback when an input is missing.
- Output committed with no drift check.
- A freshness policy chosen by inertia rather than by failure analysis.
- No owner recorded, so the step's configuration decays.

## Done checklist

- [ ] Generators, inputs, outputs listed.
- [ ] Freshness policy chosen per generator.
- [ ] Headers and no-edit guard in place.
- [ ] Missing-input failure added.
- [ ] Drift check added where output is committed.
- [ ] Owners recorded.

A further distinction is worth recording: whether the generator produces files humans read at review time, or artifacts consumed only by the machine. The first kind benefits from stable, diffable output; the second from speed and can be regenerated per build. The freshness policy that suits one is wasteful for the other.

## Sources

- OpenAPI specification as a generation input: <https://www.openapis.org/>
- Reproducible build practices: <https://reproducible-builds.org/>
- Build step ownership practice: <https://martinfowler.com/articles/continuousIntegration.html>
