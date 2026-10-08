---
name: design-health-and-readiness-probes
description: Use when a load balancer or orchestrator needs liveness and readiness signals — splits the two endpoints, keeps liveness dependency-free, and makes readiness reflect actual ability to serve.
---

# Design health and readiness probes

Liveness asks "should this process be killed?"; readiness asks "should it take traffic?". Conflating them makes an orchestrator restart every pod during a dependency blip, or route to a pod that cannot serve.

## Procedure

1. Expose two endpoints with distinct meanings:
       /healthz   liveness:  is the process itself alive and not wedged?
       /readyz    readiness: can it serve a request right now?

2. Keep liveness cheap and dependency-free. It returns 200 as long as the event loop is responsive and must never call the database, cache or any peer. A liveness probe that fails when the database is down restarts every pod at once — the classic cascading restart.

3. Let readiness check only what is needed to serve: migrations applied, config loaded, warm cache, connection pool established. Leave peer health out unless the service is genuinely useless without it.

4. Configure with real timings and separate budgets:
       livenessProbe:  { httpGet: {path: /healthz, port: 8080}, periodSeconds: 10, timeoutSeconds: 1, failureThreshold: 3 }
       readinessProbe: { httpGet: {path: /readyz,  port: 8080}, periodSeconds: 5,  timeoutSeconds: 2, failureThreshold: 2 }
       startupProbe:   { httpGet: {path: /healthz, port: 8080}, periodSeconds: 2, failureThreshold: 30 }

5. Use a `startupProbe` for slow boots so a slow start does not trip liveness and cause a restart loop; it gates the other probes until the app is up (here, up to 60 s).

6. Return an accurate status code plus a small JSON body a human can read:
       {"status":"unready","reason":"migrations_pending","version":"a1b2c3"}
   Never return 200 with `{"status":"degraded"}` — the orchestrator cannot read prose.

7. Drain on shutdown: on SIGTERM flip `/readyz` to 503 first, wait 5–10 s for the endpoint to leave the load balancer, then stop accepting, with `terminationGracePeriodSeconds` at least the in-flight drain time.

8. Keep the probe handler off the request hot path and free of any lock a stuck request could hold, or the probe itself hangs and the pod is killed.

## Pitfalls

- Readiness that probes the database: a 30 s database blip empties the endpoint list and turns a degradation into a full outage.
- Liveness with `failureThreshold: 1` and a 1 s timeout, so one GC pause restarts every pod simultaneously.
- A single endpoint serving both meanings, so you cannot restart without dropping traffic or drain without restarting.
- A readiness handler that always returns 200, so a rollout declares ready before the app can actually serve.

## Verification

    curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/healthz   # 200 while a dependency is stopped
    curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/readyz    # 503 while it is stopped
    kubectl get pods -w    # READY only after readinessProbe passes, not before

Report: the two endpoints' semantics, the probe timings, and the observed behaviour — liveness stays 200 while a dependency is down, readiness flips 503→200 without any restart.
