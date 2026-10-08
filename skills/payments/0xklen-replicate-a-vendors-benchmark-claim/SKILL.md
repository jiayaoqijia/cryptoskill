---
name: replicate-a-vendors-benchmark-claim
description: Use when a vendor or paper reports a benchmark number you might rely on. Re-runs the claim on your own harness before adopting it.
---

# Replicate a Vendor's Benchmark Claim

A reported score is a claim about someone else's harness, prompt, and split. Re-run the same claim on your harness or you are buying a number you cannot reproduce.

## Procedure

1. Extract the exact recipe: dataset version, split, prompt template, shot count, decoding settings, and scoring script.
2. Re-run the vendor's configuration first. If you cannot reproduce their number with their settings, stop — the difference is theirs to explain.
3. Then swap one thing at a time onto your harness: your prompt, your split, your scorer. Each swap shows how much of the headline survives.
   ```bash
   python3 eval.py --model vendor/x --dataset v1.0 --shots 5 --scorer exact
   ```
4. Compare with intervals: reproduce their accuracy with the same n and check the CIs overlap.
5. Test on your own held-out data, not just their public set. Generalisation off the benchmark is the actual question.
6. Check the model's training cutoff against the eval release date for contamination before congratulating anyone.
7. Report what reproduced, what did not, and the delta with the cause you could identify.

```python
import math
def ci(p, n):
    s = math.sqrt(p * (1 - p) / n)
    return round(p - 1.96 * s, 3), round(p + 1.96 * s, 3)
print("vendor", ci(.88, 1200), "mine", ci(.84, 1200))
```

## Pitfalls

- Reproducing with your own prompt and blaming the vendor when the number differs; change one variable at a time.
- Using a newer dataset version than the claim; version mismatch alone explains several points.
- Assuming a public headline generalises to your task; benchmark wins are task-specific.
- Ignoring the scorer; a lenient parser adds points that evaporate under exact match.
- Reproducing once and treating a single run as the vendor's number — run it several times for their variance too.

## Verification

    python3 eval.py --model vendor/x --dataset v1.0 --shots 5 --scorer exact --report ci   # compare CI to claim

Report: "Vendor 88% +/-1.8 reproduced at 87.1% +/-1.8 on their recipe; on our data 79% +/-2.3 — the gap is domain, not implementation."
