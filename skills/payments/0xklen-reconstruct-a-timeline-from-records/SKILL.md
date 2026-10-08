---
name: reconstruct-a-timeline-from-records
description: Use when ordering events from logs, filings, or reports. Normalises timestamps and separates event time from record time before claiming sequence.
---

# Reconstruct a Timeline From Records

A timeline is only as trustworthy as its clock discipline. The time something happened, the time it was recorded, and the time it was published are three different moments — conflating them invents causality.

## Procedure

1. Convert every timestamp to one timezone (UTC) before sorting. Parse with an aware parser: `pd.to_datetime(series, utc=True)`; never compare a naive local time to an aware one.
2. Distinguish three times per record: `event_time` (when it happened), `record_time` (when the system logged it), `publish_time` (when the source surfaced it). Order by `event_time` when known; otherwise say you are ordered by `record_time`.
3. Detect clock skew. Compare a source's timestamps to a monotonic reference (an NTP-corrected log) and note offsets; a server an hour behind shifts everything.
4. Sort and find gaps. `awk -F, 'NR>1{print $2}' events.csv | sort | uniq -c` reveals bursts and silences; a gap can be missing data, not missing events.
5. Flag contradictions: two records claiming the same event at different times, or a cause timestamped after its effect.
6. Mark precision. "2024" is not "2024-03-11T09:00Z"; downcast to the coarsest common precision before ordering ties.
7. State the resolution of the timeline (day, minute) in the output so readers do not over-read sequence.

```python
import pandas as pd
df = pd.read_csv('events.csv')
df['t'] = pd.to_datetime(df['ts'], utc=True)
df = df.sort_values('t')
print(df[['t','event']].head())
```

## Pitfalls

- DST boundaries silently shift naive local times by an hour twice a year.
- Ordering by record/ingest time when event time is available produces a fake sequence that tracks load order.
- A retried write can log the same event twice with two timestamps; pair with dedup.
- Absence of a record between two dated ones is not proof nothing happened — it may be retention limits.
- Mixed precision (year vs second) makes a "before/after" claim unsupported.

## Verification

    python3 -c "import pandas as pd; d=pd.read_csv('timeline.csv'); assert d.t.is_monotonic_increasing; print(len(d),'events,', d.t.min(),'->',d.t.max())"

Report: "Reconstructed 214 events, 2019-04-02 → 2024-11-30 UTC, ordered by event_time; 3 contradictions and 2 clock-skew offsets flagged."
