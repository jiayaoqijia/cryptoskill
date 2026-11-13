---
name: procedures-sops
domain: writing/procedures-sops
trigger: "\"write a procedure\", \"SOP\", \"runbook\", \"KB article\", \"release notes\"."
anti_trigger: "Choosing the doc set's types and README (subskills/technical-docs.md); in-product strings (subskills/ui-microcopy.md)."
scope: "Step-by-step instructions, SOPs, knowledge-base articles, release-note prose"
status: "seedling"
---

# Procedures & SOPs

## Standard

- **A procedure is a how-to guide in Diátaxis terms** (<https://diataxis.fr/>). It is problem-oriented, aimed at a competent user, preconditions first, outcome stated before step one, no theory in the runbook.
- **Templates beat one-off prompts.** One parameterised template per workflow, sections with sampled parameters and logical constraints. Amazon's open Agent SOPs pattern codifies markdown with SHOULD/MAY boundaries and chainable sub-SOPs (<https://emergentmind.com/topics/synthetic-standard-operating-procedure-sop-generation-framework>).
- **Knowledge-base articles answer one question.** One question per article, the direct answer in sentence one, a single H1 matching the title, short paragraphs and lists for steps, user-language titles.
- **Release notes are grouped and user-facing.** Deterministic generation from conventional commits (semantic-release plus the release-notes-generator plugin) where the commit log is disciplined (<https://github.com/semantic-release/release-notes-generator>). Otherwise categorise features, fixes and breaking changes by hand.
- **Freshness is a pipeline, not a hope.** Staleness signals — age untouched, ticket spikes, failed searches — feed drafting queues. Expose the last-reviewed date on every article.

## Decision rules

1. Number the steps in order. One action per step. A step with two verbs is two steps.
2. Put the condition before the step it gates — never as a note after it.
3. Mark MUST, SHOULD and MAY explicitly. An instruction with no modality is a preference nobody can enforce.
4. Every procedure carries a verification step with the expected result, and an owner plus a review date.
5. Sub-procedures are separate documents, linked, not nested inline — chainable, not page-per-task sprawl.
6. Release notes: the user's language, grouped by type, breaking changes first. Never paste raw commit text.

## Procedure

1. Walk the process once yourself, or watch someone who knows it. Record the branches.
2. Fill the template: purpose, scope, owner, review date, preconditions, steps, verification, rollback.
3. Write steps as imperative sentences: verb first, one action, no subordinate clauses.
4. Hoist every conditional above its step ("If the migration fails, stop and go to §Rollback").
5. Add the verification step with the observable pass state.
6. Test the procedure on a reader who has never done the task. Fix every step where they guess.
7. Publish with owner and review date. Set the staleness signal so the review is triggered, not remembered.
8. Release notes: group commits by type, rewrite each into the user's language, list breaking changes first, then features, then fixes.

## Anti-patterns

- Paragraph prose standing in for numbered steps.
- Conditionals buried after the step they gate.
- A procedure with no owner, no review date, no verification step.
- Nested inline sub-procedures that break the numbering.
- Release notes that are the git log.

## Done checklist

- [ ] Template filled, including owner and review date.
- [ ] Steps numbered, one action each, imperative.
- [ ] Conditionals hoisted above their steps.
- [ ] MUST/SHOULD/MAY marked.
- [ ] Verification step with expected result.
- [ ] Tested on an untrained reader.
- [ ] Staleness signal set.
- [ ] Release notes grouped and rewritten into user language.

## Sources

- <https://diataxis.fr/>
- <https://emergentmind.com/topics/synthetic-standard-operating-procedure-sop-generation-framework>
- <https://github.com/semantic-release/release-notes-generator>
- https://github.com/semantic-release/release-notes-generator
