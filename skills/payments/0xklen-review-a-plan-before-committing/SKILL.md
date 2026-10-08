---
name: review-a-plan-before-committing
description: Use when a plan is about to become a commitment to others. Runs a fixed checklist over it — ranges, assumptions, dependencies, buffer, done-definition — and blocks the commit until each item has an answer.
---

# Review a plan before committing

Committing a plan you have not audited is how you inherit surprises. Run the same checklist every time, so the gaps that matter — an unbounded assumption, an unpriced dependency, a missing done-definition — are caught before the plan leaves your hands, not after.

## Procedure

1. Work the checklist in `notes/plan-review.md` against the plan file. Each line must have a real answer or be explicitly waived:

       notes/plan-review.md
       [ ] every estimate is a range with a confidence
       [ ] each assumption is written with a date and status
       [ ] each external dependency has owner + lead time + trigger
       [ ] buffer exists and is sized, not round
       [ ] done-definition is testable; exclusions listed
       [ ] critical path identified; nearest slack known
       [ ] risks priced or spiked; top risk has a fallback
       [ ] a confidence date is stated, not a promise

2. For any unchecked line, fix it now or record the waiver and why. A waiver is a note in the file, not a silent gap.
3. Verify the plan is internally consistent with one script, not by reading:

       python3 - <<'PY'
       import re
       t=open('notes/plan.md').read()
       for h in ['assumption','deadline','milestone','scope v']:
           print(h, t.lower().count(h))
       PY

4. Sanity-check the summary number against the parts (sum of ranges vs stated total).
5. Run a pre-mortem on the top three risks: "it is three months later and this failed — why?" Add mitigations for any answer not already covered.
6. Only after every line is answered or waived do you commit the plan to stakeholders.

## Pitfalls

- Reviewing your own plan alone under deadline and rubber-stamping the comfortable items.
- Treating an unchecked line as "probably fine" instead of fixing or explicitly waiving it.
- Checking structure (headings present) while missing substance (an assumption with no date).
- Pre-mortems that list only tidy risks, omitting the uncomfortable ones nobody wants to name.
- Committing the plan and doing the review "after," which is just documenting a decision already made.

## Verification

    python3 - <<'PY'
    import re
    t=open('notes/plan-review.md').read()
    print('open_items', t.count('[ ]'), 'waived', t.lower().count('waiver'))
    PY
    # passes when open_items minus waived equals zero before the plan is committed

Report the checklist with each line's answer or waiver, the internal-consistency check output, and the top three pre-mortem risks.
