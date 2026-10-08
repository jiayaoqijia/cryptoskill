---
name: control-for-llm-judge-bias
description: Use when an LLM scores outputs. Corrects position, length, and self-preference bias, and calibrates against human labels before trusting scores.
---

# Control for LLM-Judge Bias

A model asked to grade text rewards longer, more confident, and self-authored answers regardless of quality. Untested judge scores are a mirror, not a measurement.

## Procedure

1. Fix the rubric in the prompt and forbid freeform reasoning that drifts: "Score 1–5 on (a) factual accuracy, (b) instruction-following. Output JSON only."
2. Control position bias. Run each pair twice with the order swapped and average; if A>B flips when swapped, the judge is position-biased:
   ```python
   first  = judge(a, b); second = judge(b, a)
   score = (first + (1 - second)) / 2
   ```
3. Control length bias. Report correlation between score and token count; if >0.3, strip or pad to equal length before judging.
4. Control self-preference. Never let the judge grade its own family's output without a cross-model check; use a different judge model for the final number.
5. Calibrate against humans: label ~50 items by hand and compute agreement (Cohen's κ). κ < 0.4 means the judge is not yet trustworthy; κ > 0.6 is usable.
6. Use pairwise comparison where possible — absolute 1–5 scores from an LLM cluster and drift; relative "which is better" is more stable.
7. Seed and temperature: set `temperature=0` for reproducibility, and log the model version, since a silent upgrade changes scores.

```python
from sklearn.metrics import cohen_kappa_score
kappa = cohen_kappa_score(human_labels, judge_labels, weights='quadratic')
```

## Pitfalls

- Averaging away position bias assumes the bias is symmetric; a judge can prefer position 1 *and* its own outputs, inflating both.
- A judge that agrees with humans on easy items can fail on the hard tail where you need it.
- Rubric leakage: if the judge can see the reference answer it may grade by matching phrasing.
- Score clustering at 3–4 with no spread means the rubric is too coarse to discriminate.
- Verbose judges reward verbosity in candidates ("chain-of-thought" answers win on length).

## Verification

    python3 judge_cal.py --human labels.csv --judge judge_scores.csv

Report: "κ=0.61 vs human labels (n=50); position-swap flips 4%; length-score r=0.12 — judge usable, length bias low."
