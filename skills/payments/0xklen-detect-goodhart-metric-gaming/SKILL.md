---
name: detect-goodhart-metric-gaming
description: Use when a metric is a target for a team. Checks for the shortcut it rewards and pairs it with guardrails before the number stops meaning what it should.
---

# Detect Goodhart Metric Gaming

When a measure becomes a target it stops being a good measure, because people optimise the shortest path to the number rather than the goal it stood for. Find the shortcut before it finds you.

## Procedure

1. Write the goal the metric proxies, then list the cheapest ways to move the metric without moving the goal.
2. For each shortcut, find the counter-metric that would move the wrong way and add it as a guardrail.
3. Inspect the distribution, not the mean — gaming often shows as a new mode, like a spike of rows where `closed_at - opened_at < 60s`.
4. Check the metric definition for a gaming surface: a rate built on a proxy event (page views, replies, sign-ups) invites the cheapest proxy.
5. Compare the metric against a slower, harder-to-game outcome (retention, repeat purchase, `reopened_within_7d`) and watch for divergence.
6. Look at the top movers: a few accounts or agents driving the change is a gaming signature, not a system improvement.
7. Set the guardrail as a constraint, not a trade-off: the target only counts if the guardrail holds.
8. Re-run the analysis one level down (per team, per segment) each quarter; gaming migrates to whatever is now unmeasured.
9. Alert on the ratio, not the level — a guardrail degrading while the target improves is the earliest signal.
10. When a new shortcut appears, add its counter-metric to the guardrail set rather than arguing about the definition.

## Pitfalls

- Per-agent "tickets resolved" incentivises closing early; `reopened_within_7d` is the guardrail that catches it.
- Lines of code, commits, and story points are all gameable and all get gamed the moment they are reviewed.
- Engagement metrics reward notification spam until uninstalls arrive on a lag.
- One aggregate team target with individual visibility creates the same shortcuts one level down.
- Removing the metric entirely is not the fix; pairing it with a guardrail measures the goal more honestly.
- A target and its guardrail reviewed on different cadences let the guardrail slip for months before anyone notices.
- Averaging over a long window smooths the gaming spike out of view; check weekly, not quarterly.
- A metric that is only ever reviewed, never acted on, still drifts toward the number because people assume it is used.

## Verification

    psql "$DSN" -c "SELECT agent, count(*) resolved, count(*) FILTER (WHERE reopened_within_7d) reopened FROM tickets GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"

Report: "Resolution time improved 18% but reassignment rose 26% and reopened-within-7d doubled for the top 3 agents — the target is being gamed by premature closure; guardrail added."
