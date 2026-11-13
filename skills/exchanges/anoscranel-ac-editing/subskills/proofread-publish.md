---
name: proofread-publish
domain: writing/proofread-publish
trigger: "\"proofread this\", \"is it ready to publish\", \"when do I stop editing\", \"give this a final check\"."
anti_trigger: "Consistency sweeps against a style sheet (subskills/copyedit.md); rewrites that still change meaning (subskills/revision-line.md)."
scope: "Last-pass error hunt, two-reader estimate, when to stop, publish gate"
status: "seedling"
---

# Proofread & stop rule

## Standard

⚠️ The primary standard is paywalled; these points come from secondary sources and the public summary.

- **Proofreading keys to the typeset artifact.** It catches errors introduced during typesetting (a dropped line, a wrong font, a repeated running head) (CMOS Q&A: https://www.chicagomanualofstyle.org/qanda/data/faq/topics/ManuscriptPreparation/faq0218.html; ladder in <https://ntrs.nasa.gov/citations/19760015018>). It also covers page mechanics: breaks, heads, spacing, alignment. The freelance market also uses the word for a final read of an unedited file — state which object is read before comparing rates.
- **Single-pass detection is partial.** Two independent readers at p = 0.8 leave about 4% residual; three leave about 0.8%. Independence is the weak link: shared expectations and topic familiarity reduce it. ⚠️ Source not cited inline; check the Sources list before relying on this figure.
- **The two-reader estimator.** Reader 1 finds A errors, reader 2 finds B, C are found by both: total N̂ = A·B/C; missed by both = N̂ − (A+B−C) (Pólya, *Amer. Math. Monthly* 83(1), 1976, https://www.cs.princeton.edu/courses/archive/fall07/cos323/papers/Polya76.pdf). C = 0 leaves it undefined; the Winter correction is (A−C)(B−C)/(C+1).
- **No error-density standard exists**, so a stop rule is calibrated locally. The strongest imported framework is the error budget (Google SRE Book, "Embracing Risk", https://sre.google/sre-book/embracing-risk/; <https://diymfa.com/writing/when-to-stop-editing/>). Perfection is a suboptimal target, the budget needs a neutral instrument, and its owner must be able to stop the pass.

## Decision rules

1. Proofread the final artifact. After layout changes, proofread again.
2. Two independent readers, or one reader plus one independent mechanical pass, with the estimator run on the results.
3. A high count of found errors is not evidence the page is clean. That is the satisfaction-of-search trap.
4. Stop on the budget, not on perfection. Define the acceptable residual before the pass.
5. Nothing publishes without a human approval. The agent prepares the gate list; a human clears it.

## Procedure

1. Freeze the text. No edits during a proofread except typographic repairs.
2. Change the medium: print, a different screen, or text-to-speech read-back.
3. Sweep the standing list: homophones, doubled words, broken cross-references, number formats, headings, lists, running heads, page breaks, caption alignment.
4. Second reader: an independent pass on the same artifact. Record A, B and C.
5. Compute N̂ = A·B/C and the missed-by-both count. Report the residual with the pass.
6. Compare the residual to the agreed budget. Within budget → publish. Outside → another pass on the highest-yield section.
7. Publish gate: no `[TK]` left · all copyedit queries closed · names, dates and numbers verified against the claim table · copyright and reuse cleared · human approval recorded.

## Anti-patterns

- Proofreading the manuscript after the layout changed.
- "We found a lot, so the page is clean."
- Publishing on deadline pressure with the budget unmet and unrecorded.

## Done checklist

- [ ] Medium changed from the drafting medium.
- [ ] Standing error list swept.
- [ ] Two independent passes done; A, B, C recorded.
- [ ] Residual estimated (N̂ = A·B/C) and compared to budget.
- [ ] Publish gate list complete.
- [ ] Human approval recorded before anything goes out.

## Sources

- https://www.chicagomanualofstyle.org/qanda/data/faq/topics/ManuscriptPreparation/faq0218.html
- https://sre.google/sre-book/embracing-risk/
- <https://panko.com/HumanErr/Proofreading.html>
- <https://diymfa.com/writing/when-to-stop-editing/>
