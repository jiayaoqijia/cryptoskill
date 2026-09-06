# Test layer placement (Mobile)

Orchestrate **analyze → (optional) implement → report** for a Mobile code area so
tests land in the right layer: unit, component-view (CV), integration, or e2e.

**Pilot reference:** [MMQA-2100](https://consensyssoftware.atlassian.net/browse/MMQA-2100)
(Approach A, WalletActions + PerpsCancelAllOrdersView, PR
[#33793](https://github.com/MetaMask/metamask-mobile/pull/33793)).

## Modes

| Mode                  | When                                           | What you do                                                                                                         |
| --------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **ANALYZE** (default) | User did not say implement / go / apply        | Inventory, classify, disposition plan, metrics estimate, report + Jira + PR checklist as **proposed**               |
| **IMPLEMENT**         | User explicitly asks to implement / apply / go | Execute disposition: write/migrate/delete tests, allow minimal pure extracts, re-run, then final report + Jira + PR |

Do **not** implement in ANALYZE mode. Present the plan and wait.

## Flexible intake

Accept any of: **Jira key**, **code path/folder**, **PR URL/number**. Resolve scope from what is given.

1. **Jira** — fetch issue + comments + links (Atlassian MCP / browse URL). Pull linked PRs and follow-up tickets. Prefer scope from description / AC / comments.
2. **PR** — `gh pr view` for files changed, body, linked issues. Scope = touched production + sibling test files under those folders.
3. **Path** — treat as the audit root (e.g. `app/components/UI/Perps`).
4. If only one input is given, derive the others when possible (ticket ↔ PR links, PR files ↔ paths). If scope is still ambiguous, ask one clarifying question.

Record: ticket key (if any), PR number (if any), scoped paths.

## Prerequisites — load peer skills / knowledge

Before classifying or writing tests, load as needed (do not reinvent layer rules):

| Concern                                                   | Open                                                                                                                                                                                    |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Layer decision tree                                       | installed `knowledge/testing-layers.md` (source [`../../../knowledge/testing-layers.md`](../../../knowledge/testing-layers.md); stub [`layers.md`](layers.md))                          |
| Screen UI via Redux                                       | [`component-view.md`](component-view.md)                                                                                                                                                |
| Pure helpers / CV fallback                                | [`unit.md`](unit.md)                                                                                                                                                                    |
| App↔controller seam                                       | [`integration.md`](integration.md)                                                                                                                                                      |
| Device/native E2E (only after CV + integration ruled out) | [`appium-e2e.md`](appium-e2e.md)                                                                                                                                                        |
| Unit↔CV overlap migrate/delete                            | [`placement/unit-cv-overlap.md`](placement/unit-cv-overlap.md) — if personal Cursor skill `test-layer-overlap-audit` is available, load it too and prefer its process for that sub-pass |

## Workflow checklist

Copy and track:

```
Test layer placement:
- [ ] 1. Intake (ticket / path / PR)
- [ ] 2. Inventory all layers
- [ ] 3. Classify reason → layer → decision
- [ ] 4. Unit↔CV overlap sub-pass (if siblings exist)
- [ ] 5. Disposition plan (ANALYZE stop here unless asked to implement)
- [ ] 6. IMPLEMENT (only if asked): apply + re-run
- [ ] 7. Report (canvas + Jira comment)
- [ ] 8. Always update PR description with task checklist
```

### 1. Intake

Resolve ticket/PR/path as above. Read MMQA-2100-style comments on the ticket if present (verdict, volume table, residual risks).

### 2. Inventory

For the scoped paths, find what exists. See [`placement/inventory.md`](placement/inventory.md).

Summarize per component/module:

| Module | Unit                   | CV                      | Integration | E2E         | Notes |
| ------ | ---------------------- | ----------------------- | ----------- | ----------- | ----- |
| …      | `Foo.test.tsx` (N its) | `Foo.view.test.tsx` (M) | none / path | none / spec | …     |

### 3. Classify (reason first)

For each meaningful scenario (especially each `it(...)` in shallow screen units, and each gap in production behavior):

1. **Worth covering?** Distinct realistic regression — not duplicate of existing coverage. If no → **GAP / ACCEPT**.
2. **What does this protect?** (UI visibility, nav destination, pure math, controller seam, device/native boundary, …)
3. **Best layer?** Use installed `knowledge/testing-layers.md`. Order: **CV → integration → unit fallback → E2E**.
4. **Decision:**

| Decision         | Meaning                                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| **KEEP**         | Already in the correct layer                                                                      |
| **ADD**          | Missing coverage → add at best layer                                                              |
| **MIGRATE**      | Wrong layer (usually shallow unit UI → CV); add target first, then remove source                  |
| **DELETE**       | Duplicate of coverage already owned by a better layer                                             |
| **EXTRACT+UNIT** | Toast/wiring matrix (etc.) needs a **minimal pure helper** + unit tests; do not invent product UX |
| **GAP / ACCEPT** | Intentionally uncovered or blocked (document why)                                                 |

**Hard rules**

- Screen UI / Redux-driven visibility / press→nav belonging in unit files with mocked hooks → **MIGRATE** to CV, do not “fix” mocks in place.
- Multi-screen / navigation journeys are **CV-first** when routes can be registered and state/API driven in CV.
- E2E is **not** a substitute for any scenario CV or integration can cover with equivalent confidence.
- **ADD E2E** is forbidden unless the disposition row includes all three:
  1. Why CV is insufficient
  2. Why integration is insufficient
  3. Required device/native boundary
- If those three cannot be filled, disposition must be **ADD CV**, **ADD integration**, or **GAP / ACCEPT** — never E2E by default.
- Integration owns app↔controller seams, not full-screen RTL with mocked Engine internals unless the integration skill says otherwise.
- Production changes: **tests + minimal pure extracts only**. No intentional product UX change. Call out any app LOC in the report.

### 4. Unit↔CV overlap sub-pass

When `ComponentName.test.tsx` and `ComponentName.view.test.tsx` both exist (or shallow screen units mock hooks for UI), run Approach A from
[`placement/unit-cv-overlap.md`](placement/unit-cv-overlap.md).

### 5. Disposition plan (ANALYZE output)

Present a concise plan:

- Scope + ticket/PR
- Inventory table
- Disposition table (scenario → decision → target layer/file). For any **ADD E2E** row, include columns or notes for: why CV insufficient / why integration insufficient / required device boundary
- Estimated volume deltas (unit/CV/integration/e2e `it`s)
- Residual risks / open questions
- Proposed PR task checklist (unchecked)

Then: post **analysis** Jira comment + **always** write/update the PR description with that checklist (see templates). **Stop** unless IMPLEMENT was requested.

### 6. IMPLEMENT (only when asked)

1. Apply ADD / MIGRATE / DELETE / EXTRACT+UNIT per plan.
2. For MIGRATE: add CV (or other target) **before** deleting source assertions.
3. Pure extracts only when otherwise a toast/wiring matrix would be uncovered and CV cannot own it (MMQA-2100 CancelAll pattern).
4. Re-run affected unit / CV / integration commands for touched files.
5. Refresh metrics (before/after `it` counts).
6. Final report + Jira + PR (mark completed tasks).

### 7. Report

1. Cursor canvas summarizing verdict, volume, disposition, residual risks, app-code note (see canvas skill if producing `.canvas.tsx`).
2. Markdown mirror as Jira comment — [`placement/report-template.md`](placement/report-template.md).
3. Tell the user the canvas path (MCP may not upload attachments).

### 8. PR description (always)

Whether ANALYZE or IMPLEMENT, create or update the PR body so it describes **every task** with a checklist.
Use [`placement/pr-description-template.md`](placement/pr-description-template.md).

- ANALYZE: all items unchecked, labeled proposed.
- IMPLEMENT: check off done items; leave residual / follow-ups unchecked.
- Link the Jira ticket and the report comment when available.
- Prefer `gh pr edit` / `gh pr create` as appropriate; do not force-push.

## Out of scope

- Broad production refactors unrelated to making a scenario unit-testable via a pure extract
- Committing spike-only dumps (`mmqa-*-classification.md`, inventory snapshots) into the mobile repo — keep those on Jira/canvas/skill
- This path **orchestrates**; writing tests still follows `component-view.md` / `unit.md` / `integration.md` / `appium-e2e.md`

## Examples

**ANALYZE**

```
User: Analyze app/components/UI/Predict for test layers — MMQA-2104
Agent: Inventory → classify → disposition plan → Jira analysis comment → PR body with proposed checklist. Stop.
```

**IMPLEMENT**

```
User: Implement the disposition for MMQA-2102 / path Perps
Agent: Apply plan → re-run → final report on Jira → update PR checklist.
```
