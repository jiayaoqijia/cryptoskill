---
name: contain-a-partial-outage
description: Use when one zone, shard or dependency is down but the rest is healthy — drains the bad slice, routes around it and stops retry amplification so a partial failure does not become a total one.
---

# Contain a partial outage

Most incidents start partial: one AZ, one shard, one replica, one upstream. The failure mode that turns it total is retries and traffic piling onto the remaining healthy slice. Contain it by removing the bad slice from rotation fast and protecting the survivors.

## Procedure

1. Identify the *boundary* of the failure: which zone, shard, instance or dependency. Correlate error rate and latency by label, don't eyeball a single dashboard:
       sum by (zone, upstream) (rate(http_requests_total{code=~"5.."}[1m]))

2. Take the bad slice out of rotation at the health layer rather than deleting it: fail the readiness probe so the load balancer drains it while the process stays up for inspection:
       GET /readyz → 503 when dependency "payments" is unreachable
   Deregistration is reversible; `kubectl delete pod` loses the evidence.

3. Stop retries from *amplifying* the load on the survivors. Raise the client's backoff and jitter, shorten the deadline, and trip a breaker per downstream so a broken target is not hit at all:
       max_attempts=2, base_delay=250ms, jitter=full, breaker trip after 5 consecutive failures

4. Verify the routing actually moved: request counts on the healthy slice should rise by roughly the traffic the failed slice carried, not more. More than that means retries are doubling the load:
       rate(http_requests_total{zone="az-b"}[1m]) vs rate(http_requests_total{zone="az-a"}[1m])

5. Protect shared state that all survivors now contend for — a lock table, a sequence, a leader election. The survivors concentrating on one shard can exhaust its connections even though the app is "healthy".

6. Communicate the *scope* precisely: "us-east-1b unavailable, failing over to 1a and 1c; errors limited to that zone". Vague "we are having issues" prompts users to retry everything.

7. Before declaring recovery, confirm the failed slice is genuinely healthy again (probe for a full TTL, not a single 200) and re-admit it *slowly* — one instance at a time — so a flapping dependency does not re-fail under full load.

## Pitfalls

- Retrying aggressively against the remaining slice, so a survivable one-zone failure cascades into a full outage through pure amplification.
- Failing over to a warm standby that was never load-tested, so it collapses under the traffic it just inherited.
- Re-admitting the whole failed zone at once, which instantly re-triggers the failure if the root cause is not actually fixed.
- Deleting the failing instance before pulling its logs or its final state, discarding the evidence needed to find the cause.

## Verification

    # fail one zone and confirm survivors absorb the traffic without exceeding their limit
    kubectl cordon node/az-b-1 && kubectl drain node/az-b-1 --ignore-daemonsets
    curl -s 'localhost:9090/api/v1/query?query=sum(rate(http_requests_total[1m]))' | jq '.data.result[].value'
    # total request rate stays flat (no amplification); error rate returns to baseline
    curl -s localhost:9090/readyz -w '%{http_code}\n'    # bad zone 503, good zones 200

Report: the failure boundary, the drain action and evidence routing moved without amplifying, the state that survivors contend for, and the staged re-admission result.
