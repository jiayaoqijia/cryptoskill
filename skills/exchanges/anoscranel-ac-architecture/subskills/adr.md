---
name: adr
domain: software-engineering/adr
trigger: "\"Write an ADR\", \"record this decision\", \"why did we choose X\", \"supersede the old decision\", \"set up a decision log\"."
anti_trigger: "Making the architecture choice itself (subskills/architecture.md); wording a full design proposal; code comments and generated reference."
scope: "Writing, numbering and superseding Architecture Decision Records"
status: "seedling"
---

# ADR

## Standard

- **Nygard format** (Michael Nygard, "Documenting Architecture Decisions", 2011): Title, Status, Context, Decision, Consequences.
- **MADR** (https://adr.github.io/madr/) adds considered options and pros/cons per option.
- Status lifecycle: Proposed → Accepted → Deprecated or Superseded.
- ADRs live in the repo, version with the code, and are superseded, never deleted.
- Tools: adr-tools, Log4brains (https://adr.github.io).

## Decision rules

1. Write an ADR when a decision is architecturally significant: hard to reverse, affects structure, quality attributes, dependencies, interfaces or build tooling.
2. One decision per ADR.
3. Numbers are sequential and never reused: `0001`, `0002`.
4. An Accepted ADR is immutable. Change of mind → write a new ADR that supersedes it. Edit the old one only to set `Status: Superseded by 0014`.
5. Context states forces and constraints, not the answer.
6. Consequences list good and bad results, including new risks and follow-up work.
7. Record what evidence would prove the decision wrong.
8. Accepting an ADR is **human-gated**. The agent drafts; a human sets Accepted.
9. Small reversible choices skip the ADR. A one-line comment or commit message is enough.

## Procedure

1. Check the log: `ls docs/adr/`. Find any ADR on the same topic.
2. Take the next number. Create `docs/adr/NNNN-<kebab-title>.md`:
   ```markdown
   # NNNN. Use PostgreSQL for order storage
   Date: 2026-10-17
   Status: Proposed
   Deciders: <names>
   ## Context
   <forces, constraints, requirement IDs>
   ## Considered options
   1. PostgreSQL  2. DynamoDB  3. Keep SQLite
   ## Decision
   We will use PostgreSQL because <reason tied to forces>.
   ## Consequences
   + <benefit>   − <cost>   Follow-up: <task>
   ## Revisit when
   <evidence that would reverse this>
   ```
3. Write Context from the spec or discussion. Link the spec.
4. List options with one-line pros and cons.
5. State the Decision in active voice: "We will…".
6. Write Consequences, both directions.
7. If it replaces an older ADR, set the old one's status to `Superseded by NNNN` and add `Supersedes MMMM` to the new one.
8. Add the ADR to `docs/adr/README.md` index (number, title, status).
9. Open a PR. A human sets Accepted on merge.
10. Link the ADR from the code it governs, e.g. a comment `// See ADR-0007`.

## Anti-patterns

- ADR written months later from memory.
- Editing an Accepted ADR's decision in place.
- Many decisions in one record.
- Context that argues for the answer.
- Log never reviewed, so stale ADRs stay "Accepted".

## Done checklist

- [ ] Number unique and sequential.
- [ ] Context, options, decision, consequences and revisit trigger filled.
- [ ] Superseded ADR updated with a link.
- [ ] Index updated.
- [ ] Human acceptance recorded.

## Sources

- <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
- <https://github.com/joelparkerhenderson/architecture-decision-record>
- <https://www.iso.org/standard/78176.html> S3.3
- https://adr.github.io · https://adr.github.io/madr/
