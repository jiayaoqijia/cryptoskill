---
name: detection-engineering
domain: security-hardening/detection-engineering
trigger: "Writing or assessing a detection as an engineered, tested artifact."
anti_trigger: "Not for building the preventive control itself, and not for tool selection."
scope: "Writing detections as tested code with measured precision, not grep patterns."
status: seedling
---

# Detection engineering

## Standard

A detection is a query over telemetry with a claim attached: that its output correlates with something worth acting on. Engineering it means treating that claim as a hypothesis — the detection is written, tested against known-bad and known-benign data, its false-positive rate is measured before deployment, and its precision is tracked after. A detection that never measured its own noise is an alarm, not a control.

The unit of quality is coverage against a named behavior, verified end to end. A detection that fires on the test dataset but not on the telemetry the estate actually produces covers nothing; a detection that fires on both but whose alert nobody can act on within the shift covers nothing either. The engineering loop is: name the technique, generate the test data, write the detection, measure it, deploy, and re-measure on live volume.

Primary sources: <https://www.cisa.gov/> and <https://attack.mitre.org/>.

## Decision rules

- Name the behavior the detection targets in adversary terms, not vendor terms.
- Write test data for the behavior and for the benign lookalikes before writing the rule.
- Measure false positives on representative volume before enabling alerting.
- Record the detection's data dependencies: which log sources its coverage silently requires.
- Version detections like code, with change history and an owner.
- Re-measure periodically; telemetry drifts and the rule's precision decays.

## Procedure

1. State the target behavior and the telemetry that carries it.
2. Build test cases: positive, benign lookalike, and absence.
3. Write and run the rule; record precision on all three.
4. Record dependencies and failure modes when a source degrades.
5. Deploy with an owner and a review date.
6. Re-measure on live volume and record the drift.

## Anti-patterns

- Deploying a rule on unmeasured volume and discovering the noise after.
- Treating a community rule as tested because it was shared.
- Ignoring coverage whose required log source is not actually collected.
- Removing a noisy rule without recording what coverage was lost.
- No owner, so nothing decays visibly.

## Done checklist

- [ ] Behavior named in adversary terms.
- [ ] Test cases cover positive, lookalike, and absence.
- [ ] Precision measured before enabling.
- [ ] Data dependencies recorded.
- [ ] Owner and review date assigned.
- [ ] Live drift re-measured.

## Sources

- Adversary behavior reference: <https://attack.mitre.org/>
- Operational guidance: <https://www.cisa.gov/>
- Detection framework context: <https://csrc.nist.gov/>
