---
name: choose-sampling-params-per-task
description: Use when setting temperature, top_p, and related sampling knobs. Choose them from the task's tolerance for variance, not by habit, and record the choice alongside the prompt.
---

# Choose sampling params per task

Temperature is a task parameter, not a preference. Classification wants the mode; creative work wants spread; either setting can be wrong for the other task.

## Procedure

1. Classify the task by its tolerance for variance: deterministic (extraction, classification, tool arguments) versus exploratory (brainstorming, naming, drafting options).

2. For deterministic tasks set `temperature=0` and leave `top_p` at its default (1.0). Change only one knob; adjusting both muddies the effect.

3. For exploratory tasks, start at temperature ~0.7-1.0 and tune against the diversity of *useful* output, not novelty for its own sake.

4. For structured/JSON output, keep temperature low (0-0.2) regardless of any "creativity" goal — variance here shows up as malformed or off-schema values.

5. Generate several samples (`n > 1`) when you need options, rather than raising temperature and hoping one is good; select among them.

6. Fix and record the parameters with the prompt and model version. A score is meaningless if the sampling knobs moved with it.

7. Re-check the setting when the model version changes; providers retune, and a temperature that behaved one way can shift.

8. For a task that mixes needs, split the call: one low-temperature pass to extract the facts, one higher-temperature pass to draft from them.

9. Expose the knob to product only as named modes (`fast`, `creative`), not raw numbers, so the choice stays justified rather than copy-pasted.

## Pitfalls

- Copying someone else's `temperature=0.7` without knowing the task; it is a default, not a recommendation.
- Raising temperature to "get better answers" on extraction, then adding retries to clean up the mess you created.
- Tuning `top_p` and `temperature` together, so you cannot tell which one moved the output.
- Using high temperature for a tool-calling step, producing invented argument values.
- Assuming temperature=0 gives identical runs; it lowers variance, it does not zero it.
- Setting the temperature from a model's default rather than the task's needs, so one knob serves both a classification and a brainstorm.
- Forgetting that `top_k` and `presence_penalty` also add variance; more knobs is not more control.
- Changing the temperature and the prompt in the same test, then attributing the result to the wrong one.

## Verification

    python3 -c "import json;cfg=json.load(open('params.json'));print({k:v['temperature'] for k,v in cfg.items()})"   # each task has an explicit, justified value

Report: "extraction temperature=0, brainstorm=0.9, tool-calls=0; params recorded beside each prompt version and re-validated after the model bump."
