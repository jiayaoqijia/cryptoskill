---
name: iterate-a-prompt-against-golden-cases
description: Use when tuning a prompt and tempted to change it by feel. Freeze a golden case set, change one thing at a time, and accept an edit only when the measured score moves.
---

# Iterate a prompt against golden cases

Prompt editing by intuition regresses as often as it helps, and you cannot tell which. Put a frozen case set under every change and let the score decide.

## Procedure

1. Freeze a golden set: 30-100 real inputs with hand-checked expected outputs, covering the common cases and the known hard ones. Version it with a tag (`git tag gold-v1`); do not edit it to make a change pass.

2. Define one score per case (exact match, field-level accuracy, or a rubric) plus an aggregate. Compute it in one script so numbers are comparable across runs.

3. Baseline the current prompt. Record score, cost, and latency.

4. Change one thing per iteration — an instruction, an example, a format rule. Two changes at once and you cannot attribute the movement.

5. Re-run the full set. Keep the change only if the aggregate rises beyond the run-to-run noise (repeat runs to estimate that noise).

6. Check for regressions: a higher aggregate can hide cases that flipped from pass to fail. Diff the per-case results, not just the total.

7. When a change helps, commit the prompt with the score in the message; when it does not, revert rather than accumulating "probably fine" edits.

8. Wire the run into CI: `python3 eval_prompt.py --set gold_v3.jsonl --prompt prompt.md --fail-under 0.80` gates the merge.

9. Keep old scores and prompts: `git log --oneline prompts/` shows the trajectory, and a later regression can be bisected against past versions.

## Pitfalls

- Editing the golden set to accommodate a failing change, which launders the regression into a pass.
- Judging on a handful of eyeballed examples; small sets reward overfitting.
- Changing the prompt and the sampling parameters together, then crediting the prompt.
- Optimising the aggregate while a safety or schema case silently breaks — always diff per case.
- Tuning against the same set you ship on until it overfits; hold out a slice you never tune on.
- Running the eval at a different temperature or model version than production, so the score does not transfer.
- Accepting a win without re-reading the diff; a prompt can pass the set while getting harder to maintain.
- Optimising for the aggregate score and shipping a prompt that is 5x longer and slower to serve.

## Verification

    python3 eval_prompt.py --set gold_v3.jsonl --prompt prompt.md   # prints score, delta vs baseline, and per-case regressions

Report: "candidate prompt 84.0% vs baseline 81.3% on gold_v3, +2.7 pts with 1 case regressed (fixed by adding its example); the held-out slice rose too, so kept."
