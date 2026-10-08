---
name: ask-vs-act-rubric
description: Use when deciding whether to proceed on a default or stop and ask the user. Scores reversibility, blast radius, and goal clarity to pick one, so trivial work is not blocked and risky work is not guessed.
---

# Ask vs Act Rubric

Blocking on a question that has an obvious default wastes the user's time; proceeding on a question whose answer changes what you build wastes it more. Score three axes and the action follows.

## Procedure

1. Score reversibility: `high` (edit a scratch file, run a read), `medium` (commit, change config, write outside repo), `low` (delete, deploy, send, pay, publish).
2. Score blast radius: `self` (this task only), `repo` (breaks others' builds), `external` (customers, third parties, money).
3. Score goal clarity: `clear` (one reasonable reading), `ambiguous` (two readings change the deliverable), `unknown` (you cannot name the deliverable).
4. Apply the rule:
   - `high`/`self`/`clear` → act now, no question.
   - `medium` in any axis → act on the smallest reversible version and state the assumption in your reply.
   - `low` reversibility OR `external` blast radius OR `ambiguous` goal → ask before acting.
5. When asking, ask exactly one question with a default stated: "I'll do X unless you want Y" — not an open essay prompt.
6. When acting under an assumption, label it in the final message: "Assumed the target is production-us; tell me if it was staging."
7. Never ask for information a tool can retrieve. If `git remote -v` answers "which repo", run it instead of asking.
8. If a required credential or a decision only the user can make (which account, which of two products) is missing, ask; do not invent one.

## Pitfalls

- Asking "what would you like me to do?" when the request already names a file and an action.
- Acting on an `ambiguous` goal and building the wrong interpretation at full scope instead of a reversible probe.
- Asking a compound question (three sub-questions) so the user must reply in prose.
- Treating "medium + external" as safe because the code change is small, ignoring that the effect leaves the machine.
- Guessing a default branch or environment name that a command would have revealed.

## Verification

    # Before a low-reversibility or external step, the transcript must contain an explicit user confirmation
    grep -c "confirmed by user" .hermes/handoff/<task-slug>.md
    # passes when it is >= 1 for any irreversible action taken

Report to the user: for each assumption you acted on, the axis scores and the one-line assumption you committed to.
