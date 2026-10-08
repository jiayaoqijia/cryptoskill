---
name: detect-an-agent-tool-call-loop
description: Use when an agent may be repeating the same tool call without progress. Detect the cycle mechanically from the action log and break it instead of trusting a hunch.
---

# Detect an agent tool-call loop

Agents do not announce loops; they keep working. A repeated (tool, arguments) pair with an unchanged result is the signature, and only the log can prove it.

## Procedure

1. Log every call as a canonical tuple: `tool | hash(args) | hash(result) | exit_code | turn`.
2. After each call, compare the new tuple to the previous two. Two identical tuples is the loop threshold.
3. Also watch for A-B-A-B oscillation: alternate two calls whose results never change — treat a four-turn cycle as a loop.
4. On detection, halt the current approach. Do not fire the same call a third time "to be sure".
5. Diagnose the class: stale state (the input genuinely did not change), wrong tool, or a stop condition that never becomes true.
6. Change one variable before retrying — a different tool, a broader query, or a fresh read of the state.
7. If the input is genuinely unchanged, the loop is telling you the task is done or blocked; stop and report rather than retrying.
8. Escalate to the user after the second failed break attempt; repeated self-breaks that also loop is a dead end the agent cannot see.

```python
def looped(log, n=2):
    recent = [f"{c.tool}|{c.arg_hash}|{c.result_hash}" for c in log[-n:]]
    return len(recent) == n and len(set(recent)) == 1
```

## Pitfalls

- Counting only the tool name and missing that the arguments changed, which is progress, not a loop.
- Counting only arguments and missing that the result is now different, which means the call did something.
- Treating a legitimate retry after a transient 429 as a loop and aborting a task that would have succeeded.
- Breaking the loop by silently switching tools without recording why, so the failure repeats next run.
- Forgetting to reset the counter after a real state change, so a false positive halts good work.
- Letting a stop condition read from a cache that never refreshes, so the loop never terminates on its own.

## Verification

    python3 tools/loopcheck.py notes/action.log --window 2   # prints "OK" or the repeated tuple

Report the repeated call, its argument hash, and the one variable changed to break it.
