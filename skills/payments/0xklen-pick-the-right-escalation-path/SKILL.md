---
name: pick-the-right-escalation-path
description: Use when something must be escalated and several routes exist. Send it to the lowest level that can actually decide, framed as a decision, so it does not bounce.
---

# Pick the right escalation path

Escalation sent to the wrong level bounces and costs a day. The rule is to route to the lowest authority that can genuinely decide the question, and to frame it as a decision, not a complaint.

## Procedure

1. Define the exact decision needed before choosing a route; escalating a feeling gets bounced straight back.

2. Choose the lowest authority that can decide it: peer team, their manager, your manager, then the shared owner.

3. Escalate one level at a time. Jumping two levels burns the intermediate owner and looks like an end-run.

4. Frame it as a decision request: situation, options, recommendation, deadline (see `escalate-with-a-recommendation`).

5. If you cannot name the level that owns it, ask the intended recipient where it belongs instead of guessing.

6. Escalate the boundary, not the work: "I need write access to X", not "please do this for me".

7. Log the route and the outcome; a bounce teaches you the correct level for next time.

## Pitfalls

- CC'ing everyone to cover yourself, which dilutes the ask and invites noise.

- Escalating to the top immediately, bypassing the owner who must live with the result.

- Escalating without a decision framed, so it returns with "what do you want me to do?".

- Sitting on a blocker because the route is unclear instead of asking where it goes.

- Re-escalating the same item up the chain the moment it is slow.

## Verification

```
    grep -nE 'route:|decision:' escalation.md   # the chosen level and the decision are stated
```

Report the decision, the level you sent it to, and why that is the lowest competent one.
