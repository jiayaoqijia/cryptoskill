---
name: audit-logs-for-timezone-drift
description: Use when correlating logs or debugging an incident across services — verify every log line carries the same zone, because mixed local and UTC timestamps fake ordering and fake outages.
---

# Audit logs for timezone drift

When one service logs UTC and another logs local time, a merged timeline is fiction: events appear out of order and a "20-minute gap" is really an offset. Audit the zones before you trust any cross-service timeline.

## Procedure

1. Sample the raw lines and inspect the trailing offset or its absence:
```
rg -N -o '\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?\b' /var/log/app/*.log | sort | uniq -c | sort -rn | head
```
2. Find producers that emit no zone at all:
```
rg -n '"ts":"[^"]*"' logs/ | rg -v 'Z"|\+[0-9]{2}' | head
```
3. Check each service's runtime zone, not just the config file:
```
for h in app-1 app-2 app-3; do ssh $h 'timedatectl | grep "Time zone"'; done
```
4. Standardise output to UTC with an explicit `Z`, and include a zone field if the source is local:
```json
{"ts":"2026-03-01T14:00:00.123Z","level":"info","svc":"auth","tz":"UTC"}
```
5. When combining streams, parse every timestamp to an instant before sorting; never sort the raw strings:
```bash
jq -r '[.ts, .msg] | @tsv' a.json b.json | sort -k1,1   # only valid once .ts is ISO-8601 UTC
```
6. Quantify the drift before and after the fix: take a heartbeat log emitted by two services at the same wall moment and diff their parsed instants.
```
python3 -c "from datetime import datetime; a=datetime.fromisoformat('2026-03-01T14:00:00+00:00'); b=datetime.fromisoformat('2026-03-01T09:00:00-05:00'); print(a==b)"
```
7. Add a lint/CI check that rejects log configs without a UTC formatter or with a bare `%Y-%m-%d %H:%M:%S` pattern.

## Pitfalls

- A container with `TZ=America/New_York` and the app logging `%localtime` shifts every line by the offset only in that environment, so production timelines are wrong while staging looks fine.
- Journald and syslog may stamp in local time even when the app logs UTC; normalise at collection, not at query.
- A DST fall-back repeats an hour of local log lines; sorting by the local string interleaves two different hours.
- Aggregators sometimes "helpfully" assume a missing zone is UTC and sometimes local, so the same offsetless field drifts by service version.
- A log line's in-message timestamp can disagree with the collector's ingest time by minutes under load; record both and label them.

## Verification

```
rg -o 'Z\"|[+-][0-9]{2}:[0-9]{2}\"' logs/*.json | sort -u
```
Every emitted timestamp form ends in `Z` or an explicit offset, and none is bare = drift eliminated. Report: "3 services emitted local time in non-UTC containers; all now log ISO-8601 UTC with a `tz` field; merged timeline re-parsed and sorted on instants."
