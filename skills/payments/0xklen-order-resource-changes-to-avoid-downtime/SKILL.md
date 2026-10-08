---
name: order-resource-changes-to-avoid-downtime
description: Use when an apply replaces resources that serve traffic and a naive plan drops availability. Sequences changes with lifecycle rules and staged applies so the swap is seamless.
---

# Order resource changes to avoid downtime

A correct plan can still cause an outage if it destroys before it creates. Control the order with lifecycle rules and staged applies.

## Procedure

1. Identify replacements in the plan (`delete`+`create`) on resources that serve traffic: instances, load balancers, DNS.
2. For a replacement that must be up first, set a lifecycle rule so the new resource is created before the old is destroyed:
       lifecycle { create_before_destroy = true }
3. Watch unique-name collisions: `create_before_destroy` fails when the new resource needs a name or IP the old one holds. Use a random suffix, or plan a two-phase rename.
4. For DNS cutovers, lower TTL to 60 s well before the change, apply, then raise it after:
       aws route53 change-resource-record-sets --hosted-zone-id Z123 --change-batch ttl-60.json
5. Stage multi-resource changes: apply the additive part, verify, then apply the destructive part, using `-target` scoped applies between reviews.
6. For a database never destroy-before-create without a snapshot; use the platform's multi-az failover or snapshot-and-restore.
7. Drain the old resource before it is destroyed: deregister from the target group and wait for connections to close.
8. Verify availability throughout: run a canary request loop during the apply.

## Pitfalls

- Default create-after-destroy on a singleton instance, so the service is down for the create duration.
- `create_before_destroy` on a resource with a fixed Elastic IP, which fails because the IP is still attached.
- A DNS record with a 24 h TTL, so clients keep hitting the destroyed endpoint for a day.
- Applying a stacked change atomically, so a working half and a broken half land together.
- No drain before destroy, so in-flight requests are reset rather than gracefully closed.

- A canary loop hitting a cached CDN edge, showing green while the origin behind it is down.
- `create_before_destroy` with no extra capacity, so the new instance steals the old one's slot and both are briefly down.

## Verification

    while true; do curl -sf -o /dev/null https://app.acme.com/healthz || echo "DOWN $(date)"; sleep 1; done
    # no DOWN lines through the apply

Report: the changed resources, the ordering mechanism (lifecycle rules, staged applies, TTL), and the availability loop with zero downtime.
