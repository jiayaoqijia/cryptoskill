---
name: decompose-plan
domain: research-operations/decompose-plan
trigger: "\"break this question down\", \"plan the research\", \"how do I search for this\", \"split this into sub-questions\"."
anti_trigger: "Sharpening or reframing the question itself (subskills/scope-question.md); grading the sources a round returns (subskills/source-triage.md)."
scope: "Splitting a scoped question into independent sub-questions and a round-by-round search plan with a coverage matrix"
status: "seedling"
---

# Decompose into a search plan

## Standard

- A sub-question is atomic when one query round can answer it independently.
 Two sub-questions that share every source are one sub-question.
- Decomposition size has a measured prior, not a law: optimal granularity ≈
 0.85·√(number of source items) (⚠️ single-source, clawrxiv.io/abs/2604.00690;
 never cite it as arXiv). Treat
 it as a starting point, not a target.
- Cap decomposition depth at 3-4 levels. Measured cascade radius grows from
 0.9 corrupted stages at depth 3 to 4.7 at depth 7 (arXiv 2608.05263). Shallow
 and wide beats deep and fragile.
- Search fans out; synthesis does not. Plan wide reading, single writing.

## Decision rules

- Split when a sub-question needs a different source family than its sibling
 (academic index vs market data vs code repo).
- Merge when two sub-questions would return the same source set.
- One round = one batch of queries. Plan a re-evaluation point between rounds:
 what result changes the next round.
- If the whole plan fits in one round with no decisions between, the study is
 one-hop. Leave this skill family entirely.

## Procedure

1. List the atomic sub-questions under each hypothesis.
2. Assign each sub-question its source families (scholarly, news, code,
 market, primary docs).
3. Build the coverage matrix: sub-question × source family, one mark per cell.
4. Order rounds so cheap broad sweeps run before deep expensive pulls.
5. Write the plan as `plan.md` in the study folder on disk, created before the
 first query. Append decisions as the study runs.
6. Between rounds, re-read the matrix and mark cells covered, partial, open.

## Anti-patterns

- Decomposition by synonym: ten queries that are one query reworded.
- Ten queries for a one-hop answer.
- A plan that exists only in the chat transcript.
- No re-evaluation between rounds, so round two repeats round one.

## Done checklist

- `plan.md` exists on disk before the first query.
- Every sub-question has at least one source family assigned.
- The coverage matrix has no empty rows.
- Round boundaries name what changes the next round.

The plan also needs a stopping rule attached to each branch, not only to the whole study: a sub-question that keeps producing new sub-questions is a sign the decomposition is following the literature rather than the question, and the branch should be closed with what it established rather than split again.

## Sources

- arXiv 2608.05263 (cascade radius vs depth).
- <https://osf.io/prereg/>
- <https://arxiv.org>
