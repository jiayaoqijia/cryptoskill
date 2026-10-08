---
name: separate-symptom-from-root-cause
description: Use when the obvious fix would only silence the visible failure. Traces the causal chain from the observed symptom to the earliest condition that made it possible, before editing.
---

# Separate Symptom from Root Cause

The first broken thing you see is rarely the first broken thing that happened. Fixing the symptom buys a re-report; fixing the cause ends it.

## Procedure

1. Write the symptom as a single observable sentence with a measurement: `orders created after 14:00 have total 0`, not `checkout is broken`.
2. Walk one causal step back and ask "what had to be true for this?" Repeat — this is the 5-Whys, but each answer must be checkable, not a guess.
3. For each step, demand evidence: a log line, a metric, a row, a diff. An unevidenced "because" is a hypothesis, not a link.
4. Stop when the next "why" leads outside your system (third-party, physics, user error) or to a change under your control. That boundary is your fix site.
5. Distinguish the trigger (what changed today) from the latent condition (why a change could cause this at all). Both matter; fix the latent condition so the next trigger is harmless.
6. Check for a single cause with many symptoms: if three alerts fired at once, they may share one upstream cause — find the shared node.
7. Propose the fix at the earliest controllable step, and a guard at the symptom so a recurrence is caught even if the cause form differs.
8. Re-verify the chain backward: with the fix in place, each "why" should now be blocked at its step.

## Pitfalls

- Fixing at the last link (the null check) and leaving the producer that emitted the null.
- Confusing the trigger with the cause: reverting today's deploy may hide a bug that predates it.
- Restarting to clear the symptom and losing the state that proved the chain.
- A chain built from plausibility rather than evidence, where every step is a guess.
- Stopping the "why" walk early because the next step is awkward (a config you do not own).
- Fixing one of several independent causes and declaring the incident closed.

## Verification

    git log --since=24.hours --oneline -- src/ | head
    # the trigger commit, if any, is above the symptom time; confirm it against deploy times

    grep -n "raise\|throw\|return None" src/producer.py | head
    # read the earliest controllable site; the fix belongs here, not at the consumer

Report to the user: the causal chain as evidenced steps, the trigger vs the latent condition, and the earliest controllable fix site.
