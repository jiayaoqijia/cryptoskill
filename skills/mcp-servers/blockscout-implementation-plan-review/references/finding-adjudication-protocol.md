# Finding adjudication protocol

Use this protocol for one independently investigated candidate finding from an
implementation-plan review.

## Inputs and allowed output

The launcher prompt supplies:

- a candidate `input.md`;
- the report template path;
- the exact candidate output directory;
- the implementation plan and issue snapshot paths through `input.md`.

Read the plan and issue snapshot in full before reaching a disposition. Read
repository code, tests, rules, and documentation as needed. Do not implement
the plan.

Write only `full-report.md` in the candidate output directory. The finalizer
creates `brief.md`. Do not edit `input.md`, the plan, issue snapshot, code,
tests, documentation, skill files, or another candidate's artifacts.

## Isolation

- Treat the candidate hypothesis as unproven. Confirm, narrow, question, or
  close it according to evidence.
- Do not read prior review scratchpads, prior adjudication runs, another
  candidate directory, or another adjudicator's messages.
- Do not ask another adjudicator for its conclusion or rubric.
- If an applicable repository skill requires an isolated specialist such as a
  SPEC-only consultant, it may be used. Keep the final adjudication independent.
- Do not infer desired conclusions from candidate numbering, wording, or the
  fact that the main agent selected the candidate.

## Investigation and decision method

1. State the strongest requirement interpretations both supporting and
   defeating the candidate. Separate explicit requirements, repository facts,
   and assumptions.
2. Investigate the relevant production path, tests, rules, documentation, and
   history. Seek counterevidence rather than merely accumulating support.
3. Synthesize the decisive evidence and strongest counterargument.
4. Choose exactly one disposition:
   - `Confirmed`: actionable substantially as hypothesized.
   - `Downgraded`: a narrower or lower-severity issue survives.
   - `Question`: product or ownership information is required before deciding.
   - `Closed`: no actionable issue remains.
5. Consider 2–4 genuinely feasible response variants, including no change,
   close, or narrower wording when plausible. Explicitly reject attractive but
   invalid shortcuts.
6. Build a case-specific rubric with 2–8 criteria. For every criterion give its
   provenance, scoring direction, and weight. Weights must total 100.
7. Score every feasible variant with evidence for each score and show the
   weighted totals.
8. Perform sensitivity analysis. Identify the assumptions or reasonable weight
   changes that can alter the winner.
9. State the decision boundary before the recommendation: what newly learned
   fact or changed requirement would alter the disposition or preferred variant.
10. Record residual uncertainty and likely overlap with other candidates
    without reading their reports.

Use the review severity vocabulary: `Blocker`, `Major`, `Minor`, `Question`,
`Nit`, or `None`. A `Closed` candidate must use `None`; a `Question` candidate
must use `Question`.

## Full report contract

Use the supplied `finding-adjudication-report.md` template exactly:

- preserve every section, tag, slug, disclosure value, and section order;
- preserve each required first-level heading;
- replace every `REPLACE_ME`;
- do not nest tagged sections;
- put no nonblank content outside tagged sections;
- keep recommendation after variants, rubric, evaluation, and sensitivity;
- keep all core sections combined under 1,000 words.

The `adjudication-result` comment must be valid one-line JSON:

```html
<!-- adjudication-result: {"disposition":"Closed","confidence":0.92,"severity":"None"} -->
```

The `rubric-weights` comment must be valid one-line JSON with 2–8
kebab-case criterion slugs and positive weights totaling 100:

```html
<!-- rubric-weights: {"contract-fidelity":35,"regression-risk":25,"scope":40} -->
```

`disclosure="core"` means the section is copied verbatim into the default brief.
It does not mean the section should be written first. `reference` sections are
equally important to the adjudicator's reasoning and remain available in the
full report.

Core sections must be independently understandable. In particular:

- `Evidence synthesis` includes 3–6 decisive facts and the strongest
  counterargument with source pointers.
- `Disposition` states the surviving problem and its practical severity.
- `Decision boundary` states the assumption that can flip the conclusion.
- `Recommendation` gives the concrete plan change, or explicitly says no plan
  change.
- `Residual uncertainty` distinguishes unresolved facts from speculation.
- `Overlap` names conceptual areas of likely duplication, or says none found;
  it must not cite unread candidate reports.

## Mandatory finalization loop

After writing `full-report.md`, run:

```bash
python3 <skill-dir>/scripts/finalize_adjudication.py \
  --report <candidate-output-dir>/full-report.md
```

If validation fails, fix `full-report.md` and rerun the command. Do not return
until it succeeds and creates the sibling `brief.md`. Do not edit `brief.md`
manually.

Return only:

```text
Completed.
Disposition: <value>
Confidence: <0..1>
Validation: passed
Brief: <absolute path>
Full report: <absolute path>
```
