---
name: adjust-for-multiple-comparisons
description: Use when many metrics or slices are tested at once. Applies a multiplicity correction before calling any one of them significant.
---

# Adjust for Multiple Comparisons

Test 20 metrics at alpha 0.05 and about one will look significant by chance. If you did not bound the family of tests in advance, the headline is a coin flip wearing a lab coat.

## Procedure

1. Count the hypotheses actually tested: primary, secondary, and every slice a human will look at.
2. Pre-define the family, then apply a correction. Benjamini-Hochberg for exploration (control the false discovery rate), Bonferroni for confirmation (control the family-wise error):
   ```python
   from statsmodels.stats.multitest import multipletests
   p = [0.031, 0.008, 0.21, 0.044, 0.002, 0.12]      # six metrics
   rej, padj, _, _ = multipletests(p, alpha=0.05, method='fdr_bh')
   print(list(zip(p, [round(x,4) for x in padj], rej)))
   ```
3. Report adjusted p-values (or q-values) in the table, and mark which passed after correction.
4. Use Bonferroni when one false positive is costly and the family is small; use FDR when scanning many metrics to prioritise.
5. Correlated metrics (clicks and CTR) are not independent tests; note this when interpreting a corrected result.
6. Never add a slice to the confirmatory family after seeing it move; that slice belongs in exploratory.

## Pitfalls

- Guardrail metrics are tests too; a set of ten guardrails needs the same correction.
- Picking the one significant segment out of twelve and reporting it as the finding is the failure this prevents.
- Bonferroni on a large scanning family is too conservative and hides real signals; match the method to the intent.
- Correcting only the printed metrics while silently checking dozens more does not fix the multiplicity.
- FDR controls the expected proportion of false discoveries, not the chance of any — say which guarantee you are giving.
- Pre-specify the correction before results are seen; choosing Bonferroni or FDR afterwards is another degree of freedom.
- Reusing one control against several arms in an A/B/n test is multiplicity too — split alpha across the comparisons.

## Verification

    python3 -c "from statsmodels.stats.multitest import multipletests as m; r=m([.01,.02,.03,.2,.4],method='fdr_bh'); print(r[0], r[1].round(3))"

Report: "31 metrics tested; after BH-FDR at 0.05, 2 remain significant (primary q=0.004, latency guardrail q=0.031). The other 29, including two raw p<0.05 slice wins, are exploratory."
