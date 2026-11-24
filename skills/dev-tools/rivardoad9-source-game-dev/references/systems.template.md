# SYSTEMS.md template

Write this to the project root in Phase 3, derived from `GAME_SPEC.md`.
Keep it updated live throughout Phase 4/5 — it's the single source of truth
for build order and progress, and what Phase 0 reads to resume a session.

```markdown
# Systems

Build order top to bottom. Don't reorder without a real dependency reason
— note it inline if you do.

| # | System | Status | Test notes |
|---|--------|--------|------------|
| 1 | Input/controls | pending | |
| 2 | Core movement | pending | |
| 3 | Collision | pending | |
| 4 | Camera | pending | |
| 5 | {genre-defining mechanic} | pending | |
| 6 | UI/HUD | pending | |
| 7 | Audio | pending | |
| 8 | Mobile touch input (if mobile in scope) | pending | |
| 9 | Save/progress (if scope calls for it) | pending | |
| 10 | Level/content loading | pending | |

Status values: `pending` / `building` / `testing` / `done`.

Test notes: one line per completed test — what was exercised, what was
observed, pass or fail. Keep failed attempts in the log too (don't erase
history), just update status once it actually passes.
```

Add or remove rows to match what `GAME_SPEC.md` actually needs — this list
is a starting default, not a fixed template. A word game, for instance,
won't need collision or camera rows at all, and will need a
"word validation"/"word source loading" row instead.
