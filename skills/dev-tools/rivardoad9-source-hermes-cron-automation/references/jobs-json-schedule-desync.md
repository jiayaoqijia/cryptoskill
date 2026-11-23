# jobs.json direct edits: prompts sync, SCHEDULE exprs may not (verified 3 Sep 2026)

Companion to `jobs-json-direct-injection.md` (which covers one-day prompt injections).

## Symptom

Hand-edited `~/.hermes/cron/jobs.json` — changed a job's `schedule.expr` from `30 14 * * *`
(daily) to `30 14 * * 1,3,5` (Mon/Wed/Fri) and set `next_run_at` to the next valid fire time.
The FILE was correct (re-read and confirmed), but `cronjob action=list` still showed the OLD
expr `30 14 * * *`. The daemon registry keeps its own copy of schedule state; a file edit alone
does not reliably sync it — which means a stale daily expr can still fire on a day the new
schedule should skip (e.g. the very afternoon the cadence was supposed to be cut).

## What DOES sync via file edit

- `prompt` field edits — the scheduler picks these up (verified 31 Aug 2026, see
  jobs-json-direct-injection.md; re-verified 3 Sep 2026 for GAYA/style changes in 3 jobs).
- `enabled: false` set through the `cronjob` tool (pause) — that path writes daemon state.

## Correct procedure for schedule/cadence changes

1. Prefer `cronjob action=update` (job_id + schedule) from the start — never rely on a file edit
   for expr changes.
2. If you already hand-edited: re-verify with `cronjob action=list`. Expr mismatch → re-issue
   `cronjob action=update` passing BOTH the new schedule AND the full current prompt text.
   Passing the prompt matters: daemon memory may hold the pre-edit prompt, and an update issued
   from that stale state would regress your file-side prompt edits.
3. Back up jobs.json before any direct edit (`.bak_<date>`), use `assert count == 1` style
   replace checks, and confirm `next_run_at` survives.

## Why prompt edits are safe but expr edits are not (observed behavior)

Cron runs resolve their prompt from the file at fire time, but schedule bookkeeping (next-fire
computation, registry display) lives in the running daemon. Treat jobs.json as authoritative for
CONTENT, and the cronjob tool as authoritative for TIMING.
