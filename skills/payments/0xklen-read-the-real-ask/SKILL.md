---
name: read-the-real-ask
description: Use when the request as stated may not be the outcome the user wants. Separate the literal instruction from the goal behind it before starting work.
---

# Read the real ask

Users ask for the solution they imagined, not always the problem they have. Working the literal instruction when it misses the goal wastes the whole task.

## Procedure

1. Restate the request in one sentence: the literal instruction, and the outcome it is meant to produce.

2. Name the gap. Is the requested action a means to the goal or the goal itself? A user asking for `a cron job` often wants `know when the nightly build breaks`.

3. Apply the XY test: they want X but asked for Y. Check whether Y actually delivers X, or only resembles it.

4. When Y could fail to deliver X, ask exactly one goal question before building: "What should be true when this is done?"

5. Prefer the cheaper path to the goal when it is obvious. If a `curl -fsS localhost/health` answers the goal and a full dashboard was requested, propose the health check first.

6. Record the goal in one line at the top of the working file: `GOAL: alert within 5 min of a failed nightly deploy`.

7. If the user insists on the literal ask after hearing the alternatives, build it and note the divergence in your reply.

## Pitfalls

- Building the literal ask when a simpler path reaches the goal, then discovering it was never what they wanted.

- Assuming you know the goal and discarding the explicit instruction; that is overreach, not insight.

- Asking "why do you want this?" in a loop instead of asking once and acting on the answer.

- Treating a request for a tool as proof the tool is the outcome, not the means.

- Silently substituting your own interpretation without saying so.

## Verification

```
    grep -n '^GOAL:' task.md   # one line stating the outcome, not the instruction
```

Report the goal line and, when it differs from the literal ask, the one-line reason you chose it.
