---
name: brief-an-executive-in-90-seconds
description: Use when an executive or sponsor asks for status during an incident. Delivers a 90-second spoken brief of impact, trend, decisions, and the single ask — nothing about internals.
---

# Brief an Executive in 90 Seconds

An executive needs the business impact and the decision they may have to make, not the debugging. A brief that runs long or hedges leaves them to escalate independently, which pulls more people into the incident.

## Procedure

1. Lead with business impact and duration: "Checkout has failed for 22% of orders for 40 minutes; roughly $18k/min of completed orders affected."
2. State the trend: improving, stable, or worsening — an executive's first question is which way it is moving.
3. Name decisions already made and their cost: "we rolled back 4.18; some customers saw failed orders in the window."
4. Give the one ask, or say there is none: "I need you to authorise a customer credit if the window exceeds 60 minutes — decide by 15:10." Executives add value via decisions, not monitoring.
5. Say when you will update next and state the escalation threshold: "if it recurs I elevate to SEV1 and page you."
6. Keep internals out — no service names, no "the pool", no unresolved theories presented as facts.
7. If you do not know something, say "unknown, will report at next update" rather than guessing; a brief that later contradicts itself damages your credibility on the next incident.
8. Keep it under 90 seconds spoken; a brief that needs a chart has the wrong audience.
9. Offer to take the decision off their plate if it does not need an executive, rather than inventing one.

## Pitfalls

- A 20-minute technical narrative when the ask is "are we okay?" — the executive escalates to others to find out.
- Presenting the current leading hypothesis as a confirmed cause, then reversing under questioning.
- No explicit ask, so the executive either does nothing or intervenes randomly.
- Quoting internal metrics an executive cannot interpret ("goroutine count is 40k") instead of user or revenue impact.
- Burying the trend, so the executive assumes the worst because the direction was never stated.
- Over-promising a resolution to sound in control, then having to walk it back to the same person.

## Verification

```
    grep -E 'impact|trend|ask|next update' incident/exec-brief-*.md
    # passes when the brief states business impact, direction, any decision needed with a deadline, and the next update time
```

Related: pull the numbers from `quantify-incident-customer-impact` and log the ask with `keep-an-incident-decision-log`.
