---
name: citation-grounding
domain: writing/citation-grounding
trigger: "\"cite this\", \"add references\", \"is this plagiarism\", \"which citation style\", \"did I copy this\"."
anti_trigger: "Finding and judging the source itself (subskills/research-sources.md); the journal's disclosure rules for AI use."
scope: "Binding every claim to a checkable source; citation styles; text reuse and plagiarism"
status: "seedling"
---

# Citation & grounding

## Standard

- **A citation must be checkable twice**: the reference exists, and it supports the claim. CiteAudit names the harder class explicitly — unsupported claims, misattributed findings, semantic drift between claim and source (Shi et al., arXiv:2602.23452, https://arxiv.org/abs/2602.23452).
- **The error is now industrial.** 1.07% of 56,381 AI/ML and Security papers (2020–2025) carried invalid citations, an 80.9% rise in 2025 (HALLMARK, arXiv:2607.18360, https://arxiv.org/abs/2607.18360). The dominant failure is plausible fabrication at 55% of hallucinated references.
- **False positives are the deployment bottleneck.** At venue-realistic base rates the order-of-magnitude spread in false-positive rate decides whether a verifier's flags are true catches or noise. Most models over-flag papers past their training cutoff. An undetected fabrication is still the costlier error.
- **Citation styles by venue**: APA 7 author–date for psychology and social science; CMOS 18 (2024) notes–bibliography or author–date for publishing; AP names sources in text and has no reference list; *The Bluebook* 21st ed. (2020) governs citation form in law; *CSE* 8th ed. for scientific nomenclature (https://scientificstyleandformat.org/book/ed8/front/pref.html).
- **Text reuse**: COPE decides overlap case by case on "the amount and nature of overlap" (<https://arxiv.org/abs/2608.26710>). No major policy sets a numeric threshold, and the field prefers "text recycling" to "self-plagiarism".

## Decision rules

1. Claim first, citation second. If no source can carry the claim, cut the claim or mark it ⚠️ as inference.
2. Every in-text pointer must survive the reader test: reachable, current, containing the claim.
3. One citation style per document, fixed by the venue before drafting.
4. Quotation marks mean verbatim. Anything trimmed needs ellipses; anything clarified needs brackets.
5. Reuse of your own earlier text is disclosed to the venue.
6. The reader must always tell fact from inference. Inference is labelled, never dressed as citation.

## Procedure

1. Extract the claim list from the draft. Each claim is one row.
2. For each row record: source, locator (page, section, figure), the draft's exact words, the source's exact words.
3. Verify existence first (DOI, resolver, publisher page), then support: does the passage say this?
4. Rewrite the claim where the source says less than the draft claims. This is the most common repair.
5. Format every entry in the venue's style. Build the reference list from the claim table, never from memory.
6. Run a plagiarism and reuse sweep on the final text. Record matches with their URLs.
7. Flag every unresolved item as a query for the author. Do not ship an unverifiable reference.

## Anti-patterns

- A reference list built from what the search returned, not from the claims.
- The abstract quoted as the study's finding.
- Paraphrase so close it is copy with changed words.
- The same self-reused block in two submissions, undisclosed.

## Done checklist

- [ ] Every claim maps to one locatable source.
- [ ] Existence and support checked separately for each reference.
- [ ] Quotation marks, ellipses and brackets used correctly.
- [ ] One citation style, matching the venue.
- [ ] Self-reuse disclosed.
- [ ] Inference labelled as inference.
- [ ] Unresolved items listed as queries, not shipped.

## Sources

- <https://arxiv.org/abs/2602.06718>
- <https://arxiv.org/abs/2608.26710>
- https://arxiv.org/abs/2602.23452 · https://arxiv.org/abs/2607.18360 · https://arxiv.org/abs/2607.20891
- https://apastyle.apa.org/style-grammar-guidelines/bias-free-language
