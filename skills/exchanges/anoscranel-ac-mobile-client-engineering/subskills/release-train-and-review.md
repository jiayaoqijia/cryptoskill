---
name: release-train-and-review
domain: software-engineering/release-train-and-review
trigger: "Planning a mobile release that cannot be recalled once installed."
anti_trigger: "Not for web deployments with instant rollback, and not for store policy."
scope: "Store review latency, staged rollout, and the release that cannot be recalled."
status: seedling
---

# Release train and review

## Standard

A mobile release passes through a review whose duration you do not control and lands on devices you cannot reach again. That makes the release a train rather than a deployment: you cut a build, submit it, and wait, and during the wait the code is frozen because a change would require a new submission and a new queue position.

Staged rollout is the mitigation, and it is not a substitute for testing. A release published to one percent of the base gives you telemetry before the whole population has it, and you can halt the rollout if the crash rate moves, but you cannot uninstall what has already been installed. The choice is therefore about how much of the base to expose to a build you can only stop, not undo.

Primary sources: <https://developer.android.com/> and <https://developer.apple.com/>.

## Decision rules

- Record the review latency observed for recent submissions, not the published average.
- Record the freeze window: the period during which no change can enter the build.
- Record the staged rollout percentages and the metric that triggers a halt.
- Record what "halt" achieves, since already-installed copies remain.
- Record the server-side kill switch available for features shipped in the build.
- Record the rollback path for the backend, which is the only part that is reversible.

## Procedure

1. Record recent review durations and their variance.
2. Set the code freeze and communicate it before the cut.
3. Cut the build and submit, recording the submission time.
4. Publish to a small percentage and watch the halt metric.
5. Increase in steps, recording the metric at each step.
6. Record the outcome and the time to full rollout.

## Anti-patterns

- Treating a mobile release like a web deploy with rollback.
- Letting changes into the build after submission.
- Rolling out to a hundred percent on the first day.
- Setting a halt threshold that the baseline already exceeds.
- Assuming a halted rollout removes the build from devices.

## Done checklist

- [ ] Review latency recorded.
- [ ] Freeze window set and communicated.
- [ ] Rollout percentages and halt metric recorded.
- [ ] Halt semantics recorded.
- [ ] Kill switch recorded.
- [ ] Backend rollback path recorded.

## Sources

- Android release and staged rollout documentation: <https://developer.android.com/>
- Apple release and review guidance: <https://developer.apple.com/>
- Software delivery practice reference: <https://www.software.ac.uk/>
