---
name: adopting-onto-existing-code
domain: software-engineering/adopting-onto-existing-code
trigger: "Bringing analysis to a codebase that never had it."
anti_trigger: "Not for choosing the tool, and not for the rules themselves."
scope: "Baselining an existing codebase without a big bang."
status: seedling
---

# Adopting onto existing code

## Standard

Turning analysis on across an existing codebase produces a number: hundreds or thousands of findings, most of them old, none of them newly caused. The wrong responses are both extremes — fix everything first, which never finishes and ships nothing, or suppress everything, which buries the real findings among the noise and removes the tool's future value on the only code that matters, the code being written today.

The working middle path is the ratchet. Baseline the existing findings with a recorded count, hold every new and changed line to the full standard, and let the baseline shrink through ordinary work: a function touched for a feature gets fixed while the author is in it, not as a separate campaign. Code that is only ever read keeps its grandfathered findings, which is honest — nobody pays to clean code that never changes.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Baseline before enforcing, with a recorded per-rule count.
- Enforce the full standard on all new and changed code immediately.
- Ratchet via ordinary work: fix what you touch, not what you merely see.
- Record the baseline and report its size on a cadence.
- Never bulk-suppress to zero the findings the team intends to fix.
- Time-box the adoption so the trial and the ratchet have a review date.

## Procedure

1. Run the tool across the codebase and record the findings per rule.
2. Freeze the counts as the baseline.
3. Enforce full rules on the diff from the first day.
4. Fix-in-passing on touched code only.
5. Report baseline size monthly against the start.
6. Review the adoption at the time-box and adjust.

## Anti-patterns

- The great cleanup that blocks all feature work.
- Suppressing everything and calling the codebase clean.
- A ratchet with no reported size, so drift is invisible.
- Fixing untouched code in bulk and polluting the blame history.
- Adopting with no review date, so the trial never ends.

## Done checklist

- [ ] Baseline recorded per rule.
- [ ] Full enforcement on the diff.
- [ ] Fix-in-passing rule stated.
- [ ] Baseline trend reported.
- [ ] Bulk-suppression avoided.
- [ ] Adoption review dated.

The ratchet also needs a stated answer for deleted baseline code: findings grandfathered in a function vanish when the function is rewritten, and the baseline count should fall with them. A baseline that only ever rises as rules are added, and never falls as code is deleted, has stopped measuring anything.

## Sources

- Incremental quality improvement: <https://martinfowler.com/bliki/TechnicalDebt.html>
- Continuous integration: <https://martinfowler.com/articles/continuousIntegration.html>
- Empirical studies on analysis adoption: <https://dl.acm.org/>
