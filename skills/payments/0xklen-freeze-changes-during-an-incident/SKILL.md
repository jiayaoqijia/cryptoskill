---
name: freeze-changes-during-an-incident
description: Use when an incident is open and other teams keep shipping. Declares a change freeze scoped to the affected surface, with an exception path, so unrelated deploys do not muddy the signal.
---

# Freeze Changes During an Incident

When a system is failing, a well-meaning deploy from another team changes the variables mid-investigation and can turn a contained incident into a wider one. A scoped freeze keeps the diagnostic signal clean without halting the whole company.

## Procedure

1. Scope the freeze to the affected surface, not everything: freeze deploys to the failing service and its direct dependencies, not to an unrelated docs site.
2. Announce it with the exact scope and who can lift it: "Change freeze on checkout and payments-api until further notice; IC lifts it."
3. Carve an explicit exception path: security fixes and the IC's own mitigation deploys are always allowed; everything else goes through the IC.
4. Enforce mechanically where possible — flip the CD pipeline's gate or the deploy-freeze window, do not rely on people reading the channel.
5. Record the freeze start time and scope in the decision log; if a change does land, note who approved it and why.
6. When impact is contained, lift the freeze explicitly and announce it; a freeze left on silently blocks other teams' releases and breeds workarounds.
7. A prod rollback or mitigation is NOT a change for freeze purposes — approve it. The freeze protects the investigation, it does not stop the fix.
8. Notify teams whose releases will be blocked, by name, so they can plan around it instead of discovering the gate.
9. Set a review point (e.g. at the next cadence tick) to re-confirm or lift, so the freeze cannot live past the incident.

## Pitfalls

- Freezing everything org-wide "to be safe", blocking unrelated releases and creating pressure to bypass.
- An unannounced freeze that another team unknowingly violates, wasting the investigation.
- Forgetting to lift the freeze after the incident, so it persists and is overridden without notice.
- Blocking the mitigation rollback itself because "changes are frozen" — the freeze protects the fix, it does not forbid it.
- Relying on an honour-system freeze with no pipeline gate, so a well-meaning hotfix slips through.
- Leaving the freeze scoped to a service name that is actually a dependency, so the real surface stays open.

## Verification

```
    grep -E 'freeze (on|lifted)' incident/SEV*-2026-*.md
    # passes when a scoped freeze has both an open announcement and a matching lift
```

Related: `close-an-incident-and-resume-normal` owns the explicit lift so the freeze never outlives the incident.
