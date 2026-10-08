---
name: cap-agent-tool-call-recursion-depth
description: Use when an agent can call a tool that may invoke the agent again, or spawn subagents. Bound the depth and total descendants so delegation cannot run away.
---

# Cap agent tool-call recursion depth

Agents that can spawn agents, or call a tool that re-enters the loop, grow exponentially until the budget dies. Bound the depth at a small number and refuse delegations past it.

## Procedure

1. Declare a maximum depth before the run — a flat fan-out, depth 2 (parent plus children), is usually enough.
2. Pass the current depth in every delegation call: `run_subagent(brief=..., depth=2, max_depth=3)`.
3. Refuse any call that would exceed `max_depth`, returning a clear `depth_exceeded` error the parent must handle.
4. Cap total descendants as well as depth: depth 3 with branching 10 is 1000 agents; cap the count at, say, 20.
5. Require each child to be strictly narrower than its parent — a child that re-delegates the same brief is a loop.
6. Track a delegation tree in the run state so depth and count are measured, not assumed.
7. Treat a tool that "calls the agent again" the same as spawning: carry depth through it too.
8. When depth is hit, do the work inline instead of delegating — a leaf that cannot spawn is still an agent.

```python
MAX_DEPTH, MAX_DESC = 3, 20
def spawn(brief, depth, spawned):
    if depth >= MAX_DEPTH or spawned >= MAX_DESC:
        raise RuntimeError(f"delegation refused depth={depth} spawned={spawned}")
    return run_subagent(brief, depth + 1, spawned + 1)
```

## Pitfalls

- Letting a child spawn a grandchild with the same brief, doubling work at every level.
- Capping depth but not total count, so a wide fan-out still exhausts the budget.
- Passing depth in a global variable that a child cannot see, so every child thinks it is depth 0.
- Allowing a re-entrant tool call to reset depth, so recursion never terminates.
- Setting max depth so high ("just in case") that it provides no bound at all.
- Counting only successful spawns, ignoring refused ones that still consumed a model turn.

## Verification

    grep -oE 'depth=[0-9]+' notes/action.log | sort -u | tail -1   # largest depth <= declared max_depth

Report the declared max depth and count, the deepest delegation used, and any refusal.
