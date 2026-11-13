---
name: load-model-validity
domain: software-engineering/load-model-validity
trigger: "Checking whether a load model resembles real traffic."
anti_trigger: "Not for latency optimisation, and not for capacity purchasing."
scope: "Whether the synthetic traffic resembles the real traffic."
status: seedling
---

# Load model validity

## Standard

A load test produces numbers whose meaning depends entirely on the traffic it generated. Uniform requests at a constant rate stress a system differently from a realistic mix with a heavy tail, bursty arrival, session affinity, and a distribution of payload sizes. A test that generates a million identical reads measures the cache and nothing else.

Validity is a matter of matching the dimensions that matter for the resource under test. If the bottleneck is likely to be database writes, the model must include the write mix; if it is likely to be memory, the model must include the payload distribution and the cardinality of keys. The record states which dimensions were modelled and which were fixed, so the result's scope is explicit.

Primary sources: <https://sre.google/> and <https://www.cncf.io/>.

## Decision rules

- Record the request mix and how it was derived from production data.
- Record the arrival pattern: constant, bursty, or replay of real timestamps.
- Record payload size distribution and the cardinality of keys or sessions.
- Record what was held constant for control, and the bias that introduces.
- Record the data volume in the test environment, since an empty database measures a different system.
- Record the gap between the model and production, explicitly.

## Procedure

1. Derive the request mix from production telemetry.
2. Record the arrival pattern and its burstiness.
3. Record payload and key cardinality distributions.
4. Seed the environment with realistic data volume.
5. Record what was simplified and the bias it introduces.
6. State the model's scope in the result.

## Anti-patterns

- Uniform requests at a constant rate.
- Testing against an empty or tiny database.
- Ignoring the read-write mix.
- Reporting a number without the model that produced it.
- Modelling traffic from a development environment.

## Done checklist

- [ ] Request mix recorded with its source.
- [ ] Arrival pattern recorded.
- [ ] Payload and cardinality recorded.
- [ ] Environment data volume recorded.
- [ ] Simplifications and bias recorded.
- [ ] Model scope stated in the result.

The most common validity failure is scale in the wrong dimension: a test with production request rates against a database a thousandth of the size measures a system that does not exist in either environment, and the result is neither the test system's ceiling nor production's.


## Sources

- Capacity and reliability guidance: <https://sre.google/>
- Cloud native testing practice: <https://www.cncf.io/>
- Performance measurement standards: <https://www.w3.org/>
