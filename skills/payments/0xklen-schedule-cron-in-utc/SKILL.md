---
name: schedule-cron-in-utc
description: Use when writing or reviewing a cron, systemd timer or scheduled job — pin the schedule to a fixed zone so it fires at the same instant all year, not the same local clock time.
---

# Schedule cron in UTC

A crontab entry with no zone fires on the host's local clock, so a `30 2 * * *` job runs at a different instant after every DST shift and on every host with a different `TZ`. Pin the zone once and reason in UTC.

## Procedure

1. Read what the scheduler actually does today:
```
crontab -l; systemctl list-timers --all; cat /etc/cron.d/* 2>/dev/null
```
2. Force the zone in the crontab. Vixie cron honours `CRON_TZ`; Debian/Ubuntu cron honours `TZ`; set the one your daemon reads at the top of the file:
```
CRON_TZ=UTC
30 2 * * * /usr/local/bin/rollup.sh >> /var/log/rollup.log 2>&1
```
3. For systemd, `OnCalendar` defaults to local time — append the zone explicitly:
```
[Timer]
OnCalendar=*-*-* 02:30:00 UTC
Persistent=true
```
4. Express business-local jobs deliberately. If the job must run at 02:30 *local* in New York, say so and expect the UTC instant to move twice a year:
```
TZ=America/New_York
30 2 * * * /usr/local/bin/rollup.sh
```
5. Confirm the host zone when a job cannot be forced:
```
timedatectl; date; date -u
```
6. Check the next fire instant before trusting it, not after the job misses:
```
systemd-analyze calendar --iterations=3 "*-*-* 02:30:00 UTC"
```
7. Record the chosen convention in the runbook: "all timers are UTC unless the entry names a zone."

## Pitfalls

- The 02:00-03:00 window is exactly where US DST jumps. A job at `30 2 * * *` local is skipped on spring-forward day and runs twice on fall-back if the daemon retries.
- `CRON_TZ` is absent on BusyBox and some BSD crons — the line is ignored and the job silently reverts to local. Verify with the next-fire check, not by reading the file.
- A container often ships `TZ` unset = UTC, so a job tested in a container fires an hour off in production where `TZ` is set in the base image.
- `@daily` / `@reboot` take no time; `@daily` is 00:00 local and shifts with DST just like the five-field form.
- DST-skipped timers on `OnCalendar` are missed unless `Persistent=true`, which runs them once on catch-up.

## Verification

```
systemd-analyze calendar --iterations=4 "*-*-* 02:30:00 UTC" | tail -4
```
Four successive instants that differ by exactly 24h across a DST boundary = the schedule is zone-fixed. Report: "rollup timer pinned to `02:30 UTC`; next four fires are 24h apart through the March DST change."
