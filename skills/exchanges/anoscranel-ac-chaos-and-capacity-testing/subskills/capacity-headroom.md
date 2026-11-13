---
name: capacity-headroom
domain: software-engineering/capacity-headroom
trigger: "Measuring how much load a system can absorb before degrading."
anti_trigger: "Not for cost optimisation, and not for purchasing decisions."
scope: "The knee, the plateau, and headroom measured rather than guessed."
status: seedling
---

# Capacity headroom

## Standard

A system's throughput rises with load until it reaches a knee, after which additional load produces more latency rather than more throughput, and beyond that a plateau where the system serves less work than it did before. The knee is the usable ceiling, and the plateau is the failure region where queueing has become the dominant cost.

Headroom is the distance from current load to the knee, expressed as a percentage or as a time-to-exhaustion at the current growth rate. It is measured, not asserted, and it moves when the system changes — a new dependency, a schema change, or a configuration difference can shift the knee by a large factor. A capacity number without a date is a claim about a system that no longer exists.

Primary sources: <https://sre.google/> and <https://www.cncf.io/>.

## Decision rules

- Record the load-to-throughput curve and the point identified as the knee.
- Record the latency at the knee and at the plateau.
- Record the current load and the headroom as a percentage of the knee.
- Record the growth rate and the time to exhaustion at that rate.
- Record the system version and configuration the measurement applies to.
- Record the thesis of what limits capacity, and whether it was tested.

## Procedure

1. Run a stepped load test and record throughput and latency per step.
2. Identify the knee and the plateau from the curve.
3. Record current load against the knee.
4. Record growth rate and compute time to exhaustion.
5. Record the limiting resource and test the thesis by changing it.
6. Record the date, version, and configuration.

## Anti-patterns

- Quoting a peak throughput without the latency at which it was achieved.
- Assuming headroom is a fixed percentage.
- Ignoring the plateau, where more load means less work.
- Measuring once and treating the number as a property.
- Guessing the bottleneck instead of testing it.

## Done checklist

- [ ] Load-throughput curve recorded.
- [ ] Knee and latency at knee recorded.
- [ ] Current load and headroom recorded.
- [ ] Growth rate and time to exhaustion recorded.
- [ ] Limiting resource tested.
- [ ] Date, version, and configuration recorded.

The headroom figure is most useful when expressed as a time rather than a percentage: a system at forty percent of its knee with traffic growing ten percent a month has a different urgency from one at seventy percent with flat traffic, and the percentage alone conceals which of the two it is.


## Sources

- Capacity planning guidance: <https://sre.google/>
- Cloud native capacity practice: <https://www.cncf.io/>
- Performance measurement reference: <https://www.w3.org/>
