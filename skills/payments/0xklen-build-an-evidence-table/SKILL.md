---
name: build-an-evidence-table
description: Use when a conclusion rests on several claims of varying strength. Tabulate each claim with its source, type, and confidence so weak links are visible instead of buried.
---

# Build an evidence table

Prose hides weak links; a table exposes them. This skill lays every supporting claim beside the evidence behind it, so a conclusion cannot lean invisibly on one thin source.

## Procedure

1. State the conclusion in a single line at the top of `evidence.md`.

2. Create a table with columns: `# | claim | source | type | confidence | falsifier`.

3. Set `type` to exactly one of `primary` (you ran it or read the artefact directly), `secondary` (a report of the primary), or `inference` (derived from other rows).

4. Give each row a confidence from a fixed rubric — `verified/corroborated/inferred/assumed` — so the column does not drift between reviewers.

5. Fill `falsifier` with the command or observation that would disprove the row. A row without one is unfalsifiable and should be deleted.

6. Read the table back and ask: does the conclusion still hold if the lowest-confidence row is wrong? If not, gather one more primary source before reporting.

7. Check the ratio of primary to secondary rows: `grep -c "| primary " evidence.md` versus `grep -c "| secondary " evidence.md`.

## Pitfalls

- Twenty secondary sources traced to one origin are one piece of evidence, not twenty; count origins, not copies.
- A confidence column without a rubric drifts toward optimism as rows are added.
- Padding rows to make the table look thorough dilutes nothing but the reader's trust; keep it tight.
- An `inference` row that cites only other `inference` rows is speculation; ground it or cut it.
- A source you cannot reopen later (a chat scrollback) is weaker than one with a URL or path.

## Verification

    grep -c "^|" evidence.md; grep -ci "secondary" evidence.md

Report the primary-to-secondary ratio and name the single weakest row the conclusion depends on.
