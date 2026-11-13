---
name: queues-and-calibration
domain: software-engineering/queues-and-calibration
trigger: "Building the human review pipeline and keeping reviewers aligned."
anti_trigger: "Not for classifier training, and not for enforcement action design."
scope: "Routing, reviewer guidance, and inter-rater agreement."
status: seedling
---

# Queues and calibration

## Standard

The moderation queue routes items that classifiers could not decide to humans. Its engineering concerns are routing, load, and consistency. Routing sorts items so the right reviewer specialty sees the right category at the right urgency; load management keeps queue depth within a stated service level, because a moderation backlog measured in weeks is a policy failure even when every eventual decision is correct; consistency keeps reviewers aligned with each other and with the policy.

Consistency is measured, not assumed. Inter-rater agreement is computed on shared samples of blind-duplicated items, and the resulting statistic is tracked per category and per reviewer cohort over time. Reviewer guidelines are calibrated against these measurements: where agreement falls, the guidelines or the taxonomy get an explicit fix. A moderation operation that cannot state its agreement rate is guessing at its own consistency.

Primary sources: <https://en.wikipedia.org/wiki/Content_moderation> and <https://transparency.meta.com/>.

## Decision rules

- Route by category and severity; every item carries a routing key and a deadline.
- Queue depth is monitored against a stated time-to-decision level; breaches are incidents.
- A fraction of items is blind-duplicated to shared queues for agreement measurement.
- Inter-rater agreement is computed per category and tracked over time.
- Reviewer guidelines are updated against measured disagreement, not anecdotes.
- Reviewer workload and exposure to graphic content are engineered concerns, with rotation and wellness support stated in operations.

## Procedure

1. Define routing keys from taxonomy categories and severity tiers.
2. Set the time-to-decision service level per severity; wire depth alerts.
3. Configure blind duplication of a sampled fraction into shared queues.
4. Compute inter-rater agreement per category monthly; record the series.
5. Feed persistent disagreement categories into guideline and taxonomy review.
6. Document reviewer rotation and wellness support as part of the queue design.

## Anti-patterns

- Queue depth as an invisible metric with no service level.
- Agreement never measured, so drift is only visible in appeals.
- Guidelines rewritten from a single bad case.
- Routing by reviewer availability rather than category specialty.
- Treating reviewer wellbeing as outside engineering.

## Done checklist

- [ ] Routing keys and deadlines defined.
- [ ] Queue service level with breach alerts.
- [ ] Blind duplication configured and sampled.
- [ ] Agreement computed per category, tracked over time.
- [ ] Guideline updates tied to measured disagreement.
- [ ] Rotation and wellness support documented.

## Sources

- Content moderation overview: <https://en.wikipedia.org/wiki/Content_moderation>
- Platform transparency reporting: <https://transparency.meta.com/>
- Regulatory context: <https://en.wikipedia.org/wiki/Digital_Services_Act>
