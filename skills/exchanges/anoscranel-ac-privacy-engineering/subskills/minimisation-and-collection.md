---
name: minimisation-and-collection
domain: software-engineering/minimisation-and-collection
trigger: "Deciding whether a field should be collected at all."
anti_trigger: "Not for legal basis determination, and not for analytics design."
scope: "Collection as a cost, and the fields that should not exist."
status: seedling
---

# Minimisation and collection

## Standard

Every field collected is a field that must be stored, secured, retained, deleted, disclosed on request, and defended if breached. That is a permanent liability taken on for a temporary convenience, and the honest way to evaluate a collection decision is to ask who will own the field's lifecycle in two years.

Minimisation is the discipline of declining that liability. A form that asks for a date of birth to verify age can store a boolean instead; a service that logs a full request body for debugging can mask the fields it does not need; an analytics event that carries an email address can carry a hashed identifier. Each substitution removes a liability rather than managing it.

Primary sources: <https://ico.org.uk/> and <https://www.nist.gov/privacy-framework>.

## Decision rules

- Record the purpose each field serves and the alternative that would serve it with less data.
- Record fields that can be reduced to a boolean, a range, or a hash.
- Record the fields masked in logs and the masking rule.
- Record the retention consequence of collecting the field.
- Record new collection requests that were declined, since the register of declined requests is the evidence minimisation is operating.
- Record the review point at which a field's purpose is re-examined.

## Procedure

1. For each proposed field, state the purpose and the least-data alternative.
2. Record the alternative considered and why it was rejected, if it was.
3. Apply masking to any field entering logs.
4. Record the retention consequence.
5. Log declined collection requests.
6. Review existing fields against their original purpose.

## Anti-patterns

- Collecting a field because it is available rather than because it is needed.
- Logging full request bodies for debugging convenience.
- Storing a precise value where a range would answer the question.
- Never revisiting fields whose original purpose has lapsed.
- Treating minimisation as a legal constraint rather than an engineering one.

## Done checklist

- [ ] Purpose recorded per field.
- [ ] Least-data alternative recorded.
- [ ] Log masking applied and recorded.
- [ ] Retention consequence recorded.
- [ ] Declined requests logged.
- [ ] Review of existing fields scheduled.

The register of declined collection requests has a political function as well as an engineering one: it demonstrates that minimisation is a practice rather than a slogan, and it gives the next person who asks for a field a precedent to argue against. Without it, each request is evaluated from scratch and the default drifts toward collecting.


## Sources

- Data minimisation guidance: <https://ico.org.uk/>
- NIST privacy framework: <https://www.nist.gov/privacy-framework>
- Web privacy and tracking standards: <https://www.w3.org/Privacy/>
