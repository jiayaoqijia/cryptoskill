---
name: score-retrieval-quality
description: Use when you need to know whether note retrieval returns the right things. Measures recall and precision against a small labeled set of queries.
---

# Score Retrieval Quality

"Search seems to work" is a feeling, not a measurement. Retrieval is good when the right notes come back and the wrong ones do not — both measurable on a handful of labeled queries.

## Procedure

1. Build a labeled set of 10-20 queries you have actually needed, in `notes/retrieval-eval.jsonl`.
2. For each query, list the note ids that *should* return (the gold set), by hand.
3. Run each query against your retriever and capture the returned ids.
4. Compute recall = |returned AND gold| / |gold| and precision = |returned AND gold| / |returned|.
5. Report the mean of each; a healthy store clears recall 0.8 and precision 0.6 on this set.
6. Look at the misses: a query with recall 0 usually means the note was never written, not that search failed.
7. Look at the false hits: precision 0.2 usually means the query terms are too common — add a filter.
8. Fix the cheapest side first: a tagging gap (see `tag-notes-for-precision-recall`) is cheaper than re-embedding.
9. Re-run the same labeled set after any change; the set is the regression test.
10. Keep the eval file in the repo so the score is reproducible, not remembered.

## Pitfalls

- Judging retrieval by one lucky query and declaring it good.
- Counting a note as a hit because its title matched while its content was irrelevant.
- Changing the retriever and re-scoring on a *new* query set, so nothing is comparable.
- Treating recall and precision as one number, then optimizing whichever the current query favours.
- Blaming the retriever when the gold note does not exist in the store at all.

- Scoring on queries invented for the test rather than ones you actually ran.
- Reporting a single aggregate and hiding the queries that returned nothing.
- Freezing the eval and never adding new queries, so the score stops reflecting real use.

## Verification

    jq -s '{recall: (map(.hit)|add/length), precision: (map(.prec)|add/length)}' notes/retrieval-eval-results.json
    # passes when recall >= 0.8 and precision >= 0.6 on the frozen query set

Report to the user: the query count, mean recall, mean precision, and the two worst queries with the reason.
