---
name: capture-a-lesson-as-a-minimal-repro
description: Use when a surprising bug or outage should be remembered. Reduces the incident to a committed 5-line reproducer plus the one-line rule, so the lesson is teachable and replayable instead of a story in chat.
---

# Capture a Lesson as a Minimal Repro

A retold incident fades and drifts. A committed five-line reproducer plus the rule it violates can be replayed by any future reader and re-run when the code changes underneath it.

## Procedure

1. Reduce the failure to the smallest program that still fails: strip framework, config, and I/O until under about five lines.
2. Save it under `lessons/YYYY-MM-DD-<slug>/repro.py` with the failure as an assertion or a non-zero exit.
3. Write the rule in one line in `README.md`: "a float sum of money silently drifts; use integer cents".
4. Record the trigger and the blast radius in two fields: how it was hit, who or what it affected.
5. Note the fix as a diff, then confirm the repro passes on the fixed code.
6. Mark the caveat: what the repro does not cover, so readers do not over-generalise from it.
7. Link it from the code it concerns, so the next editor finds it, e.g. a comment pointing at `lessons/`.
8. Add it to `lessons/run-all.sh` so CI re-runs every repro and catches a regression.
9. Title the directory with the failing date, not the fix date, so the order of discovery is preserved.
10. Keep exactly one rule per lesson; two rules in one repro make both untestable.
11. Run the repro on the pre-fix commit and paste the exact error string into the README.
12. Tag the lesson with the component it concerns, so it surfaces in that area of the repo.
13. Keep each lesson self-contained with no imports from the app.
14. Give the repro a name that states the symptom, not the fix.
15. Note the environment (language version, OS) the repro needs.
16. Link the repro from the postmortem so the two stay together.

## Pitfalls

- A repro that needs the whole service to run, so nobody reruns it.
- Retelling the timeline instead of reducing the cause.
- An over-broad rule ("floats are bad") that the five lines do not actually show.
- Filing the lesson where the affected code cannot find it.
- A repro with no assertion, so a silent change to the output goes unnoticed.
- Combining the incident and a wish-list of adjacent fixes into one file.
- A repro that passes on a different platform than the one that failed.
- Writing the rule in jargon the next intern cannot parse.
- Forgetting to record the version or commit where the failure happened.
- A name that gives away the fix, spoiling the exercise.
- A repro that only fails on one machine with no note of why.
- A postmortem and a repro that drift apart.

## Verification

    python3 lessons/*/repro.py ; echo "exit=$?"
    # passes when the repro exits non-zero before the fix commit and zero after it

Report to the user: the repro path, the one-line rule, and the pre/post-fix exit codes.
