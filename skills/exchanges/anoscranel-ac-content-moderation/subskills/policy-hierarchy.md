---
name: policy-hierarchy
domain: software-engineering/policy-hierarchy
trigger: "Turning platform principles into line-level decidable rules."
anti_trigger: "Not for deciding what the policy should be, and not for classifier tuning."
scope: "Principles, policies, and line-level rules in a decidable chain."
status: seedling
---

# Policy hierarchy

## Standard

A moderation policy exists at three levels, and inconsistency between them is where most enforcement disputes originate. Principles state what the platform values in one or two sentences. Policies translate each principle into named violation categories a reviewer can distinguish. Rules are the line-level operational tests — the specific phrasings, image descriptions, or behaviours that place an item in a category.

The engineering task is keeping the chain consistent downward and decidable at the bottom. A rule that cannot be applied the same way by two reviewers reading it independently is not a rule; it is an invitation to variance. Each rule names its parent policy, each policy its parent principle, and a proposed rule that would violate its own principle is caught at review, not at enforcement. The chain is versioned as a unit.

Primary sources: <https://transparency.meta.com/> and <https://en.wikipedia.org/wiki/Content_moderation>.

## Decision rules

- Record each level explicitly: principles, policies with categories, rules with operational tests.
- Every rule carries a reference to its parent policy; every policy to its principle.
- A rule is decidable only if two reviewers reading it independently reach the same category.
- Ambiguous cases go to an explicit escalation tier, never to reviewer improvisation.
- Basement rules ("everything else we deem inappropriate") are recorded as known debt, not used for enforcement.
- Version the hierarchy as a unit; a rule change without a policy review is a defect.

## Procedure

1. Collect the platform's principles and confirm each is one or two sentences.
2. Derive policy categories from each principle; record the mapping.
3. Draft line-level rules per category, each with a concrete operational test.
4. Run a two-reviewer panel on a sample of rules; any divergence triggers a rewrite.
5. Verify every rule chains upward to a principle.
6. Publish the versioned hierarchy to reviewers and record the date.

## Anti-patterns

- Rules enforced without a stated parent policy.
- Principle updates that leave the rule chain unreviewed.
- "We know it when we see it" as an operational test.
- Category proliferation without principle coverage.
- Improving enforcement without recording which level changed.

## Done checklist

- [ ] Three recorded levels.
- [ ] Rule-to-policy-to-principle mapping complete.
- [ ] Two-reviewer panel passed on a rule sample.
- [ ] Escalation tier defined.
- [ ] Catch-all categories recorded as debt.
- [ ] Hierarchy versioned and dated.

## Sources

- Platform transparency reporting: <https://transparency.meta.com/>
- Content moderation overview: <https://en.wikipedia.org/wiki/Content_moderation>
- Regulatory context: <https://en.wikipedia.org/wiki/Digital_Services_Act>
