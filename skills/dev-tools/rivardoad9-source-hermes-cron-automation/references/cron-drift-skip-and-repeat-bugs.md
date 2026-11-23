# Cron Operational Pitfalls: drift-skip, repeat TypeError, dead rekap job (2026-08-23)

## Drift-skip: jobs silently skipped after provider/model config change

Symptom: job `last_status=error`, output contains `RuntimeError: [drift_skip] Skipped
to prevent unintended spend: global inference config drifted since this job was created
(provider 'custom' -> 'deepseek'), and this job is unpinned. No inference call was made.`

Cause: the global `model.provider` / `model.default` in config.yaml changed after the job
was created; unpinned jobs refuse to run rather than spend on an unintended model. Jobs
created BEFORE the provider migration are the ones at risk — this hit the Threads promo
06:00 and value 21:00 slots (2026-08-23): both errored, promo silently missed its slot.

Fix — pin the job to the CURRENT provider+model:
```
hermes cron edit <job_id> --provider custom --model deepseek-v4-flash
```
Then confirm via `cronjob list` that the job shows the pinned model/provider.

Audit all jobs at once: read `~/.hermes/cron/jobs.json` and check every `enabled` job's
`model` / `provider` fields against the current config — jobs showing a stale provider
(or `(inherit)` after a migration) are drift risks. Pin each one proactively rather than
waiting for the first silent miss.

## cronjob tool: `repeat="forever"` throws a TypeError; omit it

Passing `repeat="forever"` to cronjob `create`/`update` raises
`'<=' not supported between instances of 'str' and 'int'`.
Workaround: OMIT the `repeat` param entirely — a recurring cron schedule defaults to
`repeat: forever` in the resulting job.

## Dead rekap job: `repeat: 1/1` + state `completed` cannot be resurrected via update

A job created with `repeat: 1/1` that reached state `completed` (and `enabled: false`)
rejects updates with the same TypeError path. Recreate it instead:
1. `cronjob create` with the same prompt + schedule + `continuity` (do NOT pass repeat)
2. `cronjob remove` the old completed job
The daily "Rekap performa + improvement harian" job died exactly this way 2026-08-23 —
the scheduler had run it once as a one-shot and silently stopped, so the morning recap
(and its strategy.md update) stopped happening. Detect this class of failure by watching
for `repeat: 1/1` on any job that is supposed to run daily.
