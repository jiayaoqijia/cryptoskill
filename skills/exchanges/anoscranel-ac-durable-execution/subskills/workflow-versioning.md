---
name: workflow-versioning
domain: software-engineering/workflow-versioning
trigger: "Changing a workflow definition while instances are running."
anti_trigger: "Not for API versioning, and not for database migrations."
scope: "Changing a definition while instances are running."
status: seedling
---

# Workflow versioning

## Standard

A workflow definition is code, and code changes while instances are in flight. An instance that started under version one and resumes under version two replays its history against code that no longer matches, and the divergence can produce a wrong branch, a missing step, or an exception during replay. Versioning is the discipline that prevents a deploy from corrupting work already in progress.

Two strategies cover most cases. The first keeps the old code path available for old instances, gated by a version check, so instances branch to the behaviour they started with and new instances take the new path. The second drains the old version before deploying the new, which is simpler but requires that in-flight work can be completed or cancelled within the deploy window.

Primary sources: <https://aws.amazon.com/builders-library/> and <https://www.enterpriseintegrationpatterns.com/>.

## Decision rules

- Record whether the workflow can be changed in place, and under what conditions.
- Record the versioning mechanism: a version gate in code, a separate definition, or a drain period.
- Record the maximum instance lifetime, since it bounds how long old code must be supported.
- Record what happens to an instance running when a version is retired.
- Record the change classes that require a new version: step order, added steps, changed compensation.
- Record the test that replays a recorded history against the new definition.

## Procedure

1. Record the maximum lifetime of an instance.
2. Choose the versioning mechanism and record the reason.
3. Record which changes require a new version.
4. Record the retirement path for the old version.
5. Replay a recorded history against the new definition as a test.
6. Write the policy with the retirement condition.

## Anti-patterns

- Editing a running workflow's definition without a version gate.
- Adding a step in the middle, which shifts every subsequent decision.
- Retiring an old version while instances still depend on it.
- Assuming a drain period is short because deploys are frequent.
- Testing only new instances and never a resumed one.

## Done checklist

- [ ] Change-in-place conditions recorded.
- [ ] Versioning mechanism recorded.
- [ ] Maximum instance lifetime recorded.
- [ ] Change classes requiring a version recorded.
- [ ] Retirement path recorded.
- [ ] Replay test recorded.

The replay test is the cheapest check available and the most often skipped: a recorded history from production, replayed against the new definition, catches divergence before the deploy rather than after the first resumed instance fails, and the recorded history is already available in the engine's store.


## Sources

- Workflow and deployment practice: <https://aws.amazon.com/builders-library/>
- Versioning patterns: <https://www.enterpriseintegrationpatterns.com/>
- Release context: <https://sre.google/>
