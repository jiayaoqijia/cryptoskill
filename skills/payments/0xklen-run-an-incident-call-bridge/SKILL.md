---
name: run-an-incident-call-bridge
description: Use when responders join a live voice bridge during an incident. Sets speaking discipline, a scribe-on-the-bridge rule, and a verbal command protocol so coordination does not drown in cross-talk.
---

# Run an Incident Call Bridge

A bridge without structure becomes several simultaneous conversations; the IC cannot follow the state and decisions get made in a corner nobody hears. Speech discipline is what keeps a call faster than chat.

## Procedure

1. IC opens with the roll call and the protocol: "state your name and role when you speak; bring problems to me, not to each other."
2. One primary speaker at a time; the IC grants the floor: "@ben, give me the pool numbers." Others type in the channel.
3. A scribe stays on the bridge and writes decisions to the channel as they happen — a bridge with no written trail loses everything.
4. IC summarises every ~5 minutes for anyone who joined late: current impact, current action, next step.
5. Direct questions at a person, never "can somebody check the logs"; broadcast questions stall.
6. When a decision is made, repeat it back: "@ana owns rollback, ETA 3 minutes, next update 14:20" — the scribe logs the verbal decision immediately.
7. Mute during others' updates; side conversations move to a breakout channel so they do not wash over the IC.
8. If the bridge exceeds ~8-10 people, split: decision-makers stay on the main bridge, investigation moves to a workstream channel.
9. Join before you speak to confirm your audio, so the first thing the IC hears is not "you're breaking up".
10. When the incident ends, the IC says so explicitly and everyone drops; a bridge left open keeps generating stray decisions.

## Pitfalls

- Everyone talking at once, so the IC hears three hypotheses and holds none.
- Debugging aloud on the bridge, narrating every command, drowning the decision stream.
- No scribe, so the bridge produces a consensus memory that diverges from the logs.
- Keeping 20 listeners on the bridge who are neither deciding nor investigating, adding noise and confusion.
- Running the incident in a DM between two people and surfacing only the outcome, so the team cannot follow along.
- Leaving the bridge open after resolution, so a straggler's decision gets mistaken for the live one.

## Verification

```
    grep -E 'floor|owns|next update' incident/SEV*-2026-*.md
    # passes when each bridge decision is written to the channel with an owner within a minute of being voiced
```

Related: `delegate-investigation-tasks-under-command` turns the bridge's talk into bounded, owned threads.
