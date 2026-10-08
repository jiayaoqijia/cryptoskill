---
name: distinguish-observation-from-inference
description: Use when writing a report that mixes what you saw with what you concluded. Separate the two so a reader can re-check the raw facts behind your reasoning.
---

# Distinguish observation from inference

Readers need to know where the evidence ends and your reasoning begins. This skill keeps that seam visible so a conclusion can be audited against the observations it stands on.

## Procedure

1. Draft the report normally, then re-read it and tag each sentence `[OBS]` (you directly saw it) or `[INF]` (you concluded it).

2. An `[OBS]` names its instrument and its output: `[OBS] tail -1 app.log -> "OOM killed pid 4412"`. An `[INF]` names its premises: `[INF from OBS-3,4] the worker exceeds its 512MB limit`.

3. Keep the tags inline, or group all `[OBS]` above a rule and all `[INF]` below it.

4. Check that every `[INF]` cites at least one `[OBS]`. An inference citing only another inference is speculation and must be grounded or dropped.

5. Strip words that smuggle judgement into observations: "clearly", "obviously", "just", and causal verbs like "caused" turn a fact into a conclusion.

6. Prefer the raw string over a paraphrase in observations; a reader must be able to confirm it themselves.

7. Before sending, read only the `[OBS]` lines in order. If they do not on their own imply the `[INF]` lines, either add the missing observation or weaken the inference until they do.

## Pitfalls

- "The service is down" is an inference; "curl returned exit 7 at 14:03" is the observation.
- Paraphrasing a log in an observation loses the exact token a reviewer needs.
- A confident inference tempts you to delete the plain observation under it — keep both.
- Tagging a restated conclusion as an observation hides the reasoning step that produced it.
- Mixing units or timestamps between obs and inference makes the link hard to follow.
- A sentence that welds an observation to a cause needs splitting into two tagged lines.

## Verification

    grep -c "\[OBS\]" report.md; grep -c "\[INF" report.md   # every INF sits below an OBS

Report with tags intact; if a reader cannot rebuild your inference from the observations, rewrite it.
