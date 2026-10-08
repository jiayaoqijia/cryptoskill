---
name: drain-in-flight-requests-on-prestop
description: Use when rolling restarts drop requests because the pod leaves endpoints and dies too fast. Adds a preStop drain hook that waits for load-balancer propagation before the process exits.
---

# Drain In-Flight Requests on PreStop

Kubernetes starts removing a pod from Service endpoints and sends SIGTERM roughly in parallel; iptables/kube-proxy rules and cloud load-balancer health checks take seconds to converge, so traffic keeps arriving at a pod that has already stopped listening. A `preStop` hook that delays the SIGTERM closes that gap.

## Procedure

1. Add a `preStop` hook that sleeps at least as long as the slowest endpoint-removal path (commonly 5–15s):
   ```yaml
   lifecycle:
     preStop:
       exec:
         command: ["sh", "-c", "sleep 10"]
   terminationGracePeriodSeconds: 40
   ```
2. Ensure the grace period covers preStop plus the app's own drain plus a margin: preStop 10s + drain 20s < 40s.
3. Do not rely on the pod's own readiness flipping to force endpoint removal; the hook is what buys convergence time.
4. If the app can signal readiness itself, make `/readyz` fail immediately on SIGTERM, but still keep a short preStop for the proxy lag.
5. For long-lived connections (gRPC streams), the drain must also send GOAWAY before the sleep ends:
   in Go, `grpcServer.GracefulStop()`; the preStop sleep must be long enough for streams to finish.
6. On a Service with an external cloud LB, check the LB's health-check interval and deregistration delay; the preStop must exceed both. For AWS NLB set `deregistration_delay.timeout_seconds` and match it.
7. Verify by watching endpoint counts during a rollout: `kubectl get endpoints <svc> -w`.

## Pitfalls

- A `preStop` `sleep` makes termination take that long for every pod, including crash recovery; keep it minimal and inside the grace period.
- If `terminationGracePeriodSeconds` is less than the preStop sleep, the container is SIGKILLed before the hook finishes and the hook is a no-op.
- `preStop` runs on the normal path and is skipped on eviction of a failed node; node-level failures drop requests regardless.
- Sending SIGTERM to a Go server that ignores it during the preStop sleep means the sleep is wasted — the app must still handle the signal after the hook.
- A mesh sidecar injects its own termination sequence; the effective drain is the max of app and sidecar. Account for the sidecar's drain duration.
- Closing keep-alive connections only at the end of the sleep still allows a request to arrive at second 9.99 and be cut at 10.0; leave headroom.

## Verification

    for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' http://x/ & done
    kubectl rollout restart deploy/x
    # all responses 200, none connection-reset

Run continuous requests across a rolling restart and assert zero non-2xx and zero resets. Report the error count observed across the rollout.
