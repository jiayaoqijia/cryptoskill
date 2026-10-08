---
name: pick-a-model-by-task-shape
description: Use when choosing which model to run a task on. Match the task's shape — reasoning depth, output length, latency budget, and volume — against model capability, then verify on a sample before committing.
---

# Pick a model by task shape

Model choice is an engineering decision, not a brand preference. Profile the task first, pick the cheapest model that clears the quality bar, and prove it on a sample before the run.

## Procedure

1. Classify the task into a shape: `classify` (short label), `extract` (structured fields from input), `generate` (free prose), `reason` (multi-step, tool-using), `embed` (vectors). Each shape has a different capability floor.

2. Write the quality bar as a checkable outcome, not a vibe: "name, date, and amount all correct on 20/20 cases". Without this you cannot compare models.

3. Estimate the demand: tokens in and out per call, calls per day, and the latency budget (interactive p95 < 2s, batch hours). This sets the cost and speed constraint.

```bash
python3 - <<'PY'
tin, tout, calls = 1800, 400, 50000
for name, pin, pout in [("small", 0.15, 0.60), ("mid", 3.0, 15.0), ("large", 15.0, 75.0)]:
    cost = calls * (tin*pin + tout*pout) / 1e6
    print(f"{name:6} ${cost:8.2f}/day  ${cost*30:9.2f}/mo")
PY
```

4. Build a 20-50 case sample from real inputs — including the messy ones — and record gold outputs. This is the only honest basis for choosing.

5. Run the top-2 candidate models on the sample and compare on the quality bar plus p95 latency and dollars per call.

6. Choose the cheapest model that clears the bar. Reserve the frontier model for the tail: the fallback, or the cases the cheap one fails.

7. Record the decision and the sample that justified it, so the next person can re-run it when prices or model versions change.

## Pitfalls

- Choosing on public benchmark scores instead of your own task sample; benchmarks do not measure your inputs.
- Defaulting to the largest model "to be safe" and paying 10-100x for accuracy you never measured.
- Ignoring latency: a model that is right 5% more often but 8x slower can fail an interactive product.
- Assuming a model upgrade is strictly better; re-run the sample before switching the pinned version.
- Comparing models on different prompts; hold the prompt fixed or the comparison is meaningless.

## Verification

    python3 score_sample.py --model A --model B --cases sample.jsonl   # prints accuracy and p95 ms per model

Report: "model X cleared the bar (19/20) at $0.03/call and 1.4s p95; model Y matched accuracy at 6x cost — chose X, sample in sample.jsonl."
