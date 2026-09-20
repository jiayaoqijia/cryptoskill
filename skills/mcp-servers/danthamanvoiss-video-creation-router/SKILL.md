---
name: video-creation-router
description: Route video planning work to the right script, storyboard, edit-plan, or video-calendar skill with concise production-stage clarification.
version: 1.0.0
tags: [core, routing, video, creative, v1]
---

## Purpose

Choose the right video skill so script writing, storyboard work, edit planning, and publishing cadence do not overlap unnecessarily.

## Use when

- The main router has identified a video-first request.
- The user needs a video deliverable but has not named the exact video skill.
- The task should stay in the video family.

## Required inputs

- Video objective and format.
- Platform, audience, and tone [if known].
- Whether the user needs script language, visual sequencing, edit structure, or calendar planning.

## Safety/authority

- Do not invent product claims, shots, or production resources that are not supported by the brief.
- Keep publish-ready outputs draft-only until approved.
- Separate script language from edit structure from content scheduling.

## Workflow

1. Clarify the format and stage of the video task.
2. Route to:
   - scripting: `short-form-video-script`
   - scene planning: `storyboard-scene-builder`
   - post-production structure: `video-edit-plan`
   - publishing cadence: `video-content-calendar`
3. Keep the route to 1–3 skills and only chain script plus storyboard plus edit plan when the user explicitly wants a fuller package.
4. Optionally pair with `anti-slop-content-review` when messaging quality needs review.
5. If the exact skill is unavailable, use the closest same-stage video alternative or ask for clarification.

## Output format

```
- Video task stage: ...
- Selected skills (1-3): ...
- Missing inputs: ...
- Optional quality layer: ...
- Next step prompt: ...
```

## Quality checks

- The selected skills match the production stage.
- Script, storyboard, edit, and calendar work are not mixed by default.
- The route stays lightweight.
- Missing format or audience context is surfaced.

## Related skills

agency-router, short-form-video-script, storyboard-scene-builder, video-edit-plan, video-content-calendar, anti-slop-content-review
