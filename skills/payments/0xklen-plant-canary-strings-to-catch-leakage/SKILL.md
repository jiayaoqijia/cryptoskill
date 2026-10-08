---
name: plant-canary-strings-to-catch-leakage
description: Use when a model might regurgitate eval answers or training data. Embeds unique canary tokens and checks whether they surface in outputs.
---

# Plant Canary Strings to Catch Leakage

A unique random token you control is the cleanest test for whether content reached a model. If the canary comes back, the data leaked — no statistics needed.

## Procedure

1. Generate a unique token per document or eval item, e.g. `CANARY-7f3a9c1e`. Random, non-guessable, never used elsewhere.
2. Insert it into the source in a semantically inert place; note its position and the surrounding text.
3. Ask the model completion-style for the region around the canary and check for the exact token:
   ```python
   import uuid
   canary = "CANARY-" + str(uuid.uuid4())[:8]
   assert canary not in model_output, "canary leaked from training data"
   ```
4. Run the probe several times with varied prompts; a rare completion may need a few attempts.
5. For an eval set, embed a canary in each gold answer and confirm no generation reproduces it during a clean run.
6. Track which canaries leak and their source; a leak points to the specific document or split that reached training.
7. Re-check after fine-tunes or retrieval-index updates; those are the usual re-entry points.

```bash
grep -rF "CANARY-7f3a9c1e" runs/*.jsonl   # any hit = the canary appeared in model output
```

## Pitfalls

- A canary that is guessable or appears in the prompt by design is not a leak test.
- Checking only the final answer misses leaks in reasoning traces, tool calls, or retrieved context.
- A single probe with one prompt can miss probabilistic regurgitation; vary and repeat.
- Leaking a canary into your own logs and then grepping logs gives a false positive — scope the search to model outputs.
- Absence of a leak is weak evidence of cleanliness; it rules out verbatim recall, not paraphrase.

## Verification

    grep -rF "$CANARY" runs/ | grep -v prompt ; echo "exit=$?"   # exit 1 = no leak in outputs

Report: "Canary probe over 200 items: 2 canaries surfaced in completions, traced to documents added after the corpus snapshot — those 2 items removed from the eval."
