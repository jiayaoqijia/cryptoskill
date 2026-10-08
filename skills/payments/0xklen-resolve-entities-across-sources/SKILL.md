---
name: resolve-entities-across-sources
description: Use when joining records about the same company, person, or paper across datasets. Maps to stable identifiers before comparing or counting.
---

# Resolve Entities Across Sources

The same real-world entity appears as "Apple", "Apple Inc.", "AAPL", and "苹果" across sources. Match on identifiers and controlled keys, not on display names, or your join silently splits and duplicates entities.

## Procedure

1. Prefer an authoritative identifier over any name string: company → LEI or CIK; paper → DOI; researcher → ORCID; place → ISO 3166 / GeoNames id; person → national id where lawful; product → GTIN.
2. Normalise the fallback key: Unicode NFKC, casefold, strip legal suffixes (`Inc`, `Ltd`, `GmbH`, `Co`), collapse punctuation, expand common abbreviations (`Corp` → `Corporation`).
3. Build candidate pairs by blocking on a cheap key (first token, country, first author), never all-pairs.
4. Score candidates with string similarity, then set a two-threshold policy:
   - score ≥ 0.92 → auto-merge
   - 0.75 ≤ score < 0.92 → human-queue
   - below 0.75 → not the same
   ```python
   from difflib import SequenceMatcher
   s = SequenceMatcher(None, norm(a), norm(b)).ratio()
   ```
5. Resolve, don't delete. Assign a canonical id and keep every alias; a mapping table (`alias → canonical_id`) beats overwriting rows.
6. Handle one-to-many and many-to-one: an acquired subsidiary and its parent, a paper with two versions, a person with two affiliations.
7. Record unresolved entities as their own cluster and report their count — do not force-merge them.

```bash
# gather all distinct spellings before matching
cut -d, -f2 entities.csv | sort | uniq -c | sort -rn | head -30
```

## Pitfalls

- Fuzzy-matching on names alone merges distinct people ("J. Smith") and splits variants ("Jon", "Jonathan").
- The same name across languages ("Apple" vs "苹果") needs a cross-lingual link table, not string distance.
- Identifiers can be recycled or reassigned; check the id's validity date when sources span years.
- A shared address or phone is weak evidence — shell companies and families share them.
- Merging then joining loses the ability to audit; always keep the alias map.

## Verification

    python3 -c "import pandas as pd; print(pd.read_csv('alias_map.csv').canonical_id.nunique(), 'canonical entities')"

Report: "1,204 raw name strings resolved to 817 canonical entities via LEI (93%) + similarity; 41 borderline pairs queued for review; 0 force-merges."
