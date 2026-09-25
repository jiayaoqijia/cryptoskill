# 04 Our Contributions

About one LNCS page: a lead-in sentence and three or four bullets (or bold-titled
paragraphs).

## Lead-in template

> Inspired by <structural observation>, we determine <bound / characterisation>.
> Building on it, we propose <framework/construction name> that <what it subsumes or
> enables>. Our main contributions are summarised below:

## Fixed order: structure → framework → algorithm → numbers

1. `\textbf{From <structure> to <new construction>.}` What structure was found; the
   characterisation it yields; the new object it produces; one coverage sentence with
   a single percentage or count (pointing to a table, not a lemma).
2. `\textbf{A unified <framework>.}` Key observation → framework → where each prior
   work sits inside it → why interior points beat the corners → "for any instance,
   the best configuration is selected by a closed-form rule".
3. `\textbf{A <algorithm> with <property>.}` "the first ... that exploits both ... at
   once" → what it does → cost formula → the theory that supports it → optional "As a
   bonus, ..." sentence.
4. `\textbf{<Metric> improvements.}` Only the two most recognisable numbers, plus
   "verified against the baselines in \Cref{tab:main}".

## Two formats

- **A. `itemize`/`enumerate` bullets** when contributions are independent.
- **B. Bold-titled paragraphs** ("Our first contribution is ...", "As a final
  contribution, ...") when they build on one another; numbers can close each
  paragraph.
- **Roadmap style** (design papers): walk through the sections ("In Section 3 we
  introduce ...; the rationale is developed in Section 4; ...") and embed the key
  ratio in the evaluation sentence.
- **One discovery, everything derived** (cryptanalysis papers): "Our main
  contribution is the discovery of <property>, on which all our other results are
  based." This is the strongest single-idea narrative.

## Wording rules

- **No Lemma/Theorem numbers** in contribution bullets; point to tables/figures
  (`\Cref{tab:...}`). Contributions read as results, not as proof references.
- **No concessions or comparisons** inside contributions; limitations go to the
  overview remarks or the evaluation section.
- **Numbers only in bullet 1 (a coverage percentage) and bullet 4 (ratios).**
- Each bullet: verb + deliverable + section pointer; 3–5 sentences; intra-bullet
  connectives "Building on", "More importantly", "Consequently".
- Strong verbs in order of force: prove / establish / show that > identify / observe >
  introduce / propose > give / provide > implement / measure / validate. Avoid
  "study", "investigate", "explore", "try to".
- The sentence "where each prior work sits" must be **identical in substance** in
  contribution 2, the related-work bridge paragraph and the overview figure caption.

## Pre-flight

Before prose: each bullet exists as a row in `CLAIMS.md` with status `survived` or
`weakened` (then the bullet uses the weakened wording). Never promise a theorem the
body does not contain.

See `examples/toy_intro_and_contributions.md` for good/bad toy bullets.

## Checklist

- [ ] 3–4 bullets in structure → framework → algorithm → numbers order.
- [ ] No lemma numbers; numbers only in bullets 1 and 4.
- [ ] Every bullet has a CLAIMS row that survived falsification.
- [ ] Placement-of-prior-work sentence consistent in three places.
