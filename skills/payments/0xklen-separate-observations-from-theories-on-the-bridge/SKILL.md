---
name: separate-observations-from-theories-on-the-bridge
description: Use when responders state causes as facts during an incident. Labels each statement as observation, inference, or hypothesis so the team debugs evidence instead of the loudest guess.
---

# Separate Observations from Theories on the Bridge

Under stress a guess spoken confidently becomes the team's shared fact and steers hours of wasted work. Labelling what is observed versus inferred versus guessed keeps the investigation anchored to data.

## Procedure

1. Tag every statement as you speak:
   - **Observed**: "p99 latency is 4.2s" — a direct measurement, reproducible.
   - **Inferred**: "so the pool is probably saturated" — a deduction from observations, still falsifiable.
   - **Hypothesis**: "I think 4.18 introduced a connection leak" — a guess to be tested.
2. IC repeats inferences as inferences: "that's a theory, not a fact — how do we test it in two minutes?"
3. Convert each live hypothesis into a cheap discriminating test before acting on it: "if it's a leak, active connections will not fall after traffic drops; if it's load, they will."
4. Keep the observation list short and shared; promote an inference to observation only when it is directly measured.
5. When a hypothesis dies, log it as ruled out with the evidence, so it is not resurrected at the next handoff.
6. Watch for a confident voice collapsing the three — a senior engineer saying "it's the cache" restarts the cycle; ask "observed or inferred?".
7. Before any destructive action, state what observation would confirm the hypothesis; if none exists, the action is a guess.
8. After a fix, check whether the result matches the hypothesis; a coincidental recovery is not a confirmed cause.

## Pitfalls

- Acting on an unlabelled inference (restarting a node because "it looked weird") and losing the system state with no evidence gained.
- Keeping a dead hypothesis alive because it belongs to the most senior person on the bridge.
- Reporting an inference to stakeholders as a confirmed cause, then walking it back.
- Restarting before measuring, so the observation that would have discriminated two hypotheses is destroyed.
- Confusing correlation ("errors rose when CPU spiked") with cause, and stopping at the first plausible story.
- Letting "we've always had that" close an investigation without a measurement to back it.

## Verification

```
    grep -cE '\b(observed|inferred|hypothesis|ruled out)\b' incident/SEV*-2026-*.md
    # passes when the timeline distinguishes measured facts from hypotheses and logs each ruled-out hypothesis with its evidence
```

Related: the IC enforces the labels here, and `keep-an-incident-decision-log` records which theory died.
