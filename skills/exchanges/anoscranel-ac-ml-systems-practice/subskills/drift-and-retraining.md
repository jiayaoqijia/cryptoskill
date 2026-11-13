---
name: drift-and-retraining
domain: software-engineering/drift-and-retraining
trigger: "Designing drift detection and the retraining decision."
anti_trigger: "Not for training-time data validation, and not for serving skew."
scope: "Data and concept drift, monitoring against a fixed training reference, and the retraining decision with its costs."
status: seedling
---

# Drift and retraining

## Standard

Skew is the pipeline lying differently at its two ends while the world stands still. Drift is the world moving. Data drift is the input distribution shifting: a new user population, a device mix change, an upstream format change. Concept drift is the relationship between features and target moving: fraud patterns evolve, language use changes, behaviour follows the news. Both are invisible to a frozen test set, which describes the past by design — and both degrade a live metric without any error being raised anywhere.

Detection only works against a fixed reference. Live feature distributions are compared to the training-time snapshot; a rolling window drifts with the very data it is meant to check, and two drifted copies of the world agree with each other. Prediction distributions are monitored as well as features, because they catch degradation the feature view cannot name.

Retraining is the response with the highest cost and the most failure modes. It is a decision triggered by measured degradation against a pre-registered policy, not a reflex. Retraining a pipeline whose features leak or whose upstream data is silently wrong does not fix the system; it re-fits the bug to more data.

Primary sources: <https://martinfowler.com/articles/cd4ml.html> and <https://developers.google.com/machine-learning/guides/rules-of-ml>.

## Decision rules

- Compare live distributions against the frozen training reference, never a rolling window.
- Monitor prediction distributions alongside feature distributions.
- Pre-register which features and which movement thresholds alarm; alert fatigue from unranked alarms is a monitoring failure.
- Record quantile or index values with timestamps, not just pass/fail, so the movement's shape is visible afterwards.
- Tie retraining to measured metric degradation on live-labelled data or a stated proxy, per policy fixed before drift appears.
- Verify the cause is drift before retraining: a pipeline change or an upstream defect can imitate drift precisely.
- After any retraining, evaluate on a fresh frozen segment and re-record the full lineage before promotion.

## Procedure

1. Snapshot the training-time feature and prediction distributions with the artefact version.
2. Pre-register the monitored features, the comparison statistic, and the alarm thresholds.
3. Fix the retraining policy: trigger metric, evaluation segment, approval path.
4. Run the comparison on a fixed cadence; store values and verdicts.
5. When degradation triggers, diagnose before acting: pipeline change, upstream defect, or drift.
6. If drift is confirmed, retrain, evaluate on the fresh segment, and record before-and-after with the new lineage.

## Anti-patterns

- A rolling reference that drifts with the data it is checking.
- Retraining on suspicion without a measured trigger.
- Retraining over leaking or corrupted features, which re-fits the defect.
- Unranked alarms on every feature's every movement.
- Promoting a retrained artefact without evaluating it against a fresh frozen segment.

## Done checklist

- [ ] Training reference snapshot stored with the artefact.
- [ ] Monitored features and thresholds pre-registered.
- [ ] Prediction distributions monitored alongside features.
- [ ] Retraining policy fixed before any drift, with its trigger metric.
- [ ] Diagnosis step between alarm and retraining.
- [ ] Fresh-segment evaluation and updated lineage after retraining.

## Sources

- Continuous delivery for ML: <https://martinfowler.com/articles/cd4ml.html>
- Rules of ML: <https://developers.google.com/machine-learning/guides/rules-of-ml>
- MLOps practice guide: <https://ml-ops.org/>
