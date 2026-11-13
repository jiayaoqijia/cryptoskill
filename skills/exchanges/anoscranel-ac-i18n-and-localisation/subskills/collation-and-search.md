---
name: collation-and-search
domain: software-engineering/collation-and-search
trigger: "Sorting, matching, or searching text across languages and scripts."
anti_trigger: "Not for relevance ranking, and not for translation."
scope: "Sorting, case folding, and search across scripts and diacritics."
status: seedling
---

# Collation and search

## Standard

Sorting text by byte value produces an order that is wrong in most languages: accented characters sort after unaccented ones, case separates words that should be adjacent, and languages with their own alphabetic tradition order letters differently. A locale-aware collation orders by the language's rules, and the choice of collation is a product decision because it changes what the user sees.

Case folding and search have the same shape. A user searching for a name without its diacritics expects to find it, and a case-sensitive index will not. The locale-aware answer is to index a folded and normalised form alongside the original, so matching becomes forgiving without the display changing.

Primary sources: <https://cldr.unicode.org/> and <https://www.unicode.org/reports/>.

## Decision rules

- Record the collation used for every user-visible sort, and whether it is locale-aware.
- Record the case folding and normalisation applied before matching.
- Record whether diacritics are significant for matching and for display.
- Record the behaviour for scripts without case, and for scripts written without spaces.
- Record the tie-breaking rule when two items collate as equal.
- Record the database collation, which may differ from the application's.

## Procedure

1. Inventory the user-visible sorts and record their collation.
2. Choose a normalisation form and a case folding rule for matching.
3. Record whether diacritic-insensitive matching is required.
4. Record the tie-breaking rule.
5. Reconcile the database collation with the application's.
6. Test with names containing accents, case variation, and non-Latin scripts.

## Anti-patterns

- Sorting by byte value and assuming it is alphabetical.
- Using a single collation for every locale in a multilingual product.
- Matching on a normalised form and displaying the normalised form.
- Assuming a space separates words in every script.
- Ignoring the database's collation because the application sorts.

## Done checklist

- [ ] Collation recorded for every visible sort.
- [ ] Folding and normalisation recorded.
- [ ] Diacritic significance recorded.
- [ ] Tie-breaking recorded.
- [ ] Database collation reconciled.
- [ ] Tested with accents, case, and non-Latin scripts.

The user-facing consequence is worth stating because it is easy to dismiss as a detail: a user whose name is sorted into the wrong place, or whose search for their own record returns nothing because they typed it without an accent, experiences the product as broken rather than as unpolished. Collation and folding are correctness, not refinement.


## Sources

- Unicode collation and normalisation: <https://www.unicode.org/reports/>
- CLDR locale data: <https://cldr.unicode.org/>
- W3C internationalisation guidance: <https://www.w3.org/International/>
