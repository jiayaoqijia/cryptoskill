---
name: copyedit
domain: writing/copyedit
trigger: "\"copyedit this\", \"make it consistent\", \"apply house style\", \"run the style sheet over this\"."
anti_trigger: "Sentence-level rewrites that may move meaning (subskills/revision-line.md); hunting last-pass errors in the final artifact (subskills/proofread-publish.md)."
scope: "Consistency and correctness against a style sheet, meaning unchanged"
status: "seedling"
---

# Copyedit

## Standard

⚠️ The primary standard is paywalled; these points come from secondary sources and the public summary.

- **The pass, defined by trade.** Copyediting is "usually the final editorial stage of preparing a manuscript for publication—a meticulous read for technical errors, style, and internal consistency, along with marking or electronically coding the text to be ready for typesetting" (CMOS Q&A: https://www.chicagomanualofstyle.org/qanda/data/faq/topics/ManuscriptPreparation/faq0218.html).
- **What it checks.** Style-sheet creation, cross-references, terminology consistency, and factual inconsistencies flagged or queried — queried, not repaired, when the answer is not certain (<https://ntrs.nasa.gov/citations/19760015018>).
- **The style sheet is the closure operation.** A guide is a default layer over an open field.
 The sheet records the decisions the guide leaves open (<https://scientificstyleandformat.org/book/ed8/front/pref.html>).
 CSE states its own limit: its recommendations "focus primarily on nomenclature and symbolization" (https://scientificstyleandformat.org/book/ed8/front/pref.html).
- **Machine consistency passes have a measured failure rate.** Across nine revision methods and six models, one-change-everywhere propagation reached 68.3–93% accuracy (<https://arxiv.org/abs/2210.15067>, arXiv:2609.03254, https://arxiv.org/abs/2609.03254). The best value was added by choosing among three parallel samples. The residual failures are silent: a missed cross-reference looks like correct text.
- **Guide differences that bite.** AP omits the serial comma, spells out 0–9 and uses downstyle headings.
 CMOS 18 mandates the serial comma, spells numbers through 100 and uses title case (<https://www.the-efa.org/>; CMOS 18 released 19 Sep 2024, https://www.chicagomanualofstyle.org/help-tools/what-s-new.html).

## Decision rules

1. Meaning is fixed in this pass. Anything that would change a claim goes out as a query, never as an edit.
2. The style sheet exists before the pass starts. No sheet, no copyedit.
3. One consistency class per sweep: numbers, terminology, cross-references, acronyms, capitalisation, punctuation.
4. Any uncertainty is a marginal query with the two options shown. Never guess between two defensible readings.
5. Machine checks run before the human pass and their output is a candidate list, not a verdict (68–93% per item).

## Procedure

1. Record the venue's rules and the base guide, then write the project style sheet (out of scope for this leaf: picking the guide and building the sheet).
2. Run the machine pass: numbers, acronym first use, cross-reference targets, banned terms, hyphenation.
3. Read the manuscript once against the sheet, in sweeps by class, not by page.
4. Raise queries inline in the agreed form: a marginal note, the two options, and a recommendation.
5. Resolve every query with the author before the pass closes. Unresolved queries block the proofread.
6. Update the sheet with every new decision made during the pass.
7. Hand the clean manuscript to subskills/proofread-publish.md.

## Anti-patterns

- Silently repairing a factual inconsistency instead of querying it.
- Editing voice, persona or claim strength in a mechanics pass.
- Applying a style with no written sheet, from memory.
- Machine output accepted as final (the residual failures are silent).
- Two different readings of the same term in one document.

## Done checklist

- [ ] Style sheet written and current.
- [ ] Machine candidate pass run and triaged.
- [ ] One sweep per consistency class.
- [ ] All queries resolved with the author.
- [ ] No meaning changed in this pass.
- [ ] Sheet updated with new decisions.

## Sources

- https://www.chicagomanualofstyle.org/qanda/data/faq/topics/ManuscriptPreparation/faq0218.html
- <https://scientificstyleandformat.org/book/ed8/front/pref.html>
- <https://arxiv.org/abs/2210.15067>
- <https://www.the-efa.org/>
