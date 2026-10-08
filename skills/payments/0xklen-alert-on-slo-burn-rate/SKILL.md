---
name: alert-on-slo-burn-rate
description: Use when alerts fire on causes instead of user pain — replaces component thresholds with multi-window SLO burn-rate alerts and a defined error budget.
---

# Alert on SLO burn rate

Alerting on CPU or a single dependency's 5xx pages someone for things that do not harm users. Define an SLO, then alert only when the error budget burns fast enough that the month's target is at risk.

## Procedure

1. Write one SLO per user journey, in user terms: "99.9% of `POST /checkout` requests succeed within 500 ms over 30 days." Keep availability and latency as separate SLOs.

2. Compute the error ratio from RED metrics:
       job:slo_error_ratio = sum(rate(reqs{code=~"5.."}[5m])) / sum(rate(reqs[5m]))
   Exclude shed-load 503s and client 4xx; those are not user-visible failures of your service.

3. Convert the target to a budget: 99.9% over 30 days allows 43m 12s of failure. Burn rate is the fraction of the budget consumed per hour.

4. Use multi-window multi-burn-rate rules (Google SRE workbook) for fast and slow detection with few false pages:
       - page:   burn-rate 14.4 over 1h AND over 5m   (2% of budget in 1h)
       - page:   burn-rate 6    over 6h AND over 30m  (5% in 6h)
       - ticket: burn-rate 1    over 3d               (10% in 3d, no page)

5. Require both the long and the short window in each rule: the long window establishes significance, the short window confirms it is happening now. Only-long pages after the incident; only-short flaps on every blip.

6. Attach an owner and a `runbook_url` to every SLO alert; a page without a runbook is a puzzle for whoever is on call.

7. Review monthly: how much budget was spent and by which incidents. A budget never spent means the SLO is too loose; one always spent means the target must rise or the service must be fixed.

## Pitfalls

- Counting availability from the server status while users see a 200 with an error body — measure what the user gets, via a client-side or synthetic check.
- Including health-check and synthetic-probe requests in the SLO ratio, which deflates it and hides real failure.
- An alert on a saturated dependency that never breaches the SLO — too noisy for the pager; keep it on a dashboard.
- A burn-rate rule with mismatched windows, so it pages 30 minutes after the incident already ended.

## Verification

    promtool check rules slo.rules.yml    # SUCCESS: N rules found
    # drill: inject 100% errors for 10 min; the 14.4/1h rule must fire within ~4 min
    curl -s 'localhost:9090/api/v1/query?query=slo:burn_rate:1h' | jq '.data.result[0].value'

Report: the SLO text and budget (43m 12s), the burn-rate windows with their page/ticket split, and the injection drill's observed fire time.
