---
name: design-a-note-taxonomy
description: Use when notes have grown into an unsearchable pile. Designs folders, tags, and naming rules that stay stable as the store grows.
---

# Design a Note Taxonomy

A taxonomy that needs rethinking every month is worse than none. Good structure uses a small, fixed set of axes and puts every note on exactly one branch.

## Procedure

1. Sample 20 real notes and write the question each answers; the questions reveal the axes you actually need.
2. Choose at most three axes, e.g. `domain` (crypto, infra, ai), `kind` (fact, decision, howto), `status` (active, archived).
3. Make folders follow one axis only; put the rest in front-matter tags, not in deeper folders.
4. Fix the naming rule: `YYYY-MM-DD-<kebab-topic>.md` sorts chronologically and greps cleanly.
5. Reserve a directory per axis value: `notes/decisions/`, `notes/facts/`, `notes/howto/`.
6. Put cross-cutting labels in tags: `tags: [infra, dns, prod]` — never invent a folder for a tag.
7. Reject a new folder unless it clears a bar: at least 8 existing notes already belong in it.
8. Split a folder only when a query keeps returning two clearly different things; merge when two folders always get co-read.
9. Document the taxonomy in `notes/README.md` with one example path per rule.
10. Migrate existing notes to fit; a taxonomy no note obeys is fiction.

## Pitfalls

- One folder per topic, so the store grows a folder a week and nobody can recall the name.
- Tags and folders encoding the same axis, so a note can be filed two ways and found inconsistently.
- Nesting four levels deep, where no query ever reaches the bottom level.
- Naming notes with free text, so `fix`, `fixes`, and `bugfix` become three topics.
- Designing the taxonomy for a future store instead of the 20 notes that exist today.
- Leaving old notes unmigrated, so the new structure has 10% coverage and search still misses.

- Copying another project's taxonomy wholesale, which fits notes you do not have.
- Renaming folders after notes already link to the old paths, breaking every link.
- Documenting the taxonomy and never enforcing it, so new notes drift immediately.

## Verification

    find notes -name "*.md" | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head
    # passes when every leaf holds >= 8 notes and no leaf has a sibling topic it always co-occurs with

Report to the user: the three axes chosen, the naming rule, and the leaf counts after migration.
