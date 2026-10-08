---
name: interpret-benchmark-results-honestly
description: Use when a model, method, or tool claims a score on a benchmark. Checks contamination, error bars, and generality before repeating the headline number.
---

# Interpret Benchmark Results Honestly

A single leaderboard number is a claim about a specific split, prompt, and scoring script. Most of the gap between the top rows is noise; the headline hides it.

## Procedure

1. Find the exact split and metric. "94% on MMLU" is meaningless without the subset, the prompt template, and whether it is few-shot.
2. Demand error bars. For accuracy p over n items the standard error is `sqrt(p(1-p)/n)`; make the API:
   ```python
   import math
   se = math.sqrt(p*(1-p)/n); print(p, "+/-", 1.96*se)  # 95%
   ```
   A 0.5-point lead over n=1000 is inside the interval — a tie.
3. Check contamination. If the test set or its near-paraphrases appear in training data, the score measures recall, not capability. Look for the split's release date vs the model's cutoff.
4. Verify the scoring, not just the answer. Substring match on multiple-choice rewards the wrong format; a stricter parser can move the number several points.
5. Look for ceiling and saturation: near 100% the benchmark no longer discriminates and differences are rounding.
6. Test generalisation off the leaderboard: run on a held-out, freshly authored set or the actual downstream task. A benchmark is a proxy, and proxies drift.
7. Report per-subgroup, not just the average — a benchmark average can hide a collapsed subgroup.

```bash
# compare two claimed scores with intervals before declaring a winner
python3 - <<'PY'
import math
for name,p,n in [("A",.941,14042),("B",.936,14042)]:
    se=math.sqrt(p*(1-p)/n); print(name,p,"+-",round(1.96*se,4))
PY
```

## Pitfalls

- Cherry-picked best-of-N runs: a benchmark rerun several times reports the max, not the mean.
- Different prompt formats across models make cross-model comparison invalid unless the harness is identical.
- Public test sets leak into web-crawled training corpora over time.
- A benchmark that rewards verbosity or format familiarity measures style, not skill.
- Not reporting the number of runs hides seed variance; run ≥3 seeds and give the spread.

## Verification

    python3 -c "import math; p=.94; n=1000; print('95% CI +-', round(1.96*math.sqrt(p*(1-p)/n),4))"

Report: "Paper claims 94.1% vs baseline 93.6% on n=14,042; 95% CIs overlap — statistical tie. Contamination not ruled out for the pre-2023 train set."
