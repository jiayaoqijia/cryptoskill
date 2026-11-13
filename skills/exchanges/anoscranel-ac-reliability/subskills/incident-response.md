---
name: incident-response
domain: software-engineering/incident-response
trigger: "\"prod is down\", \"we have an outage\", \"run the incident\", \"write the postmortem\", \"who declares SEV1\"."
anti_trigger: "Defining the SLO or alert thresholds (subskills/slo-reliability.md); adding telemetry (subskills/observability.md); rollback and release mechanics; user-facing prose beyond status updates."
scope: "Running an active outage and its blameless postmortem"
status: "seedling"
---

# Incident Response

## Standard

- **Roles**: an incident commander holds decision authority, a comms lead speaks outward, a scribe keeps the record. The roles are activities, not job titles.
- **Blameless postmortem**: introduced by John Allspaw at Etsy and adopted by Google SRE; focus on system conditions, not on whose fault it was (https://sre.google/workbook/postmortem-culture/).
- **Action items** are typed Investigate, Mitigate, Repair, Detect, Prevent, and each needs a named owner.
- **Status communication** is a three-act shape: acknowledge, update hourly while live, then resolve with a postmortem.
- **Severity ladder**: SEV1 pages now, SEV2 major, SEV3 minor, SEV4 cosmetic. ⚠️ Numbering varies by org; write your own mapping.

## Decision rules

1. Severity selects the response path. If two tiers trigger the same action, merge them.
2. Set timeboxes you can hold. An SLA you cannot meet is a lie that erodes trust.
3. When in doubt, roll back before debugging forward. A revert is reversible; a pressured fix is not.
4. One incident, one commander, even when the team is one person.
5. External status claims are **human-gated**. The agent drafts boilerplate; a human owns every claim about what broke.
6. Every user-visible event gets at least one P0 or P1 action item.
7. A postmortem closes within three to five business days.

## Procedure

1. Acknowledge within five minutes.
2. Confirm it is real: check the external uptime probe and recent deploys, not one datapoint.
3. Declare the severity and name the incident commander out loud.
4. Open an incident log with timestamps, before the first fix.
5. Post the first status update: acknowledged, known impact, next update time.
6. Check the four recent causes: last deploy, config change, expired certificate, dependency outage.
7. Mitigate first: flag off, roll back, or shed load. Debug after the bleeding stops.
8. Update the status page hourly while impact is live.
9. Keep the timeline in order, with times.
10. Write the postmortem within five business days:
    ```markdown
    Impact: <who, how long, what they saw>
    Timeline: <times, events, decisions>
    Root cause + contributing factors:
    What went well / what went badly:
    Action items (owner, due date, type):
    ```
11. Give every action item an owner and a tracked home.
12. Publish internally. External publication is **human-gated**.

## Anti-patterns

- No timeline, so the postmortem is written from memory.
- A commander who is also the only responder, with no record.
- Status updates that promise an ETA nobody can keep.
- Action items with no owner and no due date.
- A postmortem that names a person instead of a condition.
- Blaming a human while the failed control is unexamined.

## Done checklist

- [ ] Severity declared and the commander named.
- [ ] Timeline kept during the incident, not after.
- [ ] Status updated hourly while live.
- [ ] Root cause plus contributing factors recorded.
- [ ] Action items typed, owned and dated.
- [ ] Human approved any external claim.

## Sources

- <https://sre.google>
- <https://serverinspector.com/blog/incident-response-playbook-for-small-teams>
- <https://rootly.com/incident-response/support-levels>
- https://sre.google/workbook/postmortem-culture/
