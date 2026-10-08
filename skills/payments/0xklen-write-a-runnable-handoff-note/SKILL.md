---
name: write-a-runnable-handoff-note
description: Use when ending a shift or session mid-task. Leave a handoff another operator can execute end to end without reading your whole history.
---

# Write a runnable handoff note

A handoff is only useful if the next person can act from it alone. History may be gone; the note must carry goal, state, ordered commands, and open decisions.

## Procedure

1. State the goal and the current state in two lines.

2. List what is done and verified, each with the command that proves it.

3. List what is left as ordered next steps, each with the exact command.

4. Name every open decision and the default you will take if no one answers.

5. List running processes, ports, and temp files (`lsof -i :8080`), so the next person knows the environment.

6. Reference credentials by location, never by value — point at the secret store.

7. Add the one thing that would waste an hour if missed.

## Pitfalls

- "See my earlier messages" is not a handoff; the history may be unavailable.
- Leaving a background process running with no note blocks the next person.
- Steps without commands invite improvisation and drift.
- Handing off mid-decision with no default causes a silent stall.
- Copying secrets into the note leaks them; reference the vault instead.

## Verification

    ls -l HANDOFF.md && grep -c "^[0-9]\." HANDOFF.md   # ordered steps present

Hand off goal, state, ordered commands, open decisions, and running services.
