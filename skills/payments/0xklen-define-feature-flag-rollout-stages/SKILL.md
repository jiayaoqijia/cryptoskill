---
name: define-feature-flag-rollout-stages
description: Use when a feature needs to reach users gradually. Defines the flag, the staged percentages, the gate metrics, and the rollback trigger before the first cohort is enabled.
---

# Define feature-flag rollout stages

A flag without stages is just a switch someone flips at 100%. This skill plans the path from internal to everyone, with a measured gate between each step.

## Procedure

1. Name the flag in an expiration-friendly form `release.<feature>.enabled` and set an owner and a removal date in `rollout.md`.
2. Define the stages: `off -> internal -> 1% -> 5% -> 25% -> 100%`, adjusting the tail to your traffic so each stage has enough events (aim for a few hundred users per stage).
3. Attach a gate metric to each stage transition (error rate, latency p95, a conversion or completion metric) and the threshold that holds it back.
4. Set the observation window per stage (e.g. 24 hours or one business cycle) so seasonality does not fool the read.
5. Define the rollback trigger and how it fires: flag off when `error_rate > 2x baseline` for five minutes, or a p95 latency breach.
6. Ensure the flag is read at the right granularity (per request, not cached at boot) so rollback takes effect without a deploy.
7. Confirm both paths are tested: with the flag on and off, including the off path for users who already saw it.
8. Plan the cleanup: flip off, delete the flag code, and land a PR removing the branches, with the date recorded.
9. Record the baseline values for each gate metric before the first stage, or you have nothing to compare against.
10. Check whether the feature interacts with other active flags, and sequence the rollouts to avoid confounding.

11. Name who watches each stage and for how long before it advances, so the gate has an owner.

## Pitfalls

- Staging by percentage of requests rather than users, so one user sees both variants and gets confused.
- No gate metric, making the stages a formality that always advances on schedule.
- A flag cached at startup, so "rollback" requires a restart and takes minutes.
- Leaving the flag in code for years, doubling the branches every future change must handle.
- Testing only the `on` path, so the `off` path breaks the first time it is disabled.
- Enabling the flag for a percentage too small to reach statistical signal before the schedule advances.
- Forgetting to expose the flag state in logs, so a rollback cannot be tied to the affected cohort.

- Advancing a stage because the calendar says so, not because the gate metric cleared.

## Verification

    grep -cE 'stage|%' rollout.md; grep -c 'rollback\|gate metric' rollout.md

Report the stage list with gate metrics, the rollback trigger, and the flag's removal date.
