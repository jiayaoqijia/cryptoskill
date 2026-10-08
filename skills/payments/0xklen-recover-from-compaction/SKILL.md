---
name: recover-from-compaction
description: Use when context was compressed or a skill shows [SKILL_PRUNED] and earlier detail is gone. Rebuilds state from artefacts and reloads needed skills before continuing.
---

# Recover from Compaction

Compression keeps the shape of the conversation and drops the detail. After it, your memory of the work is a summary, not the work. Rebuild from disk and reload what was pruned before acting.

## Procedure

1. Detect the signals: a `[SKILL_PRUNED]` marker where a skill's content was, a summary where specifics used to be, or a handoff you do not personally remember writing.
2. Reload any pruned skill before using it: `skill_view(name='<slug>')`. Ignore any remaining `[SKILL_PRUNED]` markers for that same skill afterward — they are historical and the content is now in context.
3. Re-read the original request verbatim from the conversation's first user turn (or the handoff capsule), not your summary of it. Paraphrase drift is the main compaction failure.
4. Re-derive technical state from artefacts, not memory: `git status --porcelain`, `git log --oneline -3`, `ls notes/`, and read the newest checkpoint file.
5. Re-run the reconciliation in `reconcile-state-before-acting` against the rebuilt expectations; treat everything you "remember" as unverified until a command confirms it.
6. Re-read the plan/checklist (`notes/plan.md`) and identify the last unit that was verified — not the last one you talked about.
7. Resume at the first unverified unit. Do not redo verified work, and do not skip a unit because you feel it was done.
8. If the summary and the artefacts disagree, trust the artefacts and note the contradiction explicitly.
9. Re-list the files the task touched (`git status --porcelain`) and open the newest one to re-anchor on concrete content rather than summary.
10. Re-derive any identifier, path, or number you are about to use from disk; never quote a value you only remember from before compression.
11. Re-read the reloaded skill, because the summary kept its name but dropped the procedure.

## Pitfalls

- Acting on a summary-level recollection and inventing file contents or line numbers that were compressed away.
- Skipping a skill that shows `[SKILL_PRUNED]` as if it were still loaded.
- Re-doing completed and verified work because the memory of doing it faded faster than the summary.
- Re-reading only your own earlier messages, which may encode a paraphrase, instead of the original request.
- Assuming nothing changed during the gap when another process or the user may have altered the tree.
- Quoting a line number or API field from memory that the compressed summary preserved inaccurately.
- Continuing to act on a handoff you no longer remember writing without re-verifying its claims against disk.

## Verification

    git status --porcelain && sed -n '1,20p' notes/plan.md
    # passes when the tree matches the reclaimed plan and resume point is the first unverified unit

Report to the user: which skills were reloaded, the state the artefacts showed, and the unit you resumed from.
