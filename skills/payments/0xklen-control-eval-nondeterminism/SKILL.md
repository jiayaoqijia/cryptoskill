---
name: control-eval-nondeterminism
description: Use when a model or pipeline gives different answers to the same input. Quantifies run-to-run variance so a score change is signal, not sampling noise.
---

# Control Eval Nondeterminism

A model at temperature 0 on a shared endpoint still varies between runs. If you do not measure that variance, every re-run looks like a change.

## Procedure

1. Run the identical eval twice on an unchanged system. The difference between the two runs is your noise floor.
2. Pin what you can: model version, temperature, top_p, seed if the API supports it, and the endpoint.
   ```python
   resp = client.chat(model="x-2024-08", temperature=0, seed=42, top_p=1)
   ```
3. Repeat each item >=3 times and report the per-item flip rate. Items that flip between correct and wrong dominate the noise.
4. Report the metric as mean +/- spread across runs (std or min-max), not a single run.
5. Set the minimum detectable change at least 2x the observed run-to-run std before calling any move real.
6. Identify the noisy items and decide: genuinely borderline (keep, they are the hard tail) or broken (fix the item)?
7. Log seed, model version, and timestamp with every run so a silent provider update is discoverable.

```bash
for r in 1 2 3; do python3 eval.py --testset heldout.jsonl --seed 42 >> runs.jsonl; done
python3 -c "import pandas as pd; print(pd.read_json('runs.jsonl', lines=True).groupby('run').accuracy.describe())"
```

## Pitfalls

- Assuming temperature 0 means deterministic; batched inference and MoE routing still vary.
- Comparing two runs without a noise floor calls a 1-point move a win.
- Averaging over many seeds then reporting the mean hides that individual items flipped wildly.
- A provider model alias silently updating mid-experiment invalidates A/B comparisons.
- Treating every flip as a bug; borderline items legitimately flip and belong to the hard slice.

## Verification

    python3 -c "import pandas as pd; d=pd.read_json('runs.jsonl',lines=True); print(d.groupby('run').accuracy.agg(['mean','std']))"

Report: "Run-to-run std 1.1 points (3x500 items); the 0.8-point 'improvement' is inside noise — not a win."
