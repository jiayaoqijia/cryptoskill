---
name: separate-the-problem-from-the-solution
description: Use when a request arrives pre-shaped as a solution ("add a button that", "we need a dashboard"). Restates the underlying problem and its success signal before any solution is committed.
---

# Separate the problem from the solution

A request is usually a solution someone already picked. Building it verbatim locks in their guess; this skill reopens the problem so the cheapest correct fix stays available.

## Procedure

1. Split the ask into two lines in `problem.md`: `problem:` (who is stuck, doing what, and why it hurts) and `proposed solution:` (the thing they asked to build).
2. Test the problem line by deleting the solution: if the problem still makes sense and still hurts, it is real; if it evaporates, the "problem" was a description of the solution.
3. Name the observable success signal before any build: "a user can finish X in under Y steps" or "error rate on flow Z drops below N%". A problem with no signal cannot be verified later.
4. Ask what the user does today without the proposed solution — the manual workaround reveals the real constraint (time, trust, data, or a missing integration).
5. List at least two alternative solutions that would also solve the stated problem. If you can only see one, you have not separated solution from problem yet.
6. Compare alternatives on cost-of-delay, blast radius, and reversibility; the smallest reversible one usually wins the first slice (see `cut-the-smallest-shippable-slice`).
7. Write the chosen direction as a one-line decision naming the rejected alternatives, so the tradeoff is recorded rather than implied.
8. Hand the restated problem — not the original ask — to whoever writes acceptance criteria.
9. Ask who else is affected by the problem and who else has asked for it; a pattern across several requesters is a stronger problem than one loud voice.
10. Record the problem's owner: the person who feels the pain, not the person who forwarded the request.

11. Have the requester restate the problem back to you; if their version still names the solution, the split is not done.

## Pitfalls

- Treating the requested UI element as the requirement; a button is one of many ways to expose an action.
- Accepting a success signal you cannot measure, such as "users are happier".
- Skipping alternatives because the requester is senior; authority does not validate a solution.
- Confusing a symptom ("support gets many tickets about X") with the problem it signals.
- Letting the restated problem quietly become an argument for the solution you already preferred.
- Rewriting the request into a problem statement that flatters the original solution.
- Assuming the person who reported the problem can also decide its priority.

- A problem statement that only the author finds compelling, tested against no real user.

## Verification

    wc -l problem.md && grep -c '^problem:' problem.md && grep -c '^proposed solution:' problem.md

Report the problem line, the observable success signal, and the two alternatives you rejected with their reasons.
