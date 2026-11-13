---
name: leak-versus-limit
domain: software-engineering/leak-versus-limit
trigger: "Deciding whether exhaustion is a leak, saturation, or a mis-set limit."
anti_trigger: "Not for the per-resource diagnosis details (the sibling leaves)."
scope: "The three causes of exhaustion and the evidence that separates them."
status: seedling
---

# Leak versus limit

## Standard

Every resource exhaustion has one of three causes, and the fixes do not substitute for each other. A leak: the resource is acquired and never returned, so usage rises without regard to load. Saturation: the resource is legitimately at its limit for the load being carried. A mis-set limit: the workload's true need exceeds a number chosen by default or habit years ago. Raising a limit cures the third, postpones the first, and misreads the second entirely.

The differential evidence is the shape of the usage curve under varying load. A leak is load-independent in the long run — it climbs even at night. Saturation tracks load and returns to baseline when load falls. A mis-set limit shows usage crowding against a ceiling with no pathological curve — the ceiling is simply wrong. Two hours of samples usually separate all three without reading a line of code.

## Decision rules

- Sample the resource's usage curve across at least one low-load and one high-load period.
- Classify the curve as leak (monotone rise), saturation (tracks load), or ceiling contact.
- Record the limit's current value and the evidence for whoever set it there.
- Check the restart test: if a restart resets the curve to a lower baseline, leak is likely.
- Never change a limit before the curve is classified — it can destroy the diagnostic evidence.
- State the verdict in the record: cause, evidence, and the fix that matches the cause.

## Procedure

1. Identify the resource and its measurement command.
2. Sample usage over a period spanning both load levels.
3. Classify the curve using the load-band comparison.
4. Trace the limit's current value and its origin.
5. On leak verdicts, hand off to leak-finding with the sampling evidence attached.
6. Record cause, evidence, and the matched fix.

## Anti-patterns

- Treating every exhaustion as "we need more of it".
- Changing the limit first and classifying later.
- Sampling only during the incident, when load is at its peak.
- Reading a nighttime plateau as health when the day shows climbing floors.
- Ignoring who set the limit and why; the original reason may no longer hold.

## Done checklist

- [ ] Resource and measurement established.
- [ ] Curve sampled across load bands.
- [ ] Curve classified.
- [ ] Limit value and origin recorded.
- [ ] Restart test noted where available.
- [ ] Verdict matched to the fix.

## Sources

- Linux resource limits and their history: <https://www.kernel.org/doc/html/latest/admin-guide/>
- Capacity versus reliability thinking: <https://learn.microsoft.com/en-us/azure/well-architected/>
- Observability for resource trends: <https://sre.google/sre-book/monitoring-distributed-systems/>
