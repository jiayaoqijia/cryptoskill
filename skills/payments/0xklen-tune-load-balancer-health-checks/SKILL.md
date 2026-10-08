---
name: tune-load-balancer-health-checks
description: Use when a load balancer marks healthy nodes down, or keeps sending traffic to a broken one. Set the check path, interval, timeout, and unhealthy threshold from real p99 latency so checks reflect serving ability, not just process liveness.
---

# Tune load balancer health checks

A health check is a contract with the balancer about what "able to serve" means. Too shallow and it
routes traffic to a broken node; too strict and it churns nodes out of the pool under load.

## Procedure

1. Pick a dedicated endpoint that touches real dependencies but is cheap:
   ```bash
   curl -sf -o /dev/null -w '%{http_code} %{time_total}\n' http://10.0.1.5:8080/healthz
   ```
   The check must fail when the database or cache the app needs is unreachable, and pass otherwise.
2. Measure the endpoint's own latency, then set the timeout above its p99:
   ```bash
   for i in $(seq 1 50); do curl -s -o /dev/null -w '%{time_total}\n' http://localhost:8080/healthz; done \
     | sort -n | tail -1   # slowest of 50 ≈ p98
   ```
   Set `timeout = 2 × slowest`. A timeout below p99 causes flapping exactly when traffic is high.
3. Choose interval and unhealthy threshold from the drain budget:
   - `interval=10s`, `unhealthy_threshold=3` → 30 s to detect a dead node. Larger `interval` detects
     slower but generates less check traffic and jitter.
4. Set a *separate* healthy threshold (usually 2) so one flaky success does not re-add a bad node.
5. Return `503` from the endpoint when a dependency is down, not a `200` with a JSON body — the LB
   reads the status code, not your payload.
6. Exclude the health endpoint from auth and rate limits so the checker never gets a 401/429.
7. After changing thresholds, re-check the balancer's reported state:
   ```bash
   aws elbv2 describe-target-health --target-group-arn "$TG" \
     --query 'TargetHealthDescriptions[].[Target.Id,TargetHealth.State,TargetHealth.Reason]'
   ```

## Pitfalls

- A health check that only dials the TCP port ("connection refused = down") passes while the app returns 500 on every real request.
- A check that pings `/` (full page) hits the DB on every probe and times out under load.
- `timeout` shorter than the endpoint's p99 flaps nodes out during traffic spikes, shrinking capacity exactly when you need it.
- A `200 OK` returned by a catch-all error handler masks a dead dependency.
- Thresholds set per target group but a second target group (the one for HTTP/2 or a different port) left at defaults.
- Health endpoint behind the same auth as the API returns 401 forever, marking everything down.

## Verification

    curl -sf -o /dev/null -w '%{http_code} %{time_total}\n' http://10.0.1.5:8080/healthz
    aws elbv2 describe-target-health --target-group-arn "$TG" \
      --query 'TargetHealthDescriptions[].TargetHealth.State'

Pass means the endpoint returns 200 in under the configured timeout and every target reads `healthy`.
Report: "Timeout raised 1s→5s (p99 2.1s), interval 10s, unhealthy 3; flapping stopped."
