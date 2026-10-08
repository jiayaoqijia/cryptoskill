---
name: deduplicate-repeated-alerts
description: Use when one root cause fires the same alert from many hosts, shards, or retries at once. Groups duplicates into a single notification so responders see one incident, not hundreds.
---

# Deduplicate repeated alerts

A database blip makes every host page at once; a bad deploy makes every pod alert simultaneously. The responder needs one incident, not N copies. Group and deduplicate at the point of dispatch.

## Procedure

1. Identify the grouping key: the thing that is the same across duplicates. Usually `alertname + cluster + service`, not the host or pod, so 40 pods become one alert.
2. Add the key to the alert's labels so the dispatcher can group:
       labels: {alertname: DbConnExhausted, cluster: prod, service: payments, instance: "$node"}
       # group by alertname, cluster, service — drop instance from the group key
3. Configure the router's grouping (Alertmanager `group_by: [alertname, cluster, service]`, `group_wait: 30s`, `group_interval: 5m`, `repeat_interval: 4h`) so bursts coalesce and reminders are rare.
4. Suppress the follow-ons while the primary is firing: an inhibit rule where a firing `NodeDown` inhibits all `PodMissing` on that node, so one root cause produces one page.
5. Collapse retries at the source when you own it: a job that retries 20 times should emit one failure summary on final failure, not 20 errors.
6. Keep a distinct key for genuinely separate incidents: two different services failing must not fold into one page.
7. Send recovery only after the group clears, so a flapping set does not send "resolved" between every blip.
8. Test the grouping with a synthetic burst: fire 100 copies and confirm one notification arrives.
9. Record the group key and inhibit rules in the runbook so responders know why they saw one page for a cluster-wide failure.
10. Review after each incident whether the grouping merged too much or too little, and adjust the key, not the count.

## Pitfalls

- Grouping by `instance`, so a fleet-wide failure pages once per host.
- `repeat_interval` too short, so a long incident re-notifies every few minutes and trains people to ignore it.
- Inhibit rules that are too broad and swallow a second, unrelated outage.
- Deduplicating only in the chat integration while the paging system still sends N pages.
- Not deduplicating retries, so a flapping check produces a wall of messages.
- Losing the count — folding 100 failures into one page without saying "100 of 100".

## Verification

    # fire the same alert from many sources and count notifications
    for i in $(seq 1 100); do curl -s -XPOST localhost:9093/api/v1/alerts -d @alert.json; done
    # pass: exactly one notification for the group, recovery sent once after the last clears

Report the grouping key, the group_wait/interval/repeat values, the inhibit rules, and the result of the 100-copy burst test.
