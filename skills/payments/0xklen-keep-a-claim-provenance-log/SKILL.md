---
name: keep-a-claim-provenance-log
description: Use when a report or answer aggregates many sourced facts. Maintain a per-claim provenance log so every assertion traces to a retrievable artefact.
---

# Keep a claim provenance log

Aggregated answers lose their roots. This skill keeps a machine-checkable trail from each assertion in the deliverable back to the command, file, or URL that produced it.

## Procedure

1. Open `provenance.tsv` with tab-separated columns: `claim_id`, `assertion`, `source`, `locator`, `retrieved_utc`.

2. Assign a `claim_id` (`C1`, `C2`, ...) to every factual assertion in the deliverable.

3. Fill `source` with the kind — `command`, `file`, `url`, or `api` — and `locator` with the exact target: `src/auth/token.py:88`, `https://api.example.com/v2/models`, or `pytest -k token`.

4. Stamp `retrieved_utc` when you actually gathered the fact: `date -u +%FT%TZ`.

5. Cite the id inline at each assertion in the deliverable, e.g. "... expires at 3600s [C4]".

6. Before finishing, check the file is well formed: `awk -F'\t' 'NF!=5{print "bad row",NR}' provenance.tsv` must print nothing.

7. Confirm every assertion in the deliverable carries an id and every id has a retrievable locator; orphans in either direction are the failure mode.

## Pitfalls

- A locator like "the docs" is not retrievable; name the page and the section.
- URLs rot; the retrieval date lets a later 404 read as drift rather than as a current fact.
- When two sources disagree, log both rows and note the conflict; never average them into one.
- Citing your own earlier summary as the source restarts the chain with nothing at the bottom.
- An id with no inline citation, or a citation with no row, means the trail is already broken.

## Verification

    awk -F'\t' 'NF!=5{print "bad row",NR}' provenance.tsv; wc -l < provenance.tsv

Report the claim count and any assertion that failed to trace to a locator; fix it before delivery.
