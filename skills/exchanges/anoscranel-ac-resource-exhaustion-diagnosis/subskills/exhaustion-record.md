---
name: exhaustion-record
domain: software-engineering/exhaustion-record
trigger: "Writing the record of a resource exhaustion episode and its resolution."
anti_trigger: "Not for capacity planning documents (that is ac-chaos-and-capacity-testing)."
scope: "The written record: resource, curve, verdict, and the limit change made."
status: seedling
---

# Exhaustion record

## Standard

The exhaustion record captures one episode: the resource that ran out, the curve it followed, the verdict on the cause, and the change that was made. It exists because exhaustion recurs. The same pool will saturate again next quarter under a bigger campaign, and the person diagnosing it then inherits either a documented curve and derivation or a cold start.

The record's most valuable line is the derivation of any limit that was changed. A number without its reasoning is exactly the inherited default this skill warns about — two years from now, someone will find a pool sized at forty-seven and have no idea whether that was a measurement or a typo. The derivation converts every future limit question into a diff against known evidence.

## Decision rules

- Record the resource, its symptom, the error verbatim, and the first timestamp.
- Attach the sampled curve data or its summary shape.
- Record the verdict — leak, saturation, or mis-set limit — with the evidence named.
- Record any limit change with its derivation, headroom reasoning, and date.
- Record the fix's verification: the symptom stopped and the curve behaves as predicted.
- Record the revisit condition under which the number should be re-derived.

## Procedure

1. Write the symptom, error text, and timeline.
2. Summarise the curve with its classification.
3. Record the verdict and the evidence it rests on.
4. Record the change with its derivation.
5. Verify the change and record the post-change curve.
6. State the revisit condition in workload terms.

## Anti-patterns

- Recording "raised the limit" with no derivation.
- No post-change verification, so the fix was never tested.
- Keeping the curve data nowhere, so the classification cannot be re-checked.
- Closing the episode at the restart rather than at the verified fix.
- A revisit condition stated as a date rather than a workload change.

## Done checklist

- [ ] Symptom and timeline recorded.
- [ ] Curve and classification recorded.
- [ ] Verdict with evidence recorded.
- [ ] Change with derivation recorded.
- [ ] Post-change verification recorded.
- [ ] Revisit condition recorded.

A record of this shape also serves the next limit decision directly: the derivations of past changes accumulate into a history of what this workload needed at each stage, so a future re-sizing can be a comparison against documented growth rather than a fresh guess.

## Sources

- Capacity record-keeping: <https://sre.google/workbook/chapter-capacity-planning/>
- Resource limit documentation practice: <https://learn.microsoft.com/en-us/azure/well-architected/>
- Linux limits configuration: <https://www.kernel.org/doc/html/latest/admin-guide/>
