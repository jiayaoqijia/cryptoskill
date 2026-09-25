# 02 Abstract — the three-part paradigm

Full procedure and more examples: [abstract-craft](../../abstract-craft/SKILL.md).

## Three paragraphs, one job each

| ¶ | job | sentences |
|---|---|---|
| ① State of the art | field consensus → the bottleneck → the existing routes (grouped by approach, 1–2 representative works each with venue'year) → what remains open | 4–5 |
| ② Our technique | "We propose/present X, which views ... as ..." → one sentence per contribution, ordered structure → bound/characterisation → new construction → algorithm → cost formula | 5–8 |
| ③ Results + artifact | scoping sentence (how many instances, what security level) → range → one or two concrete points readers know → artifact/formalisation sentence | 2–3 |

For LNCS, use `\setlength{\parindent}{2em}` at the start of each paragraph inside
`abstract` if paragraph separation is desired, and keep title + abstract + keywords
on page 1 (adjust only abstract-local negative `\vspace`, never global geometry).

## Sentence rules

1. Sentence one states field consensus and needs no citation.
2. Group prior work by **route**, not by chronology; cite venue and year in
   parentheses so reviewers see you compare against the latest top-venue work.
3. End ¶① with an explicit open question: "However, whether/how ... has remained open."
4. ¶② sentence one states the **viewpoint** of the framework in one clause.
5. If you claim to unify prior work, include the sentence that places prior methods
   inside your framework ("the methods of A and B are the cases w=1 and k=1"). That
   sentence is the evidence for "unified".
6. ¶③ scoping first: "On N instances at ≥λ-bit estimated security, ..." then the
   range, then concrete points. If the scope changes, recompute every range.
7. The artifact sentence goes last, with an anonymous link in a footnote during
   review. Formalisation claims state exactly what was machine-checked.
8. Budget: the abstract must fit on page 1 with keywords and footnotes. If over,
   cut adjectives in ¶① first; do not cut ¶③ numbers or their scope.

## Forbidden in abstracts

- Words that overstate proof status: "rigorous guarantee", "turns the heuristic into
  a theorem", "optimal" without a proven optimality statement.
- Scope that does not match the tables (e.g. counting instances below the stated
  security level).
- Symbols defined only in the body or appendix.
- Attributing a composite improvement to a single component.
- Ratios against an unoptimised or outdated baseline when a stronger baseline exists.

## Plain-text form for submission systems

Prepare a separate plain-text abstract: remove `\cite` numbers, write `sqrt`, `>=`,
`x` for ×, and never copy from the PDF (hyphenation and ligature garbage). Keep it in
`paper/abstract_plain.txt` and diff it against the LaTeX abstract before submitting.

## Checklist

- [ ] ¶① ends with an open question; prior routes grouped with venue'year.
- [ ] ¶② has one sentence per contribution, same order as the contribution list.
- [ ] ¶③ begins with a scoping sentence; every number has an EVIDENCE row.
- [ ] No appendix-only symbols; no overstated proof words.
- [ ] Page 1 holds title, abstract, keywords.
