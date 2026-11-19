---
name: replay-regression
domain: software-engineering/replay-regression
trigger: "Using recorded runs to test a changed agent."
anti_trigger: "Not for live tracing, and not for debugging one incident."
scope: "Recorded trajectories as regression baselines."
status: seedling
---

# Replay regression

## Standard

A recorded trajectory — a past run's request, tool calls, and results — becomes a regression input by fixing it and re-running the agent against its first inputs with its recorded tool responses held still: same request, same external world, changed brain. The new agent's behaviour compared against the old is a diff of what changed, isolated from what the world did.

The isolation is the value, and the discipline is honest about what isolates. Determinism cannot be assumed for the model; a temperature or provider version change can alter the path even without a spec change. The comparison graph is therefore baselined: a known-good agent passes its scenario set; candidate changes are compared to baseline results under identical conditions; any result requiring further comparison is re-run with variance sensitive enough to distinguish signal from nondeterminism.

Primary sources: <https://arxiv.org/abs/2308.03688> and <https://martinfowler.com/articles/practical-test-pyramid.html>.

## Decision rules

- Fix the recorded request and all tool responses; run the new agent against them.
- Compare candidate against a known-good baseline under identical conditions.
- Never assert the changed agent matches the old exactly — the point of change is change.
- Diff the trajectory, not just the answer: where paths split tells you what changed.
- Reruns before verdicts: variance-sensitive, never single-run if nondeterministic.
- Fixed-world replay stays within its honest limit: it isolates the agent, not the world.

## Procedure

1. For each scenario, fix the recorded request and tool responses as inputs.
2. Run the candidate agent against the fixed world.
3. Diff the trajectory against the baseline run of the same scenario.
4. Classify each diff: intended change, scope leak, regression, or variance.
5. Rerun if variance is suspected; a stable reproducing difference is a real finding.
6. Record per-scenario outcome into the harness record's ship/no-ship section.

## Anti-patterns

- Treating any behavioural difference from the old agent as a regression.
- Comparing new-run results against stale thresholds the spec rewrite did not update.
- Declaring success/failure from a single run against a nondeterministic model.
- Averaging runs to smooth over a rare but real severity.
- Asserting exact trajectory equality when the spec explicitly changed the flow.

## Done checklist

- [ ] Request and tool responses fixed per scenario.
- [ ] Baseline run established under current conditions.
- [ ] Trajectory diff computed and classified per difference.
- [ ] Variance distinguished before verdict.
- [ ] Intended changes separated from scope leaks.
- [ ] Outcome recorded per scenario in the harness record.

## Sources

- Agent evaluation under controlled environments: <https://arxiv.org/abs/2308.03688>
- Test pyramid discipline: <https://martinfowler.com/articles/practical-test-pyramid.html>
- Preregistration for pre-stated comparisons: <https://osf.io/prereg/>
