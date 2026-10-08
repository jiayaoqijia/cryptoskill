---
name: mine-retrieval-evals-from-query-logs
description: Use when a hand-written retrieval eval never matches real usage. Builds the query set from logged production queries and labels gold chunks by inspection, so the eval reflects what users actually ask.
---

# Mine Retrieval Evals from Query Logs

Evals written by the engineer test the engineer's questions. Production queries are the real distribution, including the typos, the underspecified ones, and the ones nobody expected to matter.

## Procedure

1. Export logged queries with their retrieved ids and any click or follow-up signal: `SELECT q, ts, retrieved FROM query_log WHERE ts > now() - interval '30 days'`.
2. Deduplicate textually near-identical queries by lowercasing, stripping punctuation, and clustering with MinHash (`deduplicate-near-identical-chunks` applied to queries).
3. Stratify the sample: frequent head queries, a long tail sample, and the zero-result queries separately.
4. Label gold chunks by reading the retrieved set, not by trusting the ranker: mark the chunk that actually answers each query.
5. Mark queries the corpus genuinely cannot answer as `unanswerable`, and keep them in the set — they test abstention.
6. Aim for 30-100 labelled queries to start; small sets cannot distinguish a real gain from noise.
7. Include the ugliest real queries verbatim: the misspellings and shorthand are where retrieval actually breaks.
8. Freeze the labelled set into `evals/retrieval.jsonl` and version it in the repo.
9. Refresh the set periodically as the query mix drifts, but keep a frozen core so scores stay comparable over time.
10. Strip PII from logged queries before they enter the repo (see privacy rules); hash user ids rather than storing them.

11. Record for each labelled query whether it came from logs or was authored, so eval mix is visible.

## Pitfalls

- Labelling gold by what the current retriever returned, which bakes in its mistakes as the target.
- Keeping only the queries the system answered well, so the eval never exercises the failures.
- Sampling from all-time logs and mixing two product generations of queries into one score.
- Copying production queries into the repo with emails and account numbers still in them.
- A set so small that a one-query flip changes the headline number by five points.
- Letting the eval drift with every label edit, so last month's score is not comparable.

- A log exporter that deduplicates by exact string and keeps every typo variant as a separate query.
- Labelling from the click log when clicks reflect result position, not relevance.

## Verification

    wc -l evals/retrieval.jsonl; jq -r '.label' evals/retrieval.jsonl | sort | uniq -c
    # passes when the set has >=30 labelled queries, a mix of answerable and unanswerable, and no PII

Report to the user: queries mined, labelled, unanswerable count, the strata sampled, and the PII strip applied.
