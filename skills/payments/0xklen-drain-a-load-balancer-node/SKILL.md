---
name: drain-a-load-balancer-node
description: Use when taking a node out of a load balancer pool for deploy, upgrade, or maintenance. Deregister first and wait for in-flight requests and connection reuse to finish before stopping the process, so no request lands on a dead node.
---

# Drain a load balancer node

Stopping a node the moment it is deregistered cuts live requests: the pool has stopped sending new
traffic, but keep-alive clients and in-flight requests still point at it. Drain, then stop.

## Procedure

1. Fail the node's health check first so the balancer stops routing to it:
   ```bash
   curl -sf -X POST http://localhost:9000/admin/drain   # app-specific drain endpoint
   ```
   Or flip the health endpoint to return 503 for the drain window.
2. Deregister at the balancer and note the change:
   ```bash
   aws elbv2 deregister-targets --target-group-arn "$TG" --targets Id=i-0abc123
   aws elbv2 describe-target-health --target-group-arn "$TG" --targets Id=i-0abc123 \
     --query 'TargetHealthDescriptions[].TargetHealth.State'
   ```
3. Wait for `draining` to become `unused` — this is the balancer's own drain timer, default 300 s on
   ALB. Do not stop the process until the state is `unused`:
   ```bash
   aws elbv2 describe-target-health --target-group-arn "$TG" --targets Id=i-0abc123 \
     --query 'TargetHealthDescriptions[0].TargetHealth.State'
   ```
4. Confirm no active connections remain on the node (see `inspect-tcp-connection-states`):
   ```bash
   ss -tan state established '( sport = :8080 )' | wc -l
   ```
5. Only now stop the service, with a graceful-stop timeout that outlasts the longest request:
   ```bash
   systemctl stop myservice   # TimeoutStopSec must exceed your p99 request time
   ```
6. For a rolling deploy, drain and re-add one node at a time, keeping the pool above the capacity
   floor so failover headroom survives the whole rollout.
7. On re-add, verify the node passes health checks before moving to the next one.

## Pitfalls

- Stopping immediately after deregistering kills in-flight requests; the drain timer exists for a reason.
- Client-side connection pools and HTTP/2 keep-alive hold connections open past the LB drain timer.
- A health check path that always returns 200 (no dependency checks) marks a broken node healthy.
- Draining all nodes "in parallel" empties the pool and causes a full outage.
- Server-Sent Events or websocket traffic can pin a connection open indefinitely and block drain completion.
- If the app deregisters itself on SIGTERM but the LB has a shorter drain timer, requests still get cut.

## Verification

    aws elbv2 describe-target-health --target-group-arn "$TG" --targets Id=i-0abc123 \
      --query 'TargetHealthDescriptions[0].TargetHealth.State'
    # expect "unused" before the process is stopped

Report: "Node i-0abc123 drained to `unused` at 12:04, established connections hit 0, service stopped
12:05; pool stayed at 3/4 healthy throughout."
