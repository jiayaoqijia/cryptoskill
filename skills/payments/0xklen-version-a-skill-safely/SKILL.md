---
name: version-a-skill-safely
description: Use when editing a skill that running tasks depend on. Stages the change, keeps the prior version recoverable, and records what changed.
---

# Version a Skill Safely

A skill is shared behaviour; editing it in place rewrites the rules under every task that relies on it. Treat skill edits like a release: change, record, keep the old one reachable.

## Procedure

1. Read the current skill fully before editing: `cat skills/<slug>/SKILL.md`.
2. Record the baseline so a regression is detectable: `git hash-object skills/<slug>/SKILL.md` (a content hash, no repo needed).
3. Make one change per edit — a version that changes the procedure *and* the pitfalls cannot be bisected when it misbehaves.
4. Bump a version line in front-matter: `version: 3` and `updated: 2026-10-08`.
5. Note the change in a `## Changelog` block: what moved, and why.
6. If the change alters the contract, keep the old behaviour available: write `skills/<slug>-v2/SKILL.md` and mark the new one the default.
7. Re-read the edited file end-to-end; a patch that drops a heading silently breaks the skill's structure.
8. Run any example commands the skill contains once, on the target system, before trusting the edit.
9. Tell callers when a skill they use changed in a breaking way; do not rely on them noticing.
10. Keep exactly one "current" skill per slug — two live copies under the same name is the failure to avoid.

## Pitfalls

- Editing a skill mid-task so the task runs half on the old rules and half on the new.
- Changing the procedure without updating the pitfalls, leaving contradictions in the file.
- Bumping the version without a changelog line, so "what changed" is unanswerable.
- Leaving both old and new skill under the same slug, and callers picking the stale one.
- Testing the edit on a hunch instead of re-running the commands the skill contains.

- Editing the file directly in a task's context so the running task re-reads new rules mid-way.
- Keeping the changelog in the commit message only, where a skill reader never sees it.
- Retiring the old version the moment the new one lands, before a rollback is possible.

## Verification

    git hash-object skills/<slug>/SKILL.md; grep -n "^version:\|^updated:" skills/<slug>/SKILL.md
    # passes when the hash differs from baseline, version and updated are present, and one current copy exists

Report to the user: the skill edited, the old and new hash, the changelog line, and the command you re-ran to confirm it.
