---
name: mock-review
description: Use before submission (about 3 days and again 1 day before) or before a rebuttal to simulate venue-calibrated reviews. Runs falsify-first reviewer personas (expert-skeptic, generalist, implementer, plus optional data-auditor and desk-reject auditor), verifies their findings, and outputs scored reviews plus an executable fix list.
---

# Mock review

## Principles

1. **Falsify first.** The writer first produces a list of falsifiable statements
   (from `CLAIMS.md` and the contribution list: "the packing bound k ≤ N/(2tw) is
   tight", "the distinguisher holds for every key", "hypothesis H is necessary"). Reviewers are told to break them, not to praise.
2. **Personas are views of one analysis, not independent experts.** Say so in the
   output. Do not present simulated scores as a prediction of the real outcome.
3. **Only findings that can be located in the source, data or a script are accepted.**
   Reviewer agents produce false positives; the coordinating agent verifies each
   finding (reproduce the counterexample, open the log, recompute the cell).
4. **Read-only.** Mock reviewers never edit the paper; they write `REVIEWS.md`.
5. **Evidence-based and constructive.** Each weakness cites a page/section/equation
   and proposes a fix.

## Personas

| persona | stance | checks |
|---|---|---|
| **Expert-skeptic** (theory) | senior expert in the exact subfield, assumes the result is wrong | counterexamples on small parameters; hypotheses vs the paper's own parameter table; sufficient-vs-necessary confusions; body vs appendix formula mismatches; proof gaps; overclaimed proof status (heuristic stated as theorem) |
| **Generalist** (novelty/writing) | good cryptographer outside the subfield | can I restate the idea after the overview? is the delta over the closest prior work explicit? is "unified"/"first"/"optimal" justified? is the body self-contained without the appendix? |
| **Implementer** (experiments) | builds the same thing in practice | baseline strength/config; same machine/session; scope of ranges; excluded instances; overheads disclosed; ablation present; artifact runs; security estimates per instance |
| Data auditor (optional) | accountant | recomputes every ratio, sum and derived parameter in every table from EVIDENCE rows and logs |
| Desk-reject auditor (optional) | PC chair | page limit, template, fonts, page numbers, anonymity (run `anonymize-check`), links resolve, references complete |
| Links/anonymity (optional) | | curl every URL; grep identity strings in PDF text and binary; artifact README wording |

Pick 3 (default) to 5 personas; weights and venue anchors from
[venue-calibration](../venue-calibration/SKILL.md).

## Procedure

1. **Brief** (`reviews/REVIEW-BRIEF.md`): venue, paper path + hash, falsifiable
   statement list, persona assignments, what is out of scope (e.g. "we do not rerun the
   full benchmark; historical logs are not presented as fresh reproduction").
2. **Dispatch** persona agents in parallel, each with the brief and instructions to
   try to refute first.
3. **Verify** each finding: reproduce counterexamples with a script, recompute numbers,
   open cited logs. Mark each finding `confirmed | false-positive | unverifiable`.
4. **Score** with the six-point scale + confidence 1–4 per persona, plus dimension
   scores (problem value, novelty, technical soundness, experimental persuasiveness,
   precision of statements, reproducibility). Dimension scores are not averaged into
   an acceptance probability.
5. **Fix list** (`reviews/SUBMIT-FIXES.md`): items graded **must-fix** (compliance,
   integrity, confirmed errors) / **should-fix** / **won't-fix (with reason)**, each
   with file:line, old text, new text, and why. Include "good news" items (what was
   checked and found correct) so authors do not second-guess sound parts.
6. **Rebuttal prep**: list the 3–6 questions most likely to be asked and the evidence
   that answers each (feeds the `rebuttal` skill).
7. Human author decides which fixes to apply; after fixes, rerun the implementer
   (data) and desk-reject personas.

## Output format (`REVIEWS.md`)

```
## Round <k> — <date> — venue profile: <venue> — paper hash <sha256[:12]>
| persona | score | confidence | top-3 weaknesses | action item → agent |
|---|---|---|---|---|
Scope and limits of this review: <what was read, what was not rerun>
Personas are views of one analysis, not independent experts.

## Reviewer A — <persona>
Summary: 2–3 sentences.
Strengths:  S1 ... S2 ... S3 ...
Weaknesses: W1 (severity high|med|low, location, evidence, suggested fix) ...
Questions:  Q1 ... Q2 ...
Scores: overall x/6, confidence y/4; dimensions: ...
Recommendation: ...

## Reviewer B ...
## Reviewer C ...

## Meta-review (simulated discussion)
Score table | consensus points | disagreements | decisive issues |
subjective band with conditions (not a statistic) | top preparation items for rebuttal

## Verified findings
| id | finding | status confirmed/false-positive | evidence (script/log) |
```

## Frequent catches (generic)

| category | catch | prevention |
|---|---|---|
| anonymity | footnote URL to a personal code host account | anonymous mirror only; run `anonymize-check` |
| theory | body formula differs from appendix formula | copy from the proof source, never retype |
| theory | unconditional statement with a small counterexample | exhaustive search on toy parameters |
| theory | theorem hypothesis excludes some of the paper's own parameter sets | run the parameter table through each theorem |
| data | headline scope includes instances below the claimed security level | generate scope sentences from the security table |
| data | two incommensurable counters in one column | state each column's counter source in the caption |
| writing | composite gain credited to one component | label each number with its configuration |
| writing | "rigorous guarantee" for an asymptotic/heuristic result | "asymptotic, certified per instance" |
| citations | fabricated or wrong metadata, wrong author count | `lit-scout` verifies each entry against DOI/ePrint |
| layout | overprinting after negative vspace near floats | PDF overlap scan |
| strategy | best evidence (an ablation) not in the paper | ask "which experiment would convince a skeptic?" and check it is in the body |
