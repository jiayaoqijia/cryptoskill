---
name: fan-out-and-fan-in-subagents
description: Use when one task splits into many independent subtasks to run in parallel. Defines the launch wave, the per-child artifact contract, and the exact fan-in aggregation so no result is silently lost.
---

# Fan Out and Fan In Subagents

Parallel work is a fan-out of children plus a deterministic fan-in at the end. If the fan-in cannot name every child and its artifact, the parallelism produces chaos rather than speed.

## Procedure

1. Prove the subtasks are independent: no child's input is another child's output. A dependency belongs in a second wave.
2. Write the roster before launching: `notes/roster.json` with one object per child `{id, slug, brief_path, artifact_path}`.
3. Give every child a disjoint output path under a wave directory: `out/wave-01/<child-id>/`.
4. Launch the whole wave, recording each child id as it starts; a lost id is a lost result.
5. Poll for completion against the roster, not against "how many finished"; count `completed == len(roster)`.
6. Fan in by iterating the roster file in code, appending each artifact to `out/wave-01/all.jsonl` — never merge by hand.
7. Deduplicate the merged set on the child key before reporting; two children on the same key is a fan-out bug, not a merge step.
8. Verify the merged count equals the roster size: `wc -l < out/wave-01/all.jsonl` against `jq length notes/roster.json`.
9. Only if every child passed its own check does the wave advance; one failure re-runs just that child's slot.
10. Freeze the wave once merged — later waves read the frozen artifact, not a live rerun.

## Pitfalls

- Fanning out subtasks that secretly share state (same file, same counter), so results depend on scheduling order.
- Merging by concatenation without recording which child produced each block, losing provenance on a bad row.
- Collecting "the results I saw printed" rather than iterating the roster, which drops a child that timed out.
- Letting a child invent its own output path, so the fan-in glob misses it.
- Advancing the wave with a hole where a failed child should be, then discovering the gap three steps later.

## Verification

```bash
jq length notes/roster.json; wc -l < out/wave-01/all.jsonl
# passes when the two numbers are equal and every roster id appears in the merged file
```

Report to the user: the wave id, the roster size, the merged count, and any child whose artifact is missing.
