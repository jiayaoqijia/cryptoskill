---
name: validate-child-reported-metrics
description: Use when a subagent reports counts, scores, or coverage numbers. Recomputes each metric from raw output so an inflated or fabricated figure cannot enter the parent's report.
---

# Validate Child Reported Metrics

Numbers a child reports travel into your summary and become trusted facts. Recompute each one from raw evidence before it does, because a plausible count is easy to assert and hard to catch later.

## Procedure

1. Extract every numeric claim from the child's report: counts, percentages, pass rates, coverage.
2. For each, identify the command that would produce the true value, independent of the child's narrative.
3. Recompute it yourself: "12 files changed" becomes `git status --short | wc -l`; "20/20 valid" becomes the validator run.
4. Compare with a tolerance only where genuine nondeterminism exists (timing, sampled data); counts must match exactly.
5. Check the denominator as hard as the numerator: a 100% pass rate over 3 of 20 tests is not 100% coverage.
6. Scrutinise metrics the child defined itself ("I fixed 8 bugs") — confirm against commits or diffs, not the claim.
7. Reject any figure whose source you cannot reproduce; report it as UNVERIFIED rather than passing it on.
8. Record verified values in `notes/metrics.tsv`: `metric<TAB>claimed<TAB>recomputed<TAB>verdict`.
9. Report the recomputed value, not the child's, whenever they differ, and flag the discrepancy.
10. Keep the raw command output behind each recomputed number in `notes/metrics.evidence/` so the figure is reproducible later.

## Pitfalls

- Copying a child's "20/20 valid" line into your report without re-running the validator.
- Accepting a percentage without its denominator, so 3-of-3 masquerades as full coverage.
- Treating a child's self-defined metric ("8 issues resolved") as fact with no diff to back it.
- Passing rounded numbers upward until "1,847" becomes "1,800" in the final summary.
- Recomputing only the headline metric while the supporting counts go unverified.

## Verification

```bash
awk -F'\t' '$2!=$3{print "mismatch: "$0}' notes/metrics.tsv
# passes when this prints nothing, or every remaining difference is marked UNVERIFIED
```

Report to the user: each metric's claimed value, its recomputed value, and the commands you used to check them.
