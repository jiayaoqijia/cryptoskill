---
name: metering-and-reconciliation
domain: software-engineering/metering-and-reconciliation
trigger: "Counting what was spent and reconciling against the provider's meter."
anti_trigger: "Not for cloud cost attribution in general, and not for per-prompt craft."
scope: "Counting what was spent and reconciling against the provider's meter."
status: seedling
---

# Metering and reconciliation

## Standard

Between "the system believes it spent N requests" and "the provider's meter says M" lies the reconciliation gap, and an operated system closes it on a schedule. Local metering counts every outbound request at send time — queued, rejected, and served; per caller class and per API dimension — and stores the counters durably, because a budget that resets on restart is a budget that never audited itself. The provider's usage console and billing meter are the external truth the local numbers must meet.

Discrepancies have causes worth finding: a code path that bypasses the budget, a fallback chain spending on a link whose meter is read separately, a burst the local bucket counted as one, or the provider counting dimensions the local meter does not track. Reconciliation is not an accusation exercise; it is the only way the budget, the degradation ladder, and the bill can all three be trusted at once.

Primary sources: <https://docs.anthropic.com/en/api/rate-limits> and <https://platform.openai.com/docs/guides/rate-limits>.

## Decision rules

- Count every outbound request at send time, durably, with caller class and dimension.
- Reconcile local counts against the provider's meter on a set cadence — daily or weekly.
- Investigate every discrepancy past a stated tolerance, and record the cause.
- Meter the fallback links separately; a chain that hides its tail's spending has two truths.
- Reconcile the third number too: what the bill says, which prices the meter's counts.
- Publish the reconciliation result — matched or explained — in the operational record.

## Procedure

1. Implement durable send-time counters: total, per class, per dimension, per chain link.
2. Configure the provider-meter export or console read on the reconciliation cadence.
3. Set the tolerance and the rule for investigating a breach.
4. Reconcile local, provider-meter, and bill; three-way where the bill prices separately.
5. Record each reconciliation with the deltas and their explanations.
6. Feed confirmed causes back into the budgeting and ladder design.

## Anti-patterns

- In-memory counters that reset with the process.
- Reconciliation only after an overage surprise.
- A tolerance so wide the budget drifts silently for weeks.
- Fallback spending counted in neither the primary meter nor the chain's.
- Two-way reconciliation ignoring the third number: the bill.

## Done checklist

- [ ] Durable send-time counters with class and dimension.
- [ ] Provider-meter read on the cadence.
- [ ] Tolerance stated with an investigation rule.
- [ ] Chain-link meters separate.
- [ ] Three-way reconciliation where the bill prices separately.
- [ ] Results and explanations recorded.

## Sources

- Provider rate-limit documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
- Provider rate-limit documentation, OpenAI: <https://platform.openai.com/docs/guides/rate-limits>
- Handling overload, Google SRE: <https://sre.google/sre-book/handling-overload/>
