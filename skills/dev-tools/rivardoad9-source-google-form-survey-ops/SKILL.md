---
name: google-form-survey-ops
description: Use when a Google Form needs audit, QA, filling, or reach.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [survey, google-forms, research, data-quality]
    related_skills: [academic-practicum-deliverables, xlsx]
---

# Google Form survey ops (coursework / thesis)

## When to Use

- The user shares a `forms.gle` or `docs.google.com/forms` link for a class or thesis questionnaire.
- The user asks for help filling it, or asks for "dummy" respondents.
- The user needs respondents fast and wants distribution channels or message copy.
- Responses are in and need a quality check before analysis.
- A vendor's Google Form (API key request, partner or program application) has to be filled with the user's own details on his behalf.

Covers the full loop: audit the instrument, QA-test it, distribute it, then QC the data before analysis.

## Hard rule: never fabricate responses
Refuse dummy/fake submissions, even "just 10", and even when the user asks twice. Reason to give (once, briefly, no lecture): fake rows shift means and tighten variance in exactly the cells being tested, and answer patterns (identical durations, straight-lined matrices, same-minute timestamps, same IP) are what a marketing-research grader looks for. Offer a QA test instead — that is the real need behind the ask.

## Step 1: audit the instrument (5 min, before spreading)
Read the form structure from `FB_PUBLIC_LOAD_DATA_` in the viewform HTML (see Step 2). Check and report:
- **Eligibility gates not enforced**: a screening question with age/buyer criteria is just a recorded answer by default. Options outside the target band still submit. Flag it, and say the sample must be filtered manually unless a real gate is added.
- Required flags per question, number of sections, estimated minutes.
- Whether it collects email / forces login (affects response rate and dedupe).
- Long matrices (8 brands x 4 columns) are the drop-off point; recommend cutting to the core brands.
- "Open text" questions that are actually checkbox lists without a "Lainnya" option.
- Typos in question text: cheap to fix, and they make respondents distrust the form.

## Step 2: QA test with two real submissions
Agree with the user first that the two rows will be deleted. Submit two visibly different profiles (different age band, occupation, spend, brand set) so both branching and matrices get exercised.

Two submission paths:
1. **Browser** (works but flaky): click through each section, dispatch clicks on `[role=radio]` by `data-value`, `[role=checkbox]` for multi-select. Verify `document.querySelectorAll('[role=radio][aria-checked=true]')` equals the radiogroup count before hitting Next/Submit. Rapid click loops can crash the CDP session and lose progress.
2. **Direct POST** (fast, headless, survives browser death) — preferred:
   - `curl -sL --compressed -A "Mozilla/5.0" https://docs.google.com/forms/d/e/<ID>/viewform -o form.html`
   - Parse `FB_PUBLIC_LOAD_DATA_ = (\[.*?\]);` — `data[1][1]` is the item list. For type 2/4/5 the entry id is `item[4][0][0]`. For type 7 grids every row in `item[4]` carries its own entry id (`row[0]`) and label (`row[3][0]`). Type 8 = section header, type 6 = closing message.
   - Build `entry.<id>=<option text>` pairs (option text must match the form text exactly), then add `fvv=1`, `pageHistory=0,1,2,3`, `fbzx=<value from name="fbzx" in form.html>`.
   - POST urlencoded to `https://docs.google.com/forms/d/e/<ID>/formResponse`. Success = HTTP 200 and the confirmation string ("recorded" / "已记录") in the HTML; validation failures leave the question error markup instead.
- Report to the user: exact submit timestamps, the answers used per row, and the deletion path (Responses tab → Sheets icon → delete the two bottom rows, **delete rows, not filter**), plus "response count must drop by 2".
- A successful bare POST also proves there is no bot protection: mention it and suggest limiting to one response or deduping in the sheet.

## Step 3: distribution
Broadcast to groups is the lowest-yield channel; personal DM is what actually converts. Order:
1. 20 personal DMs to people who clearly match the criteria, asking each to forward to two others (snowball).
2. Class/angkatan and alumni WhatsApp groups, sent 19:00–21:00 local, not morning.
3. IG Story / Threads with a screenshot and one line of reason, not a bare link.
4. Ask 3–5 people with relevant followers to repost.
5. Lecturer or class coordinator forwarding to other classes — usually the biggest single-day jump.

Sample size rules to quote: PLS-SEM ≈ 10 x the largest indicator count (typically n=100–150); plain regression ≈ 5–10 x number of variables (n=50–80). Screening pass rate is roughly 70–80% of clicks, so seed about 1.4x the target.

## Step 4: QC before analysis
Ask for view access to the response sheet, then check: completion duration outliers, straight-lining across matrices, eligibility-question distribution (who slipped through the ungated question), duplicate submissions, and clean n vs target.

## Filling a third-party form on the user's behalf (API key, partner application)

Same mechanics as Step 2, different risk: the answers are his identity, and the submission is an external side effect.

1. **Enumerate questions and required flags before typing anything.** Parse `FB_PUBLIC_LOAD_DATA_` from the viewform HTML (Step 2). Required questions are the ones marked `*`; a missing mandatory field is the usual reason a submission fails, and that failure is silent in a scripted POST.
2. **A scripted POST answering HTTP 400 is validation, not success.** Google returns 400 with `data-error="false"` in the markup, so grepping for the word "error" tells you nothing. Fill the form in the browser instead: Google renders the rejected question inline ("此问题必须填写" / "This is a required question"), which names exactly what is missing.
3. **Only fill what is verifiably his.** Email, name, and public links/handles that exist (check the URL returns 200 and the handle resolves). Never invent a Discord ID, phone number, company, or a project description that overstates what he has.
4. **A missing mandatory identity field ends the attempt.** Ask for that one value and stop; do not substitute "n/a", a guess, or a dummy handle to get past a required field on a form that grants access or money.
5. **Confirm the final field set when the request is ambiguous**, then report the submission only after the confirmation page renders. The intake side usually answers later ("within 48 hours"), so never call the approval itself done.

## Pitfalls
- Do not treat an ungated screening question as a filter — it is not.
- Do not leave QA rows in the sheet; if the user forgets, the rows are the newest two with known timestamps.
- The form's language follows the browser locale, so section labels can appear in Chinese/English; the question text stays as authored. The submit control follows it too: it renders as a `div[role=button]` whose text is `提交` / `Submit`, so `querySelectorAll('button')` plus an English-only match finds nothing — scan `div[role=button]` against `/提交|submit/i`.
- `forms.gle` short links 302 to the `docs.google.com/forms/d/<ID>/viewform` URL — resolve it before parsing.
