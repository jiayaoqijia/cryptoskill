---
name: separate-significance-from-relevance
description: Use when a result is called significant. Converts the p-value into an effect size versus a business threshold before deciding to act.
---

# Separate Significance from Relevance

Statistical significance says an effect is unlikely to be zero; it says nothing about whether the effect is worth the cost of acting. With enough traffic, a 0.01% lift is significant and worthless.

## Procedure

1. Report the effect as a quantity in the metric's own units with a confidence interval, not a p-value.
2. State the relevance threshold first — the smallest effect that would change a decision (rollout cost, support load, margin point).
3. Compare the interval to the threshold, not to zero. An interval entirely below the threshold is conclusive irrelevance:
   ```python
   import numpy as np
   p1, n1, p0, n0 = 0.109, 50_000, 0.104, 50_000
   d = p1 - p0
   se = np.sqrt(p1*(1-p1)/n1 + p0*(1-p0)/n0)
   lo, hi = d - 1.96*se, d + 1.96*se
   print(f"lift {d*100:.2f}pt, 95% CI [{lo*100:.2f}, {hi*100:.2f}]")
   ```
4. Convert the effect to money or users at the observed rate; an annualised 40k move and a 4k move get different answers.
5. Distinguish practical from statistical by asking whether the interval excludes the relevance bar, not whether it excludes zero.
6. If the interval straddles the threshold, the test is inconclusive — report that, do not round to a win.

## Pitfalls

- "Statistically significant" read as "worth shipping" is the most common analytics error in review decks.
- Enormous n makes trivial effects significant; report effect size before p.
- Relative lift hides base rate: +10% on a 0.2% conversion is +0.02pt and may be noise in the funnel.
- Wide intervals around a significant point estimate still contain the null at the margins; check the interval, not the star.
- A significant guardrail regression can matter more than a significant primary win.

## Verification

    grep -nE 'CI|confidence' results.md | grep -iE 'lift|effect|point'   # interval must sit next to any significance claim

Report: "Lift +0.46pt (95% CI 0.12 to 0.80) on n=100k/arm — significant, but the pre-agreed relevance bar was +1.0pt; conclusive irrelevance, do not ship."
