---
name: serving-record
domain: software-engineering/serving-record
trigger: "Writing the record of a serving fleet and its operating point."
anti_trigger: "Not for engine choice, and not for cost billing ledgers."
scope: "The written record: fleet shape, operating point, and the measurements behind them."
status: seedling
---

# Serving record

## Standard

The serving record holds the fleet shape, the operating point, and the measurements behind both: model and revision, parallelism mode, replica count, admitted-concurrency value, the throughput-latency pair it runs at, TTFT and pacing percentiles at representative load, KV headroom, and the workload's sequence-length mix. Every number carries its date, because serving behaviour shifts with engine versions and workload drift more than most infrastructure does.

Its test is replacability: a new engineer should read the record, reproduce the fleet, verify the pair in a load test, and know where the operating point sits relative to the knee — without inheriting oral tradition. Drift shows up here first: queue growth at fixed concurrency, TTFT tail creeping above the UX contract, or throughput per replica sliding after an engine upgrade.

Primary sources: <https://docs.vllm.ai/en/latest/> and <https://osf.io/prereg/>.

## Decision rules

- The record pairs every throughput number with its latency percentile and concurrency value.
- Fleet shape, engine version, and model revision recorded beside every measurement.
- The curve summary — not just the current point — recorded so the knee is visible.
- Each measurement dated and load-conditioned. A dateless number is a decoration.
- Every change to the fleet or engines triggers a re-measure of the pair, logged as a dated amendment.
- The workload's sequence mix recorded with each campaign of numbers — the mix is part of the number.

## Procedure

1. Assemble fleet shape: model revision, engine, parallelism, replicas, HBM class.
2. Record the concurrency setting and the throughput-latency pair at representative load.
3. Record TTFT and pacing percentiles beside the UX contract they must satisfy.
4. Summarize the measured curve with the knee so the operating point is traceable.
5. Date every campaign of numbers and the conditions it ran under.
6. Amend locally on any change; supersede only with new measurements, never edits.

## Anti-patterns

- Throughput numbers without their latency pairs or concurrency values.
- Undated performance claims.
- A single operating point without the curve that chose it.
- Engine upgrade with no re-measure.
- Recording the SLA and the measurement in different documents.

## Done checklist

- [ ] Fleet shape and models recorded with revisions.
- [ ] Operating point and pair stated per measurement.
- [ ] Curve summary with the knee present.
- [ ] TTFT and pacing under the UX contract.
- [ ] All measurements dated with conditions.
- [ ] Changes logged as dated amendments.

## Sources

- vLLM engine documentation: <https://docs.vllm.ai/en/latest/>
- Stated-metric discipline: <https://osf.io/prereg/>
- Serving-stack landscape: <https://github.com/vllm-project/vllm>
