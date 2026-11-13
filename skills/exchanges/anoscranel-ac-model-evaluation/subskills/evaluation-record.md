---
name: evaluation-record
domain: prompt-engineering/evaluation-record
trigger: "Writing the record of a suite, its runs, and its provenance."
anti_trigger: "Not for the harness code, and not for the report itself."
scope: "The written record: cases, scoring, results, and provenance."
status: seedling
---

# Evaluation record

## Standard

The evaluation record ties the suite to everything that makes its numbers interpretable: the construct definitions and the decision each serves, the case inventory with provenance and dates, the tier map of which case is scored by check, judge, or human, the calibration numbers of every judge used, the metric definitions with their `n` and case counts, and the run results with suite version and model training cutoffs attached. A result without that context is a number — often quoted — whose meaning cannot be reconstructed by anyone, including its author, three months later.

The record earns its keep at two moments. At the next model release, it converts the regression question from re-debating the design into re-running the instrument. At the moment of doubt — a surprising score, an uncomfortable ranking, a boss asking why — it shows what was measured and what was not, which is what honest evaluation is for. Provenance is the section most often skipped and most often missed: because nothing prevents an old case from silently predating a new model's training data, and no one can weigh a score without knowing which cases were fresh when they were written.

Primary sources: <https://osf.io/prereg/> and <https://docs.anthropic.com/en/docs/about-claude/evaluate>.

## Decision rules

- The record carries construct definitions, case inventory, tier map, and metric definitions.
- Every case has provenance and a creation date.
- Every judge's calibration numbers appear beside the scores it produced.
- Every result line carries suite version, metric, `n`, case count, and model cutoff.
- Amendments and case additions version the suite; results name the version they came from.
- Superseded runs are archived, not deleted — comparisons survive later scrutiny.

## Procedure

1. Assemble the construct definitions and the decision each serves.
2. Attach the case inventory with provenance, dates, and tier per case.
3. Record judge calibration numbers and protocol per graded construct.
4. Log each run: suite version, models compared with cutoffs, metric, `n`, and results.
5. Version the suite on any case addition or scoring change.
6. Archive prior runs; keep the record append-only with dated amendments.

## Anti-patterns

- Results reported without suite version or case count.
- A case inventory with no provenance or dates.
- Judge grades with no calibration figures.
- Version numbers frozen while the suite quietly changes.
- Deleting unfavourable prior runs.

## Done checklist

- [ ] Constructs and decisions recorded.
- [ ] Case inventory with provenance and dates.
- [ ] Tier map per case.
- [ ] Judge calibrations recorded.
- [ ] Every result line fully attributed.
- [ ] Prior runs archived; amendments dated.

## Sources

- Pre-registration practice for stated protocols: <https://osf.io/prereg/>
- Claude evaluation guidance: <https://docs.anthropic.com/en/docs/about-claude/evaluate>
- Harness record practice: <https://github.com/EleutherAI/lm-evaluation-harness>
