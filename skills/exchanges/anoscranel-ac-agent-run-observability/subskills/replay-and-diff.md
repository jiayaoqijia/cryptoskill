---
name: replay-and-diff
domain: software-engineering/replay-and-diff
trigger: "Reproducing a stored run to see exactly what it did."
anti_trigger: "Not for live steering, and not for offline batch evaluation."
scope: "Reproducing a run from its trace; diffing two runs."
status: seedling
---

# Replay and diff

## Standard

Replay reconstructs what a run did from its stored trajectory: which calls were made, with what inputs, in what order, producing what outputs. The prerequisite is capture-side fidelity — full arguments, full returns, and both prompts and tool manifests recorded at start. A replayable trace turns a bug report into an inspection: the failing run already contains everything needed to see the failure, without re-running the agent against live tools or hoping the failure reproduces.

Diff is the comparison instrument: two runs over the same task, differing in one deliberate change — a prompt version, a model swap, a tool description edit — inspected step by step. The unit of comparison is the trajectory: where the runs diverge, which step first differs, and whether the change fixed the intended step without disturbing the rest. The discipline is one change per diff; a comparison over two changes attributes nothing.

Primary sources: <https://opentelemetry.io/docs/specs/semconv/gen-ai/> and <https://langfuse.com/docs>.

## Decision rules

- Verify capture fidelity first; a replay is only as honest as its stored spans.
- Use replay for inspection, not for re-execution against live systems; the stored outputs are the record.
- Diff one deliberate change at a time; label the change on the comparison.
- Compare at step granularity: the first divergent step is the finding.
- Record tool manifests and prompt versions so replay can identify mock targets.
- Include replay in the harness contract of the run-record from the beginning; retrofitting replay onto partial traces fails quietly.

## Procedure

1. Select the run by identifier; load its spans and manifests.
2. Walk the trajectory in order; verify each step's inputs are present and complete.
3. Render the trajectory for inspection, step by step, at the level the questions require.
4. For a diff: select two runs over the same task; align steps; locate the first divergence.
5. Attribute the divergent behaviour to the single labelled change.
6. Record the finding beside the comparison, with both run identifiers.

## Anti-patterns

- Replaying against live tools; the record, not the world, is the object of study.
- Diffing two runs with multiple changes between them.
- Comparing only final answers; the useful diff is where the trajectories split.
- Replay built after traces exist; the missing fields surface at the worst time.
- Treating an unexplainable divergence as noise rather than as a finding.

## Done checklist

- [ ] Run replayed from stored spans alone.
- [ ] Step inputs verified complete.
- [ ] Diff over one labelled change.
- [ ] First divergent step located.
- [ ] Manifests and prompts present for mocking.
- [ ] Finding recorded with both run identifiers.

## Sources

- GenAI trace conventions: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Trace inspection: <https://langfuse.com/docs>
- Agent evaluation background: <https://arxiv.org/abs/2308.03688>
