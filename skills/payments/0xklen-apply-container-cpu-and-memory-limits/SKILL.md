---
name: apply-container-cpu-and-memory-limits
description: Use when one container can starve its neighbours or be OOM-killed unpredictably. Sets requests and limits with matching units so scheduling and eviction behave and the container is throttled, not killed.
---

# Apply Container CPU and Memory Limits

A pod without a memory limit can consume the node and get the whole node evicted; a pod with a memory limit below its real peak gets OOM-killed mid-request. Requests drive scheduling; limits drive the cgroup ceiling. Getting both right is the difference between a slow pod and a dead one.

## Procedure

1. Measure before setting. Run under load and read the peak, not the average:
   `docker stats --no-stream` for a container, or `kubectl top pod <p> --containers` for a workload.
2. Set memory with headroom above peak (a common rule: limit = 1.3–1.5× observed peak) and requests at a value the scheduler can actually place:
   ```yaml
   resources:
     requests: { cpu: "250m", memory: "256Mi" }
     limits:   { cpu: "1",    memory: "512Mi" }
   ```
3. Set a CPU request equal to your steady-state usage and a limit for burst; CPU is compressible so throttling is safe where memory OOM is not.
4. For latency-sensitive work, consider `limits: cpu` above `requests` and watch throttling:
   `container_cpu_cfs_throttled_seconds_total` should stay low relative to `container_cpu_cfs_periods_total`.
5. Choose a QoS class deliberately: requests == limits for every resource gives `Guaranteed` (last evicted); only requests gives `Burstable`; neither gives `BestEffort` (first evicted).
6. Cap the JVM/heap to the limit, or the runtime ignores the cgroup and the kernel OOM-kills it: `-XX:MaxRAMPercentage=75.0`, not a fixed `-Xmx` above the limit.
7. Add a `LimitRange` in the namespace so a missing request is defaulted rather than silently unset:
   `kubectl apply -f limitrange.yaml`.
8. Track `container_memory_working_set_bytes` against the limit; alert at 85%.

## Pitfalls

- `512M` is 512,000,000 bytes while `512Mi` is 536,870,912; mixing decimal and binary units across a manifest and a runtime flag gives a heap larger than the limit.
- A memory limit forces the runtime to preallocate or grow into it; Go especially does not return freed memory to the OS promptly, so the working set stays near the limit — size accordingly.
- `kubectl top` shows usage at scrape time, not peak; a spike every 5 minutes between scrapes is invisible and causes periodic OOM kills.
- CPU limits throttle even when the node is idle, adding tail latency at no benefit; prefer request-only CPU for latency-critical services.
- `BestEffort` pods are evicted first under node pressure; a batch job left without requests dies whenever a neighbour spikes.
- Setting requests far above usage wastes schedulable capacity and triggers `FailedScheduling: Insufficient cpu` while `top` shows the node mostly idle.
- OOMKilled in `kubectl describe` reports exit code 137; do not read that as a crash loop from a bug.

## Verification

    kubectl top pod <p> --containers
    kubectl get pod <p> -o jsonpath='{.status.qosClass}'

Observed memory stays below the limit under peak load, `qosClass` matches your intent, and restart reason is not `OOMKilled`. Report measured peak versus limit and the QoS class.
