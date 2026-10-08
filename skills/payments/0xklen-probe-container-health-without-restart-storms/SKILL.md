---
name: probe-container-health-without-restart-storms
description: Use when a slow-starting container is killed in a restart loop by its own liveness check. Separates startup, liveness and readiness so a cold JVM or migration is not mistaken for a hang.
---

# Probe Container Health Without Restart Storms

A liveness probe answers "is this process wedged and needs a restart"; a readiness probe answers "should traffic reach it". Wiring liveness to a slow dependency turns a transient slowdown into a crash loop: the kubelet restarts the pod, it re-runs the slow init, and the cycle repeats.

## Procedure

1. Give a slow-starting service a `startupProbe` that owns the boot budget, and let liveness stay off until it passes:
   ```yaml
   startupProbe:
     httpGet: { path: /healthz, port: 8080 }
     failureThreshold: 30
     periodSeconds: 5      # 150s ceiling
   livenessProbe:
     httpGet: { path: /livez, port: 8080 }
     periodSeconds: 10
     failureThreshold: 3
   readinessProbe:
     httpGet: { path: /readyz, port: 8080 }
     periodSeconds: 5
     failureThreshold: 2
   ```
2. Split the endpoints. `/livez` returns 200 if the event loop responds and touches no dependency. `/readyz` fails when a required dependency is unreachable so the pod leaves the endpoint list without being killed.
3. Set `initialDelaySeconds` only when you cannot use a startup probe; prefer the probe so the budget is proportional.
4. Keep the handler cheap: a probe that runs a full DB query can time out under load and restart healthy pods. Cap the check at a ping or cached flag.
5. For Docker/Compose, add a `healthcheck` with the same split:
   `HEALTHCHECK --interval=10s --timeout=2s --retries=3 --start-period=60s CMD curl -fsS http://localhost:8080/readyz || exit 1`.
6. Tune `timeoutSeconds` below `periodSeconds` so a hanging probe cannot overlap the next period.
7. Observe the loop: `kubectl get pod -w` and `kubectl describe pod <p> | grep -A3 Events`.

## Pitfalls

- Pointing liveness at `/readyz` while `/readyz` depends on a database means a DB blip restarts every pod simultaneously — a self-inflicted outage.
- `failureThreshold: 1` with `periodSeconds: 1` restarts on a single GC pause; use at least 3 failures.
- A probe that returns 200 while the app is still running migrations declares readiness too early and routes traffic into a half-open schema.
- `startupProbe` and `livenessProbe` on the same port with different paths is fine; putting them on the same path reintroduces the coupling.
- A TCP probe passes as soon as the socket is listening, which is true before migrations finish — use HTTP readiness for anything with init work.
- In Docker, `--start-period` counts from container start and does not reset; a slow first boot longer than it is marked unhealthy and can trip `depends_on: condition: service_healthy`.

## Verification

    kubectl get pod -l app=x -o jsonpath='{range .items[*]}{.metadata.name} {.status.containerStatuses[0].restartCount}{"\n"}{end}'

Restart count stays 0 across a deliberate dependency outage while the pod's `READY` column flips to `0/1` and back. Report restart count and the readiness transition, not "probes are configured".
