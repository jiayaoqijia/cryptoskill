---
name: technique-overview
description: Use when writing the Technique Overview (a.k.a. "Our Techniques") subsection. Recalls prior routes per paper at a mathematical level, reduces the gap to numbered questions, and answers each with a declarative "Insight" plus one figure, so a reviewer can restate the core idea without reading the body.
---

# Technique overview

## Goal test

After reading only the abstract, introduction and overview, a reviewer can:
(a) restate the main idea in two sentences, (b) write down the key formula,
(c) say where each prior work sits relative to it, (d) believe the main theorem is
plausibly true. Ask `reviewer-sim` (generalist persona) to perform exactly this test.

## Procedure

1. **List the prior routes** from `LITERATURE.md` (usually 2, sometimes 3). For each
   paper in each route write: its key identity/formula, its cost, and the one
   factual thing it leaves open. Verify each against the original paper.
2. **Find the common object.** Phrase all routes as acting on the same mathematical
   object or optimising the same objective (Eq. (1) of the introduction). If no common
   object exists, the "unification" story is forced; tell the human author and
   consider a different framing (e.g. "two orthogonal improvements that compose",
   supported by a measured composition).
3. **Reduce to questions.** "Whether the routes compose reduces to two questions:
   (i) ... (ii) ...". Questions must be precise enough that a theorem answers them.
4. **One Insight per question.** Heading = declarative sentence stating the answer.
   Body: observation → reformulation → key formula (copied from the body theorem) →
   conclusion → why the boundary case is tight or where it fails.
5. **Figure.** A grid/axis diagram (prior works as corners/points, ours as the new
   region) or a data-flow diagram of the new algorithm. Ask `figure-artist` for it;
   caption = one sentence stating placement.
6. **Composition paragraph** with the combined identity and cost.
7. **Optional scope extender.** One paragraph showing the technique applies to a
   neighbouring scheme, quantified by formula only (cheap, raises significance). Mark
   it clearly as not implemented if so.
8. **Consistency check**: `grep` each displayed formula in the body; string-compare.

## Style rules

- Describe prior work per paper and mathematically; do not write a tutorial with
  "Why X is needed / Where the cost goes" headings.
- Use "Suppose ..." to introduce hypotheses before derivations.
- For density/asymptotic results: "asymptotic density ..., certified per instance".
- No new claims that the body does not prove; no numbers that the experiments section
  does not contain.
- Keep limitations as short remarks at the end of the relevant insight, not in the
  contribution list.

## Output

`paper/sections/overview.tex` (or inside `intro.tex`), figure request in
`paper/figs/REQUESTS.md`.

Examples: `skills/paper-playbook/sections/05_technique_overview.md`,
`skills/paper-playbook/examples/toy_overview_and_related.md`.
