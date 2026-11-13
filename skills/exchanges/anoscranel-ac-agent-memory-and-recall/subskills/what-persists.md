---
name: what-persists
domain: prompt-engineering/what-persists
trigger: "Deciding what an agent writes down so it survives the session."
anti_trigger: "Not for in-window budgeting, and not for the mid-task checkpoint."
scope: "The session-end write-down: what outlives the session and what dies with it."
status: seedling
---

# What persists

## Standard

Every session produces three kinds of knowledge: the durable facts (what changed, what was decided, what was learned), the perishable state (where the conversation went, which draft was tried first), and the noise (the back-and-forth that solved nothing). The write-down at session's end records the first class, and only the first class — a transcript is not a memory; it is a liability that must be re-read in full to find the three facts it buries.

The discipline is a triage done deliberately, not a dump done reflexively. The question for each candidate is: will a future session act differently because this is written down? Work products and outputs live in their own files and are referenced, not copied, into memory; the memory holds the fact, the pointer, and the reason, not the artefact itself.

Primary sources: <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents> and <https://en.wikipedia.org/wiki/Knowledge_management>.

## Decision rules

- Write down facts that change future action; do not write what is inferable from files on disk.
- Record the decision and its reason, not the deliberation that produced it.
- Reference artefacts by path; do not duplicate content into memory.
- Capture lessons while they are fresh: the end-of-session note is worth more than a week-later reconstruction.
- A candidate that no future session would look up is noise; leave it out.
- Date each persisted fact at the moment of writing.

## Procedure

1. At session end, list the durable candidates: changes, decisions, lessons, corrections.
2. Test each: would a future session act differently because this is remembered?
3. Drop the perishable and the inferable.
4. Write the survivors as dated notes, referencing artefacts by path.
5. Tag each note for the domain it serves.
6. Confirm nothing in memory duplicates a file that already persists it.

## Anti-patterns

- Persisting the whole conversation transcript as memory.
- Recording steps instead of outcomes.
- Duplicating file contents into notes instead of linking them.
- Writing nothing because the session felt routine; routine sessions still deposit lessons.
- Undated facts: memory without timestamps cannot go stale gracefully.

## Done checklist

- [ ] Durable candidates listed at session end.
- [ ] Action test applied to each.
- [ ] Artefacts referenced by path, not copied.
- [ ] Decisions recorded with reasons behind them.
- [ ] Notes dated at write time.
- [ ] Notes tagged by domain.

## Sources

- Context engineering for agents: <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Knowledge management fundamentals: <https://en.wikipedia.org/wiki/Knowledge_management>
- Note structure precedents: <https://en.wikipedia.org/wiki/Zettelkasten>
