# Incremental scorecards & shift alerts — patterns proven 11 Sep 2026

Companion to `references/silent-and-dedupe-patterns.md`. That file covers *how to stay
silent*; this one covers the two job shapes that grew out of the 11 Sep 2026 session:
**"report what's new since last run"** and **"alert when a market-implied number shifts"**.
Both were built as `no_agent` scripts (0 tokens) and both shipped with a bug or a trap that
is easy to repeat.

## 1. The backlog drip — the classic bug of "new since last run" jobs

Two scorecards were built (`~/.hermes/scripts/na_scorecard.py` for our own macro verdicts,
`~/.hermes/scripts/hotelier_weekly.py` for an external analyst's weekly calls). Both
compute a whole history and then report only what has not been reported yet.

The first draft did:

```python
fresh = [r for r in done if r["slug"] not in reported][-3:]   # print newest 3
...
state["reported"] = reported | {r["slug"] for r in fresh}     # mark ONLY those 3
```

Result: run 1 printed the newest 3 rows, run 2 printed the 3 rows *behind* them, run 3 the
next 3 … an ancient backlog dripped out three at a time, forever, in the operator's chat.

**Rule: the backlog is history, not news.**

- After deciding what to print, mark **every already-closed item** as reported — the whole
  backlog, not just the printed subset.
- On a **first run** (no state file) announce only the single newest item, so the operator
  sees the format without a historical dump.
- Prove it with two consecutive runs; the second must be byte-empty:
  `out=$(python3 script.py); [ -z "$out" ] && echo "SILENT ✅" || echo "❌$out"`.
- Keep a `scored` set separate from `fresh`: the cumulative stats (HIT/MISS counts, hit
  rate) must be computed over ALL scored rows, while the printed lines cover only the new
  ones. Conflating them makes the running tally reset every run.

## 2. Scorecard honesty rules (they are the reason the number is worth anything)

- A verdict that never takes a side can never be wrong. Keep `NEUTRAL` and sub-threshold
  moves in **their own buckets** and never fold them into the hit rate; report the
  denominator out loud (`25/55 = 45%`, `30 flat`, `5 neutral`).
- Always print a **baseline** next to the score — e.g. "always bullish would have scored
  55% over the same window". A hit rate without a baseline is a vanity metric.
- **Score from data, not from a frozen snapshot.** The live records are written minutes
  after an event and their later horizons are never backfilled, so an event whose 1h move
  was empty at write time is silently unscorable forever — the sample shrinks with no
  error. Fall back to computing the move from candles at score time.
- State the sample size and refuse to draw conclusions from it: "2 HIT / 0 MISS, sampel 3
  rilis — belum cukup buat klaim". The loop's value is that it *will* have data later; say
  so instead of implying a proven edge now.

## 3. Shift alerts — thresholds, context, and anti-spam

`~/.hermes/scripts/fomc_odds_watch.py` (cron `b7cd755145b5`, `*/30`, `no_agent`) alerts
when market-implied odds move. The shape generalises to any "tell me when this number
changes meaningfully" job:

- **Alert on a threshold in the *meaningful* unit** (`|Δp| ≥ 5 points`), not on any change.
- **Always ship one always-alert condition** that bypasses the rate limit — here, the
  leading outcome flipping (hike ↔ hold), or the market rolling to the next expiry. Those
  are regime changes; they must not be swallowed by a "max 1 message / 3 h" gate.
- **Every message carries its own context**: current distribution, the delta AND the
  timestamp it is measured from, plus the domain caveat and the source. An alert that says
  only "odds moved" forces the operator to go re-derive everything.
- **Print nothing on success** (the script sends via its own channel), and one error line
  on failure — see the split-channel rule in `silent-and-dedupe-patterns.md`.
- Give it `--dry-run` (print, no send, no state write) and `--force` (send regardless).

## 4. Testing a threshold/flip branch without spamming the operator

Do not wait for the market to move:

1. `cp state.json /tmp/state_backup.json`
2. hand-edit the field the comparison reads (`p_hike: 0.60` so the live value looks like a
   +19pp jump; set `leader` to the opposite value to exercise the flip branch)
3. run `python3 script.py --dry-run` and read the rendered message
4. restore the backup and show the restored numbers

Then confirm the normal path end-to-end with `cronjob action='run'`: the report status
`silent (empty output)` is the proof that the quiet case is quiet (not that the job is
broken/dead).

## 5. Two-clock pattern: instant alert + scheduled digest

These jobs pair well with an existing digest: the shift alert covers "something moved", the
weekly/daily scorecard covers "were we right". Keep them separate — one is event-driven and
must be fast, the other is scheduled and must be cheap. Do not merge them into one job that
tries to do both, or the alert inherits the digest's schedule.
