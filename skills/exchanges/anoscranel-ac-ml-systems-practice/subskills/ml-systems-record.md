---
name: ml-systems-record
domain: software-engineering/ml-systems-record
trigger: "Writing the record of an ML system and its decisions."
anti_trigger: "Not for the model's mathematical writeup, and not for the training run log itself."
scope: "The written record: lineage, promises, failure paths, monitoring policy, and every promotion decision."
status: seedling
---

# ML systems record

## Standard

The record states what the system is, what it promises, how it can fail, and every decision made about it. For an ML component, the identity is a lineage triple: the artefact, the feature set, and the dataset it was trained on. A model file alone is not an identity; the same weights with different feature definitions are a different system, and promotions, rollbacks, and incident reviews all need the full triple to mean anything.

The promises section is the part most often omitted and most often needed. Every ML component makes implicit promises — about input domain, latency, accuracy on a population, behaviour on missing fields — and the record makes them explicit so that a serving change or a retrain can be checked against them. A promise that is not written down is not testable, and an untested promise is a future incident.

Primary sources: <https://martinfowler.com/articles/cd4ml.html> and <https://ml-ops.org/>.

## Decision rules

- Record the lineage triple for every promoted version: artefact, feature set, dataset.
- Record the bundled preprocessing — encoders, scalers, vocabularies — as part of the artefact identity.
- State the promises: input domain, expected population, latency, quality metric, missing-field behaviour.
- Record the failure paths: what degradation looks like in each monitored signal, and the rung it falls to.
- Record every promotion and rollback decision with its evidence, dated.
- Record the monitoring policy — features watched, thresholds, retraining trigger — as a dated policy version.
- Amend by dated entries; a rewritten history hides the very decisions the record exists to keep.

## Procedure

1. Record the current lineage triple and preprocessing bundle.
2. Write the promises section, with each promise testable as stated.
3. Write the failure paths against the monitoring signals.
4. Record the monitoring and retraining policy with its version and date.
5. On every promotion, rollback, or retrain: append the decision, the evidence, and the new lineage.
6. Review the record at each monitoring-policy change and each incident.

## Anti-patterns

- A record that names the model file but not the feature set or dataset.
- Promises kept in a team's memory rather than the record.
- Promotions recorded without their evidence.
- A monitoring policy that exists in alert configuration but not in the record.
- Editing past entries after an incident to make the path look cleaner.

## Done checklist

- [ ] Lineage triple recorded per version.
- [ ] Preprocessing bundle recorded as part of identity.
- [ ] Promises stated and testable.
- [ ] Failure paths written per signal.
- [ ] Promotion and rollback decisions dated with evidence.
- [ ] Monitoring and retraining policy versioned; amendments dated.

## Sources

- Continuous delivery for ML: <https://martinfowler.com/articles/cd4ml.html>
- MLOps practice guide: <https://ml-ops.org/>
- Rules of ML: <https://developers.google.com/machine-learning/guides/rules-of-ml>
