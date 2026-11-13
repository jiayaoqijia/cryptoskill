---
name: reconciliation-tolerance
domain: software-engineering/reconciliation-tolerance
trigger: "Deciding when a difference between two systems is a defect."
anti_trigger: "Not for accounting judgement, and not for fraud investigation."
scope: "The difference at which a discrepancy is a defect."
status: seedling
---

# Reconciliation tolerance

## Standard

Two systems that should agree will differ by small amounts, and the engineering question is where the line sits between an accepted rounding difference and a defect. Without a stated tolerance every difference is investigated, which is unaffordable, or none is, which hides real errors among the noise.

The tolerance should be derived rather than chosen. A difference attributable to known rounding can be bounded by the arithmetic: the number of rounding points multiplied by the smallest unit. Anything beyond that bound is not rounding and deserves investigation. The record states the bound, its derivation, and the difference between the bound and a threshold set for convenience.

Primary sources: <https://www.ifrs.org/> and <https://www.iso20022.org/>.

## Decision rules

- Record the tolerance and its derivation from the arithmetic, not from preference.
- Record the number of rounding points between the two systems.
- Record whether the tolerance is absolute or relative, and the unit.
- Record the differences that exceed tolerance and their frequency.
- Record the escalation for a difference that recurs without explanation.
- Record the distinction between a tolerance and a materiality threshold, which are different questions.

## Procedure

1. Count the rounding points between the two systems.
2. Derive the bound from the points and the minor unit.
3. Record the tolerance and its derivation.
4. Classify exceeding differences by frequency and size.
5. Record the escalation path for unexplained recurring differences.
6. Record the separate materiality threshold if one exists.

## Anti-patterns

- Setting a tolerance by convenience and calling it rounding.
- A tolerance large enough to hide a systematic error.
- Investigating every difference and calling the noise a defect.
- Conflating tolerance with materiality.
- No escalation, so a persistent difference is absorbed as normal.

## Done checklist

- [ ] Tolerance recorded with derivation.
- [ ] Rounding points counted.
- [ ] Unit of tolerance recorded.
- [ ] Exceeding differences classified.
- [ ] Escalation path recorded.
- [ ] Materiality distinguished.

The bound derivation is worth writing out even when it feels obvious, because it is the only thing that distinguishes a tolerance from a wish: two rounding points and a two-decimal currency permit a difference of two minor units, and anything larger is not explained by the arithmetic regardless of how the threshold was set.


The recurrence test is what turns the tolerance from a filter into a diagnostic: a difference that stays within tolerance but recurs in the same direction every period is a bias rather than noise, and the tolerance that accepted it should be tightened once the pattern is recognised.


## Sources

- Financial reporting standards: <https://www.ifrs.org/>
- Payment and settlement standards: <https://www.iso20022.org/>
- Currency representation standards: <https://www.iso.org/>
