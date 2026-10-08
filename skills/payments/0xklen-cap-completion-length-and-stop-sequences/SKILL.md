---
name: cap-completion-length-and-stop-sequences
description: Use when model responses run long, cost more than expected, or never terminate cleanly. Set an output token cap and stop sequences, and detect the truncation the cap causes.
---

# Cap completion length and stop sequences

Unbounded generation is unbounded cost and a common source of corrupt output. Cap the response, define where it stops, and treat a cap-hit as a signal — not a silent trim.

## Procedure

1. Estimate the legitimate maximum output for the task: a classification is ~5 tokens, an extraction ~200, a summary ~500. Set `max_tokens` at roughly 1.5x that, not the model's global ceiling.

2. Pass `max_tokens` on every call. The default is often large, and a runaway loop then bills for the full ceiling.

3. Add stop sequences where the shape is known: `"\n\n"` for a one-paragraph answer, `"</output>"` for fenced blocks, a sentinel you asked the model to emit.

4. Detect the cap hit explicitly: check `finish_reason == "length"` (OpenAI) or `stop_reason == "max_tokens"` (Anthropic). A truncated response is a failure to handle, not a short success.

```python
if resp.finish_reason == "length":
    raise Truncated(task_id, cap=req.max_tokens)   # retry bigger or split the task
```

5. On a cap hit, either raise the cap for that task (if genuinely long) or split the work — do not silently accept a half answer.

6. Track the fraction of calls hitting the cap; a rising rate means your prompts or inputs grew, or the model changed.

7. Beware stop sequences that appear inside valid content — a quote containing `"\n\n"` truncates early. Choose sentinels that cannot occur naturally.

## Pitfalls

- Leaving `max_tokens` unset, so one bad prompt generates to the full limit and inflates the bill.
- Setting the cap to the model's maximum "to be safe" — you have not capped anything.
- Ignoring `finish_reason` and parsing truncated JSON, producing a decode error far from the cause.
- A stop sequence the model emits mid-content (`}`, `END`) cutting a valid answer short.
- Splitting long output only after it was truncated, losing the dropped content — split before regenerating.
- Setting one global cap for all endpoints, so the short classification inherits the long-report budget.
- Forgetting the cap is per response, not per session; a multi-call task still needs a total budget.

## Verification

    python3 -c "import json;r=[json.loads(l) for l in open('resp.jsonl')];print(sum(x['fr']=='length' for x in r), len(r))"   # cap-hit fraction; investigate if >2%

Report: "max_tokens=512 with stop='</json>'; cap-hit rate 0.3% over 20k calls, and every hit raises Truncated instead of returning a partial object."
