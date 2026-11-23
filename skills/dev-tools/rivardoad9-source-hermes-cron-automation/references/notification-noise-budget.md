# Notification noise budget

Chat is for things the user acts on. A recurring job that prints every run is a log, and the user will eventually say "berisik" and stop reading all of it. Decide delivery per job, not per fleet.

## Delivery matrix

| Job kind | `deliver` | `failure_deliver` |
|---|---|---|
| Scanner / planner that writes DB or state every N min | `local` | `origin` (a dead scanner is real) |
| Event monitor (fill, stop, target, threshold) | `local` if the user asked for "daily only"; otherwise `origin` | `origin` |
| Watchdog guarding a page/tunnel | `origin` only on a real change (silent otherwise) | `local` when failures are scheduler-side dispatch alarms |
| Daily digest | `origin`, fixed hour, always prints | `origin` |

Changing a monitor to `local` means a stop-loss at 03:00 reaches the user at the digest hour. State that trade-off in the reply; do not leave it implied.

## Daily digest shape

- `no_agent` script, bare filename in `~/.hermes/scripts/`, `deliver=origin`, one fixed hour away from other cards.
- Read the SQLite DB directly, not the local HTTP API — the digest must survive the dashboard being down.
- Sections, in this order: state (equity/cash/open slots), today's events with PnL, all-time stats, open positions, pending plans, one footer line naming the cadence.
- Print the honest all-time numbers even when they are bad (win rate, average R, realized PnL). A digest that only shows today hides a losing system.
- Always print something; empty stdout in `no_agent` mode sends nothing at all, which turns the digest into another blind lane.
- Test by running the wrapper by hand with the same interpreter the cron will use (`./venv/bin/python`), not the system python.

## jobs.json audit

```python
import json
d = json.load(open('/home/ubuntu/.hermes/cron/jobs.json'))
jobs = d if isinstance(d, list) else d.get('jobs', [])
print([(j['name'], j['id'], j.get('failure_streak'), j.get('last_error', '')[:80])
       for j in jobs if j.get('last_status') == 'error' or (j.get('failure_streak') or 0) > 0])
```

- A high `failure_streak` (dozens) means the source changed, not a transient blip. Muting it hides stale data — say plainly what is frozen and since when, instead of reporting "fixed".
- Re-read jobs.json after every update: the tool response does not always echo `failure_deliver`.

## Distinguish scheduler failure from job failure

`Restart-safe cron worker dispatch failed: '<ENV_VAR>'` is raised before the script ever runs. Prove the job itself is healthy with `hermes cron run <job_id>` (CLI path) — if that succeeds, the bug is in the gateway's worker dispatch (often under memory pressure), not in the watchdog. Do not restart the gateway from inside the running session just to test a fix; mute the failure delivery and leave the dispatch path alone.

## Reducing dispatch surface

Widening a 5-minute watchdog to 15 minutes lowers the number of spawns and therefore the chance of hitting an intermittent dispatch bug. Pick the interval from what the job guards: a tunnel URL can be checked every 15 minutes; a stop-loss cannot.

## Data tidak lengkap ≠ alat rusak

Formatter kartu opsional yang membaca feed pihak ketiga (kartu arus ETF, ringkasan pasar) harus dibungkus: kalau datanya setengah jadi, tulis peringatan ke stderr dan `return 0`, jangan biarkan exception naik. Exception di formatter berubah jadi alert gagal yang tidak bisa ditindaklanjuti user, padahal besok datanya normal lagi. Alarm chat hanya untuk kegagalan yang butuh tindakan; kekosongan data yang lewat sendiri cukup di log.