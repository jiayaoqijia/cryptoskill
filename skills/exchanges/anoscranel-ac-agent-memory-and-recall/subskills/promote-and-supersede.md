---
name: promote-and-supersede
domain: prompt-engineering/promote-and-supersede
trigger: "Moving a working fact into permanent memory, or replacing one that changed."
anti_trigger: "Not for first-draft storage of notes, and not for retrieval."
scope: "Working note to permanent memory, dedupe, and contradiction handling."
status: seedling
---

# Promote and supersede

## Standard

Memory accretes in two layers: a working layer where fresh facts sit until proven durable, and a permanent layer that future sessions trust. Promotion moves a fact up once it has survived contact — used twice, or validated against a source. The traffic is one-way in principle and honest about exceptions: a promoted fact that later proves wrong is not deleted; it is superseded, with the successor note linking back to the claim it replaced.

Supersession is the discipline that separates memory from a log. Appending a contradiction produces a memory that argues with itself; the next session retrieves both notes and cannot tell which is current. The superseding note states what changed, links the note it replaces, and carries the date; the superseded note is marked, not destroyed, because the history of what was believed and when is itself evidence.

Primary sources: <https://en.wikipedia.org/wiki/Knowledge_management> and <https://en.wikipedia.org/wiki/Zettelkasten>.

## Decision rules

- Promote only after the fact survives its second use or its first source verification.
- Never append a contradicting fact: supersede, linking the old note.
- The superseding note carries what changed and the date of the change.
- Mark superseded notes visibly; a stale note that looks current is the worst state.
- Dedupe on promotion: two working notes stating one fact collapse into one permanent note.
- Corrections record why the old claim was believed, when that history matters.

## Procedure

1. List working facts and their usage or verification status.
2. Promote the survivors, one fact per note, dated.
3. For each contradiction found, write the superseding note and mark the superseded one.
4. Link superseding to superseded in both directions.
5. Collapse duplicates at promotion time, keeping the better title.
6. Record promotion and supersession dates in the memory inventory.

## Anti-patterns

- Appending the new fact beside the old one and letting both stand.
- Promoting on first sight, before the fact has survived anything.
- Deleting the superseded note, losing the history of belief.
- Leaving stale notes unmarked because deletion feels cleaner.
- Promoting duplicates, on the theory that redundancy is harmless.

## Done checklist

- [ ] Facts promoted only after surviving use or verification.
- [ ] Contradictions superseded, never appended beside.
- [ ] Superseded notes visibly marked and linked.
- [ ] Promotion and supersession history retained.
- [ ] Duplicates collapsed into a single note.
- [ ] Dates recorded for promotion and supersession events.

## Sources

- Knowledge life-cycle: <https://en.wikipedia.org/wiki/Knowledge_management>
- Supersession structure in note systems: <https://en.wikipedia.org/wiki/Zettelkasten>
- Long-lived knowledge base practice: <https://www.gwern.net/About-This-Website>
