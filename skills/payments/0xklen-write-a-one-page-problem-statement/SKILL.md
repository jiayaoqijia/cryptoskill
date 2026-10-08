---
name: write-a-one-page-problem-statement
description: Use when starting a project or initiative that needs a shared understanding of why it exists. Compresses it to one page a newcomer can read and challenge.
---

# Write a one-page problem statement

A project without a written problem drifts to whatever the loudest stakeholder wants. This skill fixes one page that names the user, the pain, the evidence, and the non-goals.

## Procedure

1. Open `problem-statement.md` and write one sentence of context a stranger could follow: who the product serves and what they are trying to do.
2. State the problem in the user's words, not the org's: quote a support ticket or an interview line, with the date.
3. Add the evidence: how many users hit it, how often, and what it costs (time, money, churn). A number without a source is an opinion.
4. State the current workaround and why it is failing, which reveals the real constraint.
5. Write the goal as a change in an observable measure, e.g. "reduce abandoned checkouts to under 15% by Q3".
6. List the non-goals explicitly — the audience, platforms, or use cases this will not serve — to head off scope creep.
7. Add the one-line bet from `set-kill-criteria-before-launch` so the page ties into how the work will be judged.
8. Keep it to one screen; if it runs to two pages, you are writing a spec, not a problem statement.
9. Name the smallest measurable change that would prove the problem is worth solving, so the page has a test.
10. Date the statement so readers know which evidence and assumptions were current.

11. Read the statement aloud to someone outside the team and fix every term they cannot define.

## Pitfalls

- Writing the solution as the problem ("we need a microservice") and calling it a statement.
- Evidence made of opinions from a meeting rather than support data or interviews.
- No non-goals, so every adjacent request gets pulled in.
- Framing the problem as the team's convenience instead of the user's cost.
- A goal with no baseline, so improvement cannot be shown later.
- Writing the statement once and never updating it, so it describes a problem that no longer exists.
- Filling the page with adjectives about the opportunity instead of a specific user cost.

- Citing a metric as evidence without its source file or query.

## Verification

    wc -l problem-statement.md; grep -ci 'non-goal' problem-statement.md

Passes at one screen with an evidenced problem and at least one explicit non-goal. Report the goal measure and its baseline.
