---
name: build-a-prompt-regression-suite
description: Use when a prompt, system message, or few-shot set changes and must not break past behaviour. Runs a small golden set in CI on every edit.
---

# Build a Prompt Regression Suite

Prompts are code that ships without a compiler. A golden set of inputs and expected properties catches the edit that fixes one case and breaks fifteen others.

## Procedure

1. Curate 20–100 cases from real traffic or real failures, each with a must-hold property: exact string, JSON schema, classification label, or a judge rubric.
2. Assert on properties, not full strings, so harmless wording changes do not fail the suite. For structured output, validate the schema:
   ```python
   import jsonschema
   jsonschema.validate(json.loads(out), schema)   # fails if the model added a field
   ```
3. Pin the model version in the run; an upstream model change is a variable you did not intend to test.
4. Run at temperature 0 with >=2 seeds if the provider is not fully deterministic, and treat a flip as flaky, not a pass.
5. Store the suite next to the prompt and run it in CI on the prompt file's diff:
   ```bash
   python3 -m pytest tests/prompts -q --model gpt-x-2024-08
   ```
6. On failure, diff the case list against the previous run: a new failure is a regression, a fixed case is a win, a flaky case needs a looser assertion.
7. Keep the suite fast (<2 min) and cheap; a slow suite gets skipped, which is worse than no suite.

```bash
git diff --name-only HEAD~1 | grep -q prompts/ && pytest tests/prompts -q || echo "no prompt change"
```

## Pitfalls

- Exact-string assertions fail on trivia (a trailing period) and train people to ignore the suite.
- A golden set drawn only from the happy path never covers the failure the edit is meant to fix.
- Testing against a floating model alias means the suite can break with no change on your side.
- Growing the suite without pruning makes it slow and noisy; retire cases no longer relevant.
- Asserting the model reproduces one specific phrasing over-constrains it and blocks legitimate improvements.

## Verification

    pytest tests/prompts -q   # all pass on the current prompt; 1+ fail after a bad edit

Report: "64-case prompt suite in CI at 41s; the last prompt edit failed 3 cases (empty-input handling) before merge."
