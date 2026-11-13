---
name: on-call-design
domain: software-engineering/on-call-design
trigger: "Designing a rotation that does not burn out the team."
anti_trigger: "Not for incident response tactics, and not for alert threshold tuning."
scope: "Rotation, escalation, load, and the sustainability of being paged."
status: seedling
---

# On-call design

## Standard

On-call is a load on a person, and its sustainability is a design question rather than a matter of resilience. A rotation that pages someone twice a night is a rotation that produces sleep debt, and sleep debt produces mistakes that generate more pages. The design parameters are the rotation length, the escalation path, the page volume, and the authority to act.

Page volume is the number to measure. A team that receives forty pages a week for one service is telling you the service is not yet ready for the rotation it has, and the fix is reliability work rather than a longer rotation. Recording the volume, the proportion that required action, and the proportion that resolved without it converts the discussion from a complaint into a measurement.

Primary sources: <https://sre.google/> and <https://sre.google/workbook/table-of-contents/>.

## Decision rules

- Record the rotation length, handover time, and compensation arrangement.
- Record the page volume per week and the proportion that required action.
- Record the escalation path and the response time expected at each tier.
- Record the authority the on-call has to act, including to roll back or to scale.
- Record the runbook coverage and whether the pages link to a current one.
- Record the follow-up mechanism, since every page should produce either a fix or a dismissal with a reason.

## Procedure

1. Record rotation length and handover.
2. Measure page volume over several weeks.
3. Classify pages as actionable, informational, or noise.
4. Record escalation tiers and response expectations.
5. Record the on-call's authority.
6. Write the design with the volume findings.

## Anti-patterns

- Extending the rotation instead of reducing the pages.
- Alerts that fire without a documented action.
- An on-call without authority to roll back.
- Escalation paths that are never tested.
- Pages with no runbook, which make every incident a first occurrence.

## Done checklist

- [ ] Rotation length and handover recorded.
- [ ] Page volume measured.
- [ ] Pages classified.
- [ ] Escalation tiers recorded.
- [ ] Authority recorded.
- [ ] Follow-up mechanism recorded.

The page classification is the finding, not the count: a rotation where most pages are informational is a rotation whose alerting is a notification system, and the fix is to route those to a channel rather than to a person. Recording the classification turns an unbearable week into a specific list of alerts to change.


## Sources

- On-call and alerting practice: <https://sre.google/>
- Incident management: <https://sre.google/workbook/table-of-contents/>
- Reliability guidance: <https://sre.google/sre-book/being-on-call/>
