---
name: the-event-plan
domain: software-engineering/the-event-plan
trigger: "Writing the living document that maps every event and its owner."
anti_trigger: "Not for the taxonomy schema rules, and not for reading the data."
scope: "The living document that maps every event and its owner."
status: seedling
---

# The event plan

## Standard

The plan is the taxonomy written for humans: one row per event — name, owner, question answered, properties, platforms shipped, date added, proposal link — plus the name and rationale of the audit-enum lists. It is a living document with a review cadence, and its test is the same as any interface's: an engineer who has never seen it should be able to answer "does this event exist" and "who owns it" in one lookup.

The plan succeeds when the review is boring: the quarterly pass finds little to merge or retire because proposals were reviewed at intake. It fails when nobody adds events for a quarter because the review was hostile or absent, and the largest telemetry gaps turn out to be the questions that died at proposal time.

Primary sources: <https://en.wikipedia.org/wiki/Customer_data_platform> and <https://developer.mozilla.org/en-US/docs/Web/API/Beacon_API>.

## Decision rules

- One row per event, with owner and date; never versioning by deletion.
- Proposals reference their plan row so the plan and code change together.
- A status field per event (active | pending | deprecated) visible in the plan.
- A review cadence stated at adoption; reviews merge, retire, and assign.
- Each new question asked in the review meeting is written into the question backlog section.
- The plan references the property-enum documents rather than duplicating them.

## Procedure

1. Create the plan with one row per taxonomy event.
2. Pull in the conventions: naming, envelope properties, delivery classes.
3. Adopt the proposal form with its response-time expectation.
4. Set the quarterly review cadence and name the owner of the plan itself.
5. Record the emerging question backlog in its section so it is not lost.
6. The plan changes through proposals; no edits bypass review.

## Anti-patterns

- A plan file that was accurate at launch and never again.
- Deleting rows for retired events instead of marking status.
- Proposals resolving without the plan row being updated.
- No question backlog in the plan — questions raised at review are simply lost.
- The plan living in a person's head or personal doc.

## Done checklist

- [ ] Plan created with one row per event.
- [ ] Conventions documented beside rows.
- [ ] Proposal form adopted with response time.
- [ ] Review cadence and plan owner set.
- [ ] Question backlog section living.
- [ ] Status changes through review only.

## Sources

- The event aggregation layer these plans feed: <https://en.wikipedia.org/wiki/Customer_data_platform>
- Delivery quality classes: <https://developer.mozilla.org/en-US/docs/Web/API/Beacon_API>
- Event stream background: <https://en.wikipedia.org/wiki/Clickstream>
