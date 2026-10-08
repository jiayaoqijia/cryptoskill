---
name: tag-notes-for-precision-recall
description: Use when search returns too much noise for a query. Adds structured tags and metadata so queries can filter to the right subset without losing hits.
---

# Tag Notes for Precision and Recall

Free-text search fails when a query term is everywhere: "prod" matches every note. Tags give the query a filter axis so it can narrow without losing the true hits.

## Procedure

1. Find the noisy query: the one with high recall and low precision in `score-retrieval-quality`.
2. Identify the axis that separates the good hits from the noise, e.g. `env`, `kind`, `status`.
3. Add tags to front-matter as a fixed vocabulary — never free text: `tags: [dns, prod, howto]`.
4. Publish the allowed values in `notes/README.md` so writers pick from the list.
5. Query with the filter: `grep -l "tags:.*prod" notes/**/*.md | xargs grep -l "does-not-resolve"`.
6. Backfill tags on the existing notes that the noisy query should have surfaced.
7. Measure recall and precision again after tagging; precision should rise without recall falling.
8. Reject tags that only ever co-occur with one note — that is a name, not a tag.
9. Keep the vocabulary small: past ~20 values, people stop using them consistently.
10. Retire a tag that stops matching anything; a dead tag is noise in every filter.

## Pitfalls

- Free-text tags, so `prod`, `production`, and `prd` become three axes.
- Tagging everything, which is the same as tagging nothing for precision.
- Adding a filter that drops the gold hit along with the noise, cutting recall.
- A vocabulary so large nobody remembers the values, so tags are applied inconsistently.
- Leaving old notes untagged, so filtered queries silently miss the history.

- Tagging by hand once and never tagging new notes, so the vocabulary decays to noise.
- Adding a tag that duplicates the folder axis, so the same filter appears twice.
- Filtering on a tag that half the notes predate, silently cutting recall on old notes.

## Verification

    grep -rhoE 'tags: \[[^]]*\]' notes/ | tr -d '[]' | tr ',' '\n' | sort | uniq -c | wc -l
    # passes when the vocabulary is under 20 values and the noisy query's precision rose without recall loss

Report to the user: the noisy query, the tags added, the vocabulary size, and the before/after recall and precision.
