---
name: collect-web-vitals-rum
description: Use when you need per-route, per-device field vitals you own. Instruments Core Web Vitals with attribution and ships them to your own endpoint.
---

# Collect Web Vitals RUM

CrUX gives you an origin-level p75 once a month; your own RUM gives you the failing route, the device class and the element. Own the pipeline so you can segment it.

## Procedure

1. Install the library and subscribe to every metric, not just LCP:

       import {onLCP, onINP, onCLS, onFCP, onTTFB} from 'web-vitals/attribution';

2. Include attribution so a regression names the cause, not just the number:

       onLCP(m => send(m), true);
       function send(m) {
         navigator.sendBeacon('/rum', JSON.stringify({
           name: m.name, value: m.value, delta: m.delta, id: m.id,
           route: location.pathname, conn: navigator.connection?.effectiveType,
           attribution: m.attribution
         }));
       }

3. Sample at high traffic (for example 10%) rather than dropping to aggregate-only; a fixed sample keeps query cost predictable.
4. Include the connection type, device memory and the app version so a deploy that regresses a route is attributable within minutes.
5. Send on `visibilitychange` to hidden as a fallback, since some metrics only finalise when the page is backgrounded.
6. Store raw rows with a TTL; compute p75 per route per day in a batch job rather than on the write path.

## Pitfalls

- Sending one beacon per metric and per delta, flooding the endpoint; debounce and batch.
- Counting hard navigate + bfcache restore as two samples for the same `id`, skewing toward fast reloads.
- Computing a mean instead of a p75; Core Web Vitals are explicitly p75-defined and a mean hides the bad tail.
- Losing samples when the beacon fires during unload; use `sendBeacon` or `fetch(..., {keepalive:true})`, not `XMLHttpRequest`.
- No app version in the payload, so you cannot tell whether a regression started before or after the release.

## Verification

    curl -s 'http://localhost:8080/rum' -H 'content-type: application/json' \
      -d '{"name":"LCP","value":2100,"id":"v1-1","route":"/p/1"}' -o /dev/null -w '%{http_code}\n'

A 204 from the collector means the beacon is accepted. Report the routes receiving samples and the p75 LCP per device class.
