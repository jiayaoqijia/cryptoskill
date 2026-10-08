---
name: attach-a-runbook-link-to-every-alert
description: Use when an alert fires and the responder has to guess the first step. Requires every alert to carry a link to a runbook written for someone woken at 3am.
---

# Attach a runbook link to every alert

An alert without a runbook hands the responder a mystery at the worst time. Every alert template must include a link to a runbook that starts with the first action, not with background.

## Procedure

1. Add a `runbook_url` annotation to every alert rule and make it required by a lint step in CI so a rule without one fails:
       annotations:
         runbook_url: https://wiki/runbooks/nightly-reconcile
         summary: "Nightly reconcile has not completed in 36h"
2. Write each runbook the way the on-call reads it: symptom, first command, expected output, what to do if that fails, who to escalate to.
3. Put the copy-pasteable diagnostic commands in the runbook, with the exact paths and flags, not paraphrases.
4. State the rollback or mitigation step explicitly and near the top — on-call needs to stop the bleeding before understanding the cause.
5. Keep runbooks version-controlled next to the code that alerts, and fail the alert-lint if the URL does not resolve.
6. Record the last time the runbook was exercised (a drill or a real incident) with a date; stale runbooks mislead.
7. Link outward only one hop: the runbook may reference other docs, but the first action must be on the runbook page.
8. Review the runbook after every page it produced: did the first step work? If not, fix it in the same PR as the incident follow-up.
9. For runbooks that need access (a bastion, a DB, a vault path), name the access so the responder is not blocked mid-incident.
10. Keep the alert message short and point to the runbook for the long form; do not paste the whole procedure into the notification.

## Pitfalls

- A runbook that is a design doc: history first, first action on page nine.
- A link to a wiki page that was renamed or deleted; the responder finds nothing.
- Commands in the runbook that reference hosts or paths that no longer exist.
- Runbooks that assume the reader wrote the system.
- Alert rules merged without the link because linting was not wired.
- A runbook that only says "investigate" — that is not an action.

## Verification

    # fail if any alert rule lacks a runbook_url
    yq '.[] | select(.annotations.runbook_url == null) | .alert' alerts/*.yaml   # expect empty
    curl -sf -o /dev/null -w '%{http_code}\n' https://wiki/runbooks/nightly-reconcile   # 200

Report each alert's runbook link, the first action line, and the date the runbook was last exercised.
