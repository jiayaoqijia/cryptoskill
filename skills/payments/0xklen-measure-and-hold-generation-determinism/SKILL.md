---
name: measure-and-hold-generation-determinism
description: Use when output stability matters — caching, diffing, tests, or reproducible runs. Set the determinism you can, measure the residual variance, and never assume identical inputs give identical output.
---

# Measure and hold generation determinism

LLM outputs are only as reproducible as the stack allows, and often not at all. Measure the variance you actually get; design as if it is non-zero, because it is.

## Procedure

1. Reason about the sources of variance: seed, temperature/sampling, batch effects (concurrent requests), and provider-side version drift. Kernel non-determinism persists even at `temperature=0`.

2. Set the controls the API exposes: `temperature=0`, a fixed `seed` if supported, a fixed model snapshot, and serial requests (batching can change results).

3. Measure: send the identical request N=20 times and count distinct outputs.

```bash
for i in $(seq 20); do curl -s "$API" -d @req.json | jq -r '.choices[0].message.content'; done | sort | uniq -c
```

4. Record the result: one unique output means the path is stable now; several means you have variance to design around.

5. For anything cached or asserted on, key on a normalised hash of the output, not raw bytes — trailing whitespace and key order vary.

6. Re-run the determinism probe when you change seed, snapshot, temperature, or provider. Version drift flips a formerly-stable call.

7. Where you need true reproducibility, store the exact response and replay it rather than re-calling the model.

## Pitfalls

- Assuming `temperature=0` means deterministic; GPU kernels, MoE routing, and batching still produce variance across runs.
- Caching on the prompt alone and serving a stale output when the model version changed underneath.
- Diffing raw text — key order and spacing differences create false diffs.
- Testing determinism once, on one input; variance shows up on your long or ambiguous prompts, so test those.
- Relying on provider seed support that is documented as best-effort, not guaranteed.
- Concluding from a single repeat run; twenty identical calls is the minimum to see the spread.
- Measuring determinism at a different concurrency than production; batching changes the result.
- Assuming a stable result today survives the next model bump; re-probe on every version change.

## Verification

    for i in $(seq 20); do curl -s "$API" -d @req.json; done | jq -r '.choices[0].message.content' | sort -u | wc -l   # 1 = stable, >1 = measure the spread

Report: "20 identical calls with seed=7 and temperature=0 produced 3 distinct outputs; caches key on a normalised hash and the determinism probe reruns on every model bump."
