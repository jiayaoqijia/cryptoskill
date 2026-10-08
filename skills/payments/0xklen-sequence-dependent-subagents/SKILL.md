---
name: sequence-dependent-subagents
description: Use when subtasks depend on each other's output. Orders them into waves with explicit handoff artifacts so no child starts before its inputs exist.
---

# Sequence Dependent Subagents

Dependencies cannot be parallelised away. Put them in ordered waves and hand each wave's outputs to the next as concrete files, so a child never starts on inputs that do not exist yet.

## Procedure

1. Draw the dependency edges first: for each child, list which children's artifacts it consumes.
2. Topologically sort into waves: wave 1 has no inputs, wave 2 reads wave 1, and so on.
3. Reject any cycle — two children each needing the other is a design error; merge them or break the loop.
4. Define the handoff contract per edge: the exact file path and schema a consumer will read.
5. Freeze a wave's outputs before starting the next by hashing them into `notes/waves.log` so drift is detectable.
6. Launch each wave only after the previous wave's outputs all pass their checks and are frozen.
7. Give each child only the upstream paths it declared, not the whole prior wave's output.
8. Validate the handoff: a consumer should fail loudly, not silently, if its input file is missing or empty.
9. Keep the wave graph in `notes/dag.tsv` (`child<TAB>depends-on`) so the order is inspectable and reproducible.
10. On rerun, invalidate only the descendants of a changed child; upstream and unrelated branches stay frozen.

## Pitfalls

- Launching dependent children concurrently and hoping the faster one finishes first.
- Handing a consumer the entire prior wave instead of its declared input, so it reads a half-written sibling.
- Freezing outputs by memory rather than hash, so a later edit to wave 1 silently invalidates wave 2.
- A hidden cycle in the graph that only surfaces as two children waiting on each other forever.
- Re-running one mid-DAG child without invalidating its descendants, leaving them built on stale input.

## Verification

```bash
tsort notes/dag.tsv 2>&1 | tail -1; sha256sum out/wave-01/*
# passes when tsort reports no cycle and each wave's hashes match the frozen values
```

Report to the user: the wave order, each handoff path, and any descendant invalidated by a rerun.
