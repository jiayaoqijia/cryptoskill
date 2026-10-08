---
name: curate-a-reading-path-for-a-new-domain
description: Use when someone must get up to speed in an unfamiliar field. Builds a short ordered path of primary sources with a reason and a time budget each, instead of dumping a link list on them.
---

# Curate a Reading Path for a New Domain

A list of links is not a curriculum. An ordered path where each item earns its place, primary sources first and a stated time budget, gets a newcomer to working understanding without drowning them.

## Procedure

1. Cap the path at 5-8 items. More is abandonment dressed as thoroughness.
2. Lead with the primary source: the spec, the RFC, or the original paper, not a blog summary of it. For HTTP caching that is `RFC 9111`.
3. For each item give three fields: why it sits here, what to extract, and a time budget (`skim 15m` vs `read 90m`).
4. Order by dependency: each item should use only concepts from earlier ones.
5. Mark a stopping point: "after item 4 you can do X; items 5-8 are for when you hit Y".
6. Include one item that shows the field's current debate or known failure, so the learner does not take the rest as settled.
7. Store it as `reading-path.md` in the project so it is versioned, not lost in a chat thread.
8. Give the reader one small task that forces them to use the material: a config to write, a request to trace.
9. Re-vet the links every quarter; a moved spec or dead blog rots the path quietly.
10. Note the assumed starting knowledge so the path is not pitched above or below the reader.
11. Tag each item as primary or secondary so the reader knows what to trust most.
12. Add a one-line 'after this you can...' outcome to each item.
13. Keep a dated changelog of edits to the path, so its trustworthiness is visible.
14. State the reader's assumed background in one line at the top of the path.
15. Give each item a 'skip if you already know X' note so experts do not read everything.
16. Add a 'you are done when you can...' line at the end so the path has a finish.

## Pitfalls

- Nine blog posts where one spec plus one critique would do.
- Summaries of primary sources that silently drop the caveats the learner needs later.
- No time budgets, so the learner spends a whole day on a skim item.
- Ordering by popularity instead of by concept dependency.
- Never checking the links, so two of the five are 404 by the time a new joiner reads them.
- A path with no task, so the reading never converts into skill.
- Mixing three difficulty levels so a beginner stalls on item two.
- A path whose items all come from one author, hiding disagreement in the field.
- Including a paywalled source with no open alternative.
- A path with no stated prerequisites, pitched at the wrong reader.
- No skip notes, so a senior wastes hours on the basics.
- An open-ended path that never signals completion.

## Verification

    grep -c '^[0-9]' reading-path.md ; grep -c 'primary' reading-path.md
    # passes when item count is 5-8 and at least one is marked 'primary source'

Report to the user: the ordered list with each item's extraction goal and time budget.
