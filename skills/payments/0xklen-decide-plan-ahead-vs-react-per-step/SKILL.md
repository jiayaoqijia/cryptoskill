---
name: decide-plan-ahead-vs-react-per-step
description: Use when an agent must choose between committing to a written plan and reacting step by step. Pick per task by how much of the path is knowable up front.
---

# Decide plan-ahead vs react per step

Planning every step wastes tokens when the path is obvious; reacting blindly burns budget when the path is long and known. Choose the mode from information you already have, and switch when it changes.

## Procedure

1. Ask one question: can I name the next two or three steps with confidence right now? If yes, plan; if no, react.
2. Plan-ahead when the task is multi-step, deterministic, and expensive to restart — e.g. a migration with fixed phases.
3. React when the next step depends on what the last tool returned and you cannot predict it — e.g. exploratory debugging.
4. Write the plan as a numbered list with a completion check per step, then execute against it; do not re-derive the plan from scratch each turn.
5. In react mode, keep a running scratchpad of observed facts so you do not loop back over ground already covered.
6. Switch modes on evidence: two consecutive surprises mean the plan is stale, so re-plan; three closed steps with no surprise mean stop reacting and commit.
7. Cap re-planning. After the second rewrite of a plan, either finish the current approach or escalate — churning plans is a hidden loop.
8. Log the mode per phase: `phase=2 mode=plan steps=4` or `phase=3 mode=react reason="unknown error"`.
9. When the brief already fixes every step, do not re-derive a plan — execute the given order and only switch to react if a step fails.
10. Record the trigger for any switch, so a reviewer can tell a deliberate replan from a drift into thrashing.

## Pitfalls

- Writing a ten-step plan for a task whose first step may invalidate steps two through ten.
- Reacting one tool call at a time through a procedure that was fully specified in the brief.
- Re-planning silently every turn, so the plan never accumulates and budget vanishes.
- Committing to a plan after the environment has contradicted two of its assumptions.
- Confusing "I have a plan" with "I have verified the plan works" — the first step still needs a check.
- Letting react mode drift into thrashing when a single clarifying question would reset it.
- Re-planning because a step is slow rather than because it is wrong; slowness is not evidence the plan is stale.
- Treating the plan as fixed once written, so a step that clearly cannot succeed is forced through anyway.

## Verification

    grep -E 'phase=[0-9]+ mode=(plan|react)' notes/action.log | wc -l   # equals the number of phases run

Report the mode chosen per phase and the trigger that caused any switch between them.
