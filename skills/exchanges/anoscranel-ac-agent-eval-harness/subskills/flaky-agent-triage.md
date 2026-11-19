---
name: flaky-agent-triage
domain: software-engineering/flaky-agent-triage
trigger: "Deciding whether a failed agent run is a real defect."
anti_trigger: "Not for general software flakiness, and not for guardrail incidents."
scope: "Dividing nondeterminism from real defects."
status: seedling
---

# Flaky agent triage

## Standard

An agent harness against a nondeterministic model produces failures that are not defects: the same scenario passes and fails on alternate runs. Running twice is quick and wrong — twice-unstable may still be variance, and twice-stable may still be luck. The triage discipline treats each failing scenario as a question with tiers: rerun to observe, isolate the variance source (model, tool double, harness bug, environment), and only then classify as real defect or nondeterminism to be tolerated-and-bounded.

The variance budget is stated. A tolerance threshold — pass-rate-at-n over reruns, bounded below — separates accepted nondeterminism from instabilities that mask real defects. Scenarios whose failure rate sits at the boundary are reexamined on every harness run, while stable-pass rate below threshold is treated as a red flag to investigate, not a pass to hide.

Primary sources: <https://en.wikipedia.org/wiki/Flaky_test> and <https://testing.googleblog.com/>.

## Decision rules

- No verdict from a single run of a scenario known to have variance.
- Rerun tier one: same conditions, observe; record pass/fail per attempt.
- Isolate tier two: temperature pinned, doubles fixed, harness code inspected.
- Classify: real defect, harness defect, or accepted nondeterminism.
- State the acceptance threshold for each scenario up front; below-threshold is investigated.
- A defect that reproduces across variance tiers is a defect regardless of luck.

## Procedure

1. Rerun the failing scenario to gauge the failure's stability.
2. Pin variance sources one at a time; narrow the cause.
3. If the harness or double is at fault, fix and re-enter the suite.
4. If the agent fails deterministically, file a defect with a reproducing entry.
5. If variance remains, bound it with a rerun protocol and threshold.
6. Record both the finding and the threshold in the harness record.

## Anti-patterns

- Rerun-until-pass treated as a clean result.
- Both variable outcomes suppressed to protect an appealing summary metric.
- Model nondeterminism assumed where the harness double had drifted.
- Rerunning only failures, never verifying passes near the threshold.
- A blanket global retry count masking the root cause of each instability.

## Done checklist

- [ ] Rerun observed, pass/fail per attempt recorded.
- [ ] Variance source isolated.
- [ ] Classified as defect, harness, or accepted.
- [ ] Threshold stated up front.
- [ ] Defect reproduced across variance tiers when present.
- [ ] Tolerated bounds recorded per scenario.

## Sources

- Flaky test discipline: <https://en.wikipedia.org/wiki/Flaky_test>
- Google testing practice: <https://testing.googleblog.com/>
- Software testing overview: <https://en.wikipedia.org/wiki/Software_testing>
