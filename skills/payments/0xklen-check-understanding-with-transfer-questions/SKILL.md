---
name: check-understanding-with-transfer-questions
description: Use when you must confirm a learner actually understood, not just followed. Asks a variant of the taught case whose answer changes, and requires them to predict before running, so recognition is separated from understanding.
---

# Check Understanding with Transfer Questions

Asking "does that make sense?" gets a nod every time. Understanding shows when the learner predicts the outcome of a case they have not seen and turns out to be right.

## Procedure

1. Never re-ask the taught example; re-asking measures memory of the answer, not the rule.
2. Pose a variant that changes exactly one dimension: new input, reversed order, or one removed line.
3. Require a prediction before execution: "Before you run it — what prints?" Write the guess down.
4. Run it and compare the guess to the actual output, e.g. `python3 quiz/variant_3.py` after predicting `[2,2,2]`.
5. Advance when 3 of 4 variants are predicted correctly; below that, return to the worked example.
6. Ask the learner to state the rule in their own words and name one case where it does not hold.
7. Watch for confidence without accuracy — a fast, wrong prediction means the rule is mis-formed, not missing.
8. Record each guess and outcome so the pattern across variants is visible, not just the score.
9. If they pass all four but cannot state the rule, they memorised the shapes; go back to the example.
10. Keep the variants in `quiz/variants/` so the same checks can be reused with the next learner.
11. Have the learner predict the sign or direction of a change, not only the final value, for numeric rules.
12. Keep each variant inside one concept; a second concept makes a miss ambiguous.
13. Quote the learner's stated rule back to them, so they see their own model in words.
14. Vary the surface form but keep the rule the same, to catch shape-matching.
15. Keep a running tally of which rule the learner misses, so re-teaching targets the gap.
16. Re-check the same rule a week later, since one right answer is not retention.

## Pitfalls

- Accepting "yeah I get it" as the check.
- Asking a variant so different it tests a second concept, confounding the result.
- Letting the learner run first and reason backwards from the output.
- Treating one correct answer as mastery when it was a lucky guess.
- Asking the same variant twice and counting it as two checks.
- Rewriting the variant after seeing the guess, so the check becomes a discussion.
- Running the variant in the same sitting without a break, so it measures memory not transfer.
- Telling the learner the answer when the prediction misses, instead of letting the run show it.
- Scoring how well they explain the rule instead of whether the prediction was right.
- Varying the names as well as the logic, so you cannot tell what they matched on.
- Letting the learner revise their prediction after seeing the output.
- Treating a same-session pass as durable understanding.

## Verification

    ls quiz/variants/*.py | wc -l
    # passes when >= 4 variant files exist and the recorded guess/outcome log shows >= 3 matched

Report to the user: the variant that failed prediction and the exact rule the learner stated in their own words.
