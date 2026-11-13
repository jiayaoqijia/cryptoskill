---
name: research-sources
domain: writing/research-sources
trigger: "\"check my sources\", \"find evidence for this\", \"where did this number come from\", \"verify these quotes\", \"what can I say\"."
anti_trigger: "Binding the finished source list into the text as citations (subskills/citation-grounding.md); searching literature for a review's study set."
scope: "Finding, judging and logging sources and quotes before drafting"
status: "seedling"
---

# Research & sources

## Standard

- **Institutional checking practice.** *The New Yorker* runs independent checkers who build corroboration binders and read factual assertions back to sources.
 *Der Spiegel* runs Europe's largest checking unit (~70 researchers) with metadata audits, image geotag checks and on-site spot checks.
 *ProPublica* runs dual-track review and has senior data editors replicate statistical code before release (<https://www.newyorker.com/>).
- **Source tier ladder**: Tier 1 court dockets, sworn depositions, SEC filings, server logs → Tier 2 agency responses, contemporaneous memos → Tier 3 trade press, corporate PR → Tier 4 single-source tips. Tier 1 outranks everything below it.
- **Attribution tiers** (AP / Washington Post conventions): on the record, on background, deep background, off the record. Ground rules are struck before disclosure.
- **Fabricated references are now common.** An audit of ~2.5M papers and 97.1M references found 4,046 references to studies that do not exist (Topaz et al., *The Lancet* 2026, https://doi.org/10.1016/S0140-6736(26)00603-3). The share of affected papers rose 1-in-2,828 (2023) → 1-in-458 (2025) → 1-in-277 (early 2026), and 98.4% were never corrected.

## Decision rules

1. A fact needs two independent lineages, or one Tier 1 primary. Same-index repeats (Bing, Yahoo, DuckDuckGo) count as one.
2. Every number, name, date, quote and URL is a claim. Tag them while drafting.
3. Superlatives need comparative proof ("largest" needs the comparison set).
4. A quote needs its surrounding sentences. Never trim ellipses to sharpen a quote.
5. Never round, convert or rephrase a figure. Copy the figure and its unit as printed.
6. Keep raw snippets, not paraphrase. Paraphrase at capture time is how drift starts.
7. Circular reporting is not corroboration: repetition volume mimics agreement.

## Procedure

1. List the claims the document must support, one per row:
   ```markdown
   | Claim | Source (title, publisher, date, URL) | Tier | Locator | Retrieved | Status |
   ```
2. Status is one of: supported, contested, my inference, unverified. Only "supported" rows leave this leaf.
3. Search the exact figure in quotes, plus "source". Search the first 8–10 words of a quote verbatim.
4. Open every supplied URL. A link that 404s or leads elsewhere fails the claim.
5. For each key figure, read the source's own text — not the summary that quotes it.
6. Record conflicts side by side. Contested facts get both readings or a flag ⚠️, never the convenient one.
7. Strike ground rules with any human source before an interview, not after.

## Anti-patterns

- Two outlets that share one lineage counted as two sources.
- Superlatives with no comparison set.
- Vendor accuracy claims treated as measurements.
- The summary used in place of the study.

## Done checklist

- [ ] Every number, name, date, quote and URL tagged and checked.
- [ ] Claim table complete with tier, locator and retrieval date.
- [ ] Conflicts recorded, not smoothed.
- [ ] Quotes read in context; ellipses flagged.
- [ ] Attribution level agreed with each human source.
- [ ] No claim rests on a single Tier 3 or Tier 4 source.

## Sources

- <https://www.newyorker.com/>
- <https://arxiv.org/pdf/2502.10855v2>
- <https://arxiv.org/abs/2602.06718>
- https://doi.org/10.1016/S0140-6736(26)00603-3
