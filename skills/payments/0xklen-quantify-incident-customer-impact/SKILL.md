---
name: quantify-incident-customer-impact
description: Use when an incident needs an honest impact number for comms or review. Computes affected users, failed actions, and duration from logs with stated error bars, avoiding both understatement and drama.
---

# Quantify Incident Customer Impact

Impact numbers drive comms tone, mitigation priority, and eventually credits or regulatory reporting. A hand-waved "many users" or a doubled estimate both mislead — the first hides severity, the second erodes trust when corrected.

## Procedure

1. Define the population precisely: active users, requests, or orders, per minute. "Affected" means the denominator you would have served without the incident.
2. Compute affected actions from logs, not vibes:

       # failed orders during the window, from the app log
       grep -c '"checkout","status":"error"' app.log --from 13:50 --to 14:52
       # served baseline: normal rate x window minutes

3. Estimate affected users deduplicated, not a raw request count — one user retrying ten times is one user.
4. Multiply by duration in whole minutes and state the window with UTC bounds.
5. Give a range, not a point, when sampling: "roughly 6,000-7,500 orders, +/-15%." State the method and the main uncertainty (did silently-failed requests log?).
6. Separate customer-visible impact (failed actions) from internal (retries, pager noise); only the former goes to customers and credits.
7. Recompute after mitigation; the end time matters as much as the start.
8. State the method alongside the number so a reviewer or auditor can reproduce it.
9. Round to the precision you can defend — "about 7,000 orders", not "6,943 orders", when the input is sampled.

## Pitfalls

- Counting retries as separate failures, inflating the number tenfold.
- Reporting request-failure counts as "affected customers", overstating the human impact.
- Using a point estimate with no method, which the review or a regulator will find unverifiable.
- Missing silent failures that returned a 200 with no work done, understating impact — check a work-completed metric, not just error codes.
- Freezing the number at the peak and never revising it down after mitigation.
- Quoting a number once and reusing it after the window changed, so the impact and the deadline disagree.

## Verification

```
    grep -Ei 'affected|window|UTC|range' incident/SEV*-2026-*.md
    # passes when the impact cites a defined population, UTC window, method, and an uncertainty range
```

Related: the range you compute here feeds `brief-an-executive-in-90-seconds` and the final `write-a-stakeholder-status-update`.
