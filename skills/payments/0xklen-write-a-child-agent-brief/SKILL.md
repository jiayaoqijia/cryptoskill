---
name: write-a-child-agent-brief
description: Use when delegating work to a spawned subagent or helper agent. Produces a brief naming the exact deliverable, input paths, forbidden scope, stop conditions, and report format so the child cannot drift or guess.
---

# Write a Child Agent Brief

A subagent knows only what its prompt says; every unstated assumption becomes a confident guess executed at full speed. Brief a child like an outside contractor with no memory of this conversation.

## Procedure

1. Open with the deliverable as one sentence that names an exact path: "Write `skills/foo/SKILL.md`; change nothing else."
2. Point at inputs by path and line range, never by description: "read `BRIEF.md` lines 11-13 and `TEMPLATE.md` in full."
3. Add an explicit forbidden list: "do not touch other skills, do not edit `TEMPLATE.md`, do not run git."
4. Paste the acceptance check verbatim so the child can self-test: `python3 tools/validate.py --only foo`.
5. Fix the report shape: "reply with the slug, then the validator summary line, nothing else."
6. Set a stop condition with a number: "if validation still fails after 3 attempts, stop and report the failing lines."
7. Hand over environment facts the child cannot cheaply rediscover: workspace root, the python interpreter, the scratch directory.
8. Freeze shared interfaces — names, schemas, IDs — that the child must copy exactly; the parent inherits any casing or spelling drift.
9. Cap the brief at roughly 300 words; long briefs bury the deliverable.
10. Repeat the deliverable in the final line, so truncation still leaves the ask visible.
11. Save the brief to `notes/children/<child-id>.brief.md` before spawning, so it can be re-read, diffed, and reused on retry.

## Pitfalls

- Writing requirements you never made checkable ("make it robust"), which the child cannot verify and will interpret its own way.
- Naming inputs as "the repo files" so the child reads forty files and burns its own context budget.
- Omitting the forbidden list, so a helpful child refactors a neighbour's file you were not tracking.
- Letting the child choose the artifact path, so its output lands where the parent never looks.
- Giving a report format that excludes raw command output, so a fabricated pass is indistinguishable from a real one.
- Assuming the child inherited your earlier conversation; it starts blank and guesses whatever you left implicit.

## Verification

```bash
ls notes/children/*.brief.md && grep -c 'skills/' notes/children/<child-id>.brief.md
# passes when the brief names an exact path and lists an explicit forbidden scope
```

Report to the user: the child id, the deliverable path, and the acceptance command you handed it.
