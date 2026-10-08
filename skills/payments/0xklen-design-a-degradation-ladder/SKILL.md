---
name: design-a-degradation-ladder
description: Use when a service must survive a partial dependency outage with reduced function instead of failing — defines ordered rungs from full to static and the trigger that moves between them.
---

# Design a degradation ladder

Full function and total outage are not the only two states. A ladder names the intermediate rungs — cached, read-only, static — and the concrete signal that moves the service down or back up, so degradation is a rehearsed step rather than an improvised panic.

## Procedure

1. Define the rungs in order, from least to most degraded, and what each still does. For a typical read-heavy service:
   1. **Full** — live reads, live writes.
   2. **Cached reads** — serve stale cache with `Cache-Control: max-age=60`; reject mutations.
   3. **Read-only** — serve persisted reads, disable background enrichment.
   4. **Static** — serve a pre-rendered fallback page and `503` for everything dynamic.

2. Give each rung a *trigger that is a number*, not a feeling: cache hit ratio below 60% for 3 min, dependency error rate above 5% for 2 min, primary DB unavailable. Reuse the existing SLO burn signals rather than inventing new ones.

3. Implement the ladder as one flag with ordered values, read on every request, so an operator moves one knob and the whole fleet follows within the flag TTL (keep that under 5 s):
       rung = flags.int("degrade_level", 0)  // 0 full .. 3 static
       switch rung { case 3: serveStatic(w); return }

4. Make each downward move *safe to happen at any time*: rung 2 and 3 must not require a deploy, must not lose in-flight writes, and must be testable in staging by setting the flag. A rung that only works after a code path is warmed is not a rung.

5. Move *up* deliberately and slowly, one rung at a time, after the trigger has been clear for 2× its window. Auto-recovery that jumps straight to full re-triggers the failure that caused the descent.

6. Emit the current rung as a gauge and alert if it stays above rung 0 for more than 15 min — a degraded steady state is an incident that has not been noticed.

7. Document, per rung, what the user sees (which fields go empty, which buttons disappear) so support and status-page copy match the actual behaviour.

## Pitfalls

- A ladder with rungs that are not independently reachable — "cached" that still calls the dead dependency on a cache miss, so it is really just "full with extra steps".
- Auto-descending fast but auto-ascending fast too, an oscillation that flaps between modes and makes both worse.
- Serving a 200 with a silently empty body at a low rung; users and monitors cannot tell degradation from correct-but-no-data. Return a header (`X-Degraded: cached`) or a visible banner.
- Forgetting writes: a read-only rung that still accepts and queues mutations, then floods the recovered primary on the way back up.

## Verification

    # drive the service to each rung via the flag and probe it
    for lvl in 0 1 2 3; do
      curl -s -X POST localhost:9090/flags/degrade_level -d "{\"value\":$lvl}"
      curl -s -o /dev/null -w "rung=$lvl %{http_code} %{time_total}\n" localhost:8080/api/feed
    done
    # expect 200 fast..200 slow..200..503, latency rising then a clean fallback

Report: the rung table with each trigger threshold, a staged run where each rung is reached by its flag and probed, and the alert rule on the current-rung gauge.
