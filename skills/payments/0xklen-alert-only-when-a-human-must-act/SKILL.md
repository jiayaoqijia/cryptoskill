---
name: alert-only-when-a-human-must-act
description: Use when designing alerting for a job or service and tempted to notify on every failure. Sends a page only when a person must act now and demotes the rest.
---

# Alert only when a human must act

Every notification competes for attention. If an alert does not require a specific human to do a specific thing now, it is not a page — it is a log line, a ticket, or a dashboard panel.

## Procedure

1. For each candidate alert, write the required action in one sentence: "Operator X restarts the consumer." If you cannot name the actor and the action, it is not a page.
2. Classify each signal into one of four buckets: page (act now, waking a human is justified), ticket (act during business hours), dashboard (look when investigating), log (evidence only).
3. Route by classification: page to the paging system, ticket to the issue tracker, dashboard to a graph, log to logs. Do not send all four to chat.
4. Apply the auto-recoverable test: if the system heals itself, the event is dashboard or log, not a page. Transient retries that succeed belong in metrics.
5. Alert on symptoms users feel, not on causes that may be harmless: page on "checkout error rate > 1% for 5 min", not on "one pod restarted".
6. Attach a runbook link and an owner to every page; a page without a runbook is an interruption, not an alert.
7. Set a duration condition so a single blip does not page: `for: 5m` on a Prometheus rule, or an equivalent consecutive-failures count.
8. Review every page against its action: if the last N pages required no action, demote the alert. Track the ratio of actioned to unactioned pages.
9. Do not page on information already shown on a dashboard the on-call checks anyway.
10. Batch low-value notifications into a digest (a daily unresolved-failures summary) instead of streaming them.
11. Keep exactly one paging path with a tested reachability check; nothing erodes trust faster than a page that never arrives.

## Pitfalls

- Paging on every non-zero exit of a retried job; the retry usually succeeds and the page was noise.
- Sending dashboard-grade metrics to the phone because the tooling only has one channel.
- An alert with no owner, so everyone assumes someone else looked.
- Alerting on a cause you cannot act on (a third-party 500) when the symptom is stable.
- Thresholds with no duration, so normal jitter pages.
- Growing the alert list and never retiring entries.

## Verification

    # count pages in the last 7 days and how many had a linked action
    grep -c '"type":"page"' alerts.log
    # pass: every page names an actor+action and has a runbook link; unactioned pages are demoted

Report the action sentence for each page, its classification bucket, and the ratio of actioned to total pages last week.
