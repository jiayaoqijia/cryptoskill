---
name: pair-program-as-the-teacher
description: Use when pairing with someone less familiar to transfer skill, not just ship. Assigns driver and navigator with a think-aloud rule and a role handoff every 25 minutes, so the junior types and the reasoning is spoken aloud.
---

# Pair Program as the Teacher

If the expert types, the junior watches and learns little. Putting the junior in the driver's seat and forcing the reasoning to be spoken turns a work session into a lesson.

## Procedure

1. Pick a task sized for one 50-minute block; a task that outlasts the block becomes a lecture.
2. The junior drives from the first keystroke; the expert navigates and does not reach for the keyboard.
3. Enforce think-aloud: the driver says the intent before the edit; the navigator asks "why that?" when it is missing.
4. Hand off roles at the 25-minute mark, or when the driver is stuck for more than 3 minutes.
5. When the driver is stuck, the navigator asks a question, not a fix: "what does the error say?"
6. Log the concept that came up, one line, for later exercises in `pair-log.md`.
7. End with the driver stating what they would do differently, before anyone closes the tab.
8. Timebox the block hard; stop at 50 minutes even mid-feature, and leave a next-step note.
9. Debrief for two minutes: what the driver now understands that they did not at the start.
10. Rotate who chooses the task so the junior also practices scoping, not just typing.
11. Set the block goal in one sentence at the start, so the lesson has a finish line.
12. When a concept surfaces twice, stop and turn it into a drill rather than repeating it.
13. Take a two-minute break at the handoff; fatigue hides as confusion.
14. Agree the definition of done for the block before starting.
15. Ask the driver to narrate the plan for the next five minutes before typing.
16. Capture one 'aha' per block for the driver's own notes.

## Pitfalls

- The expert grabbing the keyboard to "just fix it", which teaches nothing and signals distrust.
- Silence while one person types; nothing is being transferred.
- A task too large for the block, so it becomes a demo.
- Switching roles constantly so neither person holds a thread long enough to reason.
- Ending the session with no note, so the next block restarts from zero.
- Letting the expert pick every task, so the junior never practices deciding what to build.
- The navigator dictating keystrokes instead of asking questions.
- Journaling during the block instead of after, which breaks the flow.
- Letting one person own the keyboard past their block, so the other goes passive.
- Starting to type with no agreed finish line.
- Rushing from problem to edit with no plan spoken.
- Letting a good insight evaporate with no note.

## Verification

    grep -E '^driver:|^concept:' pair-log.md | tail -10
    # passes when each 25-minute block names a driver and at least one concept

Report to the user: the block boundaries, who drove, and the concept each block surfaced.
