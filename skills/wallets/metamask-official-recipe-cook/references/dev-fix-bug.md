# Dev and fix-bug rules

Apply the sections for this flow and platform at each step.

## Task and sandbox

- Work top to bottom; apply Cook's blocked rule. Mark each completed gate with artifact paths.
- `<task>` means TASK.md `TASK_DIR`; bare `mm-harness` means `<task>/mm-harness`.
- Keep proof under `<task>/artifacts/` and out of product commits.
- Put clones, installs, tooling and loop workspaces in `<task>/../scratch-<id>` or `temp/`, never `artifacts/`.
- Confirm the handoff's checklist path; never estimate or rewrite it.
- Capture the summary and ACs, then verify retained tooling with `.agents/skills/mms-recipe-cook/scripts/init-template --resume-task-dir <task>` and read its recorded `mm-harness help --json`.
- Preserve TASK.md, CHECKLIST.md, markers and receipts. If tooling verification fails, stop with that cause; never resolve a replacement for this task.
- Follow `/mms-recipe-harness`: doctor/status/launch-or-reuse/verify for this checkout. Require `artifacts/sandbox.json` with `ready: true`.
- Mobile requires the running simulator/device app; Extension requires reachable CDP. First recover with harness launch/doctor; block only on an external farm/device failure.
- Create or switch to the local task branch before product edits. Do not open a PR.

## Plan and baseline

- Discover the harness catalog before drafting: `mm-harness run --list --json`; use Recipe v1 `workflow.{entry,nodes}` and live runtime evidence. Tests corroborate only.
- Core targets packages/controllers and fixtures, using headless `state`, `command` or `log` proof without PNGs. A `command` proof drives the controller through its public API as a client does (real messenger, mocked only at the network boundary); it never runs Jest or another unit-test probe.
- Mobile targets iOS, Android or both; Extension targets popup, sidepanel, fullscreen or dapp. Record the rationale.
- UI ACs use state/visual/mixed proof; visual proof requires a human-read PNG. Extension copy, labels, warnings, modals and toasts are visual or mixed.
- Development UI proof plans bind a fixture, semantic intent and verified live postcondition. Mobile uses adapter-owned current route mappings; Extension discovers runtime controls and keeps task recipes in `artifacts/recipe-library/recipes/`.
- Name UI AC nodes `ac<N>-...`, plumbing nodes `setup-`/`teardown-`/`gate-`, and baseline captures `before-...`.
- For persisted UI changes, assert the expected start state in setup and restore it in teardown.

### Development

- Read affected code end to end; write `artifacts/approach.md` with affected files, current behavior/insertion point, chosen approach and trade-offs.
- Mobile/Extension: choose the most defensible approach without pausing. Before editing existing UI, capture comparable `before-*` evidence on the same route, state, target and viewport. For purely additive work, write `Baseline: N/A. additive` in TASK.md.
- Draft the recipe file and require `mm-harness run <recipe> --plan` PASS.
- Run it before implementation with `--artifacts-dir <task>/artifacts/recipe-baseline-run --json`; require failure at the first new-behavior AC assertion, not setup, before marking the recipe gate.
- Place regression guards before the first new-behavior AC; guards must pass before and after implementation. If every AC is a guard, require the baseline run to pass end to end.
- Record the recipe path and command, including for visual/mixed proof. Implement only after the recipe gate is marked PASS.

### Bug fixing

- Keep the sandbox green before baseline and fix. No product behavior edits before baseline; locator testIDs are allowed, as is the Mobile reproduction marker.
- Mobile/Extension: until the minimal-fix step, write only TASK.md, checklist marks and `<task>/artifacts/`, apart from those locator/marker exceptions.
- A premature UI behavior change requires `artifacts/ordering-violation.md`; restore baseline order before continuing.
- Plan the expected buggy evidence and each AC's state. Missing state that setup actions can build is not UNTESTABLE; Extension reserves that verdict for infrastructure limits.
- Probe reused recipe entry/setup boundaries with a short bound before baseline. For recipe, recipe-library or action-contract mismatches, copy the closest recipe into the task, adapt to current actions and continue; never block.
- Core: list `mm-harness actions --json` as well as recipes and write `artifacts/recipe-decision.json` with `version: 1`, boolean `required`, a non-empty `reason` string and non-empty `actionsChecked`/`claims` arrays.
- When proof is required, the decision also sets `recipePath: "artifacts/recipe.json"`.
- Core: `required: false` requires no listed action that can exercise the change. Missing setup state is not an exemption; diagnose and repair missing runtime prerequisites first.
- Core: when required, draft `artifacts/recipe.json` asserting fixed behavior, prefer reusable recipes and require plan PASS. Run it into `recipe-baseline-run/` and require failure at the reported bug's AC assertion. Focused tests are never the baseline proof for a runtime claim.
- Mobile/Extension: draft `artifacts/recipe-baseline.json` asserting buggy real-app behavior through live actions or run-scoped markers/logs; require plan PASS, then run it into `recipe-baseline-run/` with `--record-video=full-run --json` and read every visual PNG.
- For already-fixed/not-reproduced cases, write `artifacts/no-change-report.md` and `artifacts/learnings.md`, then follow Cook's Finish before marking no-change. UI flows add `--already-fixed` to the terminal mark when this branch already fixes it; setup/environment failures follow Cook's blocked rule.
- After the minimal fix, UI `artifacts/recipe.json` keeps the baseline nodes, asserts fixed values, passes plan and fails with the fix reverted.

## Implementation and checks

- Keep implementation AC-mapped; bug fixes are minimal, without unrelated refactoring.
- Development reuses domain helpers for external identifiers.
- Reuse or extract a helper beside the existing hook/util before repeating a derivation or parser; leave unrelated duplication alone.
- Core changes add each required package CHANGELOG entry.
- New development UI interactive elements use Mobile `testID` or Extension `data-testid`; bug fixes allow those locator additions.
- Mobile development literal-colour requirements use `theme.brandColors`; semantic tokens change in dark mode.
- Run `mm-harness check diff [--fix] --artifacts-dir <task>/artifacts` as the fast lint/format gate. Never discover or run separate repository lint/format commands.
- The default fast profile skips typecheck. Require PASS before marking the gate; UI flows retain `validation-summary.json`.
- Extension bug fixes also run `yarn verify-locales --quiet` for changed locale files and `yarn circular-deps:check` for changed imports.

## Runtime proof

- Keep the authored final recipe at `artifacts/recipe.json`; run `<task>/mm-harness run <task>/artifacts/recipe.json --artifacts-dir <task>/artifacts/recipe-run --json`.
- Mobile/Extension add `--record-video=full-run`; Mobile video is under `recipe-run/videos/`. Core bug-fix recipes run only when required and must pass.
- Core setup failures: inspect retained state/logs, diagnose and repair drift with `--heal auto`; never weaken assertions. Apply Cook's blocked rule.
- After self-review, rerun proof when proven behavior changed; otherwise record an explicit no-rerun decision.

### UI evidence

- Read every visual/mixed PNG. The claimed target must be visible, without clipping, covers or a generic home/empty screen, and follow `ui.wait_for` on that target.
- Bug-fix after captures must differ from `before-...` as the bug-to-fix claim describes. Fix insufficient evidence and rerun instead of shipping a caveat.
- If video cannot start, retain the unsupported reason and mark visual ACs UNTESTABLE/BLOCKED; never substitute a recorder.
- Stop missing-capability probing after 10 minutes; record the gap in `learnings.md` and use the simplest supported proof.
- Prove disabled controls with their visible reason, a read PNG and a real press attempt. Retain press refusals in a separate expected-fail probe.
- If the press succeeds, assert unchanged state and no action/submission log. Never claim a press had no effect when it did not run.
- Write recipe `intent` as the user-visible goal, without action narration or UI text targets.

### Mobile runtime

- After source edits and before each recorded run, run `mm-harness call app.lifecycle command=restart`; HMR is off.
- Fetch the bundle URL and find an introduced string. On a miss, run `mm-harness stop`, then `launch --clear-metro --verify`, and recheck.
- Label stale runs `*-stale*` and never cite them. Use testIDs when hidden mounted sheets can absorb text presses.
- The HUD renders intents on screen; Mobile text matching uses case-insensitive contains.

### Extension runtime

- Reload before recorded runs with `mm-harness doctor --expect-live`; run `mm-harness launch --verify` if the extension stopped responding. HMR is off.
- Accept capture-helper screenshots only; reject screencapture and `Page.captureScreenshot` fallbacks.
- File/JSON assertions over command output must depend on that command's success and read a file written inside this run's artifacts directory; old files are not evidence.
- The HUD renders intents in-page; `ui.wait_for` matches any rendered text.

## Tests

- Core: focused tests and AC-required domain smoke only. Do not substitute repo build/typecheck for the fast-profile skip.
- Build Core only for changed exports, types or build wiring, with root `yarn build`; per-package builds need sibling outputs. Development records why a build is unnecessary.
- Check new/changed Core exports in emitted files named by `exports`, including `types` for type-only exports.
- Run Core build, tests and lint sequentially.
- Mobile: use `/mms-mobile-testing` for the layer policy and [component view guidance](mobile-testing/component-view.md) for UI behavior. If absent, follow `docs/testing/unit-testing.md` and record the gap.
- Run Mobile `yarn test:view:one <path> --runInBand`, `yarn test:integration:one <path> --runInBand` or `yarn jest <paths> --runInBand --no-coverage`, including affected consumers. Confirm every suite ran tests.
- Require >=80% Mobile changed-file coverage using the same command with `--coverage --collectCoverageFrom=<changed-file>`; `coverage:analyze` needs an open PR.
- Extension: use `/mms-extension-testing`; if absent, follow `.cursor/rules/unit-testing-guidelines.mdc` and record the gap.
- Run Extension `yarn jest <files> --no-coverage`, then require >=80% changed-file coverage with `--coverage --coverageReporters=text-summary --collectCoverageFrom=<changed-file>`.
- Never use `--findRelatedTests`. Bug-fix tests cover the reported bug condition.

## Self-review

Apply [review verdicts](team-libraries.md#review-verdicts).

- Mobile/Extension: run `/mms-review-pr non-interactive` as self-review of this checkout; apply Cook's blocked rule if the skill is missing.
- Core has no `review-pr` overlay; review correctness, error/boundary paths, performance, named constants, separation of concerns, dead/debug code, scope, simpler alternatives, downstream compatibility and exports.
- Include committed, staged, unstaged and untracked changes; record base, head, working-tree state, findings and skipped/unchecked areas in `artifacts/review.md`.
- Fix findings here; rerun affected tests, `check diff` and proof when proven behavior changed.
- Core tests must fail when their guarded behavior is removed.
- Block on duplicated derivation, parsing or formulas introduced by this diff, including copies of existing logic.
- A test that waits on a real timer (sleep, real poll, backoff or timeout) is a blocking finding; use fake timers.
- At the domain step, follow `references/team-libraries.md#dev-and-fix-bug-domain-review` with the checklist's stated parent step number.

## Mainnet

Apply Cook's Mainnet rule in `.agents/skills/mms-recipe-cook/SKILL.md`.

## Coverage and finish

- Write `artifacts/recipe-coverage.md` with one row per AC/claim: proof mode, evidence path under `recipe-run/`, recipe nodes, verdict and rationale.
- UI verdicts are PROVEN/WEAK/UNTESTABLE/MISSING. Check bug-fix rows against `recipe-run/trace.json`; failed nodes are never PROVEN. Fix WEAK/MISSING proof and rerun.
- Include `What this recipe does NOT prove`, ending with `Overall recipe coverage: <N>/<M> ACs PROVEN (untestable: <list or "none">, weak: 0, missing: 0)`.
- Build `artifacts/recipe-quality.json` through Cook's [Finish instructions](../skill.md#finish). Never pass UI WEAK/MISSING rows, development assertions that also pass before implementation, or bug-fix recipes that pass with the fix reverted.
- Core bug fixes write recipe coverage/quality when `artifacts/recipe.json` exists; non-recipe AC verdicts remain required.
- List all ACs with `.agents/skills/mms-recipe-cook/scripts/acceptance-cli <task> list`.
- Render the engine-owned coverage with `.agents/skills/mms-recipe-cook/scripts/acceptance-cli <task> render`; reconcile it with the retained recipe assertions and coverage rows.
- Missing verdicts require eligible recipe proof, including non-UI claims. Never write verdicts; only a verified person handles exceptions.
- Write `artifacts/pr-description.md` with only repository-template prose, `TICKET_URL` when set and proof summary; bug fixes include root cause, and Mobile includes marker SHA/log excerpt. Never paste recipe JSON or run output into renderer-owned sections.
- Run `mm-harness pr-body render <task> --out <task>/artifacts/pr-body.md --json` with mm-harness 0.92.21 or newer, then read that file. Preserve `--command <invocation>` when supplied. Require exit 0, `status: ok` and the generated body; renderer failure must not fall back to authored prose. Keep task markers and the locked harness receipt unchanged.
- Write `artifacts/evidence-manifest.json`: UI includes PROVEN visual evidence only, paths relative to `artifacts/`. Read video names from each run's `artifact-manifest.json` and prefix its run folder; manifests use run-relative paths.
- Put visual comparisons under `before_after_pairs`, with `label`, `covers`, `before` and `after`; use `standalone` for evidence that is not a comparison. Keep paths relative to `artifacts/`, including their run folders; never match captures by basename or invent a missing side.
- The manifest accepts only `version`, `preferred_mode`, `summary`, `before_after_pairs`, `standalone`, `omit` and `videos`. Keep draft, review and runtime-status notes in the report, not additional manifest keys.
- Development `before` images require screenshot nodes before the failing AC assertion. Core uses a media-free manifest, `{"version":1,"summary":"..."}`.
- Core also writes `artifacts/report.md` with summary/root cause, changed files, validation commands/results, recipe verdict/evidence, risks and client follow-ups.
- Write `artifacts/learnings.md` and satisfy host handoff prerequisites. Commit only when requested: one Conventional Commit of product paths, scope from the task domain/changed area, descriptive subject; never amend. Mobile marker commits remain separate.
- Finish with `<task>/mark complete --mark-last`, subject to the skill's required-proof completion rules.
