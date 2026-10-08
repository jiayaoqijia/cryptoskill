---
name: design-an-eval-that-can-actually-fail
description: Use when building a test or evaluation for an agent, model, or pipeline. Includes controls and thresholds that let a bad system fail instead of always passing.
---

# Design an Eval That Can Actually Fail

An eval that everything passes measures nothing. Build in negative controls, a baseline, and a pass threshold computed before you see results, so a broken system is visibly broken.

## Procedure

1. Write the failure condition first: what output would prove the system wrong? If you cannot state one, you have a demo, not an eval.
2. Include negative controls. Cases the correct system must refuse or return empty. If these ever pass your pipeline, the pipeline is broken.
3. Set a baseline, not a vibe: a trivial rule ("always output the majority class"), the previous version, or a random choice. Beat it by a stated margin or the result is null.
4. Compute the minimum detectable effect from n before running: with accuracy p≈0.5 and n items, the 95% half-width is `1.96*sqrt(0.25/n)` — pick n so the gap you care about exceeds it.
   ```python
   import math
   n = 400
   print("half-width", round(1.96*math.sqrt(.25/n), 4))  # 0.049
   ```
5. Split into dev (tune) and held-out test (report once). Tuning on the test set and reporting the best dev iteration is overfitting.
6. Mix difficulty deliberately: clear cases, ambiguous cases with a documented adjudication, and adversarial cases. Report accuracy per slice, not pooled.
7. Fix the scoring rule in code and hash it before results; changing the scorer to fit the winner is the classic eval foul.
8. Require the eval to fail a known-bad input *exactly once*: plant a canary the system should get wrong-by-design and confirm the harness flags it.

```bash
python3 eval.py --testset tests/heldout.jsonl --scorer scorers/v3.py --baseline majority
```

## Pitfalls

- Every case passing on the first run signals the eval is too easy, leaked, or the scorer is a no-op — investigate before celebrating.
- Averages hide a slice that fell to zero; always report the weakest slice.
- Non-deterministic systems need ≥3 seeds; a single run cannot separate signal from noise.
- Letting the model see the rubric verbatim turns the eval into prompt-matching.
- Unclear cases with no documented adjudication produce arbitrary labels; write the rule down.

## Verification

    python3 eval.py --selftest   # plants a canary; must report 1 planted failure caught

Report: "Eval of 400 held-out items: system 71%, baseline 54%, half-width ±0.049 — margin exceeds noise; weakest slice (multi-hop) 38%."
