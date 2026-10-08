---
name: pin-metric-definitions-in-one-place
description: Use when a number means different things to different people or two dashboards disagree. Canonicalises each metric as one versioned definition with an owner and SQL.
---

# Pin Metric Definitions In One Place

If "active user" lives in three dashboards and means three things, every meeting is an argument about arithmetic instead of a decision. A metric is a spec: definition, owner, source, version.

## Procedure

1. For each contested metric write a one-line definition in the form `<verb> <entity> <qualifier> <window>`, e.g. "distinct users who logged in at least once in the trailing 7 days".
2. Record the four ambiguous knobs explicitly: population (all users? paying?), event (login vs any request), window (trailing 7d vs calendar week), grain (user-day vs user-week).
3. Put the canonical SQL in a version-controlled model, e.g. dbt `models/marts/metrics/active_users_7d.sql`, with a `description:` and `owner:` in the schema YAML.
4. Deprecate the copies: grep the BI tool for the old definition text and repoint every chart to the model.
5. Version the definition. A change to population or window is a new `v2`; never silently edit in place.
6. Publish a glossary mapping each dashboard column to the canonical metric and its version.
7. When two systems disagree, resolve by tracing both to raw events before editing either dashboard.

```bash
# find every place a competing definition is spelled out
grep -rniE 'active user|DAU|WAU' dbt/models dashboards/ | grep -i 'distinct'
```

## Pitfalls

- "DAU" that counts sessions rather than distinct users always exceeds a user-count dashboard; the gap is not a bug.
- The window timezone changes the number: a calendar day in UTC and in America/Los_Angeles differ by seven hours of events.
- Trailing 7d and calendar-week windows give different values for the same day; pick one and say which.
- Renaming a column but keeping the old SQL leaves a definition that lies about its own grain.
- An unowned metric drifts; every canonical metric needs a named owner in the YAML.
- Two metrics that differ only by timezone are the same metric in disguise; put the zone in the definition line itself.
- A metric defined on a filtered view changes silently when the view changes; define on the raw fact and filter at query time.

## Verification

    grep -rl 'owner:' dbt/models/marts/metrics/ | wc -l   # equals the count of metric models

Report: "Canonicalised active_users_7d (distinct users, any authenticated request, trailing 7d, UTC); 3 dashboards repointed; the 11% gap vs the old session-based DAU is explained by the grain change."
