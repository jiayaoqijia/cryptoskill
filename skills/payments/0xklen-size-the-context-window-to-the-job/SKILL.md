---
name: size-the-context-window-to-the-job
description: Use when a prompt is near the context limit, costs too much, or drops instructions under truncation. Count input tokens, decide what stays in context versus what is fetched on demand, and measure before sending.
---

# Size the context window to the job

Every token you send is paid for and competes for attention. Fit the prompt to the job: keep the instructions and the load-bearing evidence, move reference material behind a retrieval step, and count tokens before the request fails.

## Procedure

1. Compute the real input size, not an estimate — tokenise the full prompt. Counts differ per model family.

```bash
python3 -c "import tiktoken as t; print(len(t.encoding_for_model('gpt-4o').encode(open('prompt.txt').read())))"
# model-agnostic fallback: one token ~4 chars of English
wc -c prompt.txt
```

2. Set a hard budget below the model's limit — leave 20-30% for the response and for prompt variance across real inputs: `budget = window * 0.7`.

3. Sort the prompt into three tiers: (a) must-have — task, constraints, output format; (b) conditional — examples and evidence the task actually needs; (c) reference — docs, tables, whole files.

4. Move tier (c) out of the prompt. Retrieve only the rows or sections the current input needs (search, then include top-k). A 200-page manual becomes 2 pages of relevant text.

5. Trim tier (b) to the smallest set that still clears your quality sample; drop examples that duplicate coverage.

6. Prefer summarising over truncating: a model given a summary of prior context beats one given the last N tokens with the middle silently cut.

7. Re-measure after each cut and record tokens-in per call, so cost per request is a tracked number rather than a surprise on the invoice.

## Pitfalls

- Relying on the provider to "just truncate": the cut is usually from the middle or the oldest turns, silently dropping the instruction or the one relevant fact.
- Treating the context limit as the budget; the response also consumes the window and truncated output is corrupt output.
- Estimating with `chars/4` for non-English or code-heavy prompts; CJK text and code run far denser and blow the estimate.
- Stuffing the whole corpus "just in case" — it raises cost linearly and lowers accuracy as attention dilutes.
- Forgetting the system prompt, tool schemas, and few-shot block in the count; they are input tokens too.
- Retrieving into every call when the task is stable; a fixed, smaller prompt is cheaper than a per-request search step.

## Verification

    python3 count_tokens.py prompt.txt tools.json   # must be < window*0.7; prints total and per-section

Report: "prompt is 3,140 tokens against a 12k budget (26% of window); moved the API reference behind retrieval, saving ~9k tokens per call."
