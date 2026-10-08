---
name: pick-a-tool-by-capability-not-novelty
description: Use when choosing which tool to call for an agent step. Match the tool to the capability and side-effect profile of the step, not to what is newest or most familiar.
---

# Pick a tool by capability, not novelty

Agents default to whatever tool they called last. The right choice is the narrowest tool whose capability, side effects, and cost actually fit the step — decided before the call and justified after it.

## Procedure

1. Write the step as an outcome before picking a tool: `write 42 rows to customers.db`, not `use the db helper`.
2. Score each candidate on three axes: capability (can it do the job), side effects (read / write / spend / network), cost (latency, tokens, money).
3. Prefer the narrowest tool that still completes the step: `grep -n` over `web_search`, `read_file` over `terminal("cat ...")`.
4. Reject a familiar tool whose side effects exceed the step. A read-only step must not call a tool that writes, spends, or hits the network.
5. When two tools tie on capability, pick the one with a typed schema over raw shell — schemas reject bad arguments before execution.
6. Record the choice in the action log: `step=3 tool=read_file why="single file, no side effects"`.
7. If no available tool fits, escalate to the user rather than repurposing a tool with the wrong side-effect class.
8. Re-evaluate after every third step: the cheapest tool for step 1 is often wrong for step 3.
9. Keep a short note of tools you tried and rejected, so a later step does not re-litigate the same choice.
10. When a tool's description is ambiguous, prefer the one whose failure mode you can detect — an explicit error beats a silent wrong result.

## Pitfalls

- Choosing `terminal` for everything because it is general: it hides side effects and skips schema checks.
- Reaching for `web_search` to answer a question already present in a local file.
- Using a write tool to "test" connectivity, leaving state behind on a read step.
- Optimising for a tool you happen to remember instead of one the environment lists.
- Treating a fuzzy-match tool result as ground truth instead of following up with an exact read.
- Ignoring cost when the same result is available from a cheaper tool with fewer round-trips.

## Verification

```bash
grep -E 'step=[0-9]+ tool=' notes/action.log | awk '{print $2, $3}' | sort | uniq -c
# passes when each step shows one tool and no read step uses a write-class tool
```

Report the tool chosen per step with the one-line reason recorded next to it.
