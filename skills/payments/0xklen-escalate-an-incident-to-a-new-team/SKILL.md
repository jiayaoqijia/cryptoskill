---
name: escalate-an-incident-to-a-new-team
description: Use when an incident outgrows the current responders and must be handed to another team. Packages a self-contained brief so the new team starts working in the first minute instead of re-asking.
---

# Escalate an Incident to a New Team

Escalation fails when the new team is paged with "we have a problem, join the bridge" and spends twenty minutes rebuilding context. A self-contained brief gets them acting on the first minute.

## Procedure

1. Page with the incident id, severity, and a one-line impact — never "URGENT come to the bridge".
2. Hand over a compact brief a stranger can act on:

       Need: platform team. Symptom: DB writes timing out, 30% of requests.
       Tried: pool resize (helped 10%), rollback of 4.18 (no effect).
       Ruled out: query plans, disk IOPS. Suspect: storage volume IOPS cap.
       Evidence: /tmp/SEV2-iostat.txt, decision log above.

3. State explicitly what you want from them: "own the storage-layer investigation" — not "help out".
4. Transfer role ownership in writing: does the new team take IC, or only the storage thread? Ambiguous ownership duplicates work.
5. Keep the escalation contacts list current so you page the right rotation, not a personal phone number.
6. When the new team owns a thread, step back from it; the original IC coordinates and does not shadow-debug.
7. Give the new team the same comms cadence and channel so they do not re-derive state from logs.
8. Confirm receipt: the new owner restates the ask before you consider the escalation done.

## Pitfalls

- Escalating without the "tried and ruled out" list, so the new team repeats two hours of work.
- Paging an individual rather than the rotation, so escalation fails when that person is asleep.
- Two ICs after escalation because ownership was never explicitly transferred.
- Leaving the new team out of the comms cadence, so they re-derive state from logs.
- Dumping the whole investigation narrative instead of the four-field brief, which takes longer to read than to reconstruct.
- Escalating too late, after a fix has already been attempted that the new owner must now undo.

## Verification

```
    grep -E 'Need:|Tried:|Ruled out:|Suspect:' incident/SEV*-2026-*.md
    # passes when the escalation brief contains all four fields and names the requested owner
```

Related: `page-the-correct-on-call-rotation` carries the brief to the right rotation without naming a person.
