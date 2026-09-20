---
name: appointment-setting-playbook
description: Draft appointment-setting sequences, qualification gates, and calendar handoff prompts using supplied lead context.
version: 0.1.0
tags: [sales, appointment-setting, playbook, draft-only]
---

## Purpose

Draft appointment-setting sequences, qualification gates, and calendar handoff prompts using supplied lead context.

## Use when

- A qualified or semi-qualified lead needs a clear path to book a meeting.
- You need message variants and follow-up cadence before handing to calendar ops.

## Required inputs

- Lead status and relevant qualification evidence from supplied notes.
- Offer/service context from context/BRAND-CONTEXT.template.md and context/CLIENT-CONTEXT.template.md (filled variants).
- Approved booking flow details, constraints, and [SalesPortl workspace/link].

## Safety/authority

- No fabricated prospect interest signals, objections, or timeline claims.
- No implied confirmed booking until client/prospect explicitly confirms.
- Keep outputs draft-only; no direct calendar/CRM writes.

## Workflow

1. Confirm objective, meeting type, and booking authority.
2. Build message variants by channel (email/SMS/DM) with role-specific CTA options.
3. Define cadence, stop conditions, and fallback paths when no response.
4. Output scheduling handoff notes plus unknowns requiring confirmation.

## Output format
```

- Appointment-setting summary
- Message sequence table (touch | channel | draft copy | trigger)
- Booking handoff checklist
- Unknowns and confirmation questions
```

## Quality checks

- Each CTA aligns with provided offer and approved booking process.
- Cadence includes explicit stop/opt-out handling and no invented claims.

## Related skills

lead-qualification, outreach-sequence-draft, meeting-followup-draft
