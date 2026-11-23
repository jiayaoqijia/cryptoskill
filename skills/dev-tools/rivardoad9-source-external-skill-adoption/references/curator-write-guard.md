# Curator/background review turns: why SKILL.md writes bounce (and what to do)

Observed 2026-10-07 during a background curator pass on this very skill. Worth knowing before planning an
edit, because it costs 4-5 wasted tool calls otherwise.

## The symptom

Any `skill_manage action=patch|edit` aimed at **SKILL.md** is refused with:

```
Refusing background curator patch for skill '<name>': the current SKILL.md content has not been loaded in
this review turn. Call skill_view(name) for SKILL.md, or skill_view(name, file_path=...) for a supporting
file, then retry the write using the content just returned.
```

Retrying the read then hits the dedup path instead of satisfying the guard:

```
skill_view(name) → {"status": "unchanged", "dedup": true, "content_returned": false,
                    "message": "Skill content unchanged since it was loaded earlier in this conversation …"}
```

So the guard wants "content returned **in this turn**", but the session-level dedup refuses to return content
because it was already loaded earlier in the conversation. Catch-22: once you have read a skill's SKILL.md
earlier in a session, you cannot rewrite SKILL.md in that session's curator pass — a supporting-file view is
accepted by the guard's own wording but does **not** satisfy it in practice, and issuing view+write in one
message does not help either (the view still dedups).

## What actually works

1. **Land the whole change in ONE write, before any other write to that skill.** A `write_file` to
   `references/…` has **no** read-before-write guard — it succeeded repeatedly while every SKILL.md write
   bounced. If the learning fits a reference, this is the reliable path.
2. Prefer **`skill_manage action=create`** for a *new* skill (no prior content, no guard), or do the
   SKILL.md-level edit in a **foreground/user-present turn** where the guard is not applied.
3. Don't burn calls re-viewing: after the first dedup answer, the guard will not clear. Write to
   `references/` and report the situation instead.

## Discoverability without a SKILL.md pointer

`skill_view(<name>)` always returns a `linked_files` map, so a `references/<topic>.md` added this way is
visible to any future session that loads the skill — the "add a pointer line in SKILL.md" step is nice to
have, not required. Name the file for the class of work (`<bundle>-operations.md`), not for today's task.

## Note for the next curator pass

If you get a foreground turn on this skill, fold the two `references/remotion-opus-*.md` files into the
SKILL.md body (step 8 + pitfalls + reference list) so the guidance is loaded without a second read.
