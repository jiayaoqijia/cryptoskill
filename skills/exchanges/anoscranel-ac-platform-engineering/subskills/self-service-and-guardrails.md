---
name: self-service-and-guardrails
domain: software-engineering/self-service-and-guardrails
trigger: "Letting teams provision infrastructure without a ticket."
anti_trigger: "Not for access control policy, and not for cost allocation."
scope: "Provisioning without tickets, and the guardrails that make it safe."
status: seedling
---

# Self-service and guardrails

## Standard

Self-service replaces an approval with a constraint. A team that requests a database through a ticket waits for a person who may be busy; a team that provisions one through a platform gets it in minutes, subject to guardrails that bound what is possible: which sizes are available, which regions, which retention, which network segments.

The design question is which decisions are safe to delegate. Delegating the choice of database engine is usually safe within a supported set; delegating the retention of personal data is not, because the consequence extends beyond the team. Guardrails should encode the decisions whose consequences cross a boundary, and leave the rest to the team, because a guardrail that constrains a local decision adds cost without protecting anyone.

Primary sources: <https://csrc.nist.gov/> and <https://sre.google/>.

## Decision rules

- Record what is provisionable and the parameters exposed to the team.
- Record each guardrail and the boundary it protects: security, cost, data retention, compliance.
- Record the approval path for requests outside the guardrails, which should be rare and specific.
- Record how a team discovers a guardrail, which should be at request time rather than after an incident.
- Record the default values and whether they are the safe ones.
- Record the reversal path: how a provisioned resource is decommissioned and its data removed.

## Procedure

1. List what teams can provision and the parameters exposed.
2. Record the guardrails and the boundary each protects.
3. Record defaults, preferring safe by default over permissive.
4. Record the exception path and its expected frequency.
5. Record how guardrails surface at request time.
6. Write the model with its deletion path.

## Anti-patterns

- Guardrails that constrain local decisions and leave cross-boundary ones open.
- Safe defaults that are documented but not applied.
- An exception path so common that it is the real path.
- No decommissioning route, so provisioned resources accumulate.
- Guardrails discovered through an audit rather than at the point of request.

## Done checklist

- [ ] Provisionable resources and parameters recorded.
- [ ] Guardrails and their boundaries recorded.
- [ ] Defaults recorded.
- [ ] Exception path recorded.
- [ ] Discovery at request time recorded.
- [ ] Decommissioning path recorded.

The guardrail's own failure mode deserves a line: a constraint that blocks a legitimate request pushes teams to the exception path, and when the exception path becomes common the guardrail is providing neither safety nor speed. Recording the exception rate is how that is detected before the exception becomes the norm.


## Sources

- Security control guidance: <https://csrc.nist.gov/>
- Reliability and platform practice: <https://sre.google/>
- Cloud governance context: <https://csrc.nist.gov/publications>
