---
name: cap-a-stack-with-a-cost-budget
description: Use when infrastructure cost can creep past a threshold unnoticed. Sets a budget with forecast alerts and a hard ceiling where the cloud supports one, so a runaway stack is caught before month-end.
---

# Cap a stack with a cost budget

Cloud bills arrive after the spend. A budget with alerts, plus a hard cap where possible, moves detection to when it can still be acted on.

## Procedure

1. Create a budget scoped by tag or account, matched to the stack:
       aws budgets create-budget --account-id 1234 --budget '{
         "BudgetName":"prod-app-monthly","BudgetLimit":{"Amount":"4000","Unit":"USD"},
         "TimeUnit":"MONTHLY","BudgetType":"COST",
         "CostFilters":{"TagKeyValue":["user:cost_center$app"]}}'
2. Set two alerts: at 80% of forecast (early warning) and at 100% actual (breach), to a channel someone watches:
       aws budgets create-notification --account-id 1234 --budget-name prod-app-monthly \
         --notification '{"NotificationType":"FORECASTED","ComparisonOperator":"GREATER_THAN",
           "Threshold":80,"ThresholdType":"PERCENTAGE"}' \
         --subscribers '[{"SubscriptionType":"EMAIL","Address":"ops@acme.com"}]'
3. For a hard ceiling, enforce where the cloud supports it: a Service Control Policy denying the instance class, or a quota on instances per type.
4. Add a monthly cost-anomaly monitor so a step change alerts within hours, not at billing close.
       aws ce create-anomaly-monitor --anomaly-monitor '{"MonitorName":"app","MonitorType":"DIMENSIONAL","MonitorDimension":"SERVICE"}'
5. Attribute the budget to the same tag used in code (`cost_center`), so budgets and tagging share a key.
6. Alarm on the trend, not only the absolute: a stack growing 30% month over month hits the ceiling soon.
7. Document the response: who reduces capacity, and at what threshold.
8. Review the budget against the bill monthly and adjust, or people start ignoring a budget that is always red.

## Pitfalls

- A budget with no alert subscriber, so nothing happens at 100%.
- A budget scoped to the whole account, so a runaway stack hides inside normal spend.
- Forecast alerts that fire on a seasonal spike every month and get muted.
- Believing the budget enforces a stop; only a quota or SCP does. Budgets notify.
- Tag-based budgets set before cost-allocation tags are activated, so the filter matches nothing.

## Verification

    aws budgets describe-budget --account-id 1234 --budget-name prod-app-monthly
    aws ce get-cost-forecast --metric UNBLENDED_COST --granularity MONTHLY \
      --time-period Start=2026-10-01,End=2026-11-01   # compare to BudgetLimit

Report: the budget scope, the alert thresholds and subscribers, the current forecast against the limit, and the enforcement mechanism if any.
