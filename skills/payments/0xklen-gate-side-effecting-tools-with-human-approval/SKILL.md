---
name: gate-side-effecting-tools-with-human-approval
description: Use when an agent step writes, spends, deletes, or sends something irreversible. Pause for explicit human approval before the side effect, showing exactly what will change.
---

# Gate side-effecting tools with human approval

An agent that can send money, delete rows, or post publicly is one bad guess from damage no retry undoes. Insert a human gate before the effect, present the exact diff, and block until a decision arrives.

## Procedure

1. Classify tools by blast radius: `read` (none), `local-write` (reversible), `remote-write` / `spend` / `send` (irreversible or external).
2. Gate every irreversible class. Reads and reversible local writes may proceed without a prompt.
3. Before the gated call, render the precise effect: the command, the target, the row count or amount, and the pre-state.
4. Show the diff, not a summary: `DELETE FROM sessions WHERE expires_at < now() -- affects 1,204 rows`.
5. Offer three explicit outcomes: approve once, approve for this run, or reject. Default to reject on no answer.
6. Bind approval to a specific call — an approved delete of 1,204 rows does not authorise the next delete.
7. Re-prompt if the arguments change between approval and execution; approval of a stale arguments is no approval.
8. Log the decision: `gate=delete-sessions decision=approve-once approver=user turn=11`.
9. For batch fan-out, gate the batch as one decision with the full item list, not one prompt per item.
10. Record a timeout as a rejection, not an implicit approve; an unanswered gate must not let the effect through.

## Pitfalls

- Summarising the effect as "clean up old sessions" so the human cannot see the row count or table.
- Caching one approval and reusing it for a different command or target in the same run.
- Asking after the write has already landed, which turns a gate into a notification.
- Defaulting to approve when the user does not respond in time.
- Prompting for a reversible local write and training the human to click approve without reading.
- Letting a fan-out child take the gated action under a parent's blanket approval it never received.
- Showing the proposed command in a language the approver cannot read, so the decision is nominal.
- Filing the approval in a chat message that scrolls away instead of the action log beside the call.

## Verification

    grep -c 'gate=.*decision=' notes/action.log   # every irreversible call has a matching decision line

Report each gated action with its target, the shown effect, and the human's decision.
