---
name: champion-challenger-and-canary
domain: software-engineering/champion-challenger-and-canary
trigger: "Deploying a model into comparison rather than a blind cutover."
anti_trigger: "Not for A/B measurement of product features, and not for code rollout mechanics."
scope: "Deploying models into comparison, not into the void."
status: seedling
---

# Champion-challenger and canary

## Standard

A new model version replacing the champion outright is the highest-risk deployment pattern available: if it is worse, the first evidence is production. Champion-challenger runs the new model in shadow — fed the same live inputs, its predictions logged but not served — until offline evaluation says it is worth a live comparison; canary then serves it to a small, stable slice of traffic while the champion serves the rest.

The distinction that keeps this honest is measurement discipline. The online comparison is an experiment with the same requirements as any other: a pre-registered success metric, a guardrail metric with a stopping rule, and a horizon fixed in advance. The deployment mechanic is separate from the measurement: this leaf owns the mechanics of comparison deployment, and the experiment itself must meet evaluation standards before its result is trusted.

Primary sources: <https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning> and <https://martinfowler.com/articles/cd4ml.html>.

## Decision rules

- Shadow the challenger on live inputs before any live traffic sees it.
- Log challenger predictions with the identifier of the champion prediction they would have replaced.
- Canary on a stable, hash-assigned traffic slice; the assignment must not change mid-canary.
- Pre-register the comparison metric, guardrails, and stop conditions before the canary starts.
- Roll back mechanically: the champion artefact is retained and one switch restores it.
- Promote only on the pre-registered criteria; a canary that "looks fine" is not evidence.

## Procedure

1. Verify the challenger's serving path handles live inputs within latency budget, in shadow.
2. Compare shadow predictions against champion outcomes offline to justify live traffic.
3. Assign a canary slice by stable hash; record the assignment rule.
4. Serve the canary; watch guardrails at the pre-declared cadence and stop rule.
5. At horizon, evaluate the pre-registered metric and decide: promote, extend, or retire.
6. On promotion, retain the champion as the rollback target; record both versions.

## Anti-patterns

- Replacing the champion because offline evaluation was good; offline is the entry ticket, not the verdict.
- A canary on a self-selected slice — the newest users, internal accounts.
- Comparing canary and champion on different traffic, times of day, or metric windows.
- Keeping the canary running past its horizon until the metric turns favourable.
- Deleting the champion artefact on promotion day.

## Done checklist

- [ ] Challenger shadowed and verified on live inputs.
- [ ] Canary slice stable and hash-assigned.
- [ ] Metric, guardrails, stop rule pre-registered.
- [ ] Champion retained as one-switch rollback.
- [ ] Horizon fixed in advance and honoured.
- [ ] Decision taken on the pre-registered criteria.

## Sources

- MLOps continuous delivery architecture: <https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning>
- CD4ML, continuous delivery for ML: <https://martinfowler.com/articles/cd4ml.html>
- MLOps overview: <https://ml-ops.org/>
