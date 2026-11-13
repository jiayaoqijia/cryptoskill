---
name: taxonomy-and-labeling
domain: software-engineering/taxonomy-and-labeling
trigger: "Designing violation categories that make disagreement measurable."
anti_trigger: "Not for writing the rules themselves, and not for classifier training."
scope: "Violation categories that make disagreement measurable."
status: seedling
---

# Taxonomy and labeling

## Standard

A moderation taxonomy is the set of violation categories items can be assigned to, and its quality decides whether the whole system can be measured. Categories must be mutually exclusive enough that a reviewer's choice is informative, exhaustive enough that nothing lands in an undefined state, and granular enough that enforcement can scale by category severity. When two reviewers systematically disagree on category assignment, the taxonomy — not the reviewers — is the defect until proven otherwise.

The labeling scheme sits on top of the taxonomy: each reviewed item carries its category, the reviewer who assigned it, a confidence or severity field where used, and the policy version at decision time. These fields are what make inter-rater agreement, error rates, and appeal outcomes computable later; a queue that does not record them cannot be calibrated, audited, or improved, only operated.

Primary sources: <https://en.wikipedia.org/wiki/Content_moderation> and <https://en.wikipedia.org/wiki/Precision_and_recall>.

## Decision rules

- Categories are mutually exclusive or have a stated precedence order for overlaps.
- An "other" or "unclassifiable" bucket exists, is monitored, and shrinks over time.
- Every label records: category, reviewer identity, decision timestamp, policy version.
- Severity is a category attribute, not a reviewer guess; the category carries it.
- Taxonomy changes are versioned; historical labels keep the version they were made under.
- Category definitions include worked examples of both inclusion and exclusion.

## Procedure

1. List the violation categories from the policy hierarchy.
2. Check pairwise overlaps; write precedence rules or merge.
3. Add the residual bucket with a monitoring target.
4. Define the label schema: category, severity, reviewer, timestamp, policy version.
5. Add worked inclusion and exclusion examples per category.
6. Version the taxonomy; record the change history.

## Anti-patterns

- Categories so broad two reviewers rarely agree.
- No residual bucket, forcing bad fits into wrong categories.
- Severity decided by reviewer mood rather than category definition.
- Taxonomy edits that silently reinterpret historical labels.
- Overlap categories without precedence, so assignment is a coin toss.

## Done checklist

- [ ] Categories checked pairwise for overlap.
- [ ] Precedence rules written where needed.
- [ ] Residual bucket with monitoring target.
- [ ] Label schema fixed with policy version.
- [ ] Worked examples per category.
- [ ] Taxonomy versioned.

One structural warning from measurement practice: when the residual bucket grows while established categories stay flat, the taxonomy has stopped fitting the traffic rather than the traffic changing — and the correct response is a taxonomy revision, not more reviewer training on categories that no longer describe what arrives.

## Sources

- Content moderation overview: <https://en.wikipedia.org/wiki/Content_moderation>
- Measurement foundation: <https://en.wikipedia.org/wiki/Precision_and_recall>
- Platform transparency reporting: <https://transparency.meta.com/>
