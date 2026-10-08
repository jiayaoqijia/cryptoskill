---
name: pre-register-eval-pass-criteria
description: Use when starting an evaluation whose result will guide a decision. Writes the metric, threshold, and analysis plan before running, to block moving the goalposts.
---

# Pre-register Eval Pass Criteria

Deciding what counts as success after seeing the numbers is how every failed experiment becomes a win. Write the criteria first, timestamp them, and hold to them.

## Procedure

1. Before running, write a one-page plan: primary metric, threshold, comparison baseline, sample size, and slice rules.
2. Name the single primary metric. Everything else is secondary and cannot rescue a failed primary.
3. State the analysis you will run (paired test, bootstrap CI) and the significance level. Changing the test later is p-hacking.
4. Fix the stopping rule: how many items, one look at the end. Optional stopping on a fixed-n test inflates false positives.
5. Commit the plan with the code so git proves the order of events:
   ```bash
   git add EVAL_PLAN.md && git commit -m "pre-register eval criteria" && git rev-parse HEAD
   ```
6. After the run, report the primary result as-is. If it failed, report the failure; do not swap in a secondary that passed.
7. If you must deviate, log the deviation and the reason, then report the planned and the exploratory result separately, labelled.

```markdown
# Eval plan (frozen 2026-09-30)
Primary: exact-match on heldout.jsonl (n=1200)
Pass: lower 95% bound >= 0.78
Baseline: v2 prompt, paired McNemar
Slices reported: language, input length
```

## Pitfalls

- A "primary metric" chosen after the fact among five measured ones is HARKing.
- Reporting a secondary slice as the headline when the primary missed.
- Quietly lowering the threshold by a point "to account for noise".
- An unfixed stopping rule lets you stop when the run looks good.
- A plan written but never committed leaves no evidence it predated the result.

## Verification

    git log --format='%H %ci' -1 -- EVAL_PLAN.md   # plan commit time must precede the results commit

Report: "Plan committed (a91f3c) before the run; primary metric 0.76 < 0.78 → FAIL reported as-is, no criteria moved."
