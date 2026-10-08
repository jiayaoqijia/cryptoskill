---
name: stratify-eval-scores-by-slice
description: Use when reporting an eval accuracy or win rate. Splits the pooled number into slices and surfaces the worst slice instead of hiding it in the mean.
---

# Stratify Eval Scores by Slice

A pooled 82% can sit on top of a slice at 20%. The average is the number you tell people; the worst slice is the number that decides whether you ship.

## Procedure

1. Define slices before scoring — by language, input-length bucket, source, difficulty, or customer segment. Post-hoc slices are story-hunting.
2. Score every slice separately and print the table, not just the mean.
   ```python
   import pandas as pd
   r = pd.read_json("results.jsonl", lines=True)
   r["len_bucket"] = pd.cut(r.tokens, [0, 256, 1024, 4096, 10**9])
   print(r.groupby("len_bucket")["correct"].agg(["mean", "count"]))
   ```
3. Report the worst slice with its count. A zero on n=3 is a different claim from a zero on n=300.
4. Set a per-slice floor, not just a pooled floor: "no slice below 70%" catches a collapse the mean hides.
5. Weight slices deliberately if you pool. Equal-weighted slice averages differ from sample-weighted ones; state which you use.
6. Look for slices that anti-correlate — a change lifting easy items while dropping hard ones nets flat but hurts the tail.
7. Re-check the weakest slice on a fresh sample; small slices swing and one bad draw can look like a collapse.

```bash
python3 slice_report.py --results results.jsonl --by language,source,len_bucket | sort -k3 -n | head
```

## Pitfalls

- Many small slices produce false collapses; require a minimum count (>=30) before calling a slice broken.
- Choosing slices after seeing where you lost is fishing; freeze the slice list in the eval config.
- Reporting only the slices that moved up; a slice can regress while the pooled mean rises.
- A pooled CI does not bound a slice CI — compute the interval per slice.
- Hiding a weak long-input slice behind strong short inputs is the most common way a mean lies.

## Verification

    python3 slice_report.py --results results.jsonl --by len_bucket | sort -k3 -n | head   # lowest slice first

Report: "Pooled 82%, but the >4096-token slice is 41% (n=60) and non-English 55% (n=120); the no-slice-below-70% ship gate fails."
