---
name: batching-strategies
domain: software-engineering/batching-strategies
trigger: "Choosing how requests group into accelerator passes."
anti_trigger: "Not for the batching API discount, and not for data pipelines."
scope: "From static batching to continuous: what each trades."
status: seedling
---

# Batching strategies

## Standard

Static batching admits N requests as a group, runs the group's decoding as a unit, and returns the batch when its slowest member completes. If one sequence runs long, the whole batch waits on it: completed requests sit in the slot until the slowest is done, wasting the memory and bandwidth their finished KV caches still occupy. Static batching's cost is measured in those held slots.

Continuous (in-flight, iteration-level) batching admits and completes requests one slot at a time at each decode step: as a request finishes its slot is immediately filled with the next queued request. The trick is that every decode step already processes all active sequences — a batch is a scheduling concept, not a fixed group. The route to high throughput is continuous joining with the KV-management that makes room for it.

Primary sources: <https://arxiv.org/abs/2309.06180> and <https://docs.vllm.ai/en/latest/>.

## Decision rules

- Identify which scheme the serving stack actually implements before predicting behaviour.
- Measure slot-hold waste in static mode: the fraction of decoder steps producing already-done requests.
- State admission priority: arrival order, longest-prefix match, or length bucketing — and keep it stated.
- Record what a preemption or shedding decision does at admission time as well as mid-decode.
- Combine with the KV leaf's memory arithmetic: batching gains materialize only if cache headroom admits the larger active set.
- Re-measure on the workload's real length distribution — synthetic uniform lengths overstate static batching.

## Procedure

1. Categorize the deployed stack: static, static-with-early-exit, or continuous.
2. Profile the workload's finished-length spread at peak hours.
3. Compute or measure slot-hold waste on that spread.
4. If continuous: record join and exit costs per step and any tail effects.
5. Set admission priority and shedding rules in writing.
6. Express the measured gain as throughput at equal latency percentiles — the two must travel together.

## Anti-patterns

- Reporting static-batch throughput at mean length; the variance is where the waste lives.
- Claiming continuous batching preserves per-request latency without measurement.
- Admission that ignores KV headroom, causing mid-decode preemption churn.
- Length bucketing tuned on synthetic uniform data.
- Treating batching as a flag rather than as a queueing-policy decision.

## Done checklist

- [ ] Deployed scheme identified.
- [ ] Length spread profiled at peak.
- [ ] Slot-hold waste measured or computed.
- [ ] Join/exit priority written.
- [ ] Shedding rules written.
- [ ] Gains reported throughput AND latency together.

## Sources

- PagedAttention continuous batching: <https://arxiv.org/abs/2309.06180>
- vLLM scheduling docs: <https://docs.vllm.ai/en/latest/>
- TensorRT-LLM engine: <https://docs.nvidia.com/tensorrt-llm/>
