# Cron job edits: schedule changes, file-vs-tool ordering, doc bloat

Verified 3 Sep 2026 on this user's stack (Threads content jobs + FlowMetrix).

## Schedule expr edits belong in the cronjob TOOL, not jobs.json

Direct `~/.hermes/cron/jobs.json` edits are fine for **prompt** changes (scheduler picks
them up; see jobs-json-direct-injection.md) but a `schedule.expr` edit made file-side can
leave the daemon's registry — and therefore `cronjob action=list`'s schedule display —
STALE, even though `next_run_at` (file field) refreshes. If the daemon still thinks the
old expr, the job fires on the wrong days (e.g. a "Sen/Rab/Jum" change not applied until
you sync).

Procedure that works:
1. Do tool calls that persist daemon memory FIRST (`cronjob pause` / `resume` / `update`),
   THEN any direct jobs.json prompt edits last — otherwise the daemon's next persist can
   clobber your file edits.
2. For schedule changes: `cronjob action=update` with `schedule` (and the full current
   prompt if the daemon's cached copy predates your file edits — pass `prompt` too so the
   update doesn't persist an older prompt).
3. Verify with `cronjob action=list`: schedule expr AND `next_run_at` must both show the
   intended value. `next_run_at` alone changing is NOT proof the expr took.
4. Backup jobs.json before surgery: `cp jobs.json jobs.json.bak_<date>`.

## Token cost of bloat in agent-read docs

Every cron agent run re-reads its briefing docs in full. Measured on this stack:
a 35KB content bible ≈ 9-10K tokens × ~17 content runs/week ≈ 170K tokens/week just
reading the file; the daily recap reading a 53KB strategy log cost another ~15K/run.
Controls that work:
- Keep agent-read docs lean: archive dated narrative into an `archive/` subfolder; keep
  only active rules in the live doc. (3 Sep 2026: 34.8KB → 21KB, 52.7KB → 16.9KB.)
- Embed a maintenance rule IN the doc the automation reads, e.g. "JANGAN tambah blok
  narasi baru; update blok aktif; jaga dokumen < ~15KB; narasi & data → <log file>" — the
  appending agent then self-limits instead of growing the file forever.
- Point agents at the lean doc + mention the archive path for deep context ("entri lama
  diarsip di ... kalau butuh konteks jauh").
