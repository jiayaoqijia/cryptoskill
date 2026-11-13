---
name: model-knobs
domain: prompt-engineering/model-knobs
trigger: When choosing the model class, temperature, reasoning effort, or snapshot for a prompt, and when a model upgrade breaks a working prompt.
anti_trigger: Editing the prompt text itself, or evaluating whether a prompt change helped.
scope: Choosing the model class and generation settings and pinning snapshots, knowing the rules invert between reasoning and instruction models.
status: seedling
---

# Model and reasoning knobs

## Standard

Pick the model class first; it decides which prompt rules apply. OpenAI's analogy:
a reasoning model is a senior coworker you hand a goal; a GPT-class instruction model is
a junior who needs explicit steps
(https://developers.openai.com/api/docs/guides/prompt-engineering). On reasoning models,
keep the prompt simple, give the goal and constraints, and do not add chain-of-thought
wording; OpenAI states it "may not enhance performance (and can sometimes hinder it)"
(https://developers.openai.com/api/docs/guides/reasoning-best-practices). Anthropic's
extended-thinking doc likewise prefers general instructions over prescriptive thinking
steps. For reproducibility, pin a dated model snapshot (<https://developers.openai.com/api/docs/guides/prompt-engineering>). ⚠️ Temperature 0 cuts variance but is not documented as deterministic. On Gemini 3.x, keep
temperature, topP, and topK at defaults; changing them degrades complex reasoning
(<https://ai.google.dev/gemini-api/docs/prompting-strategies>).

Primary sources: <https://developers.openai.com/> and <https://ai.google.dev/gemini-api/docs/prompting-strategies>.

## Decision rules

| Situation | Knob |
|---|---|
| Multi-step reasoning, math, planning, agentic work | Reasoning class; goal-plus-constraints prompt |
| Formatting, extraction, short classification, cheap bulk work | Instruction class; explicit steps are legal there |
| Regression testing, comparisons, CI | Temperature 0 and a pinned snapshot |
| Creative spread wanted | Raise temperature deliberately, never by accident |
| New model version drops | Treat as a migration: rerun the golden set before rewording |

## Procedure

1. Write the task's failure mode down (reasoning depth vs instruction obedience).
2. Pick the class, then a dated snapshot; record it next to the prompt in code.
3. Set temperature 0 for anything measured or compared.
4. On reasoning models, delete all chain-of-thought wording; keep goal, constraints,
 output contract.
5. On upgrades: run old-model and new-model on the same fixed cases before touching the
 prompt, so model drift and prompt drift never confound (behavioral change
 control).

## Anti-patterns

- Carrying wording tuned on one model family to another; micro-copy does not transfer.
- Twiddling samplers to fix an information problem; add the missing fact instead.
- Paying reasoning effort for a task a cheap instruction model passes at ceiling.
- Running comparisons unpinned; you measured the model calendar, not your edit.

## Done checklist

- [ ] Model class chosen from the failure mode, not habit.
- [ ] Snapshot and temperature recorded beside the prompt.
- [ ] Reasoning-model prompts carry no step-by-step wording.
- [ ] Every upgrade goes through the old-vs-new paired run first.

The knob that most often matters is the one that is not a number: whether the model is asked to reason before answering changes the output more than a temperature adjustment does, and the setting is usually a structural choice rather than a parameter. Recording which structural choice was made is more useful than recording the sampler values.

## Sources

- <https://developers.openai.com/>
- <https://ai.google.dev/gemini-api/docs/prompting-strategies>
