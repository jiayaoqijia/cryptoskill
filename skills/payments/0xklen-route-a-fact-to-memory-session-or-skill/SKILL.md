---
name: route-a-fact-to-memory-session-or-skill
description: Use when deciding where a new fact belongs — durable memory, session scratch, or a reusable skill. Routes by lifetime and reuse so knowledge lands where it will be read again.
---

# Route a Fact to Memory, Session, or Skill

Storing a fact in the wrong place means it is either lost at session end or clutters a store it does not belong in. Route by two axes: how long it stays true, and how often it will be reused.

## Procedure

1. Classify the fact by lifetime: `ephemeral` (true only this session), `durable` (true for weeks or months), or `procedural` (a repeatable how-to).
2. Route by class:
   - `ephemeral` -> session scratch, e.g. `notes/session.md`. Never promote it.
   - `durable` -> the memory store under `~/.hermes/memories/`, written as one dated line with a source.
   - `procedural` -> a skill under `skills/<slug>/SKILL.md`, with commands and pitfalls.
3. Ask whether the fact will be *read again*. A one-off value you will never query belongs in the current transcript, not in any store.
4. Check for an existing home before writing a new one: `grep -ri "<key>" ~/.hermes/memories/ skills/`.
5. Write durable facts with a date and an origin: `2026-10-08 deploy host = prod-2 (source: aws describe-instances)`.
6. When a durable fact changes, edit the existing entry rather than appending a second — appending creates a conflict for later readers.
7. Promote an ephemeral fact only after it has survived a session and been needed twice; the second need is the evidence.
8. Send procedural knowledge that has run correctly three times to a skill; before that, keep it in scratch.
9. Keep memory for *facts*, skills for *steps*. A memory entry that reads as a numbered list is a skill in disguise.
10. Record the routing decision in one line so a future reader knows why the fact lives where it does.

## Pitfalls

- Writing a reusable procedure into memory, where it will be read as a fact and never executed.
- Promoting a session value ("current build id") into durable memory, where it goes stale in a day.
- Appending a corrected fact next to the old one instead of editing it, so the store now contradicts itself.
- Creating a new skill for a one-off command that ran exactly once.
- Storing a fact with no date, so a later reader cannot tell if it is still true.
- Leaving scratch files where the next session auto-loads them, polluting the fresh context.

## Verification

    grep -c "^20[0-9][0-9]-" ~/.hermes/memories/*.md 2>/dev/null; ls skills/
    # passes when every durable fact carries a date and every procedure lives under skills/

Report to the user: the fact, the class you assigned, the store it landed in, and the one-line reason.
