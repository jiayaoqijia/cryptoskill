---
name: gpu-fleet-scaling
domain: software-engineering/gpu-fleet-scaling
trigger: "Scaling model replicas on a GPU fleet under load."
anti_trigger: "Not for CPU service autoscaling, and not for cost attribution."
scope: "Replicas, batch admission, and why CPU autoscaling rules do not transfer."
status: seedling
---

# GPU fleet scaling

## Standard

Autoscaling rules written for CPU services misfire on inference fleets for one structural reason: a model replica is not a cheap process. It holds multi-gigabyte weights pinned in HBM, takes tens of seconds to become warm, and serves a bounded number of concurrent slots dictated by KV headroom. Adding replicas is slow and expensive; removing them mid-load strands queued requests that cannot migrate — a request's KV cache lives in the replica that decoded it.

That immobility changes the scaling logic. Sheds and queues live at the fleet edge; once a request is admitted to a replica, it finishes there or is re-executed from scratch elsewhere. The fleet therefore scales on queue depth and admission thresholds, not on CPU-style per-process metrics, and the scale-down rule must respect warm-restart cost and in-flight work.

Primary sources: <https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html> and <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>.

## Decision rules

- Compute per-replica capacity from KV headroom and concurrency headroom, not from CPU or request-rate figures.
- State the admission threshold where the fleet scales up, tied to the SLA's queue-wait tail.
- Scale-down must drain: no replica terminates with admitted requests still decoding on it.
- Record warm-start time per replica so scale-up expectations match reality.
- Prefer queueing at the edge over preemption inside a replica; preemption re-executes from scratch.
- Monitor at fleet level: per-replica metrics mislead when the queue, not the replica, holds the tail.

## Procedure

1. Fix the per-replica concurrency from the KV arithmetic.
2. Set fleet admission thresholds on queue depth and expected wait.
3. Wire the edge queue with priority classes if mixed traffic shares the fleet.
4. Define the drain rule for scale-down and test it under synthetic load.
5. Measure warm-start time and put it in the scale-up latency budget.
6. Record the fleet shape, thresholds, and drain behaviour in the serving record.

## Anti-patterns

- CPU-utilization autoscaling triggers applied to GPU replicas.
- Killing a replica with in-flight requests because the fleet looked overprovisioned.
- Preempting mid-decode requests as a routine load-shed path.
- Expecting instant capacity from a scale-up while warm-start takes minutes.
- Scaling on per-replica averages while the edge queue holds the real tail.

## Done checklist

- [ ] Per-replica capacity computed from memory, not CPU.
- [ ] Admission thresholds tied to the queue-wait tail.
- [ ] Drain-before-scale-down tested.
- [ ] Warm-start time budgeted.
- [ ] Edge queueing with priorities if traffic is mixed.
- [ ] Fleet-level monitoring in place.

## Sources

- Real-time endpoint autoscaling: <https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html>
- Deployment and replica mechanics: <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>
- Serving-engine deployment context: <https://huggingface.co/docs/text-generation-inference/index>
