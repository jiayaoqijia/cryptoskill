---
name: platform-record
domain: software-engineering/platform-record
trigger: "Writing the record of an internal platform and its adoption evidence."
anti_trigger: "Not for architecture documentation, and not for service runbooks."
scope: "The written record: path, catalogue, guardrails, and adoption evidence."
status: seedling
---

# Platform record

## Standard

The platform record states the golden path and its measured length, the catalogue's fields and how they are maintained, the guardrails and the boundary each protects, the toil it was built to remove, and the adoption evidence. That last item is what distinguishes a platform record from a design document: a platform is justified by use, not by capability.

Its second function is to keep the platform honest about its own cost. A platform team that publishes the toil it has removed, measured before and after, has an argument for its next investment. One that publishes only features has an argument about features, which is a different and weaker conversation.

Primary sources: <https://dora.dev/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the golden path and the measured comparison against the alternative.
- The catalogue's fields are recorded with their maintenance mechanism.
- Each guardrail is recorded with the boundary it protects.
- Toil removed is recorded with its before and after measurement.
- Adoption is recorded as a count of teams and services using the path, not as a claim.
- Review triggers are dated: path change, catalogue field change, adoption plateau, new guardrail.

## Procedure

1. Record the golden path and its measurement.
2. Record the catalogue fields and maintenance.
3. Record guardrails and their boundaries.
4. Record toil removed with before and after.
5. Record adoption as counts.
6. Set review triggers and amend at each.

## Anti-patterns

- Recording capabilities without adoption evidence.
- A toil claim with no before measurement.
- A catalogue field recorded without its maintenance mechanism.
- Guardrails listed without the boundary they protect.
- No trigger for an adoption plateau, which is the signal to change the path.

## Done checklist

- [ ] Golden path and measurement recorded.
- [ ] Catalogue fields and maintenance recorded.
- [ ] Guardrails and boundaries recorded.
- [ ] Toil reduction measured.
- [ ] Adoption counted.
- [ ] Triggers dated.

The record should also name the alternative the golden path competes with, since adoption is a comparison rather than an absolute: a platform used by eight teams because there is no alternative is not evidence that it is good, and the record reads differently when the competing path is stated.


The record should also state the platform's scope boundary, because a platform that claims everything is a platform whose failures are attributed to it whether or not it owns them: naming what the team does not run, and where the handoff is, keeps the record honest about its own responsibility.

## Sources

- Delivery performance research: <https://dora.dev/>
- Pre-registration practice for stated evidence: <https://osf.io/prereg/>
- Reliability and platform practice: <https://sre.google/>
