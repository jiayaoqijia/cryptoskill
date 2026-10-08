---
name: trim-context-with-a-sliding-window
description: Use when a multi-turn conversation or long session exceeds the context window. Drop or summarise old turns deliberately, keep the system block and pinned facts, and re-state what must survive.
---

# Trim context with a sliding window

Long conversations grow past the window and the provider silently drops the oldest turns — often the ones that established the constraints. Manage the trim yourself so you choose what is lost.

## Procedure

1. Reserve the fixed part first: the system prompt, tool schemas, and any pinned facts (the user's original goal, agreed constraints) are never eligible for trimming.

2. Budget the rest: `history_budget = window - system_tokens - reserved_for_response`. Compute it, do not guess.

3. Trim by policy: drop the oldest turns once the budget is exceeded, but always keep the last few turns verbatim — immediate context matters most.

4. Prefer summarising the dropped region into a compact carried-forward note over hard deletion: "Earlier: user chose USD, file X, deadline Friday."

5. Re-state load-bearing constraints at the head of the trimmed context; do not rely on a middle turn that just got cut.

6. Count tokens after trimming, every turn, and trim before the send, not after a truncation error.

7. Log when a trim fired and what it dropped, so a sudden quality drop can be traced to the context change.

```python
def trim(history, budget):
    if sum(tokens(t) for t in history) <= budget:
        return history
    dropped, keep = history[:-KEEP_RECENT], history[-KEEP_RECENT:]
    return [summary(dropped)] + keep
```

## Pitfalls

- Letting the provider truncate from the middle or the oldest turn, cutting the constraint the task depends on.
- Summarising the immediate last turn, losing the specific detail the next reply needs.
- Trimming the system block or tool schemas, which breaks the call entirely rather than just degrading it.
- Assuming the summary is faithful; a lossy summary can invent a constraint that was never agreed.
- Never trimming, then hitting a hard context-length error that drops the whole request mid-batch.

## Verification

    python3 -c "import json;ctx=json.load(open('ctx.json'));print(sum(tokens(m) for m in ctx))"   # total never exceeds the window budget over a 50-turn replay

Report: "sliding window keeps the system block, pinned facts, and last 6 turns; older turns summarised into a running note; a 50-turn replay never exceeded 20k tokens and no constraint was lost."
