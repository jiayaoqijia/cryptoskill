---
name: audit-a-flow-for-dead-ends
description: Use when reviewing a user journey before release. Walks every screen and branch to find states where the user cannot progress, go back, or recover.
---

# Audit a flow for dead ends

A dead end is a screen where the user is stuck with no way forward or back. This skill walks the flow branch by branch and names every one before users hit it.

## Procedure

1. Draw the flow as a directed graph in `flow.md`: nodes are screens, edges are actions, and every branch is a labelled edge.
2. Enumerate the terminal nodes and confirm each is an intended end (success, confirmation), not an accident.
3. For each node list the exits: primary action, back/cancel, and any escape (close, sign out). A node with only a forward action and no back is a trap.
4. Check failure edges: for every action that can fail, is there an edge to a state where the user can retry or leave? A failed action that lands on a spinner is a dead end.
5. Walk the graph looking for cycles with no exit: a validation loop that rejects every input, an auth redirect that bounces back to itself.
6. Test deep links and refresh: landing mid-flow via URL or reloading should not strand the user with no history; check that session state restores.
7. Mark each dead end with the node id and the missing exit, then specify the fix (a link, a retry, a cancel).
8. Re-walk the patched graph and confirm every non-terminal node has at least one exit.
9. Test each branch with the slowest and the failing backend, since most dead ends appear only under failure.
10. Check the flow at the smallest supported viewport, where dismiss controls often fall off-screen.

11. Walk the flow as a brand-new user with no history and as a returning user with partial state.

## Pitfalls

- Testing only the happy path, which by construction has no dead ends.
- A "Back" that returns to a stale screen rather than the previous step.
- Modal dialogs with no dismiss affordance on small screens or after an error.
- Sign-in walls that drop the user's in-progress state on return.
- A timeout screen with no way to resume where the session was lost.
- Reviewing the graph on paper and never clicking the real build, which hides rendering-level traps.
- Assuming a browser back button exists; in-app flows often replace history rather than push.

- A dead end that only appears after a successful action, which the happy-path test never reaches.

## Verification

    grep -c -- '->' flow.md; grep -cE 'dead end|missing exit' flow.md

Report every dead-end node with its missing exit and any node that has no back edge.
