---
name: clock-skew
domain: software-engineering/clock-skew
trigger: "Reasoning about timestamps produced by different machines."
anti_trigger: "Not for which clock to read (that is monotonic-versus-wall)."
scope: "How far machines disagree, and reasoning safely across their timestamps."
status: seedling
---

# Clock skew

## Standard

Two machines tell two different times. The disagreement, skew, is not a defect — synchronisation is approximate, correction is periodic, and a datacentre's worth of hosts will disagree by milliseconds at best and by seconds on any host whose synchronisation quietly failed. Cross-machine reasoning must therefore treat every remote timestamp as a value with error bars.

The practical rule is to compare within tolerance where precision matters and to prefer sequence over time where it matters more. Ordering events by comparing wall timestamps across hosts will misorder anything closer than the skew; a sequence number, a logical clock, or a single authority's timestamp is the honest substitute. Where tolerance comparison is unavoidable — reconciling logs from two hosts — the tolerance must be measured, not assumed, because the true skew is almost always larger than the team's guess.

## Decision rules

- Never order events across hosts by wall timestamp when the gap can be within the skew.
- Measure the deployment's actual skew window before relying on cross-host comparison.
- Prefer a sequence number or single source for ordering; use timestamps only as a fallback.
- When reconciling logs across hosts, widen the search window by the measured skew.
- Treat a host whose clock drifts beyond tolerance as a fault to fix, not an input to work around.
- Record the measured skew and refresh it, since hosts and synchronisation change.

## Procedure

1. Inventory the hosts whose timestamps will be compared.
2. Measure the current disagreement window between them.
3. Record the skew as the tolerance for comparisons.
4. Where ordering matters, add a sequence or single-source timestamp.
5. Widen any cross-host log analysis by the measured tolerance.
6. Alert on hosts that drift beyond the tolerance.

## Anti-patterns

- Ordering events across hosts by timestamp and trusting sub-second differences.
- Assuming synchronisation means identical clocks.
- A fixed tolerance pulled from nowhere, smaller than the real skew.
- Working around a drifting host for months rather than fixing it.
- Comparing timestamps from zones that were never normalised to UTC.

## Done checklist

- [ ] Hosts in comparison inventoried.
- [ ] Skew measured, not guessed.
- [ ] Tolerance recorded and used.
- [ ] Ordering uses sequence where it matters.
- [ ] Log analysis windows widened.
- [ ] Drift alerting in place.

## Sources

- NTP and its precision: <https://www.rfc-editor.org/rfc/rfc5905>
- Timestamp format with timezone: <https://www.rfc-editor.org/rfc/rfc3339>
- Distributed systems time and ordering: <https://www.distributed-systems.net/>
