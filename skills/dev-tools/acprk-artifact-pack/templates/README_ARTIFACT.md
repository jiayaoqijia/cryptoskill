# Artifact for "<Paper title>"

> During review this artifact is anonymous. Do not add names, affiliations or
> personal URLs.

## 1. Claims and how to check them

| paper item | claim | command | expected output | time | tolerance |
|---|---|---|---|---|---|
| Table 3 | stage X is a–b× faster than baseline on sets 1–9 | `scripts/reproduce_table3.sh` | `expected/table3.csv` | ~40 min | ratios within ±10%; op counts exact |
| Fig. 2 | cost model matches measured counts | `scripts/reproduce_fig2.sh` | `expected/fig2.csv` | ~2 min | exact |
| §6.2 | security estimates | `scripts/estimate_security.sh` | `expected/security.csv` | ~1 h | exact at pinned estimator commit |

Items not reproduced by this artifact: <list + reason>.

## 2. Requirements

- Hardware: x86-64, ≥ N GB RAM, ≥ M GB disk; results in the paper: <CPU model>,
  single thread.
- Software: see `env/` (Docker image or pinned requirements). Baselines are fetched
  at pinned commits by `scripts/fetch_baselines.sh` (see `baselines/MANIFEST.md`).

## 3. Quick start

```bash
bash scripts/fetch_baselines.sh
bash scripts/build.sh
bash scripts/smoke.sh          # < 10 min, must print "SMOKE OK"
```

## 4. Full reproduction

```bash
bash scripts/reproduce_all.sh  # runs every reproduce_* script, writes results/
python3 scripts/compare.py results/ expected/
```

## 5. Measurement notes

- Ratios are computed from interleaved A/B runs in one session (median of n).
- Absolute times depend on the machine; compare ratios and exact counts.
- Every run verifies correctness against a cleartext reference and aborts on mismatch.

## 6. Layout

`env/`, `baselines/`, `scripts/`, `expected/`, `results/`, `EVIDENCE.md`.

## 7. License

<license>
