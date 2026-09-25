---
name: related-work-writing
description: Use when writing or auditing the Related Work section. Organises prior work by axis rather than chronology, builds the asymptotic comparison table with an "Ours" row, writes the bridge and "Our work" paragraphs, and checks every characterisation of prior work against its source.
---

# Related-work writing

## Inputs

`LITERATURE.md` (related-work matrix from `lit-scout`), `refs.bib` (verified), the
objective equation and framework from the introduction/overview.

## Procedure

1. **Choose axes.** From the literature matrix pick one or two axes along which all
   relevant works improve (what they reduce, what structure they exploit). Write them
   as a pair of contrasting verbs if possible ("restricts where" / "restricts how";
   "fewer rounds" / "fewer bytes").
2. **Place each work.** For each work record: axis, method in one line, cost formula
   in its own notation translated to ours, scope restrictions (†/‡), venue'year.
   Verify each cost formula against the original (page/section noted in
   `LITERATURE.md`). Where later papers paraphrase an earlier paper's bottleneck,
   compare with the earlier paper's own experiments section.
3. **Build the table** (`templates/paper/sections/related_table.tex` style): grouped
   rows, last row `\textbf{Ours}`, caption defines all symbols.
4. **Write the paragraphs**: lead-in (3 sentences) → classic works on axis 1 (one
   sentence each, shared limitation last) → recent works (two contrasting bullets) →
   bridge (`\textbf{Insight from ...}`) → `\textbf{Our work.}` (five sentences) →
   complementary approaches → concurrent work.
5. **Tone filter**: remove "unfortunately", "fail", "naive", "suffer", "only";
   replace with factual scope statements ("... assumes ... rather than showing ...",
   "... instantiates a single case, leaving open ...").
6. **Self-citation check**: own prior work in third person, critiqued like others.
7. **Coverage check** with `lit-scout`: the last 12–18 months of ePrint for the
   topic keywords; any close concurrent work gets a labelled paragraph.
8. **Bib hygiene**: published versions over preprints when they exist; ePrint entries
   with the exact author list of the ePrint page; braces around acronyms in titles for
   `splncs04`. (Bib verification itself is owned by `lit-scout`.)

## Placement in the paper

- IACR LNCS: usually §1.1 inside the introduction.
- Design papers: a "State of the art" subsection in the constraints/design section,
  one paragraph per competitor: who → technical core → its trade-off; last sentence
  points to the performance comparison section.
- Security conferences: often a separate section near the end; keep a short
  positioning paragraph in the introduction anyway.

## Anti-patterns

- A chronological list of summaries without a thesis.
- Characterising a prior work by a number from a secondary source.
- A table whose "Ours" row differs from the abstract formula.
- Omitting the strongest baseline because it is inconvenient (reviewers will name it).

## Output

`paper/sections/related.tex`, table in the same file or `related_table.tex`,
verification notes appended to `LITERATURE.md`.
