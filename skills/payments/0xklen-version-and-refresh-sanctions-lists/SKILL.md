---
name: version-and-refresh-sanctions-lists
description: Use when operating the feed that keeps screening data current: pinning list versions, diffing deltas, scheduling refreshes, and failing closed when a list goes stale or unreachable.
---

# Keep sanctions lists versioned and fresh

Screening accuracy decays with the age of the list. Designations land between refreshes, and a
programme that cannot say which list version it used on a given date cannot defend any decision it
made.

## Procedure

1. Refresh on a schedule tighter than your slowest decision. Fetch hourly for programmatic lists
   and daily where a file is published daily; never let a cron failure be silent.

       curl -sSfL --max-time 60 -o /srv/lists/sdn.csv.tmp \
         "https://www.treasury.gov/ofac/downloads/sdn.csv" \
         && mv /srv/lists/sdn.csv.tmp /srv/lists/sdn.csv || echo "FETCH FAILED" >&2

2. Write atomically (download to `.tmp`, then rename) so a reader never sees a half-written list.
   Compute the digest after the rename and append it to a ledger.

       sha256sum /srv/lists/sdn.csv >> /srv/lists/versions.log
       wc -l /srv/lists/versions.log

3. Diff each refresh against the previous one and emit only the delta to the case-management
   queue, so re-screening focuses on changed rows:

       diff <(sort /srv/lists/prev.csv) <(sort /srv/lists/sdn.csv) \
         | grep '^>' | tee /srv/lists/delta-$(date +%F).txt

4. Stamp every screen with the list digests in force at that moment, not the digest at report
   time. Store `{list, sha256, fetched_at}` alongside the decision.

5. Define a staleness budget and fail closed. If `now - fetched_at > budget` for any required
   list, block new outbound transfers and page the owner. Serving traffic on a stale list is
   worse than an outage.

       python3 -c 'import time,os; age=(time.time()-os.path.getmtime("/srv/lists/sdn.csv"))/3600;
       print("STALE" if age>6 else f"fresh {age:.1f}h")'

6. Keep retired versions. When a designation is delisted, historical decisions must still be
   judgeable against the list in force at the time; never overwrite in place.

## Pitfalls

- Overwriting the list in place, which destroys the ability to reconstruct a past screen and
  turns a routine audit request into an unfalsifiable claim.
- Silent cron failure. A feed that has not updated in three weeks looks identical to one that has
  not needed to update.
- Treating one vendor's curated list as the whole universe; authoritative lists are the primary
  source and vendors lag them.
- Refreshing the file but not re-running re-screens, so an updated list never reaches the
  customer population.
- Clock skew between the fetch host and the decision log, which makes "which version was live"
  ambiguous by minutes — the exact window a fast designation exploits.

## Verification

    tail -1 /srv/lists/versions.log
    python3 -c 'import time,os;print("ok" if time.time()-os.path.getmtime("/srv/lists/sdn.csv")<21600 else "stale")'

A pass prints `ok`, meaning the active list is under the staleness budget and its digest is the
last line of the version ledger.

Report the list names, active digests, fetch ages, and the delta row count since the previous
refresh. Whether a stale window requires a filing or a lookback is a compliance call for a
qualified officer, not for this procedure.
