---
name: separate-durable-facts-from-session-scratch
description: Use when a session is mixing throwaway state with facts that must outlive it. Splits the two into different stores so scratch never pollutes durable memory.
---

# Separate Durable Facts from Session Scratch

Mixing scratch into the durable store is how memory fills with values that were true for ten minutes. Two stores, one rule each: scratch dies with the session, facts survive it.

## Procedure

1. Name the two stores explicitly at the start: durable at `~/.hermes/memories/`, session at `notes/session.md`.
2. Route every write by asking "will this be true and useful next month?" — no means scratch.
3. Keep transient values in the session file: build ids, temp paths, the current task's progress.
4. Keep durable facts dated and sourced; a value you cannot re-derive later is durable only if you date it.
5. Serve reads from scratch first for in-session data, falling back to the durable store.
6. Never promote scratch wholesale at session end; promote line by line, only what proved durable.
7. At session end, archive the scratch file rather than deleting it, so a fast follow-up can still read it.
8. Give the session store a TTL: prune anything older than 7 days automatically.
9. Keep the two in separate directories so a bulk grep of memory never returns scratch noise.
10. When the same scratch fact is needed in three sessions, that repetition is the promotion signal.

## Pitfalls

- Writing a session temp path into durable memory, where it points at nothing a day later.
- Promoting a whole scratch file at session end, importing the noise along with the one real fact.
- Serving durable reads from scratch and reading a stale in-session value as if it were the fact.
- Deleting scratch at session end and losing the mid-task detail a follow-up task needed.
- One store for both, so every durable query returns a mix of live facts and dead temporaries.

- Storing the session file inside the memory directory, so it is read as durable next load.
- Promoting by filename rather than by line, importing scratch directives as if they were facts.
- Letting one tool write both stores from a single call, so the split is decided by the tool, not you.

## Verification

    grep -L "^20[0-9][0-9]-" notes/session.md; find ~/.hermes/memories -name '*.md' -exec grep -L "^20[0-9][0-9]-" {} +
    # passes when scratch holds no dated facts and memory holds no undated values

Report to the user: the two store paths, what was written to each, and the rule that decided the split.
