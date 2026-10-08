---
name: define-done-for-a-feature
description: Use when "done" is ambiguous and work keeps reopening. Writes the closing checklist — behaviour, tests, docs, telemetry, cleanup — a feature must satisfy to be called finished.
---

# Define done for a feature

Undefined "done" turns every feature into a permanent branch. This skill fixes the shared checklist that marks a feature finished, so reopening has a bar to clear.

## Procedure

1. Write `done.md` with a checklist; each item is a yes/no observation, not a judgement.
2. Behaviour: every acceptance criterion in `AC.md` passes and is mapped to a test (cross-check `trace.md`).
3. Tests: the new tests run in CI on a clean checkout, and they fail when the change is reverted (a test that passes without the change proves nothing).
4. Docs: the user-facing doc or changelog entry exists and is linked from the pull request; runbooks updated if operations changed.
5. Telemetry: the events from `events.md` fire in staging and are visible on a dashboard.
6. Cleanup: feature flags have a removal date, debug logging is off, and dead code and temp files are deleted.
7. Deployability: the change can be rolled back without a data migration, or the migration is reversible and tested.
8. Sign-off: name the reviewer and the date; "done" is claimed by a person, not inferred from green CI.
9. Run the checklist at the end of the work and attach the evidence for each ticked box.
10. Add an item for the changelog or release note a stranger would need to understand the change.
11. Include a line for any follow-up ticket the work created, with a link, so loose ends are named not lost.

12. Keep the checklist in the repository and link it from the pull request template, so it is not remembered.

## Pitfalls

- Calling it done when CI is green but no criterion-to-test mapping exists.
- Treating docs and telemetry as optional polish that "we'll do next sprint" forever.
- A checklist so long nobody reads it; keep it to the items that have actually been missed before.
- Marking done without the negative-path test from the acceptance criteria.
- Skipping the rollback check because the migration "looked fine" in staging.
- Reopening scope under the label of a bug because done was never defined.
- A checklist that exists but is never attached to the pull request where it is checked.

- Declaring done verbally in a standup, leaving no artefact a later reader can check.

## Verification

    grep -cE '^\s*-\s*\[[ x]\]' done.md; grep -c '\[x\]' done.md

Report unchecked items and any ticked item without attached evidence (test run, screenshot, link).
