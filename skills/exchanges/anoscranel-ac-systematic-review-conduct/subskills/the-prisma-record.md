---
name: the-prisma-record
domain: research-operations/prisma-record
trigger: "Keeping the PRISMA flow counts while the review runs, not after."
anti_trigger: "Not for drawing the diagram at write-up from memory."
scope: "The flow diagram as a counting record, kept while the review runs."
status: seedling
---

# The PRISMA record

## Standard

The flow record is the review's arithmetic: records identified, deduplicated, screened, excluded at each stage, retrieved, excluded with reasons, and included. Each number is a count of real objects that existed at a real time, and the diagram's honesty is inherited entirely from whether those counts were written down as they happened. Reconstructed at the end, the numbers converge on plausibility rather than truth.

Keeping it live is cheap and it changes behavior. When the excluded-at-full-text count must be categorized by reason as it happens, the team notices that "wrong population" is doing too much work, and the categories refine while refinement is still legitimate. The record also carries the non-trivial counts that diagrams often omit: records awaiting translation, full texts never retrieved, and studies excluded for discontinuous outcome reporting.

Primary sources: <https://prisma-statement.org> and <https://training.cochrane.org/handbook>.

## Decision rules

- Record counts at every stage transition as they happen, with dates.
- Categorize full-text exclusions by reason at the moment of exclusion.
- Track unretrieved full texts and records awaiting translation as their own counts.
- Keep the deduplication count and the method that produced it.
- Reconcile the totals before writing: identified minus duplicates minus screened-exclusions equals assessed.
- Version the record when the search is updated, keeping both runs.

## Procedure

1. Create the count sheet at first search with the initial identification total.
2. Add counts at each stage as the stage completes.
3. Categorize each full-text exclusion by coded reason as it happens.
4. Track exceptional counts: translations, retrievals, duplicates by source.
5. Reconcile the arithmetic end-to-end before write-up.
6. Archive the sheet with the conduct record.

## Anti-patterns

- The diagram drawn from recall at submission time.
- Exclusion reasons invented to fill the categories.
- Duplicates counted differently at different stages.
- Unretrieved texts dropped from the accounting entirely.
- A search rerun with only one run's numbers kept.

## Done checklist

- [ ] Counts recorded live at every stage.
- [ ] Exclusion reasons coded at exclusion time.
- [ ] Exceptional counts tracked separately.
- [ ] Deduplication method and count logged.
- [ ] Arithmetic reconciled before write-up.
- [ ] History preserved across search updates.

The flow record is also the place where the review's honesty is visible at a glance: a search identifying thousands but yielding three included studies tells a different story from a search that identified hundreds, and the intermediate exclusions explain the difference. Reviewers and editors read the flow diagram first precisely because the numbers there cannot be styled, only counted, and the record kept live is the only one that can be trusted not to have been arranged.

## Sources

- PRISMA 2020 statement and flow: <https://prisma-statement.org/>
- Cochrane Handbook, selecting studies: <https://training.cochrane.org/handbook>
- EQUATOR reporting guidance: <https://equator-network.org/>
