---
name: scope-and-boundaries
domain: software-engineering/moderation-scope
trigger: "Deciding what the moderation system covers and where adjacent surfaces begin."
anti_trigger: "Not for security telemetry detection, and not for model evaluation."
scope: "What the system covers, adjacent surfaces, and regime changes."
status: seedling
---

# Scope and boundaries

## Standard

A moderation system covers user-generated content against the platform's rules. Around it sit surfaces that look similar and are owned elsewhere: endpoint abuse and bot traffic are security engineering; security alerts from telemetry are security operations; and judging machine-generated outputs against a quality bar is model evaluation, not content moderation, even when a human reviews the output. Boundary confusion shows up as teams shipping the wrong tool for a problem.

The second boundary is regulatory regime. Moderation rules are increasingly law-shaped: platform regulation may require notice-and-action flows, transparency reporting, and appeal rights with defined service levels. These obligations are inputs to the system like the policy hierarchy is — versioned, cited to their source, and wired into the workflows they mandate — and a regime change is a moderation-record event with a migration plan, not a surprise discovered at audit time.

Primary sources: <https://en.wikipedia.org/wiki/Digital_Services_Act> and <https://en.wikipedia.org/wiki/Content_moderation>.

## Decision rules

- Record the content types and surfaces the system covers explicitly.
- Rate limiting, credential stuffing, and bot defence route to security engineering.
- Security alert triage routes to security operations, not the moderation queue.
- Model-output quality judgement routes to evaluation tooling, not moderation.
- Regulatory obligations are versioned inputs, each cited to its source.
- Regime changes get a migration plan and a dated record entry.

## Procedure

1. Enumerate the content surfaces the platform hosts.
2. For each, record whether moderation, security, or evaluation owns it.
3. List applicable regulatory regimes and their citation sources.
4. Map each obligation to the workflow that satisfies it.
5. Define the regime-change intake: who notices, who plans, who records.
6. Publish the boundary map alongside the policy hierarchy.

## Anti-patterns

- Routing bot abuse into content moderation queues.
- Moderating machine-generated output under content rules meant for users.
- Treating regulation as a legal memo rather than versioned system input.
- Regime changes handled as one-off heroics with no record.
- Boundary decisions made per-incident by whoever is on call.

## Done checklist

- [ ] Content surfaces enumerated with owners.
- [ ] Adjacent-surface routing table written.
- [ ] Regulatory obligations versioned with citations.
- [ ] Obligation-to-workflow map complete.
- [ ] Regime-change intake defined.
- [ ] Boundary map published.

The boundary map earns its keep during incidents: when a new abuse pattern appears, the on-call needs to know in one glance whether it is a moderation case, a security case, or an evaluation case, because the routing decision made in the first minutes decides which team's tooling and evidence apply.

## Sources

- Regulatory context: <https://en.wikipedia.org/wiki/Digital_Services_Act>
- Content moderation overview: <https://en.wikipedia.org/wiki/Content_moderation>
- Platform transparency reporting: <https://transparency.meta.com/>
