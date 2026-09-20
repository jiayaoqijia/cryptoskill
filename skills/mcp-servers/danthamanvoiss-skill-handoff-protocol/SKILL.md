---
name: skill-handoff-protocol
description: Standardize a lightweight handoff block so one skill's output becomes clean input for the next skill.
version: 0.1.0
tags: [core, workflow, handoff, portability]
---

## Purpose

Document a simple, reusable handoff structure that lets one skill pass only the most relevant context, decisions, and unknowns to the next skill in a chain.

## Use when

- One skill's draft or plan will feed another skill.
- You want to reduce repeated prompting across multi-step workflows.
- Outputs need to stay portable between SalesPortl and other harnesses using the same skill suite.

## Required inputs

- Source skill name and its completed output or working draft.
- The downstream objective the next skill needs to accomplish.
- Any key decisions, constraints, approvals, or unknowns already identified.

## Safety/authority

- Keep the handoff factual and traceable to the source skill output.
- Separate confirmed decisions from open questions or placeholders.
- Do not upgrade authority during handoff; draft-only remains draft-only unless the user explicitly changes it.

## Workflow

1. Capture the source skill name and the downstream objective.
2. Distill the source output into only the decisions, constraints, and assets the next skill actually needs.
3. List open questions, approval gaps, and placeholders so the downstream skill does not treat them as settled facts.
4. Emit a compact handoff block using the same headings each time.
5. When relevant, include which context source was used so downstream skills know whether the input came from harness-native context, root defaults, or a client folder.

## Output format
```
[Skill handoff]
Source skill: ...
Next objective: ...
Context source: ...
Key decisions: ...
Constraints / approvals: ...
Assets or references: ...
Open questions / unknowns: ...
```

## Quality checks

- The handoff is short enough for the next skill to consume quickly.
- Decisions, constraints, and unknowns are clearly separated.
- Source attribution is present so downstream skills can trace the origin.
- The structure is simple markdown guidance, not a schema or executable format.

## Related skills

agency-router, context-loader, output-organization-guide, cross-harness-collaboration-notes
