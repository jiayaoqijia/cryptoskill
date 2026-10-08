---
name: do-a-gap-analysis
description: Use when before declaring research or a review complete. Names what the search could not have found and how that absence could change the conclusion.
---

# Do a Gap Analysis

The most dangerous gaps are the ones your method structurally could not reach. Before calling a review complete, map the empty space and say how it could overturn the answer.

## Procedure

1. Enumerate the coverage dimensions and mark what you actually searched: languages, time period, regions, databases, source types, and query terms used.
2. List structural blind spots: paywalled journals, non-English literature, grey literature, retracted work, offline-only records, private datasets, and sources that would exist only if a result were negative (publication bias).
3. Check for publication bias explicitly. A field showing only positive results and no null findings is a funnel plot lying flat — the missing nulls are the gap.
   ```bash
   # how many included studies report a null result?
   grep -ciE 'no (significant )?(effect|difference)' included.txt
   ```
4. Search the negative space: for reviews, run `web_search("<topic> not found")`, `web_search("<topic> failure")`, and check citation chains *forward* to find contradicting work the original cites never did.
5. For each gap, state the direction of the possible bias: which way would it move the conclusion if filled?
6. Rank gaps by how decision-relevant they are — a gap that could flip the recommendation outranks one that only adjusts a decimal.
7. Report the gaps in the deliverable, with the search that would close them, rather than silently omitting them.

## Pitfalls

- "No evidence found" is not "evidence of no effect"; state which one you mean.
- Restricting to one language or database manufactures a gap you then mistook for consensus.
- A gap you could not search is different from a gap you chose not to search — label which.
- Forward citation checking finds contradictions that keyword search and reference-chasing both miss.
- Ranking gaps by ease of filling rather than by impact on the conclusion inverts the point.
- A gap you found by accident (one non-English paper) signals the whole non-English space is unexplored, not that the gap is small.

## Verification

    grep -cE 'gap|not searched|publication bias|limitation' report.md

Each coverage dimension has a stated status (searched / not searched) and every ranked gap names a direction of possible bias.

Report: "Covered English + German 1990–2024, 3 databases; gaps: grey literature, Chinese-language work, and probable unpublished nulls — conclusion could weaken if nulls exist."
