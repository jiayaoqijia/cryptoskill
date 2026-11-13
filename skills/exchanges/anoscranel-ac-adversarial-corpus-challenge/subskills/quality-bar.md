---
name: quality-bar
domain: research-operations/quality-bar
trigger: "\"was the corpus actually challenged\", \"judge the adversarial round\", \"write the round record\", \"the review ran but changed nothing\"."
anti_trigger: "Running the round; scoring individual claims; applying corrections to files."
scope: "Judging whether a corpus was genuinely challenged: trade-offs, edge cases, the round record, and honest reporting of what a round measured"
status: "seedling"
---

# Quality bar

## Standard

- A corpus is genuinely challenged when an independent breaker attacked every headline claim, each got a disposition, every landed break survived re-check, and failed attacks are documented.
- Round numbers are descriptive, not benchmarks. A few runs are an existence proof, not a base rate.
- The audit trail must let a stranger reconstruct the round: charter, returns, re-checks, amendments, stop.
- In an illustrative round the audit trail ran longer than the findings, deliberately.

## Decision rules

1. Call a corpus challenged only if every claim has a disposition.
2. A break without re-check is incomplete, not landed.
3. Fewer well-evidenced breaks beat many shallow ones.
4. Zero breaks with a full ledger is a pass. Say so.
5. Stop at the time box, when sources repeat, or when evidence stops changing conclusions. State the criterion.
6. Do not compare raw counts without claim count and corpus size.

**Trade-offs.**

| Approach | Pros | Cons |
|---|---|---|
| Break-mandate round | Finds what producing rounds miss; cheap | Breaks often narrow; repair costs time |
| Self-review by producers | Free | Blind to the framing |
| More producing rounds | Finds new material | Produces more, not better |
| External human review | Highest judgment | Slow; unavailable unattended |
| Re-sampling a failing criterion | The numbers look better | Manufactures a pass |

**Edge cases.**

- A true claim stated badly: narrow the wording, not the substance.
- A break needing a source the round cannot add: unrepairable.
- A defect no register could catch: file a new defect shape; highest-value output.
- A break that kills the thesis: the thesis dies; report the narrower claim.
- A fix that is really a measurement project: narrow, record the residual, open a thread.
- Two claims that conflict across files: fix the shared root.
- A round that finds nothing: report saturation, stop.

## Procedure

Write the round record before the round closes:

| Field | Entry |
|---|---|
| Charter, corpus version, claims attacked | version; count and ids |
| Breaks attempted and landed | attempted; broken, narrowed, overturned |
| False positives and unrepairable rows | counts, reasons, open threads |
| Propagation | files changed; shipped-state re-check |
| Stop reason | criterion; claims untested |
| Residual doubts | targets for a later round |

An illustrative round attacked eleven conclusions: four broke, five narrowed, none overturned, and four repair cycles followed. The figures describe one corpus, not a target for the next.

## Anti-patterns

- **Round counted because it ran.** Activity is not a challenge.
- **Breaks without dispositions.** A list of concerns is not a scored round.
- **Raw-count comparison.** Eleven claims and forty do not compare.
- **Endless rounds.** Another pass to avoid an empty result is manufacture.
- **Audit trail as performance.** Length is not evidence; reconstructability is.

## Done checklist

- [ ] Every headline claim has a disposition.
- [ ] Every landed break has a re-check.
- [ ] Failed attacks and their conditions are recorded.
- [ ] False positives and unrepairable rows are counted.
- [ ] Propagation and the shipped-state check are recorded.
- [ ] Stop reason, residual doubts, and untested claims are named.

## Sources

- Stanford Encyclopedia of Philosophy, "Karl Popper", https://plato.stanford.edu/entries/popper/
- Center for Open Science, "Preregistration", https://www.cos.io/initiatives/prereg
- U.S. Army, University of Foreign Military and Cultural Studies, "The Red Team Handbook" (⚠️ edition unverified; cite the copy you read).
