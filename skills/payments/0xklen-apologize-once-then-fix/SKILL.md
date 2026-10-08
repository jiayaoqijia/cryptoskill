---
name: apologize-once-then-fix
description: Use when you caused an error, missed a commitment, or broke something. Acknowledge it in one line, then spend the rest of the message on the fix.
---

# Apologize once, then fix

Regret does not restore a lost file. One line of ownership clears the air; the rest of the message should return value in the form of a fix and a prevention.

## Procedure

1. Acknowledge the failure in one sentence, naming the act: "I overwrote the config; that is on me."

2. Do not explain or justify inside the acknowledgement; save cause for the fix section.

3. State what you have already done to contain it — e.g. restored from `git reflog` — and whether it worked.

4. Give the corrective action with owner and deadline.

5. Offer the prevention: the check or guard that stops a repeat.

6. Keep the whole message under ten lines; the fix earns more space than the regret.

7. Do not repeat the apology later in the thread; one acknowledgement, then work.

## Pitfalls

- A paragraph of apology delays the fix the reader actually needs.
- "I'm sorry you feel that way" deflects; own the act instead.
- Over-explaining your intent reads as excuse-making.
- Apologising without a prevention invites the same error next week.
- Repeating the apology adds noise; fix it and move on.

## Verification

    head -3 postmortem.md   # names the act, then containment, then the fix

One line of ownership, then the containment, the fix, and the prevention.
