---
name: set-kill-criteria-before-launch
description: Use when a feature, experiment, or product bet goes live without a stopping rule. Defines the metric, threshold, and date that end it, agreed before the team is invested.
---

# Set kill criteria before launch

Without a pre-agreed stopping rule, sunk cost decides instead of data. This skill writes the conditions that end a bet, while the team can still be honest about them.

## Procedure

1. State the single bet in one line: "we believe X will make Y happen". No multi-clause beliefs; split them.
2. Pick one primary metric that moves if the bet is right, plus one guardrail that must not regress (e.g. retention, error rate). More than one primary metric invites cherry-picking.
3. Set the threshold and the measurement date before launch: "if day-30 activation is under 25%, we stop", with the cohort and window named.
4. Add a cost criterion: a maximum spend or engineer-weeks before the decision is forced, so effort cannot creep indefinitely.
5. Write the options explicitly: `continue`, `iterate once with a named change`, or `stop and unwind`. Pre-committing the third removes the negotiation.
6. Name who decides and who can veto, so the call does not default to the loudest person.
7. Record the stopping plan: how the feature is disabled (flag off), who tells users, and what data is kept.
8. Re-read the criteria six weeks in and check they still describe the bet; if the bet changed, re-cut them.
9. Publish the criteria somewhere the team sees them, not in a private doc that only the author rereads.
10. Set an interim checkpoint before the final date, so a failing bet is noticed early rather than at the deadline.

11. Write the criteria in the language of the metric, so anyone can compute them without interpretation.

## Pitfalls

- Choosing metrics after seeing early data, which is fitting the rule to the result.
- Setting the bar so low that any outcome passes; the criterion must be able to fail.
- "We'll review it" with no date, which means never.
- Killing on a guardrail blip without checking the sample size or seasonality.
- No unwind plan, so a stopped feature lingers half-live for months.
- Writing criteria that only the launch author can evaluate, so no one else can call the stop.
- Treating a single early spike in the metric as proof the bet worked.

- Killing a bet on a metric the team can still influence after the measurement window.

## Verification

    grep -c 'primary metric\|guardrail\|date:\|threshold' kill.md; grep -cE 'continue|iterate|stop' kill.md

Report the primary metric, its threshold and date, the decision owner, and the flag used to disable the feature.
