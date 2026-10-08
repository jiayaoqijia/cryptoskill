---
name: size-an-eval-for-a-meaningful-delta
description: Use when planning how many eval items to run to detect a difference of a given size. Computes the smallest detectable effect from n so a small gap is not called a win.
---

# Size an Eval for a Meaningful Delta

A 3-point win over 100 items is noise. Before you run, decide the gap you care about, then size the set so the gap exceeds the confidence interval — not the other way around.

## Procedure

1. Fix the decision rule first: "we ship if accuracy beats baseline by >=5 points". Convert that to an absolute difference `d`.
2. Compute the 95% half-width for two independent proportions:
   `h = 1.96 * sqrt(2 * p*(1-p) / n)`.
   ```python
   import math
   def half_width(n, p=0.5):
       return 1.96 * math.sqrt(2 * p * (1 - p) / n)
   for n in (100, 400, 1600, 6400):
       print(n, round(half_width(n), 4))
   ```
3. Solve for n: `n = 2 * p*(1-p) * (1.96/d)**2`. For d=0.05 and p=0.5 that is ~768 items per arm.
4. Use paired items when possible — the same items scored by both systems cut variance and can roughly halve n.
5. Add a difficulty margin: hard slices have lower p and wider intervals; size the smallest slice you will report on, not just the pooled total.
6. Budget for nondeterminism: if each item is run 3 times, the effective n is the run count, not the item count.
7. Write the minimum detectable effect into the config so a later reader cannot over-read a small result.
   ```yaml
   n_items: 1600
   mde_abs: 0.035      # gaps below this are not actionable
   ```

## Pitfalls

- Powering for the pooled metric while deciding on a slice — the slice is underpowered even when the total is fine.
- Using the observed difference to justify a bigger n after the fact; size before the run.
- Ignoring base rate: at p=0.99 a 1-point move needs far more items than at p=0.5.
- Calling a non-significant result "no effect" when the interval is wide; it is underpowered, not equal.
- Forgetting multiple comparisons: testing 20 slices inflates false positives unless the primary slice is pre-declared.

## Verification

    python3 -c "import math; print('n per arm', round(2*.25*(1.96/0.05)**2))"   # ~768

Report: "Decision is a 5-point gap; n=768/arm gives a +/-5% half-width. We ran 1600/arm, MDE +/-3.5% — a 2-point lead is below the MDE and reported as a tie."
