---
name: person-handoff
domain: collaboration/person-handoff
trigger: "Shift handover; on-call handoff; hand this to the next person; incident handover; what does the next engineer need to know"
anti_trigger: "Machine checkpoints and session state (subskills/session-handoff.md); writing the state capsule's sections (subskills/handoff-artifact.md); the acceptance test (subskills/quality-bar.md)"
scope: "Colleague, shift, and incident handoffs: shift reports, on-call transition, acknowledgment closes the loop, escalation notes"
status: "seedling"
---

# Person Handoff

## Standard

- **Google SRE Book, "Being On-Call"**: the on-call engineer logs work and communicates status at shift change; the handover carries live incidents, ongoing operations, and what is watchable. <https://sre.google/sre-book/being-on-call/>
- **Google SRE Workbook, "On-Call"**: healthy rotas treat handover as a designed step, with the incoming engineer reading the recent record before taking the pager. <https://sre.google/workbook/on-call/>
- **Starmer et al., NEJM (2014) / I-PASS**: structured elements including situation awareness with contingency planning and synthesis by receiver; roughly one quarter fewer medical errors in the study. <https://www.ipasshandoffstudy.com/>; <https://www.nejm.org/doi/full/10.1056/NEJMsa1405556> ⚠️ paywalled.
- **IHI, "SBAR Tool"**: Situation, Background, Assessment, Recommendation; the opener for a transfer under time pressure. <https://www.ihi.org/resources/tools/sbar-tool-situation-background-assessment-recommendation>

## Decision rules

1. Open with SBAR: situation first, history second; the receiver needs what is live before what happened.
2. Every live item gets a state (stable, degrading, recovering) and an observation channel where it is watched.
3. Every risk gets a trigger: "if X, do Y and page Z". A risk without a trigger is decoration.
4. Escalation notes name the who and the threshold, never "escalate if needed".
5. Rank by urgency, not chronology: act-now items before watch items.
6. The handoff is not complete until the receiver reads back and explicitly takes over; until then the sender stays reachable.

## Procedure

1. Write the SBAR opener: situation in one line, short background, assessment of the trend, recommendation of what is needed.
2. List live items: state, observation channel, owner.
3. List actions taken this shift and their effects, one line each.
4. List open risks with triggers, actions, and escalation paths: who to contact, at what threshold.
5. List known future events: maintenance windows, expected spikes, scheduled changes.
6. Hand over; the receiver reads back the live items and triggers in their own words.
7. The receiver acknowledges explicitly; the sender records the acknowledgment and the loop closes.
8. File the handoff where the team keeps shift records, so the next reader inherits the record.

## Anti-patterns

- **Monologue handover.** The sender talks, the receiver listens, nothing is checked. Fix: read-back before takeover.
- **"Nothing is happening."** No evidence, no watch list. Fix: name the watch items and their channels.
- **Chronological tour.** Everything in order, the live incident buried at minute forty. Fix: rank by urgency.
- **Untriggered risks.** "Watch the database." Fix: threshold, action, and who to page.
- **Silent takeover.** The receiver starts work without acknowledging; the sender never knows the loop closed. Fix: explicit acknowledgment, recorded.

## Done checklist

- [ ] SBAR opener present.
- [ ] Live items carry state and observation channel.
- [ ] Risks carry triggers and escalation paths.
- [ ] Future events listed.
- [ ] Read-back completed by the receiver.
- [ ] Explicit acknowledgment recorded; loop closed.
- [ ] Handoff filed in the team record.

## Sources

- Google SRE Book, "Being On-Call": <https://sre.google/sre-book/being-on-call/>
- Google SRE Workbook, "On-Call": <https://sre.google/workbook/on-call/>
- I-PASS program: <https://www.ipasshandoffstudy.com/>; Starmer et al., NEJM 2014: <https://www.nejm.org/doi/full/10.1056/NEJMsa1405556> ⚠️ paywalled.
- IHI, "SBAR Tool": <https://www.ihi.org/resources/tools/sbar-tool-situation-background-assessment-recommendation>

⚠️ The SRE guidance is public but single-organization practice; the I-PASS effect size is from one clinical study, not a software-team measurement.
