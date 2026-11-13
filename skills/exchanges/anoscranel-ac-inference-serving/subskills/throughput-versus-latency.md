---
name: throughput-versus-latency
domain: software-engineering/throughput-versus-latency
trigger: "Choosing and stating an operating point for the serving fleet."
anti_trigger: "Not for engine marketing comparisons, and not for capacity headroom tests."
scope: "The one dial: where an operating point is chosen and stated."
status: seedling
---

# Throughput versus latency

## Standard

Throughput and per-request latency trade against each other through a single mechanism: how many requests the fleet decodes concurrently. More concurrent requests share the same memory bandwidth, so each decodes slower; fewer concurrent requests finish faster each but leave bandwidth idle. The operator chooses a point on this dial, and every downstream number — cost per million tokens, TTFT tail, pacing variance — is a consequence of that point.

The discipline is to state the point. A fleet described as "low latency" without its concurrent-batch, or "high throughput" without its latency percentile, is describing a mood. The record carries the pair (throughput, latency percentile) for each fleet shape; changes to one number without the other are meaningless. Engine comparisons run at matched operating points or not at all.

Primary sources: <https://arxiv.org/abs/2309.06180> and <https://docs.nvidia.com/tensorrt-llm/>.

## Decision rules

- Every published number is the pair: throughput at stated latency percentile.
- The concurrency admission value is the operating-point knob; write it beside the numbers.
- Match operating points before comparing engines or hardware generations.
- Know which constraint each side of the dial truly needs: interactive serving versus bulk scoring differ.
- Monitor for the dial drifting: queue-time growth at fixed concurrency signals a steeper curve.
- Re-derive the whole curve after weight updates, engine upgrades, or prompt-length shifts — not just the old point.

## Procedure

1. Fix fleet shape: model, cost, replica count, HBM class.
2. Sweep the concurrency / admitted-batch values across the realistic range.
3. Record throughput and TTFT/inter-token percentiles for each value.
4. Identify the knee — where latency cost per throughput gain turns steep.
5. Set the production operating point just below the knee for a safety margin.
6. Publish the pair at the chosen point; keep the curve out of the marketing and in the serving record.

## Anti-patterns

- Improvement announcements that quote throughput without its latency, or vice versa.
- Engine comparisons where the two sides ran at different batch counts.
- Operating at the knee with no slack.
- Re-measuring a single point after an upgrade and calling it the new curve.
- Comparing interactive and bulk workloads on a single dial.

## Done checklist

- [ ] Throughput-latency curve swept per fleet shape.
- [ ] The knee identified.
- [ ] Operating point set below the knee, written beside the published pair.
- [ ] Comparisons only at matched points.
- [ ] Queue growth monitored for drift.
- [ ] Clinch: the pair recorded in the serving record.

## Sources

- PagedAttention throughput-latency behaviour: <https://arxiv.org/abs/2309.06180>
- TensorRT-LLM performance specifics: <https://docs.nvidia.com/tensorrt-llm/>
- vLLM operating guidance: <https://docs.vllm.ai/en/latest/>
