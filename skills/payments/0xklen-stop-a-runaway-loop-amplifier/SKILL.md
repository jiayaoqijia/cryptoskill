---
name: stop-a-runaway-loop-amplifier
description: Use when two or more services or agents call each other and a failure multiplies instead of settling — adds a hop budget, correlation dedupe and a loop breaker so one request cannot fan out into thousands.
---

# Stop a runaway loop amplifier

A retry that spawns a retry, a webhook that triggers a callback that triggers the webhook, an agent that re-plans itself: these are loops where volume multiplies at each hop. They fill queues, wallets and rate limits in seconds. Break the cycle with a hop budget and a dedupe on the causal chain, not just a timeout.

## Procedure

1. Trace *one* failing request end to end and count the calls it spawns. If a single request can generate more than a bounded number of downstream calls, you have an amplifier regardless of what the trace looks like on a happy path.

2. Propagate a hop count on every cross-service call and refuse beyond a small limit. Stick it in the same header as correlation so it travels automatically:
       x-hop-count: 0 → 1 → 2 → 3 (drop)
       if int(r.Header.Get("x-hop-count")) >= 3 { return 429, "hop budget exceeded" }

3. Dedupe on the causal chain: carry the originating event id and drop any work whose `(origin_id, step)` has already been processed. A webhook that fires in response to an event its own handler emitted is caught here:
       if redis.set(f"seen:{origin}:{step}", 1, nx=True, ex=300) is None { return }   // already handled

4. Make triggers *edge-triggered on change*, not level-triggered on state. A poller that enqueues work every time it sees a non-empty queue re-enqueues its own output forever; enqueue only when the value *transitions*.

5. Bound each queue's max depth and each consumer's in-flight, and shed when full rather than buffering without limit. An unbounded buffer hides the loop until memory runs out, which is a worse failure than a shed.

6. Put a global rate fuse on outbound calls per origin id: if one causal chain exceeds N calls/second, trip a breaker for that origin and alert. This catches loops you did not foresee.

7. Break the cycle at the design level where you can: make one direction of the loop asynchronous-only, or have the handler ignore events it caused (by `emitter == self`). Cheaper than any runtime guard.

## Pitfalls

- A timeout that stops *waiting* but not the loop: the caller gives up while the callee keeps spawning.
- Correlation id forwarded but not the hop count, so the trace is observable but the loop is not bounded.
- Idempotency keyed on `(message_id)` where the loop generates a fresh id at each hop, making every iteration look new.
- A retry with backoff but no cap on *attempts*, so a slow loop still multiplies, just over a longer window.

## Verification

    # emit one event and count the resulting calls; it must stay bounded
    curl -s -X POST localhost:8080/events -d '{"type":"order.created","id":"e1"}'
    curl -s 'localhost:9090/api/v1/query?query=sum(increase(calls_total[1m]))' | jq '.data.result[].value'
    # expect a small bounded number, not growth; x-hop-count capped in logs
    grep 'hop budget exceeded' /var/log/*.log | wc -l
    redis-cli keys 'seen:e1:*'   # dedupe keys present for each step

Report: the hop limit, the dedupe key scheme, the per-origin rate fuse, and an injected loop where volume stayed bounded and the breaker tripped instead of multiplying.
