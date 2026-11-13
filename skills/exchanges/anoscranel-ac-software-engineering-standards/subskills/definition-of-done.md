---
name: definition-of-done
domain: software-engineering/definition-of-done
trigger: "\"definition of done for\", \"what does good look like\", \"when is this change done\", \"set the done criteria\"."
anti_trigger: "Doing the activity itself, or building its detailed checklists. This leaf states the finish line, not the race."
scope: "Done criteria per lifecycle activity: what must be true before the activity counts as complete"
status: "seedling"
---

# Definition of Done

## Standard

One line per activity: the conditions under which that activity counts as done. The conditions are generic; each project's craft work decides how to meet them.

- **Specify**: every requirement is testable as written; acceptance criteria exist; each non-functional requirement carries a number and a check method.
- **Plan**: every task is independently deliverable; estimates carry their risk list; a human picked build versus buy.
- **Design**: the structure and its trade-offs are recorded; the external contract is drafted; significant decisions exist as written records.
- **Build**: the change is one self-contained unit; it compiles and its tests pass; in-repo documentation that ships with the code is current.
- **Test**: the portfolio covers the stated risks; every fix carries a test that failed before and passes after; the suite is green.
- **Review**: the diff is small enough to judge in one sitting; every comment is labelled; merge to protected main is human-gated.
- **Ship**: pipeline gates pass; rollback is a working command, not a hope; evidence is produced per build, never assembled at audit time.
- **Operate**: telemetry answers who is affected and since when; reliability targets and alerts exist as records; outages close with owned, dated action items.
- **Retire**: dependents were notified on a dated schedule; telemetry shows removal is safe; a human approved the removal.

## Decision rules

Use the line matching the lifecycle activity in question. Every clause of that line must be true before the activity counts as done; the line states the finish line, never the method (each project's craft work decides how to meet it).

Any compliance, authorship, conformance or publication claim goes through a human. The agent drafts; a human attests.

## Procedure

1. Name the activity. 2. Read its line. 3. Check each clause against the artifact. 4. Report gaps as the remaining work, nothing more.

## Anti-patterns

- Expanding a line into a how-to checklist within this leaf.
- Treating a partially-met line as done.

## Done checklist

- [ ] The activity's line was read in full and each clause answered true or false.
- [ ] A human reviewed any compliance, authorship, conformance or publication claim.

## Sources

- Built from the corpus definition-of-done conventions for the software lifecycle (SWEBOK v4 topic map, <https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics>).
