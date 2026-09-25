# 03 Introduction — funnel, pipeline, objective, open question

Target: about one page (LNCS) before Related Work, written as a historical narrative,
not a bullet list. It must read as if written by a person who knows the field.

## Move sequence

```
[field]        One sentence on what the primitive enables; cite the founding works.
[schemes]      Which schemes/protocols are the ones of choice for this task, and why.
[need]         Why the expensive component exists at all (e.g. noise → bootstrapping;
               data → OPRF evaluation; rounds → trail search).
[lineage]      The line of work in one sentence, citing it once as a block of refs.
[bottleneck]   What has remained the dominant cost throughout that line, ideally with
               a citable measurement from prior work.
[pipeline]     "Concretely, X factors into k stages:" one bullet per stage, each with
               its map/formula and its cost in O(.) notation.
[focus]        "In this work we concentrate on stage j."
[objective]    Cast every previous construction as solving one numbered optimisation
               problem, e.g.  minimise cost(P) s.t. P satisfies the functional spec. (1)
[open]         "Whether <some further structure> can lower (1) further has remained open."
```

Why the objective equation matters: Related Work, the contributions and the overview
can all point back to Eq. (1). It becomes the anchor of the paper.

## Rules

- Citation density: 3–4 citations in the first paragraph; the lineage sentence cites
  the whole line at once instead of one citation per sentence.
- The pipeline bullets let a reader understand "we only change stage j" without
  reading the preliminaries.
- Use the standard transition vocabulary: temporal ("Subsequently", "More recently"),
  contrastive ("However", "Nevertheless", "In contrast"), causal ("Consequently",
  "Accordingly"). Do not stack three connectives in a row.
- A "what this paper is not" sentence is useful when a closely related earlier
  paper exists (including your own, cited in the third person); it defuses
  "substantial overlap" concerns.
- Arguments for "existing work is insufficient" come in three strengths. Weak:
  "existing schemes are slow" (never alone). Medium: "scheme A wins on metric M but
  pays a hidden cost on M'". Strong: "existing schemes are suboptimal along a
  dimension they did not consider". Use strong in the intro and overview, medium in
  related work.
- If the change could look like parameter tuning, add a pre-emptive sentence:
  "Neither observation is a parameter tweak: the first identifies a dimension of the
  technique that was never used, the second replaces an implicit convention by an
  explicit optimisation against Eq. (1)."

## Sub-structure after the opening

`1.1 Related Work` → `1.2 Our Contributions` → `1.3 Technique Overview`
(→ `1.4 Organisation`). See files 04–06.

Alternative for design papers (three titled subsections that form an argument):
"X: what it is and why it was abandoned" → "Why revisit X now" → "Our approach and
roadmap".

## Toy example (T3, PSI; numbers illustrative)

> Private set intersection (PSI) lets two parties learn the intersection of their
> sets and nothing more [..]. Among the many designs, OPRF-based protocols are the
> ones of choice for unbalanced sets, since the large set is processed once offline
> [..]. [...] Throughout this line of work, communication has remained linear in the
> larger set [...]. Concretely, an OPRF-based protocol factors into three stages:
> (i) hashing ..., cost O(n); (ii) OPRF evaluation ..., cost O(m) group operations;
> (iii) comparison ..., cost O(m log m) bits. Every previous construction can be cast
> as solving
> min comm(H) s.t. H is an (m, n, ε)-hashing scheme with false-positive rate ≤ 2^{-σ}. (1)
> Whether structure in the hashing scheme beyond its load factor can lower (1)
> further has remained open.

## Checklist

- [ ] Funnel reaches the bottleneck within the first paragraph.
- [ ] Pipeline bullets with a cost per stage.
- [ ] One numbered objective equation that later sections reference.
- [ ] Explicit open question as the last sentence before Related Work.
- [ ] Own prior work cited in the third person.
