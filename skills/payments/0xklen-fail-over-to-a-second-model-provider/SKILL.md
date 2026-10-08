---
name: fail-over-to-a-second-model-provider
description: Use when a single model provider is a single point of failure for a live feature. Configure a second provider with parity on the output contract, and fail over only when the primary is genuinely down.
---

# Fail over to a second model provider

One provider's bad afternoon is your outage. A second provider that matches your output contract turns a hard failure into a slower success — but only if it is wired and tested before you need it.

## Procedure

1. Define the contract every provider must meet: same schema, same field names, same units, same refusal semantics. Differences here cause the failover to emit subtly wrong data.

2. Adapt each provider behind one interface: your code calls `generate(request)`, and provider-specific request/response shaping lives in the adapter.

3. Trigger failover on failures that mean "provider down": 5xx, timeout, 429 after backoff, or a provider status incident — not on a single schema failure, which is your prompt's problem.

```python
try:
    return primary.generate(req, timeout=8)
except (Timeout, PrimaryDown):
    return secondary.generate(req, timeout=12)   # budget for the slower path
```

4. Test the failover path on purpose — point the primary at a dead endpoint weekly, or run a chaos flag — so it is not discovered broken during an incident.

5. Account for parity gaps: if the secondary is weaker on some task, gate the failover to the tasks it handles well or flag low-confidence output.

6. Log which provider served each call; a silent failover that changes quality without a trace is worse than an error.

7. Cap the failover: if both providers fail, return a typed error, not a hung request.

## Pitfalls

- Different output schemas between providers, so failover rows silently miss fields or use the wrong units.
- Failing over on the first error, including transient 429s that backoff would fix — you amplify the incident.
- Never testing the secondary, then finding its key expired or its model renamed when it matters.
- Falling over to a model with a much lower quality bar and not marking the output degraded.
- Retrying primary and secondary in a loop with no total deadline, so the request never returns.

## Verification

    python3 chaos_failover.py --kill-primary   # request completes via secondary; log shows provider=secondary and one degraded flag

Report: "failover tested with the primary key disabled — 100% of requests served by the secondary, 0 schema breaks, every failed-over call tagged provider=secondary in the log."
