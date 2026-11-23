# Migrating the whole cron fleet to a new timezone (2026-08-25, UTC+8 → WIB)

Goal: make cron natively express the user's timezone so no "server time vs user time" conversion is ever needed again (user: "atur WIB, jangan pake zona waktu lu").

## Procedure (order matters)

1. Change the SYSTEM timezone first: `sudo timedatectl set-timezone Asia/Jakarta` (verify: `date` shows WIB).
   - The running gateway scheduler keeps its OLD timezone until restart (Python caches TZ at process start) — so after this step `date` and cron interpretation temporarily disagree. Nothing fires differently yet because schedules are still old-shifted.
2. WAIT for any in-flight cron/delegation runs to complete — a restart KILLS running cron agents mid-turn (e.g. a post job that hasn't published yet). Check `~/.hermes/logs/agent.log` for "completed successfully"/delivered markers first.
3. Shift EVERY schedule by the TZ delta so absolute fire times are unchanged (UTC+8 → UTC+7, delta −1h: `0 7 * * *` → `0 6 * * *` for a 06:00 WIB slot). Include no_agent script jobs and paused jobs; update job names that embed times ("… 12:00 WIB" → "… 16:00 WIB").
4. Restart the gateway detached (see hermes-gateway-ops skill) so the scheduler picks up the new TZ + new schedules together.
5. Verify: `hermes cron list` → every `Next run` shows the new offset (+07:00) AND the intended WIB time; `date` confirms TZ.

## Pitfalls

- Never edit schedules to the new values BEFORE the TZ change takes effect in the scheduler: while the old-TZ scheduler is still alive it interprets shifted schedules and fires jobs EARLY (a 09:00 WIB slot firing at 09:00 old-time = 08:00 WIB). Edits and restart must land in the same short window, before the next scheduled fire.
- Historical `last_run_at` values keep their old offset (+08:00) — expected; they're past events.
- `drift_skip` can fire in EITHER direction (provider 'custom' -> 'deepseek' and vice versa) and goes SILENT after the first alert (drift_skip:silent) — a job that "never runs" may show no error at all. Audit `~/.hermes/cron/output/<id>/*.md` Error sections when a job silently stops.
- After any config/TZ change, pin ALL agent jobs to the current provider+model (`hermes cron edit <id> --provider custom --model deepseek-v4-flash`) so future config flips can't silently skip them.
- Timezone facts go stale fast: after the migration the old mapping ("server = user + 1h") is GONE. Update skills/memory that hardcode the old mapping.
