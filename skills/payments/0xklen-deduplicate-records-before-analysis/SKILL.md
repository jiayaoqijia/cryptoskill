---
name: deduplicate-records-before-analysis
description: Use when combining rows from multiple sources or a crawl. Removes exact and near-duplicate records before counting so totals are not inflated.
---

# Deduplicate Records Before Analysis

Duplicates inflate every count and bias every average toward whatever gets echoed most. Deduplicate before you compute, and report how many you removed.

## Procedure

1. Count first: `wc -l raw.csv` and `sha256sum` each row's canonical fields to see exact duplicates.
2. Exact dedup on stable keys: `sort -u`, or in pandas `df.drop_duplicates(subset=['id'])`. Report rows before/after.
3. Normalise before comparing: strip whitespace, lowercase, Unicode NFKC, collapse internal spaces, strip tracking params from URLs.
4. Near-duplicate detection for text: shingle and compare. Two records with Jaccard ≥ 0.9 on 5-grams are the same document:
   ```python
   from difflib import SequenceMatcher
   def near(a, b): return SequenceMatcher(None, a, b).ratio()
   ```
5. Block to keep it tractable: only compare records sharing a cheap key (first 3 tokens, domain, first author) — full O(n²) is unaffordable past a few thousand rows.
6. Decide the merge rule and apply it consistently (keep earliest, keep longest, keep highest-trust source). Record which record survived and why.
7. Never dedupe silently in a pipeline that later joins on the dropped keys; log removed rows to `dupes.csv`.

```bash
# exact dupes on a natural key
awk -F, '{print $1"|"$3"|"$5}' raw.csv | sort | uniq -c | sort -rn | head
```

## Pitfalls

- Deduping on too few fields merges genuinely distinct records (two people named "J. Smith").
- Deduping on too many fields misses the same record reformatted across sources.
- Fuzzy thresholds near 0.8 flip many borderline pairs; inspect samples on both sides of the cut.
- Aggregating after dedup is order-dependent if you kept the wrong survivor.
- A crawl that revisits a page with a changed URL (session id, slug) produces a "new" record for old content.

## Verification

    echo "raw=$(wc -l < raw.csv) dedup=$(wc -l < dedup.csv) removed=$(wc -l < dupes.csv)"

Report: "11,204 raw rows → 9,873 unique (1,331 duplicates removed, 1,102 exact + 229 near, Jaccard ≥ 0.9); removed rows written to dupes.csv."
