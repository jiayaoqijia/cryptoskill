---
name: appeals-and-error-correction
domain: software-engineering/appeals-and-error-correction
trigger: "Building the appeal path as the system's error-rate measurement."
anti_trigger: "Not for enforcement action design, and not for queue calibration."
scope: "Appeals as the system's error-rate measurement."
status: seedling
---

# Appeals and error correction

## Standard

An appeal is the user's route to challenge a moderation decision, and from the engineering side it is the only measurement channel that reaches the system's false-positive rate on real cases. A moderation operation that receives appeals, resolves them by policy rather than reflex, and tracks reversal rates per category has an error measurement; one that treats appeals as a nuisance to be deflected has opinions about its own accuracy.

The design holds two paths in one queue: the appeal review re-examines the original decision against the rule and context, with a reviewer who did not make the first decision. Reversal rates are computed per category, per classifier threshold, and per enforcement rung — the resulting series feeds guideline review and threshold recalibration. The path to correct false negatives — content that stayed up but should have been removed — is a separate escalation intake, and both error directions are recorded, because a system that only measures its over-removal has calibrated only half its errors.

Primary sources: <https://en.wikipedia.org/wiki/Content_moderation> and <https://en.wikipedia.org/wiki/Digital_Services_Act>.

## Decision rules

- Every automated and human enforcement action carries a stated appeal route.
- Appeal review is performed by a reviewer other than the original decider.
- Reversal outcomes are recorded per category, threshold, and enforcement rung.
- The false-negative path exists separately and its intake is monitored.
- Both error directions are reported together in the moderation record.
- Appeal service level and grant rate are tracked, not concealed.

## Procedure

1. Attach the appeal route to every enforcement action's notification.
2. Route appeals to reviewers excluding the original decider.
3. Record the outcome: upheld, reversed, or adjusted, with the reason.
4. Compute reversal rates per category and per threshold monthly.
5. Feed persistent reversal clusters into guideline and threshold review.
6. Stand up the false-negative intake and record both error directions.

## Anti-patterns

- Appeals handled by the original reviewer with no independence.
- Reversal rates computed but never fed back into thresholds.
- Measuring only over-removal while ignoring missed violations.
- Appeal routes buried so users cannot find them.
- Treating a high reversal rate as a reviewer problem rather than a system signal.

## Done checklist

- [ ] Appeal route attached to every action.
- [ ] Independent appeal reviewer guaranteed.
- [ ] Outcomes recorded per category and threshold.
- [ ] False-negative intake exists and is monitored.
- [ ] Both error directions reported.
- [ ] Reversal clusters fed back into guidelines.

## Sources

- Content moderation overview: <https://en.wikipedia.org/wiki/Content_moderation>
- Regulatory context: <https://en.wikipedia.org/wiki/Digital_Services_Act>
- Platform transparency reporting: <https://transparency.meta.com/>
