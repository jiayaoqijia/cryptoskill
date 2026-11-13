---
name: case-construction
domain: prompt-engineering/case-construction
trigger: "Building eval cases from the task's real failure surface."
anti_trigger: "Not for prompt engineering against cases, and not for judge design."
scope: "Building cases from real failure modes, not ease."
status: seedling
---

# Case construction

## Standard

Cases come from the task's real surface or they measure nothing. The strongest sources are, in order: real production requests with known outcomes, real requests where the current model failed, edge cases that practitioners in the domain know break systems of this class, and only as a last resort invented examples that merely illustrate the task. A suite of invented examples evaluates a model's ability to handle invented examples, and its ranking diverges from production ranking in ways that only surface after the choice is made.

Coding cases deserve specific discipline, because code evaluation has a structure human-style grading lacks: task-native artifacts — files, real function signatures, real dependency constraints — make a case reproducible and a verdict checkable. Cases built on real structure also resist the two classic corruptions of code evals: the imaginary API that no library contains, and the solve-by-pattern-match that a case copied from a tutorial invites. Failing cases are more informative than passing ones: a suite of all-pass cases cannot rank models, so the difficult tail is where discrimination lives.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/evaluate> and <https://github.com/EleutherAI/lm-evaluation-harness>.

## Decision rules

- Sample cases from the real request population, and record the sampling story.
- Include known-failure cases at a share that reflects their production frequency.
- Build code cases on task-native artifacts with real signatures and dependencies.
- Prefer failing and borderline cases; a suite that everything passes ranks nothing.
- Record provenance per case: where it came from, when, and who vouched for it.
- Freeze the set before comparing models; additions are a new version of the suite.

## Procedure

1. Draw the candidate pool from production requests and domain experts' edge lists.
2. Classify each candidate by construct and difficulty.
3. Build each case on task-native structure with a stated acceptance check.
4. Balance the set to the production frequency of its categories.
5. Record provenance and the date for every case.
6. Freeze and version the set; log every later addition as a version bump.

## Anti-patterns

- Invented examples as the primary source.
- Cases copied from documentation the model was trained on.
- All-easy suites that produce 98 percent everywhere.
- Code cases against APIs that do not exist.
- Editing a frozen suite mid-comparison to punish one model.

## Done checklist

- [ ] Sampling story recorded.
- [ ] Failure share reflects production.
- [ ] Cases on task-native artifacts.
- [ ] Difficulty tail present.
- [ ] Provenance and date per case.
- [ ] Suite frozen and versioned.

## Sources

- Claude evaluation guidance: <https://docs.anthropic.com/en/docs/about-claude/evaluate>
- Evaluation harness case practice: <https://github.com/EleutherAI/lm-evaluation-harness>
- Human-eval style coding evaluation: <https://github.com/openai/human-eval>
