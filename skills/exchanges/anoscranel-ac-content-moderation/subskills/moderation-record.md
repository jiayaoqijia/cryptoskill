---
name: moderation-record
domain: software-engineering/moderation-record
trigger: "Writing the record of the moderation system and its error rates."
anti_trigger: "Not for deciding policy, and not for the reviewer's case notes."
scope: "The written record: policies, thresholds, outcomes, error rates."
status: seedling
---

# Moderation record

## Standard

The moderation record is the document that makes the system reviewable: the policy hierarchy version in force, the taxonomy with its versions, classifier operating points with measured error rates, queue service levels and agreement statistics, the enforcement ladder with its override audit, and the appeal reversal rates in both error directions. It exists because a moderation system that cannot be reconstructed from its record cannot be audited, improved, or defended — only operated.

The headline section is the error budget in both directions: over-removal measured by appeal reversals, and under-removal measured by the false-negative intake. These two numbers, tracked per category over time, are the honest summary of the whole system, and trends in them are the early warning that thresholds, guidelines, or taxonomy have drifted. The record is append-only; changes to any operating point are dated amendments with the evidence that prompted them.

Primary sources: <https://transparency.meta.com/> and <https://en.wikipedia.org/wiki/Content_moderation>.

## Decision rules

- The record holds: policy versions, taxonomy versions, thresholds with error rates, queue levels, ladder versions, appeal statistics.
- Over-removal and under-removal are both tracked per category and dated.
- Every operating-point change is a dated amendment citing its evidence.
- Volume statistics are published on a cadence: items processed, actions, reversals.
- Override audits appear in the record, not in a separate log that dies with a tool.
- The record survives tooling changes; it is the system's memory, not a vendor's.

## Procedure

1. Assemble sections from the leaves: policy, taxonomy, classifiers, queues, ladder, appeals.
2. Compute the two-directional error budget per category for the current period.
3. Append the period's volume and outcome statistics with dates.
4. Record any operating-point changes as dated amendments with evidence.
5. Review the record on a cadence; carry trend findings into guideline review.
6. Version the record's own schema when sections change.

## Anti-patterns

- A record of volumes with no error rates.
- Amendments without dates or evidence.
- Over-removal tracked with under-removal absent.
- Override audits living outside the record.
- A record that cannot outlive the current tooling.

## Done checklist

- [ ] All six record sections present.
- [ ] Two-directional error budget per category, dated.
- [ ] Volume and outcome statistics appended per period.
- [ ] Operating-point changes as dated amendments.
- [ ] Override audits included.
- [ ] Record schema versioned.

## Sources

- Platform transparency reporting: <https://transparency.meta.com/>
- Content moderation overview: <https://en.wikipedia.org/wiki/Content_moderation>
- Regulatory context: <https://en.wikipedia.org/wiki/Digital_Services_Act>
