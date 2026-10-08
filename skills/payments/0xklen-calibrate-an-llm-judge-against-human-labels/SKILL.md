---
name: calibrate-an-llm-judge-against-human-labels
description: Use when replacing or supplementing human ratings with an LLM judge. Measures agreement, per-class error, and drift before the judge decides anything.
---

# Calibrate an LLM Judge Against Human Labels

An LLM judge is a measuring instrument. Until you have compared it to the human label it replaces, its scores are an opinion wearing a number.

## Procedure

1. Sample 50–100 items spanning the score range, including the ambiguous middle. Label them by hand under the same rubric you gave the judge.
2. Compute chance-corrected agreement, not accuracy against yourself: quadratic-weighted Cohen's kappa for ordinal scores, or Krippendorff's alpha with several raters.
   ```python
   from sklearn.metrics import cohen_kappa_score, confusion_matrix
   k = cohen_kappa_score(human, judge, weights="quadratic")
   print("kappa", round(k, 3)); print(confusion_matrix(human, judge))
   ```
3. Read the confusion matrix, not the summary. A judge right on average but swapping 4<->5 erases the top of your scale.
4. Check per-class recall: a judge can be 80% overall and 0% on the "unsafe" class you actually care about.
5. Check calibration drift with model version. Re-run the same 50 items after any provider upgrade; a silent update can move kappa by 0.1.
6. Set the trust threshold before use: kappa >= 0.6 usable as the primary metric; 0.4–0.6 triage only with human audit; < 0.4 the judge is not measuring what you think.
7. Keep the labelled set as a permanent regression fixture and re-run it each release.

```bash
python3 judge_cal.py --human labels.jsonl --judge judge_out.jsonl --metric kappa
```

## Pitfalls

- Human labels are not ground truth; if annotators disagree, calibrate to the adjudicated set, not to one rater.
- Reporting raw percent agreement on imbalanced classes; kappa corrects for chance, percent does not.
- Calibrating on easy items only — the judge looks excellent and fails exactly where it is used.
- Kappa computed on 20 items has a huge interval; always state n and the CI.
- Letting the judge see the reference answer turns calibration into a copying test.

## Verification

    python3 judge_cal.py --human labels.jsonl --judge judge_out.jsonl --metric kappa   # prints kappa and confusion

Report: "Judge vs 60 human labels: kappa=0.58 (quadratic). Confusion shows 4<->5 swaps on 40% of top scores; using it for triage only with a 10% human audit."
