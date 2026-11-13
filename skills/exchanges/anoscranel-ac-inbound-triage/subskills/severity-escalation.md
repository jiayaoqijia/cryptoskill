---
name: severity-escalation
domain: collaboration/severity-escalation
trigger: "Assigning a severity to an incident or a request; deciding when to page; deciding who to escalate to"
anti_trigger: "Running an active incident or the incident command itself; triaging the order of ordinary non-incident items"
scope: "Severity classes and escalation: matrices for incidents and requests, the paging threshold, a ladder of named people"
status: "seedling"
---

# Severity Escalation

## Standard

- **Google, _Site Reliability Engineering_ (2016), "Managing Incidents"**: one person owns the response — the incident commander holds the high-level state and every role they have not delegated; when load grows, the role-leader adds staff rather than dropping the role. <https://sre.google/sre-book/managing-incidents/>
- **PagerDuty, "Understanding Severity Levels"**: a small fixed set of levels, each with a definition of impact and a response time, keeps the word "urgent" from meaning everything; severity is set by impact, not by loudness. <https://response.pagerduty.com/before/severity_levels/>

## Decision rules

1. If an incident affects users or revenue, it is a higher severity than one that does not, regardless of who reported it.
2. If a request has a real external deadline, its severity rises; if the deadline is only stated, it does not.
3. If the paging threshold is met, page; if it is not, do not. The threshold is the rule, not a feeling.
4. If escalation adds people, ownership stays with the same person; help arrives, responsibility does not move.
5. If severity is raised without a change in impact, the raise is wrong; record who raised it and why.

## Procedure

1. Define a severity scale for incidents: for each level, the impact and the target response time.
2. Define the same for requests: what makes a request high versus low severity, and the deadline that each implies.
3. Name the paging threshold: the lowest level that pages someone out of hours.
4. State who may raise severity: the reporter, the owner, and the escalation contact, but not anyone at will.
5. Write the escalation ladder with names, not roles: "call Alex, then Priya, then the on-call manager".
6. On escalation, send the new person the item, the severity, and what is already done; keep the original owner.
7. Review every raise weekly: did impact change, or did pressure change?

## Anti-patterns

- **Severity by volume.** The person who shouts loudest gets the highest severity. Fix: score impact, not noise.
- **No paging threshold.** Every item is a judgment call, and every off-hours call feels optional. Fix: name the level that pages.
- **Escalation as abdication.** The owner hands the whole problem up and walks away. Fix: escalation adds help, keeps the owner.
- **Roles instead of names.** "Escalate to the manager" is a dead end at 2 a.m. Fix: write actual names and numbers.
- **Severity raised to skip the queue.** A request is relabeled urgent to jump ahead. Fix: raises require a stated impact change.

## Done checklist

- [ ] A severity scale exists for incidents and for requests, with impact and response time per level.
- [ ] The paging threshold is named.
- [ ] Who may raise severity is stated.
- [ ] The escalation ladder lists names, not roles.
- [ ] Escalation keeps the original owner.
- [ ] Severity raises are reviewed weekly for impact versus pressure.

## Sources

- Google, _Site Reliability Engineering_ (2016), "Managing Incidents": <https://sre.google/sre-book/managing-incidents/>
- PagerDuty, "Understanding Severity Levels": <https://response.pagerduty.com/before/severity_levels/>