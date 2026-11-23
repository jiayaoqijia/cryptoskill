# Per-run token cap guard (plafon biaya per job)

> **STATUS: DIMATIKAN 6 Okt 2026 (operator).** Job cron `6234aeaebf29` dihapus dan scriptnya
> dipindah ke `~/.hermes/data/retired/token_guard.py.removed_20261006` (+ state-nya ke
> `token_guard_state.json.removed_20261006`). Jadi **nggak ada lagi alert plafon token**.
> Pulihkan kalau perlu: `cp data/retired/token_guard.py.removed_20261006 scripts/token_guard.py`
> lalu bikin ulang job `no_agent` `20 */6 * * *` script `token_guard.py`.
> Catatan penting yang sering salah dipahami: guard ini **cuma baca-baca `usage_audit.jsonl` lalu
> lapor** — dia TIDAK nge-cap, nge-throttle, atau ngeblok run/job/model apa pun. Ngehapus dia
> nggak nambah kuota token, dan ada-nya dia juga nggak pernah bikin API call gagal.
> Sisanya di bawah ini = dokumentasi desain historis, disimpan buat kalau mau dihidupkan lagi.

**Why:** the audit (`usage_audit.jsonl`) only tells you AFTER the money is gone. Measured here
(6 Okt 2026): 11 deleted jobs = **23,3 juta token** total; `63e55c0b5cfd` alone = **11,8 juta
token in 3 days (≈695rb/run)** and nothing flagged it. Active LLM jobs also ran fat: `thesis-ai`
**839rb prompt/run**, Deep Dive 409rb, narasi audit 196rb, news briefing 134rb.

## The guard

- Script: `~/.hermes/scripts/token_guard.py` (stdlib only, `no_agent` → 0 token).
- Cron: `6234aeaebf29` — `20 */6 * * *`, `deliver=origin`, silent by design.
- State: `~/.hermes/data/token_guard_state.json` (`seen`: max token pernah dilaporkan per job;
  `hard`: `fire_id` yang sudah dilaporkan sebagai anomali).

Thresholds (constants at top of the script):

| const | value | meaning |
|---|---|---|
| `CAP_RUN` | 500_000 | batas normal per run |
| `HARD_RUN` | 1_500_000 | 3× cap → anomali, lapor sekali per `fire_id` |
| `BUMP` | 1.25 | lapor kalau rekor max naik >25% |
| `WINDOW_H` | 24 | jendela baca audit |

## Design rules that make it usable

1. **Change-only alerting, always.** A job permanently over cap must NOT alert every 6 h — that
   just trains the operator to ignore it. Only (a) a job that newly crossed the cap, or (b) a
   record max that grew >25% since last report. Otherwise: silent, 0 token.
2. **Label ghost jobs.** Job ids present in `usage_audit.jsonl` but missing from `cron/jobs.json`
   are deleted jobs → render as `(job dihapus)`, don't crash.
3. **Anomalies are separate from the cap.** A single run >3× cap is reported once per `fire_id`
   regardless of the `seen` table, so a one-off monster run can't hide behind a "already
   reported" state.
4. **Style:** build the message through `msgstyle.finish(..., kind="alert", add_regime=False)`
   (see `cron-output-style`); keep it ≤8 lines since the alert cap trims beyond that.
5. **Dry-run + reset:** `--dry-run` prints without writing state; `--reset` clears state (useful
   right after a first run has already "consumed" the current offenders).

## Gotchas hit while building it

- `jobs.json` job objects key the id as **`id`**, while `usage_audit.jsonl` keys it as
  **`job_id`** — using the wrong key makes every job look like a ghost (`KeyError`/all `(job dihapus)`).
- The first real run legitimately alerts (that's how `thesis-ai` at 982rb = 2.0× cap surfaced).
  That's correct behaviour, not a bug.
- Guard the cap floor at the *run* level, not per day: a job with 24 tiny runs is fine; one
  2-million-token run is what wrecks the budget.
