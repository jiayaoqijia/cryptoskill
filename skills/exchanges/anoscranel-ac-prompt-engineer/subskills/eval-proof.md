---
name: eval-proof
domain: prompt-engineering/eval-proof
trigger: "When you must know whether a prompt edit, model swap, or retrieval change actually improved anything."
anti_trigger: "Triaging one specific failing output right now — that is debugging, not measurement."
scope: "Proving a prompt change helped: golden sets, oracle hierarchy, judge limits, statistical gates, and CI wiring."
status: "seedling"
---

# Evals and plays: prove the prompt got better

## Standard

A prompt is a fitted object with an expiry date; treat "what works" as a claim you must
measure (<https://ai.google.dev/gemini-api/docs/prompting-strategies>).
Maintain a golden set of 25-50+ real inputs with known-good outputs, covering key use
cases, known failures, and production edge cases; version it with the code and refresh
it from production traffic (<https://developers.openai.com/api/docs/guides/prompt-engineering>; https://www.braintrust.dev/articles/llm-evaluation-guide). Run it before and after
every change. Version prompts in code with typed inputs and tests; OpenAI is retiring
stored prompt objects in favor of code-managed prompt builders by November 2026 (OpenAI
guide, live-fetched 2026-10-21). For CI, promptfoo-style gates on every pull request
that touches prompts are the dominant stack.

## Decision rules

Prefer graders in this order: deterministic code checks; formal policy; reference
answers; rubric-graded model judges; pairwise model judges; humans last for subjective
quality (<https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>).
Model judges exhibit position, verbosity, and self-preference bias: randomize order, use
multiple judges, calibrate against a blind human gold set, and keep judges advisory on
safety and policy calls (MT-Bench, arXiv 2306.05685).
Zero failures in n trials only bounds the failure rate near 3/n at 95% confidence, so
"30 passes" is not proof (rule of three).

## Procedure

1. Freeze the set: golden regression cases, a challenge set, and an untouched holdout.
2. Pin the candidate: same model snapshot, temperature 0, same retrieval state.
3. Run old and new prompts on the same cases; pair the runs.
4. Grade with determinism first, judges second, humans for the subjective residue.
5. Decide with a predeclared bar (pass rate, non-inferiority margin), not vibes.
6. Ship behind a small canary or staged rollout for risky traffic.

## Anti-patterns

- "Looks better on two examples" — anecdotes are not evidence.
- One aggregate score; aggregates mask dangerous slice failures.
- A judge model from the same family grading its family without calibration.
- Reusing the holdout set for iteration; it stops being a holdout.

## Done checklist

- [ ] A versioned golden set exists and covers production failure modes.
- [ ] Old and new were compared on identical cases and pinned settings.
- [ ] The grading mix follows the oracle hierarchy.
- [ ] The decision bar was declared before the run.

The proof needs a held-out set that was never inspected while the prompt was being edited, because a prompt tuned against a visible set has learned that set rather than the task. The size of the held-out set matters less than the discipline of not looking at it.

## Sources

- <https://ai.google.dev/gemini-api/docs/prompting-strategies>; <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>; <https://www.braintrust.dev/articles/llm-evaluation-guide>; <https://developers.openai.com/api/docs/guides/prompt-engineering>
