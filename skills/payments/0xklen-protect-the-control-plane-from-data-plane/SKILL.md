---
name: protect-the-control-plane-from-data-plane
description: Use when heavy data-plane traffic can starve health checks, auth or admin access — reserves separate capacity so operators can still reach the system while it is overloaded.
---

# Protect the control plane from data plane

The control plane is how you fix an outage: health checks, the admin API, auth, the kill switch, the metrics endpoint. If it shares a pool with user traffic, then the moment user traffic saturates the pool it also takes away your ability to see or stop the problem. Reserve capacity for it explicitly.

## Procedure

1. Classify every listener and endpoint as control plane or data plane. Control plane: `/healthz`, `/readyz`, `/metrics`, `/admin/*`, auth token validation, flag and config endpoints, the kill-switch reader. Everything user-facing is data plane.

2. Give the control plane its own capacity: a separate listener on a distinct port, its own thread pool / semaphore, and its own timeout. Reserve it as a fixed slice (e.g. 5% of the process budget) that data-plane saturation cannot touch:
       ctrl := make(chan struct{}, 50)   // reserved; data plane uses a different pool
       data := make(chan struct{}, 950)

3. Make health checks *cheap and dependency-light*. A `/healthz` that does a live DB query fails when the DB is slow and gets the pod killed — removing the very capacity needed to recover. Liveness must check only "the process is alive"; readiness may check critical deps, but must have a short timeout.

4. Keep auth path-independent: the token-validation or session check the control plane needs must not queue behind data-plane work. Cache verification keys and never call the data plane's slow services from the control plane.

5. Put the metrics and log pipeline on its own egress; a saturated data-plane egress must not drop the metrics you need to observe the incident. Scrape from a sidecar or agent, not in-process over the user path.

6. Reserve a *break-glass* path: a network route or IP allow-list to the admin API that survives a failed load balancer or DNS, so an operator can reach a pod by IP during a full-edge failure.

7. Rate-limit and cap the control plane *higher* than data plane, but still cap it — an unauthenticated `/metrics` or an admin endpoint hammered by a loop is its own outage.

## Pitfalls

- A liveness probe that queries the database, so DB slowness triggers pod kills and amplifies the outage in exactly the wrong direction.
- Sharing one HTTP server/thread pool across `/admin` and `/api`, so data-plane saturation locks the operator out of the fix.
- Scraping metrics through the application's user-facing path, so the metrics vanish precisely during the incident they should record.
- An admin API reachable only through the same LB/DNS that is failing, leaving no way in when the edge is down.

## Verification

    # saturate the data plane, then confirm the control plane still answers
    hey -z 60s -c 2000 http://localhost:8080/api/search > /dev/null &
    curl -s -o /dev/null -w '%{http_code} %{time_total}\n' localhost:9000/healthz   # 200, fast
    curl -s -o /dev/null -w '%{http_code} %{time_total}\n' localhost:9000/metrics
    curl -s -o /dev/null -w '%{http_code} %{time_total}\n' localhost:8080/api/search # data plane may 503
    grep -E 'livenessProbe|readinessProbe' k8s/deploy.yaml   # liveness has no DB check

Report: the control-plane endpoints and their reserved capacity, proof they answer fast while the data plane is saturated, and a liveness probe that does not depend on the database.
