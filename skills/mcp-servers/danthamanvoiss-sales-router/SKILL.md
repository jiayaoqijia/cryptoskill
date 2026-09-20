---
name: sales-router
description: Route sales tasks to the right sales skill sequence with stage-specific clarifying questions and minimal overlap.
version: 1.0.0
tags: [core, routing, sales, v1]
---

## Purpose

Choose the right 1–3 sales skills after a small amount of sales-specific clarification so outreach, qualification, discovery, follow-up, and handoff work do not blur together.

## Use when

- The main router has already identified the request as primarily a sales task.
- You need to decide which sales stage the task belongs to.
- The user wants a sales output but has not named the exact skill yet.

## Required inputs

- Sales objective and requested deliverable.
- Funnel stage or best current guess [if known].
- Audience, offer, and any known constraints or approvals.

## Safety/authority

- Keep claims, pricing, guarantees, and competitor statements grounded in approved context only.
- Treat all external send actions as draft-only until explicitly approved.
- Do not force later-stage sales skills when early qualification or discovery is still missing.

## Workflow

1. Clarify the minimum sales specifics needed: who the audience is, what stage the prospect/client is in, and what output is needed.
2. Map the task to the nearest sales stage:
   - early qualification: `lead-qualification`
   - discovery prep: `discovery-call-prep`
   - prospecting or follow-up messaging: `outreach-sequence-draft`, `meeting-followup-draft`, or `objection-handling-draft`
   - scheduling and conversion: `appointment-setting-playbook`
   - proposal or handoff: `proposal-scope-draft` or `salesportl-account-handoff`
   - pipeline cleanup: `pipeline-hygiene-review`
3. Select 1–3 skills maximum, usually one execution skill plus one adjacent support skill.
4. If the task includes approved message quality review, optionally pair with `anti-slop-content-review`.
5. If the exact requested sales skill is unavailable, choose the closest same-stage alternative that is available or ask a clarifying question.

## Output format

```
- Sales task type: ...
- Clarifications needed: ...
- Selected skills (1-3): ...
- Optional quality layer: ...
- Missing inputs: ...
- Next step prompt: ...
```

## Quality checks

- The selected skills match the real sales stage.
- The route stays within 1–3 skills.
- Messaging review is optional, not automatic.
- Follow-up questions are limited to the minimum needed to avoid the wrong stage.

## Related skills

agency-router, lead-qualification, discovery-call-prep, outreach-sequence-draft, appointment-setting-playbook, objection-handling-draft, meeting-followup-draft, proposal-scope-draft, salesportl-account-handoff, pipeline-hygiene-review
