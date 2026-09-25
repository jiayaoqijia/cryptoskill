---
name: log-to-evidence
description: Turn raw logs into EVIDENCE.md rows and LaTeX/Markdown tables so that every number in the paper traces to a command, a log, a commit and a machine. Use after every benchmark or estimation campaign, and before every paper build, where `crbench audit-tex` must pass.
---
# log-to-evidence

## Rule

**No number enters the paper without an EVIDENCE row.** Each row records the number
*as printed* (after rounding), the exact command, the log path, the commit, the machine,
the date, and runs/statistic. Derived numbers (ratios, sums, percentages) get their own
row with `derived: <formula over IDs>`.

## Procedure

1. **Parse** the logs with a registered parser:
   `crbench parse results/x/new/r003.log --parser criterion`, or
   `crbench stats results/x/run.json --baseline base`.
   For a new log format, register a parser. A regex plus a test is enough: see
   `lib/bench/crbench/parsers.py`, `regex_parser`.
2. **Recompute** the number from the raw logs. Do not copy it from an earlier summary.
   Keep the recomputation script under `scripts/` so it can run again.
3. **Decide the printed form**: significant digits, unit, rounding rule. Use the same
   rule everywhere. Document whether you round or ceil: a `round()` vs `ceil()`
   mismatch between two tables produces off-by-one discrepancies that reviewers catch.
4. **Add the row**:
   ```bash
   crbench evidence add EVIDENCE.md --printed '0.61 s' \
     --command 'crbench run -a base=... -a new=... -n 7 --threads 1' \
     --log results/2026-01-01-toy-ab/run.json --runs '7 / median' --target ./src
   crbench evidence add EVIDENCE.md --printed '2.02×' --command 'derived: E1/E2' --log -
   ```
   `--commit auto` records the target repository's SHA and a `+dirty` flag;
   `--machine auto` records a host hash.
5. **Generate the table** from the same `run.json`, with evidence IDs:
   `crbench table results/x/run.json --latex --evidence new=E2 new:speedup=E3`.
   In LaTeX each cell carries `\evid{E3}`. Add `\providecommand{\evid}[1]{}` to the
   preamble so the markers are invisible in print, or render them as superscripts in
   drafts.
6. **Audit** before every paper build:
   ```bash
   crbench evidence check EVIDENCE.md --root .      # rows complete, logs exist
   crbench audit-tex paper/main.tex EVIDENCE.md     # each measurement-like number traced
   ```
   Fix every `untraced` and `mismatch` finding. Use `% crbench:ignore` only for numbers
   that are not claims (a year, a section count), and prefer rewording.

## Row examples (synthetic)

```markdown
| ID | number/fact as printed in paper | command | log path | commit | machine | date | runs/median |
|---|---|---|---|---|---|---|---|
| E1 | 1.23 s | crbench run -a base='./b/bench --set toy' ... -n 7 --threads 1 | results/2026-01-01-toy-ab/run.json | 1a2b3c4d5e6f | host:3f9a0c1d2e4b | 2026-01-01 | 7 / median |
| E2 | 0.61 s | (same run, arm new) | results/2026-01-01-toy-ab/run.json | 1a2b3c4d5e6f | host:3f9a0c1d2e4b | 2026-01-01 | 7 / median |
| E3 | 2.02× | derived: E1/E2 (CI [1.95, 2.08], paired bootstrap) | - | - | - | 2026-01-01 | - |
| E4 | ~~2.40×~~ | withdrawn: not reproducible in a same-session rerun (see E3) | results/2025-12-30-toy-ab/run.json | ... | ... | 2026-01-01 | - |
| E5 | 2^128.4 | sage -python est.py toy128 (MATZOV, estimator commit abcdef0) | results/est/toy128.log | abcdef0 | host:3f9a0c1d2e4b | 2026-01-01 | 1 |
| E6 | 7 results, zero sorry | lake build && scripts_check_no_sorry.sh | results/lean/build.log | 7a8b9c0 | host:3f9a0c1d2e4b | 2026-01-01 | 1 |
```

## Pitfalls

- **Mixed-configuration rows.** Each table row must come from *one* configuration. A
  best-time column and a best-op-count column taken from different sweep points must
  not share a row. If you report both "fastest" and "fewest operations", use two
  sentences and two rows.
- **"Best over the sweep"** must really be the best, for both arms. Recompute it.
- **Consistency.** The same claim printed in the abstract, introduction, evaluation and
  appendix must cite the same ID.
- **Negative results** (timeouts, noise-budget failures, unsupported configurations)
  also get rows. The paper may cite them as boundaries.
- **Contaminated sessions.** If a later same-session rerun contradicts a row, withdraw
  the row visibly, with a reason. Do not overwrite it.
