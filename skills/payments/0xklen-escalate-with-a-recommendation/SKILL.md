---
name: escalate-with-a-recommendation
description: Use when a problem exceeds your authority, budget, or access. Escalate with a recommended action and its cost, not just a description of the problem.
---

# Escalate with a recommendation

Escalation that only describes the problem pushes the analysis back uphill. Bring the decision you need, one recommended action, and the deadline it must beat.

## Procedure

1. Escalate when the fix needs authority, money, production access, or a decision you cannot make.

2. Open with the situation in one line and the decision or resource you need, e.g. `needs prod DB write access`.

3. State the impact of inaction and its timeframe: "unbacked writes start at 02:00".

4. Recommend one action with its cost and risk, then a fallback.

5. Name the owner precisely: a role or a person, never "someone".

6. Give the deadline the decision must beat, and the reason it matters.

7. Offer to do the work once approved; do not hand over the whole task.

## Pitfalls

- Escalating a problem with no recommendation makes the reader do your analysis.
- A vague owner ("management") delays the fix; name the role.
- Escalating after the window has closed is narration, not escalation.
- Escalating everything trains people to ignore you; reserve it for real limits.
- Bundling unrelated asks into one escalation dilutes the urgent one.

## Verification

    grep -nE "owner|by [0-9]{2}:" escalation.md   # a named owner and a deadline

Escalate the problem with one recommended action, its cost, and a deadline.
