---
name: effect-measures
domain: research-operations/effect-measures
trigger: "Choosing the effect measure before pooling anything."
anti_trigger: "Not for the review's search and screening, and not for writing up."
scope: "Ratio, difference, and standardised measures, and when each distorts."
status: seedling
---

# Effect measures

## Standard

The effect measure is the currency of the entire synthesis, and choosing it after seeing the results converts a method decision into a result decision. Ratio measures — risk ratio, odds ratio, hazard ratio — express relative change and behave well when events are rare, but the odds ratio exaggerates the risk ratio as events become common, and a constant ratio is a changing difference. Absolute measures — risk difference, mean difference — answer the question a decision-maker actually faces but become unstable when events are rare.

Standardised measures — the standardised mean difference — exist to pool studies that used different scales, and the price is that the result lives in standard-deviation units rather than anything interpretable. For outcomes measured on a common scale, the raw mean difference is preferred precisely because it means something; standardisation is for genuinely incommensurable scales, not for convenience.

Primary sources: <https://training.cochrane.org/handbook/current/chapter-10> and <https://handbook-5-1.cochrane.org/chapter_9>.

## Decision rules

- Choose the effect measure before results are extracted, in the protocol.
- Match the measure to the outcome type: binary, continuous, time-to-event, rate.
- Prefer absolute measures when a decision depends on baseline frequency.
- Reach for standardisation only when scales genuinely differ across studies.
- Record the direction of benefit per outcome once, and keep it fixed.
- Zero-event studies: record the handling — continuity correction or exclusion — in advance.

## Procedure

1. Classify the outcome type from the protocol.
2. List the plausible measures for that type.
3. Choose one, with the reason, before extraction.
4. Fix the benefit direction per outcome.
5. Decide the zero-event handling in advance.
6. Record measure and rationale; any later change is a protocol amendment.

## Anti-patterns

- Switching measures after seeing which is more favourable.
- Reporting odds ratios as if they were risk ratios in common-event outcomes.
- Standardising when a common scale exists.
- Pooling measures that mix directions across outcomes into one story.
- Letting software defaults choose the measure silently.

## Done checklist

- [ ] Measure chosen in the protocol, with reason.
- [ ] Outcome type matched.
- [ ] Absolute versus relative justified by the decision use.
- [ ] Standardisation justified by scale difference.
- [ ] Benefit direction fixed.
- [ ] Zero-event handling fixed in advance.

A further discipline is direction-keeping across a multi-outcome synthesis: when one outcome is better smaller and another better larger, a table of pooled estimates without the direction label invites misreading, and the protocol's per-outcome direction map is the only thing that prevents an analyst or a reader from inverting a finding while every number stays technically correct.

## Sources

- Cochrane Handbook, meta-analysis chapter: <https://training.cochrane.org/handbook/current/chapter-10>
- Cochrane Handbook 5.1, summary statistics: <https://handbook-5-1.cochrane.org/chapter_9>
- Reporting guideline directory: <https://equator-network.org/>
