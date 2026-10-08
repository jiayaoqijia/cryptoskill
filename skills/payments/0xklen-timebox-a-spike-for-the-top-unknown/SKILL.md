---
name: timebox-a-spike-for-the-top-unknown
description: Use when an unknown could change the whole estimate and thinking about it is not resolving it. Runs a fixed, time-boxed investigation that ends in a decision, not a half-built feature.
---

# Timebox a spike for the top unknown

The unknown that dominates your uncertainty range should be attacked, not budgeted. A spike is a deliberately throwaway investigation with a time box and a question — it produces knowledge, and its code is not shipped.

## Procedure

1. Pick the single largest-uncertainty item from the plan; do not spike everything. One or two spikes maximum.
2. Write the decision question the spike must answer, with a pass/fail: "Can library Y index 1M rows under 2s? yes/no."
3. Set the time box before starting — hours, not days. Two to four hours is typical; if it needs more, the unknown is really a project and should be re-scoped.
4. Put a literal timer on it:

       timeout 14400 ./spike.sh   # hard 4h stop, exit 124 means it hit the box

5. Work only enough to answer the question. Do not build error handling, tests, or a UI — those are for the real task if the answer is yes.
6. Record the answer and the evidence in the plan: "spike 2026-02-08: library Y indexed 1M rows in 1.7s on m5.large → yes, use it."
7. Fold the answer back into the estimate, replacing a wide range with a tight one, then delete or park the spike branch: `git branch -D spike/library-y`.
8. If the box expires with no answer, that itself is information: the unknown is larger than assumed. Widen the estimate and say so.

## Pitfalls

- Letting the spike grow into the feature; throwaway code that ships is a liability.
- No written question, so the spike "explores" and ends without a yes/no.
- No hard stop, so the box is a suggestion and the spike eats a week.
- Spiking a low-uncertainty item because it is comfortable, while the plan's real risk sits untouched.
- Keeping the spike's conclusions only in the branch, so the next person repeats the work.
- Spiking with no written decision question, leaving a pile of code and no answer.

## Verification

    grep -n 'spike 2026' notes/plan.md
    # passes when each spike records date, question, result, and the estimate change it caused

Report the question, the time box, the answer with its evidence, and the new tighter estimate.
