---
name: lit-matrix
description: Build and lint the related-work matrix (work, venue/year, setting, technique, asymptotics, concrete numbers + source, code available?, our delta) and the novelty-check log in LITERATURE.md. Use in P1, whenever a new baseline appears, and before writing the related-work section.
---

# lit-matrix

The matrix is the single place where "who did what, under which parameters, with which numbers" lives.
Writers copy from it; the falsifier attacks it; baselines are chosen from it.

## Format (in `LITERATURE.md`)

```markdown
## Related-work matrix

| work | venue/year | setting | technique | asymptotics | concrete numbers + source | code? | our delta |
|---|---|---|---|---|---|---|---|
| [@RS21] VOLE-PSI | EC 2021 | 2PC semi-honest, n=2^20 | VOLE + OKVS | O(n) comm | 51 MB, 1.3 s LAN (Tab. 3) | yes https://... | we ... |
```

Column rules (enforced by `scripts/lit_matrix.py`):

- **work** — bib key (`[@key]` or `\cite{key}`) or ePrint id, plus a short human name.
- **venue/year** — venue of the version you cite (ePrint-only is fine, say so).
- **setting** — everything needed to compare fairly: parameter set / security level / threat model /
  network model / ring dimension / field / number of parties / hardware.
- **technique** — ≤12 words; the mechanism, not the marketing.
- **asymptotics** — the cost measure the community uses (ops, mults, depth, rounds, key-switches, comm).
- **concrete numbers + source** — numbers *with* a pointer (Tab./Fig./Sec./p.) or `measured E<n>` (an EVIDENCE
  row, if we re-ran it). Numbers from a paper and numbers we measured are never mixed in one cell without saying so.
- **code?** — `yes <url>` / `no` / `unknown`.
- **our delta** — what we do that this row does not. `none` is an honest answer and triggers a PI decision.

## Procedure

1. Seed from `references/reading-lists/<area>.md`, then expand with `eprint-search` (last 12 months first).
2. One row per *result* (a paper with two incomparable results gets two rows).
3. Fill numbers only from the paper's tables/figures; if the paper's parameters differ from ours, note it in
   *setting* instead of "normalising" silently.
4. Mark the 2–4 rows that are the real competitors (**bold** the work cell); `baseline-engineer` pins those.
5. Lint: `python3 skills/lit-matrix/scripts/lit_matrix.py LITERATURE.md --bib refs.bib`.
6. `python3 skills/lit-matrix/scripts/lit_matrix.py --template` prints an empty skeleton.

## Reading the matrix for gaps

Sort by *setting*, then look for (a) settings with no row (application gap — weakest kind of novelty, must be
argued), (b) a technique used in one setting but not the neighbouring one (transfer), (c) a parameter every row
fixes to the same value (a "hidden fixed parameter" — hand to `idea-miner`), (d) asymptotics that nobody has a
lower bound for.
