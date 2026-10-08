---
name: document-a-fix-with-its-evidence
description: Use when a debugging session is resolved and the fix is about to ship. Writes a short ticket-level record linking symptom, evidence, cause, fix, and guard so the next reader does not relitigate it.
---

# Document a Fix with Its Evidence

A fix without its evidence gets reverted by the next person who cannot see why it was there. The record is six concrete fields, each backed by a command's output — not a narrative.

## Procedure

1. Symptom: one sentence with a measurement and a time window. "cart total returned 0 for orders after 2026-09-30 14:00 UTC."
2. Reproduction: the exact command and its exit code, from `reproduce-a-bug-before-fixing`. Paste, do not describe.
3. Evidence: the two or three artefacts that proved the cause — a stack frame, a diff, a query result, a stack sample. Link each to a file under `evidence/`.
4. Cause: the earliest controllable step from `separate-symptom-from-root-cause`, stated as code or config, with `file:line`.
5. Fix: the change, why it addresses the cause (not the symptom), and its blast radius (what else the changed code touches).
6. Guard: the regression test name, and the check that fails if the bug returns. Cite it by path, not "added a test".
7. Note what was ruled out — the dead ends — so they are not re-borne. Two lines is enough.
8. If the root cause was deferred, say so explicitly and file the follow-up; do not imply the fix is total.
9. Read the note once as a stranger: if any field needs the live context you had, it is under-written.

## Pitfalls

- Narrative prose ("we suspected a cache issue and eventually found...") instead of the six fields; nobody reads it twice.
- Omitting the evidence because "the fix speaks for itself" — the fix is exactly what a future reader will question.
- Recording the trigger but not the latent condition, so the class of bug looks solved when it is not.
- A guard described as "added tests" with no name, so nobody can confirm it still exists.
- Blaming a person or a team rather than a mechanism; it stops honest reporting.
- Writing the note after the memory faded, inventing a plausible cause the evidence does not support.

## Verification

    ls evidence/ && grep -n '^## ' docs/fixes/bug-1234.md
    # passes when every section (Symptom, Repro, Evidence, Cause, Fix, Guard) has content

    pytest -k <guard_test_name> -q
    # the named guard test exists and passes; its name appears verbatim in the note

Report to the user: the note path, the cause at file:line, and the guard test name — one line each.
