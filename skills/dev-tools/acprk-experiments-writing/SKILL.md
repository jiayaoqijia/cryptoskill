---
name: experiments-writing
description: Use when turning benchmark results into the evaluation section. Enforces that every printed number traces to an EVIDENCE.md row, prescribes table designs (parameters, main results, ablation, comparison), fair-comparison statements, and boundary/limitation statements.
---

# Experiments writing

## Iron rule

**Every number printed in the paper (text, table, figure, caption, footnote,
abstract) has an `EVIDENCE.md` row**: `ID | number as printed | command | log path |
commit | machine | date | runs/median`. Tables are generated from the data files
behind those rows (e.g. with the `crbench` table generator), not typed. Put
`% EV:<ID>` comments next to hand-placed numbers so a script can cross-check.

## Procedure

1. **Freeze the data.** Ask `experimenter` for the final json/csv and the EVIDENCE
   rows. Anything measured after the freeze requires a new row and a note in
   `DECISIONS.md`.
2. **Decide the scope sentence** for every range ("on the 9 parameter sets at ≥128-bit
   estimated security"). Scope comes from the parameter/security table, generated.
3. **Write the section** following `paper-playbook/sections/10_experiments.md`.
4. **Generate tables** (below). Mark the best cell per column (bold, optional light
   colour); two-level headers with `\multicolumn`; captions define every abbreviation
   and symbol.
5. **Write the fairness statements** (below) that apply.
6. **Write boundary/limitation remarks** (below).
7. **Cross-check script**: `crbench audit-tex paper/main.tex EVIDENCE.md` (lib/bench),
   or extract every number from the PDF text (`pdftotext -layout`) and match it to
   EVIDENCE rows; unmatched numbers are errors unless they are parameters or
   citations. Record the result in `SUBMISSION.md`.

## Table set

| table | contents | notes |
|---|---|---|
| Parameters | one row per set: all scheme parameters, derived values, security estimate(s) | `\resizebox{\linewidth}{!}` if wide; security column mandatory |
| Main results | per set: each configuration's time for the changed stage, total time, overheads (capacity, memory), ratio | ratio column states "vs <baseline>" in the header |
| Ablation | each component alone vs composed; failure counts/timeouts for variants that do not work | strongest evidence that the combination is necessary |
| Mechanism check | model-predicted vs measured operation counts | supports a cost model claim |
| Comparison with published work | Method, Ref, per-stage times, total, ratio; "measured by us" vs "as reported" marker; threads; failure probability; key/communication sizes | incomparable rows: symbol + "—" in ratio column + caption explanation |
| Client-side / communication | client cost, key sizes, setup cost | reviewers of transciphering/PSI/MPC ask for it |

Layout: `\scriptsize`, `\arraystretch` ≈ 0.92, `\tabcolsep` ≈ 2.6pt; tables at `[t]`;
table captions above tables, figure captions below figures.

## Fair-comparison statements (use the ones that apply)

- **Same pipeline:** "All ratios are against <baseline> run in our pipeline with the
  same <radix/parameters/library commit>; only <stage> differs."
- **Measured vs claimed:** "Rerunning the artifact of [X] on our machine reproduces
  their claimed a–b× as c–d×; we report both."
- **General caution before cross-paper tables:** "Such comparisons must be read with
  care because of differences in libraries, hardware and failure probabilities; we
  mark numbers taken from the original papers with ◇."
- **Metric orientation remark:** "Our goal is throughput; for latency-critical
  applications <other scheme> remains preferable."
- **Parallelism remark:** "All our numbers are single-threaded. Evaluating
  independent instances in parallel helps every scheme equally, so single-thread
  numbers compare designs, not hardware."
- **Security-level parity:** "Both our parameters and the baseline's are estimated
  at λ bits with <estimator commit>; where the estimator has moved since the baseline
  was published, we re-estimate both."
- **Baseline strength:** "We use the fastest configuration of <library> for the
  baseline (<flags>), not the default one." (Reviewers and shepherds check this.)

## Boundary / limitation statements

- Exclusions: "The k instances below the claimed security level are excluded from the
  headline ranges and flagged in Table <n>."
- Overheads: "The composed evaluator consumes 1.2–1.5× [ill.] the baseline's
  memory/capacity."
- Regime where we lose: "For t ≥ 7 [ill.], [X] is faster because ...; the regimes do
  not overlap." Say it before a reviewer does.
- Not applicable: "Our method requires <condition>; for instances violating it the
  implementation falls back to the baseline (log shows '<message>')."
- Measurement noise: "Absolute times vary with machine load across sessions; all
  ratios come from interleaved back-to-back runs in one session."

## Measurement hygiene to report (and to follow)

- Interleave A/B runs (ABAB...) in the same session; report median and IQR/CI.
- No concurrent heavy jobs; use a bench lock; pin threads.
- Never mix numbers from different sessions in one ratio; if an earlier number is not
  reproducible, retract it explicitly (and say so in the rebuttal if already quoted).
- Decryption/output verification for every run.

## Output

`paper/sections/experiments.tex`, generated tables in `paper/tables/`, the
cross-check report in `SUBMISSION.md`.
