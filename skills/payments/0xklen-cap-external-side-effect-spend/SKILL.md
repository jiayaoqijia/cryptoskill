---
name: cap-external-side-effect-spend
description: Use when a bug, loop or runaway job could send money, emails or provisioned resources faster than intended — puts a hard cumulative cap and idempotency guard on every external side effect.
---

# Cap external side-effect spend

Retries, loops and bad deploys do not send one email or charge one card — they send thousands. Every external side effect that costs money or reaches a human needs a cumulative budget, an idempotency key, and a break that trips at the cap instead of after it.

## Procedure

1. Classify side effects by cost and reversibility: payments (money, near-irreversible), emails/SMS (reputation, irreversible), provisioning (cloud spend, reversible), notifications (cheap). The first two need hard caps in code, today.

2. Track cumulative spend or send count per window and per tenant in a store the workers share, and check *before* the call, not after:
       key = f"spend:{tenant}:{date}"
       total = redis.incrby(key, amount_cents)
       if total == amount_cents { redis.expire(key, 172800) }   # set TTL once, on first incr
       if total > daily_cap_cents { return ErrBudgetExceeded }

3. Trip a breaker at the cap: stop calling the provider, alert, and require a human to raise the cap. A limit that only warns is a limit that does nothing at 3 a.m.

4. Make every call idempotent so a retry after a timeout cannot double-charge — pass a stable key derived from the business event, not from the attempt:
       stripe.Charge(idempotency_key=order_id + ":" + event_type, ...)
   A timeout that actually succeeded, retried without a key, charges twice.

5. Cap fan-out *rate*, not just total: `100 emails/second` prevents a warm-up burst from tripping provider spam heuristics even when the daily total is fine. Ramp slowly for notification-heavy changes (1 → 100 → 10000).

6. Sandbox the first send of any new path: always deliver the first N messages to an internal test list, confirm they render, then cut over to real recipients. A broken template sent to 200k people cannot be recalled.

7. Log every side effect with tenant, amount, idempotency key and cumulative total, so a reconciliation can reconstruct exactly what was sent in a bad window.

## Pitfalls

- Checking the cap after the charge, so the cap is always exceeded by exactly one call — fine for one, catastrophic in a tight loop.
- A global cap with no per-tenant split, so one tenant's runaway job exhausts everyone's budget and blocks legitimate sends.
- Idempotency keys derived from `uuid4()` per attempt, which are unique every retry and provide no protection at all.
- No circuit breaker: exhausting the daily cap yet still calling the provider (and getting declined) floods logs and may trip provider-side rate bans.

## Verification

    # drive the send path past the cap and confirm it breaks, not just warns
    for i in $(seq 1 200); do curl -s -X POST localhost:8080/notify -d '{"tenant":"acme"}'; done
    redis-cli get "spend:acme:$(date +%F)"
    # after the cap, responses are 429 and no new provider calls appear in the provider log
    grep -c "idempotency_key" /var/log/payments.log   # every send carries a stable key

Report: the cap value and window per tenant, evidence the path refuses calls past the cap, an idempotency-key scheme that survives retries, and a sandbox-first send result.
