---
name: use-paired-comparison-to-cut-judge-noise
description: Use when comparing two systems or prompts with an LLM or crowd judge. Uses pairwise win rates instead of absolute scores to remove scale drift.
---

# Use Paired Comparison to Cut Judge Noise

Absolute 1–10 scores from an LLM cluster around the middle and drift between runs. "Which of these two is better?" is a far more stable measurement, and it needs only a win rate.

## Procedure

1. For each item, show the judge both outputs and ask for one bit: A, B, or tie. Do not ask for a score.
2. Swap the positions and re-ask. Count the pair as resolved only if the judge keeps the same winner; a flip is position bias.
   ```python
   wins = sum(judge(a, b) == "A" and judge(b, a) == "B" for a, b in pairs)
   rate = wins / len(pairs)          # order-consistent win rate
   ```
3. Report the win rate with an interval: for n pairs, the 95% half-width is `1.96*sqrt(0.25/n)` around 0.5.
4. Break ties explicitly and count them; a judge that answers "tie" 80% of the time is discriminating nothing.
5. Aggregate many pairs into a ranking with a Bradley–Terry / Elo fit rather than counting raw wins, so strength is estimated from who beat whom.
6. Stratify the win rate by slice; a system can win overall while losing the hard slice.
7. Convert to a ship decision: win rate >= 0.5 + MDE on the primary slice is a win; otherwise call it a tie.

```python
from statsmodels.stats.proportion import proportion_confint
lo, hi = proportion_confint(wins, len(pairs), method="wilson")
```

## Pitfalls

- Forgetting the swap: one-shot pairwise judging carries the same position bias as absolute scoring.
- Reusing the same item many times inflates n; count distinct items, not judgements.
- Ties hidden from the metric look like losses if you only count A-wins.
- A judge biased toward its own model family skews the win rate toward whichever side is the judge's family.
- Win rate ignores magnitude — barely winning everywhere differs from winning big sometimes; report both when the decision needs it.

## Verification

    python3 pairwise.py --pairs pairs.jsonl --swap   # prints order-consistent win rate + Wilson CI

Report: "Prompt B beats A on 213/400 order-consistent pairs (53%, 95% CI 48–58%) — a tie, not a win; B loses the hard slice at 41%."
