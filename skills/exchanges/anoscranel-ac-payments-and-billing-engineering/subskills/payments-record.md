---
name: payments-record
domain: software-engineering/payments-record
trigger: "Writing the record of payment-system behaviour over time."
anti_trigger: "Not for the transaction log itself, and not for processor selection."
scope: "The written payments record: state rules, boundary, metrics, and incident history."
status: seedling
---

# Payments record

## Standard

The payments record is the design document of the money system: the state machines and their transition rules, the idempotency key policy, the dunning schedules, the ledger account taxonomy, the PCI boundary decision, and the represent-or-accept rules. It is written before the system runs, dated, and amended only by explicit, dated revisions; it says not only what was built but what the builders decided about the operations' meanings — which declines are retried, which evidence classes are always represented, which corrections are allowed and never otherwise.

Its value is continuity across incidents and staff. A dispute arriving three years after launch lands in an environment where the collectors of evidence may no longer be present; the record tells the responder what the evidence package was designed to contain and where each part lives. The reconciliation report is the record's pulse: a standing schedule of comparisons between the ledger and the processor's view, with every mismatch filed and its resolution written. A quiet reconciliation week is itself recorded — because a system that stops reporting may have stopped running, and the record is how that is noticed after everyone assumed otherwise.

Primary sources: <https://docs.stripe.com/billing/subscriptions/overview> and <https://www.pcisecuritystandards.org/document_library/>.

## Decision rules

- The record contains the state machines, key policies, dunning schedules, ledger taxonomy, PCI boundary, and dispute rules; each with its author, date, and rationale.
- Amendments are dated, versioned, and referenced from the sections they change; nothing is silently rewritten.
- The reconciliation schedule and its recent results are recorded, including the quiet weeks.
- Incident entries carry the state the payment was in, the events that preceded it, the applied transition, and the outcome.
- Metrics that appear to stakeholders — duplicate-charge rate, dunning recovery rate, dispute win rate by evidence class — are defined in the record with their exact computation.
- The record names, for each external integration, which processor behaviours were assumed and when that assumption was last verified against current documentation.

## Procedure

1. Write the record at design time from the leaves: state machines, policies, schedules, taxonomy, boundary, dispute rules.
2. Version it; date every amendment; reference it in code review templates for money-touching changes.
3. Record each reconciliation run's outcome, including silent ones.
4. For each incident, record state, timeline, response, and the follow-up it created.
5. State each published metric's computation in the record and update both together, never one alone.
6. Annually, or on processor change, re-verify the recorded assumptions against current documentation.

## Anti-patterns

- A payments doc that describes the happy path and leaves the schedules and rules as folklore.
- Amendments without dates; a reader cannot tell which rule was in force when the incident occurred.
- Reconciliation outcomes only recorded when they find something; silence passes unremarked and an evaporated job is invisible.
- Metrics whose formulas live in a dashboard rather than the record; the number drifts from its own historic values.
- Assumptions about processor behaviour carried for years without re-verification.

## Done checklist

- [ ] Sections from every leaf, with authors and dates.
- [ ] Versioned amendments with references.
- [ ] Reconciliation runs recorded, including quiet ones.
- [ ] Incidents recorded with state and response.
- [ ] Metric definitions recorded with formulas.
- [ ] Assumptions re-verified annually and on processor change.

## Sources

- Billing subscription lifecycle: <https://docs.stripe.com/billing/subscriptions/overview>
- PCI standards library: <https://www.pcisecuritystandards.org/document_library/>
- Disputes documentation: <https://stripe.com/docs/disputes>
