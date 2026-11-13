---
name: limits-from-evidence
domain: software-engineering/limits-from-evidence
trigger: "Setting a resource limit from measured need rather than a default."
anti_trigger: "Not for diagnosing an exhaustion already under way (the sibling leaves)."
scope: "Setting ulimits, pool sizes, and quotas from measured need, not defaults."
status: seedling
---

# Limits from evidence

## Standard

Limits are decisions, but most of them were never made — they were inherited. The file descriptor cap, the pool size, the thread count: each came from a defaults file, a tutorial, or a number that was once correct for a machine nobody remembers. Setting a limit from evidence means reading the workload's actual need at peak and at rest, and writing down a number with its derivation, so the next person inherits the reason as well as the figure.

The measurement discipline matters more than the arithmetic. Peak is not the average and not the highest single sample; it is the highest sustained level the workload reaches under its worst realistic load, plus headroom for spikes the samples caught. A limit set at the observed average will break on the first real Monday; one set at a momentary spike multiplied by ten wastes resources quietly for years.

## Decision rules

- Measure the resource's usage across the peak and rest periods, not just one day.
- Use the highest sustained band, not the single maximum sample, as the need.
- State headroom explicitly as a percentage and say why that percentage.
- Record the limit, its derivation, and its date in the deployment configuration's documentation.
- Record the failure mode when the limit is exceeded — reject, queue, or kill — and confirm callers can absorb it.
- Revisit limits when the workload changes by an order of magnitude, not on a calendar.

## Procedure

1. Identify the limit to set and the measurement that reflects it.
2. Sample across the extremes of the workload's pattern.
3. Derive the sustained peak and select headroom.
4. Compute the new limit.
5. Deploy the change and verify the failure mode produced when it is hit.
6. Record the number, its derivation, and the revisit conditions.

## Anti-patterns

- Copying a limit over unchanged between services with different shapes.
- Setting limits at the observed average.
- Multiplying a momentary spike by a round safety factor and calling it capacity.
- Raising a limit with no failure mode test — callers must absorb the new behaviour.
- Inheriting a number whose justification nobody can recall.

## Done checklist

- [ ] Peak and rest samples collected.
- [ ] Sustained peak derived from the samples.
- [ ] Headroom stated with reasoning.
- [ ] Failure mode on breach tested.
- [ ] Limit, derivation, and date recorded.
- [ ] Revisit condition recorded.

## Sources

- Linux process resource limits: <https://www.kernel.org/doc/html/latest/admin-guide/>
- Container resource management: <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>
- Capacity planning from measurement: <https://sre.google/workbook/chapter-capacity-planning/>
