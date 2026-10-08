---
name: scope-a-spike-before-building
description: Use when a requirement rests on an unknown that could invalidate the plan. Defines a time-boxed spike with one question, a stop condition, and a throwaway artifact.
---

# Scope a spike before building

When the plan depends on an unknown, building the real thing tests the wrong thing. This skill opens a time-boxed spike that answers one question and is then thrown away.

## Procedure

1. Write the single question the spike must answer in `spike.md`: "can we read the partner API's paging cursor without an admin token?" One question, or split it.
2. Define what a yes and a no would each mean for the plan; a spike whose answer changes nothing is curiosity, not research.
3. Time-box it in hours (not days) and state the stop condition: when the box expires, stop and report, even with an inconclusive answer.
4. Declare the output type: a one-paragraph answer, a throwaway script under `spikes/`, and a link to the evidence (a log, a response, a measurement).
5. Forbid production polish: no tests, no error handling, no naming; the code is scaffolding to be deleted.
6. Run the smallest experiment that discriminates yes from no — hit the API once, not a full integration.
7. Report the answer plus the confidence and what would raise it; an inconclusive spike is a valid result.
8. Fold the answer back into the estimate or spec, then delete the spike branch so it does not leak into the build.
9. Write down what you already know, so the spike tests the unknown and not the known again.
10. Capture the commands and raw responses you ran, so the answer is reproducible by someone else.

11. Timebox the writing as well as the running; a spike that spends an hour on the doc has already exceeded its box.

## Pitfalls

- A spike that grows into the feature because the code "mostly works already".
- No stop condition, so the time box becomes the whole sprint.
- Answering a question the plan did not depend on, which is a distraction.
- Keeping the spike code as production, inheriting its missing error handling.
- Reporting only a yes/no without the evidence trail, so nobody can trust or reproduce it.
- Running the spike on production data without a snapshot, risking real state for a throwaway answer.
- Spending the box polishing output instead of answering the one question it was opened for.

- Reusing the spike's auth or credentials in mainline code without raising their scope.

## Verification

    grep -c 'question:\|box:\|stop:' spike.md; git branch --list 'spike/*'

Report the question, the answer with evidence, the box it stayed inside, and whether the spike branch was deleted.
