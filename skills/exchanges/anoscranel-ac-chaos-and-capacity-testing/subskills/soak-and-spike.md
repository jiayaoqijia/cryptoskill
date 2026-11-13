---
name: soak-and-spike
domain: software-engineering/soak-and-spike
trigger: "Running a long-duration test or a sudden-onset test."
anti_trigger: "Not for steady-state capacity measurement, and not for profiling."
scope: "Long-duration leaks and sudden onsets, and what each reveals."
status: seedling
---

# Soak and spike

## Standard

A soak test runs a moderate load for a long time, and it finds the defects that only appear with duration: memory that is not released, connections that are not returned, caches that grow without eviction, logs that fill a disk, and counters that wrap. None of these are visible in a short test, and all of them are production failures.

A spike test does the opposite: it applies a sudden onset and observes whether the system recovers or collapses. The interesting response is not the peak throughput but the recovery — whether queues drain, whether autoscaling catches up, and whether the system returns to its baseline latency or stabilises at a worse one. Recording the recovery curve is what distinguishes a spike test from a stress test.

Primary sources: <https://sre.google/> and <https://www.cncf.io/>.

## Decision rules

- Record the soak duration and the resource metrics sampled throughout.
- Record the growth rate of memory, connections, and disk against the duration.
- Record the spike's onset rate and its magnitude.
- Record the recovery time and whether the system returned to baseline.
- Record the autoscaling behaviour and its lag.
- Record the metric that would have shown the leak before it caused a failure.

## Procedure

1. Choose the soak duration long enough for the suspected leak.
2. Sample resource metrics throughout and record their trend.
3. Extrapolate the growth to the failure point.
4. Run the spike and record onset, peak, and recovery.
5. Record whether the baseline was restored.
6. Record the leading indicator for future monitoring.

## Anti-patterns

- A soak test shorter than the suspected leak's cycle.
- Measuring only error rate during the soak and not resource growth.
- A spike so gradual it is a load test.
- Recording the peak and not the recovery.
- Assuming autoscaling recovers instantly.

## Done checklist

- [ ] Soak duration and metrics recorded.
- [ ] Growth rates recorded and extrapolated.
- [ ] Spike onset and magnitude recorded.
- [ ] Recovery time recorded.
- [ ] Baseline restoration recorded.
- [ ] Leading indicator recorded.

The soak's duration should be derived from the suspected leak rather than chosen for convenience: a cache that grows one percent an hour needs a hundred hours to show a doubling, and a four-hour soak will report stability that the production system will contradict within a week.


## Sources

- Reliability and capacity practice: <https://sre.google/>
- Cloud native operational guidance: <https://www.cncf.io/>
- Performance measurement standards: <https://www.w3.org/>
