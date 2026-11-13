---
name: decompose-job
domain: prompt-engineering/decompose-job
trigger: Before writing a prompt for any job with more than one deliverable, and whenever one prompt keeps failing at several duties at once.
anti_trigger: A single short request with one checkable output.
scope: Deciding how many prompts or steps a job needs, and which logic belongs in the prompt text versus in code, tools, or retrieval.
status: seedling
---

# Decompose the job

## Standard

Decomposition converts one opaque failure into several locatable ones: split tasks so
each intermediate output is individually validatable (<https://ai.google.dev/gemini-api/docs/prompting-strategies>). Write prompts at
the "right altitude": not brittle hardcoded if-else logic, not vague guidance
(Anthropic, https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
Complexity belongs in code: if a human cannot definitively pick which tool applies, an
agent cannot either, so curate a minimal tool set and move branching into code (same
source). The production unit is a typed contract (objective; authority policy; context;
examples; tool and permission contracts; output schema), and every assembly layer must
earn its cost (<https://developers.openai.com/api/docs/guides/prompt-engineering>).

Primary sources: <https://www.anthropic.com/engineering/building-effective-agents> and <https://developers.openai.com/>.

## Decision rules

| Signal | Decision |
|---|---|
| One prompt retrieves, decides, and formats | Split: retrieve; decide; format |
| A step's output can be checked in code (parse, schema, regex) | Keep it as its own step and check it mechanically |
| Two duties disagree on tone, format, or audience | Split them; one prompt cannot serve two contracts |
| Same input re-processed by many runs | Move stable rules into a typed config or tool, out of the text |
| A human expert could not do the step with the given context | No prompt fixes it; add information or retrieval first |

## Procedure

1. List the job's deliverables. One deliverable per candidate step.
2. For each step, write its check: what makes this step's output acceptable, in words a
 test or a reviewer can apply.
3. Classify each step: prompt (judgment or language), code (rules, parsing, branching),
 tool (lookup, side effect), retrieval (missing facts). Logic that is pure branching
 goes to code.
4. Draw the handoffs between steps as data: typed fields, not prose summaries, where
 possible.
5. Prompt only the judgment steps. Write each of those as its own small prompt.
6. Add the fallback per step: what the step emits when it cannot answer (abstain,
 escalate, retry once).

## Anti-patterns

- One mega-prompt doing retrieve-plus-decide-plus-format (the classic failure shape).
- Decomposing into steps whose outputs nobody can check.
- Stuffing edge cases into the prompt instead of fixing the classifier or tool call.
- if-else chains in prose where a lookup table in code is cheaper and exact.
- Splitting so finely that reassembly costs more than the original failure.

## Done checklist

- [ ] Every step has exactly one deliverable and one written check.
- [ ] Every rule-based branch lives in code or config, not in prompt text.
- [ ] Each step's failure mode names its fallback.
- [ ] A mid-chain output can be inspected without rerunning the whole job.

## Sources

- <https://www.anthropic.com/engineering/building-effective-agents>
- <https://developers.openai.com/>
