---
name: handle-clock-skew-between-hosts
description: Use when ordering events or comparing timestamps across machines — bound the NTP skew, do not trust wall clocks for ordering, and widen tolerance to the measured offset.
---

# Handle clock skew between hosts

Two hosts disagree about `now` by milliseconds to seconds even under NTP. Ordering events by their wall-clock stamps across machines is therefore a guess; treat the skew as a measured quantity and design around it.

## Procedure

1. Measure the skew you actually have before assuming one:
```
chronyc tracking        # "System time" line = current offset
ntpq -p                 # "*" marks the chosen peer, "offset" in ms
timedatectl show-timesync --all 2>/dev/null | grep -i offset
```
2. Read the reported offset; if it exceeds your ordering tolerance, fix NTP before trusting the logs:
```
chronyc makestep        # step the clock once when the offset is large
```
3. Record a sk_ew budget in the design: e.g. "events ordered within a 250ms window are unordered." Do not claim ordering tighter than the measured offset.
4. Do not order events by wall time across hosts at all. Use a per-source monotonic counter plus the source id, or a sequence number from the producer:
```sql
SELECT * FROM events ORDER BY source_id, seq;   -- not created_at alone
```
5. If a global order is unavoidable, use a logical clock (Lamport counter) or a consensus sequence; wall time can break ties only within one host.
6. When correlating logs, widen the join window to the measured skew instead of exact-match on timestamps:
```python
# hosts skewed by up to 400ms: join on a window, not equality
match = abs((a.ts - b.ts).total_seconds()) <= 0.4
```
7. Alert on skew, not just time-sync drift: a host whose offset crosses the tolerance is a monitoring event.
```
chronyc tracking | awk '/System time/{print $4, $5}'   # e.g. "0.000123456 seconds fast"
```
8. For auth flows (JWT `exp`, TLS validity, signed URLs), add explicit leeway sized to the skew, not a blanket large value.

## Pitfalls

- Assuming two hosts share a clock makes an event from the "future" appear after its cause; ordering claims in postmortems become unreliable.
- `makestep` while a service is running can step time backwards and break monotonic-based timeouts (see `measure-elapsed-time-with-a-monotonic-clock`).
- Kubernetes nodes usually sync via the host; a pod cannot fix a node's skew, so checking inside the pod misleads.
- Virtualised clocks can drift between hypervisor sync windows; a VM paused for a snapshot returns skewed.
- A millisecond-tolerance ordering hides multi-second skew in a fresh fleet; measure per-host, not once.

## Verification

```
chronyc tracking | grep -E 'System time|Last offset'
```
The reported offset is below the design tolerance, and the ordering query uses `source_id, seq`, not `created_at` alone. Report: "measured skew 38ms across 6 hosts; cross-host ordering by `(source_id, seq)`; correlation joins widened to 400ms."
