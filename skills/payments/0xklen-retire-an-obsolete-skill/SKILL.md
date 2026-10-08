---
name: retire-an-obsolete-skill
description: Use when a skill no longer matches reality and misleads tasks that load it. Deprecates it, redirects callers, and removes it without leaving a gap.
---

# Retire an Obsolete Skill

A skill that no longer works is worse than a missing one: it loads confidently and gives wrong steps. Retirement is a controlled removal — redirect first, then delete.

## Procedure

1. Prove obsolescence with a concrete failure: run its main command and show it errors or does the wrong thing.
2. Find who loads it: `grep -rl "<slug>" . --include='*.md'`.
3. Write the replacement first — retire only once the successor exists and is verified.
4. Mark the old skill deprecated rather than deleting immediately: `status: deprecated` plus a pointer to the successor.
5. Redirect callers by editing their references to the new slug.
6. Keep the deprecated file for one release cycle so an external caller does not break silently.
7. After the cycle, delete the directory and remove any index or listing entry for it.
8. Check the slash-command or skill registry for a leftover entry that still routes to it.
9. If it has no successor and the procedure is simply gone, say so plainly rather than leaving a broken skill.
10. Record the retirement: slug, reason, successor, date.

## Pitfalls

- Deleting the skill before the replacement is verified, leaving a gap.
- Leaving a deprecated skill unmarked, so it still loads and still misleads.
- Marking deprecated but not fixing the references, so callers keep invoking the old slug.
- Retiring because the skill is old rather than because it is wrong — age is not obsolescence.
- Forgetting the registry or index entry, so the name still resolves to nothing.

- Deprecating a skill that an automated task references and never updating the task.
- Burying the successor pointer in a comment instead of where a reader loads it.
- Deleting the directory while a task is mid-run and depending on it.

## Verification

    grep -rn "<slug>" . --include='*.md' | grep -v deprecated; ls skills/<successor>/SKILL.md
    # passes when no live reference points at the old slug and the successor exists

Report to the user: the slug retired, the failure that proved it obsolete, the successor, and the references redirected.
