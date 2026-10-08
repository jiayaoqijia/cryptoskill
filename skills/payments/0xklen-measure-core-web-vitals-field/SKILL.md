---
name: measure-core-web-vitals-field
description: Use when a performance claim needs real-user numbers rather than one Lighthouse run. Pulls CrUX field data and instruments RUM with the web-vitals library.
---

# Measure Core Web Vitals in the Field

A lab score is a screenshot of one machine; field data is what your users actually got. Never sign off a perf change without the p75 field number behind it.

## Procedure

1. Pull the 28-day p75 for the origin before touching code:

       curl -s "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
         -d '{"origin":"https://shop.example.com","metrics":["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift"]}' | jq

2. Compare against the thresholds: LCP <= 2500 ms, INP <= 200 ms, CLS <= 0.1. Read p75, never the mean.
3. If the URL is below the CrUX popularity threshold, add RUM with the `web-vitals` package instead:

       import {onLCP, onINP, onCLS} from 'web-vitals';
       onLCP(m => navigator.sendBeacon('/rum', JSON.stringify({n:'LCP',v:m.value,id:m.id})));

4. Segment by device class using `navigator.deviceMemory` and the connection `effectiveType`; the cohort that matters is mobile.
5. Store raw values with the metric id so duplicates from bfcache restores can be de-duplicated (the same `id` arrives twice).
6. Report each metric's p75 with its window, device class and sample size.

## Pitfalls

- Quoting the lab median as the field p75; on LCP they routinely differ by 1-2 s.
- Instrumenting only `load` events, which miss the SPA route changes where most INP violations happen.
- Aggregating across device classes, letting a healthy desktop cohort hide a failing mobile one.
- Treating "no CrUX record" as a pass; it means the URL was never sampled.
- Sending one beacon per metric without batching; the endpoint gets hammered at p99 traffic.

## Verification

    curl -s "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
      -d '{"origin":"https://shop.example.com"}' | jq '.record.metrics.largest_contentful_paint.percentiles.p75'

A value under 2500 passes the field LCP threshold. Report the p75, its 28-day window and the device class it came from.
