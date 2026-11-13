---
name: run-observability-record
domain: software-engineering/run-observability-record
trigger: "Writing the record of what the tracing layer captures and keeps."
anti_trigger: "Not for the traces themselves, and not for dashboards."
scope: "The written record: coverage, retention, tracing contract."
status: seedling
---

# Run observability record

## Standard

The run-observability record is the tracing layer's own document: the capture contract (what every span must carry), the sampling policy in force with its version, the retention schedule per tier, the sensitive-field redaction rule, and the dashboards' standing question list. It exists so the observability layer is itself auditable — when a debugging question cannot be answered from traces, the record shows whether the capture contract omitted the field or the sampling policy dropped the run.

Its second purpose is drift detection. Tracing policies decay silently: a new tool added without instrumentation, a retention window shortened to save storage, a redaction rule broadened past its stated purpose. The record carries dated changes with reasons, and a periodic check compares the live capture against the written contract — a mismatch is a defect in one of them.

Primary sources: <https://opentelemetry.io/docs/specs/semconv/gen-ai/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the span capture contract: required fields per span type.
- The sampling policy is stated with its fraction, rationale, and version.
- Retention is stated per tier: full traces, outlines, totals — with periods.
- The sensitive-field redaction rule is stated with its named fields.
- The dashboard question list lives here; panels are added and pruned against it.
- Changes are dated amendments; the contract is periodically reconciled against live captures.

## Procedure

1. Write the span contract: per type, the required fields.
2. Attach the sampling policy version in force.
3. State retention per tier with the reason for each period.
4. Record the redaction rule and its field list.
5. Record the dashboard questions; prune and add against them.
6. Reconcile contract against a live capture sample quarterly; date each check.

## Anti-patterns

- A tracing layer whose capture rules live only in code.
- Retention changed silently to meet a storage quota.
- Redaction broadened without a recorded reason.
- The dashboard list absent, so panels are judged only by aesthetics.
- No periodic contract-versus-capture reconciliation.

## Done checklist

- [ ] Span contract written per type.
- [ ] Sampling policy versioned.
- [ ] Retention per tier with reasons.
- [ ] Redaction rule and field list recorded.
- [ ] Dashboard questions maintained.
- [ ] Quarterly reconciliation run and dated.

The record's final test is succession: a new operator reading it alone should understand what is captured, why, for how long, and under what redaction — without reading the tracing code. When the record makes the tracing layer legible on its own, it has earned its place beside the traces it governs.

## Sources

- GenAI conventions: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Stated-policy practice: <https://osf.io/prereg/>
- Tracing practice: <https://langfuse.com/docs>
