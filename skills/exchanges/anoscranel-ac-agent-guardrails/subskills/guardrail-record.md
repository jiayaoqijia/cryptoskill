---
name: guardrail-record
domain: software-engineering/guardrail-record
trigger: "Writing the record that proves the guardrail layer exists and works."
anti_trigger: "Not for SIEM design, and not for compliance mapping."
scope: "The written record: gates, checks, firings, and their reviews."
status: seedling
---

# Guardrail record

## Standard

The guardrail record documents the whole layer in one place: the current action-class table with its rationale, the interception-point map, the per-destination screen sets with threshold derivations, the interrupt-path test results with dates, the blast-radius derivations, and the incident log with classifications and fix routings. It is the artifact that answers "what is actually enforced right now?" — the question an auditor, a customer, or a 3am responder asks first.

Its second job is keeping the layer alive. The record shows the noise-syndrome and silent-death counters, review-SLA adherence, and threshold-change history with rationale, so the two failure modes that kill guardrail deployments are visible rather than felt. And because guardrails are risk-management controls by design, the record states what the layer does not cover — unclassified paths, probabilistic screens with known FP/FN, resources not capped — rather than leaving the reader to assume coverage.

Primary sources: <https://www.nist.gov/itl/ai-risk-management-framework> and <https://osf.io/prereg/>.

## Decision rules

- The record carries the live action-class table, screen sets, and derivations, not a snapshot frozen at deployment.
- Interrupt-path test results are recorded with dates and re-run after every bus or manifest change.
- Firing statistics appear per class with trend arrows, not single-day counts.
- Threshold changes are dated amendments with the reason and who decided.
- A coverage-limits section names what the layer does NOT enforce — always present, never implied.
- Silent-death and noise metrics are on the first page, not buried.

## Procedure

1. Assemble the sections from the six leaves with live references.
2. Record every interception-point invariant as an assertion — restated after every infrastructure change.
3. Pull firing statistics into the record's summary on each release cadence.
4. Maintain the threshold-change log as append-only.
5. Write and refresh the coverage-limits section each release.
6. File the record beside the agent's deployment manifest and version both together.

## Anti-patterns

- The record written at launch and never revisited as the manifest evolves.
- Test results recorded once with no re-run trigger.
- No coverage-limits section: silent over-coverage is the deadliest document lie.
- Firing counts with no per-class breakdown or trend.
- The record filed with the agent's docs team while the enforcement lives in the platform team's repo.

## Done checklist

- [ ] Live table, screens, and derivations in one place.
- [ ] Interrupt tests dated and re-run on change.
- [ ] Firing stats with per-class trends.
- [ ] Threshold-change log append-only.
- [ ] Coverage-limits section present and refreshed.
- [ ] Record versioned with the deployment manifest.

## Sources

- NIST AI RMF, documentation of controls: <https://www.nist.gov/itl/ai-risk-management-framework>
- Stated-limits discipline: <https://osf.io/prereg/>
- OWASP LLM Top 10 as control reference: <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
