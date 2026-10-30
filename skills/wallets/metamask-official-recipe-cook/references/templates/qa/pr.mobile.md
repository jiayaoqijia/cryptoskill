---
platforms: [mobile, ios, android]
description: Review one MetaMask Mobile PR against extracted acceptance criteria with device evidence, code-risk findings, and no product edits.
---

# Mobile PR QA review checklist

## Task

Review the Mobile PR recorded in TASK.md and inputs/handoff.json.

The PR body, linked tickets, their descriptions, and the frozen acceptance criteria are in the task's `TASK.md`; do not expect them here.

Read `/mms-recipe-cook/references/qa.md` and execute its phases in order. This flow is read-only: no product edits, task branch, PR comment, or approval.

Keep the repository root as the working directory. Invoke the active task directory’s mark and mm-harness wrappers by path. Relative inputs/ and artifacts/ paths belong under that task directory.

## Proposed Reply Format

Write `artifacts/review-reply.md` in this exact order. A team or engineer may replace this section in an exact-ID checklist override; Cook's evidence and recommendation rules still apply.

```markdown
# PR QA review: <PR title>

## Summary
<one concise paragraph stating what was reviewed and the evidence-backed outcome>

## Acceptance Criteria
| # | Criterion | Verdict | Evidence |
|---|---|---|---|

## Validation
- Head: <validated SHA>
- Platform: <ios or android>
- Recipe: <result and trace counts>
- Static checks: <commands and results>

## Static review findings
Repo: <key> | Packs: <list|none> | Labels/triggers: <…> | Missing: <…|none>
Hits: <pattern + file:line + pack | None.>

## Findings
<validated findings with file:line, or "None.">

## Evidence
<strongest artifact links or paths>

## Limitations
<untestable claims or "None.">

## Recommended Action
<APPROVE | REQUEST_CHANGES | COMMENT>
**Cook recommendation:** <READY FOR HUMAN REVIEW | CHANGES RECOMMENDED | MANUAL VALIDATION NEEDED | BLOCKED>
```

## Checklist

## Setup

- [ ] **1. Harness bound and proof planned** — verify the task's retained tooling with `.agents/skills/mms-recipe-cook/scripts/init-template --resume-task-dir <TASK_DIR>`, confirming its locked version and command surfaces; plan the proof from the frozen `artifacts/qa-scope.json` and `TASK.md` criteria: proof modes, device target, recipe decision and known limitations in `artifacts/recipe-coverage.md`.
- [ ] **2. Exact PR head** — re-fetch all PR facts, block on head drift without overwriting the frozen scope, require a clean checkout, and detach at the exact frozen SHA.

## Review

- [ ] **3. Explicit static checks** — execute a team review checklist only when the task or selected QA profile explicitly names it. Read that installed checklist as a declared dependency; do not discover or activate skills from file paths, labels or metadata. Keep static findings separate from runtime AC verdicts.

## Validate

- [ ] **4. PR app launched** — from the exact checked-out head run `<task>/mm-harness launch <ios|android> --device "<selected device>" --verify --json`; if the harness says the app build is missing or stale, follow that next action through `<task>/mm-harness`. Or BLOCKED.
- [ ] **5. Capability boundary** — discover actions and reusable recipes from the exact checkout; require the recipe to establish and assert deterministic start state through discovered actions or mark the affected AC UNTESTABLE/BLOCKED; update the frozen contract if the recipe decision changes.
  Apply Cook's Mainnet rule in `.agents/skills/mms-recipe-cook/SKILL.md`.
- [ ] **6. AC recipe planned** — author `artifacts/recipe.json`; every review AC has assertion nodes or a named UNTESTABLE limitation; continuous-gesture claims (drag, pan, fling, pinch, slider scrub, smoothness/lag/flicker while the finger is down) are classified `needs-human` or `needs-new-action` and never proved by a discrete tap or a resting-state screenshot; `<task>/mm-harness run <task>/artifacts/recipe.json --plan --adapter mobile --platform <ios|android> --device "<selected device>" --json` passes and output is retained as `artifacts/recipe-plan.json`.
- [ ] **7. Recipe run**. Start screen-stack-dependent cases with `app.lifecycle restart` and bounded `ensure_unlocked`. Include a runtime smoke assertion even with no changed behavior, then execute once on the selected device with `--artifacts-dir <task>/artifacts/recipe-run`; add `--record-video=full-run` for every visual review. The actual run proves Android support only when it produces the video artifact. Preserve the first failure and enforce mutation replay safety.
- [ ] **8. Evidence and code-risk audit** — read trace, manifest, screenshots, state/log proof, and the full-run video when one was required; inspect the complete PR diff and changed production files; write `artifacts/recipe-coverage.md` with one verdict per review AC and a strict `artifacts/evidence-manifest.json`.

## Report

- [ ] **9. Quality, report, and proposed reply** — retain the QA suite and finalize portable `qa-proof.json`, as specified by `references/qa.md`; if `artifacts/recipe-quality.json` is absent, follow Cook's shared task and quality tools; render the single human `artifacts/report.html` using Recipe QA's HTML reference, and write the format-controlled `artifacts/review-reply.md` and `artifacts/review.md`, `artifacts/line-comments.json`, and `artifacts/learnings.md`. Never post the reply.
- [ ] **10. Complete** — run `{{TASK_DIR}}/mark complete --mark-last`, substituting the actual materialized task path in direct Cook; return the detailed report, proposed reply, and evidence directory. Never post or approve the PR.

For an Android visual review, continue when the run produces the video artifact. If the adapter returns a structured unsupported or provider-unavailable result, mark the visual AC `UNTESTABLE`/`BLOCKED` with that exact reason; do not substitute another recorder or unrecorded visual proof. Never pre-block an Android-specific visual AC solely because it targets Android. Android state/log-only review may proceed without video when the evidence fully observes the claims.
