---
name: write-an-on-call-runbook
description: Use when a new alert pages someone who has never handled it — writes a runbook with copy-pasteable diagnosis, a numeric decision tree, and a safe mitigation per alert.
---

# Write an on-call runbook

A 3 a.m. page must be actionable by someone who did not write the service. Produce one runbook per alert, linked from the alert itself, with copy-pasteable diagnosis and a mitigation known to be safe.

## Procedure

1. Use a fixed template: What this alert means, User impact, First 5 minutes (diagnosis), Decision tree, Mitigation, Escalation, Related dashboards.

2. Link it from the alert annotation so it is one click from the page:
       annotations:
         runbook_url: "https://wiki/runbooks/checkout-error-ratio"

3. Put the exact queries in the runbook, not prose:
       # is it one version, one route, or global?
       sum by (version, route)(rate(http_requests_total{code=~"5.."}[5m]))
       kubectl logs -l app=checkout --since=10m | rg '"level":"error"' \
         | jq -r '.error.code' | sort | uniq -c

4. Write the decision tree as branches with thresholds: "if error ratio > 5% and flat across versions → dependency; check `breaker_state`; if open, do B. If only `version=canary` → roll back (link the rollback runbook)."

5. Give one safe mitigation per branch, ordered by blast radius: shed load → set canary weight to 0 → roll back → scale up → fail over. Prefer reversible actions and state the expected effect and how long until it shows.

6. State the escalation path with thresholds and the actual rotation link: "not mitigated in 15 min → page the service owner; 30 min → declare SEV1 and open an incident channel."

7. Test the runbook at the next on-call handover: a different engineer executes it against a staging fault, and every failing or ambiguous command gets fixed in the runbook rather than left in someone's head.

## Pitfalls

- Prose diagnosis ("investigate the database") instead of a command — the on-call guesses under pressure.
- Mitigations that need permissions the on-call lacks (database write, production deploy) with no documented escalation.
- Dashboards referenced by a renamed title; link by URL and check the link in CI.
- Only the happy path, with no "if that did not help, do this next", so the on-call loops on one command.

## Verification

    for a in alerts/*.yml; do yq '.annotations.runbook_url' "$a"; done \
      | xargs -n1 curl -o /dev/null -s -w '%{http_code}\n'    # every alert resolves 200
    rg -c 'kubectl|curl|promql|jq' runbooks/checkout-error-ratio.md   # >= 5 commands

Report: the runbook URL wired into each alert, a colleague's timed dry-run in staging (target under 5 min to mitigation), and any step that needed rewriting.
