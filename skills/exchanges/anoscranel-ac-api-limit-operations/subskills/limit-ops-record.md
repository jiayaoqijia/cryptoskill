---
name: limit-ops-record
domain: software-engineering/limit-ops-record
trigger: "Keeping the operational record of budgets, rejections, and degradations."
anti_trigger: "Not for per-request ledgers, and not for incident postmortems in general."
scope: "The written record: budget, rejections, degradations, and reconciliation."
status: seedling
---

# Limit ops record

## Standard

The limit-ops record is the system's account of its life under the provider's contract: the archived limit pages with their dates, the budget configuration and every change to it, the rejection and throttling events with their triggers, each degradation activation with its rung and duration, the key-pool operations, and the reconciliation results. It is the difference between a system that merely survived its limits and one whose operation is legible to the next operator.

Its discipline is completeness in the ordinary, not only in the incident. A month with zero rejections and zero degradations is a finding — the contract's margin has held and the design's headroom is real — and the record that can show a quiet month can also show when the margin closed, before the quiet month becomes a loud one. The record pairs with the provider's own re-read cadence: when the contract changes, the record holds both the old and new numbers and the dates between which each was true.

Primary sources: <https://docs.anthropic.com/en/api/rate-limits> and <https://osf.io/prereg/>.

## Decision rules

- Archive every limit-page read with its date, and supersede visibly when the contract changes.
- Log budget configuration changes with time, change, and reason.
- Log every 429, throttle, and queue-exhaustion event with its trigger and duration.
- Log every degradation activation with rung, trigger, and customer-visible behaviour.
- Log key-pool operations: additions, rotations, revocations, with entitlement references.
- Attach each reconciliation result with its deltas and explanations.

## Procedure

1. Record the limit-page archive and the re-read cadence on day one.
2. Wire the budgeting, degradation, and metering layers to emit to the record automatically.
3. Review the record at the same cadence as the reconciliation.
4. On contract change, record old and new numbers with their validity ranges.
5. On any incident, extract the timeline from the record rather than from memory.
6. Summarise each month: rejection count, degradation count, margin trend.

## Anti-patterns

- A record that starts only after the first incident.
- Manual logging of events the layers can emit automatically.
- Silence on the quiet months, so the margin trend is invisible.
- Overwriting the archived limit page when the contract changes, losing the old truth.
- Two records — the operator's memory and the system's log — disagreeing.

## Done checklist

- [ ] Limit pages archived with dates and supersessions.
- [ ] Budget changes logged with reasons.
- [ ] Rejection and throttling events wired automatically.
- [ ] Degradation activations logged with rungs and triggers.
- [ ] Pool operations logged with entitlement references.
- [ ] Reconciliations attached; monthly summary written.

## Sources

- Provider rate-limit documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Handling overload, Google SRE: <https://sre.google/sre-book/handling-overload/>
