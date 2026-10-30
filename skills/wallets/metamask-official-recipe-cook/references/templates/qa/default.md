---
platforms: [mobile, ios, android, extension, chrome-extension, core, cli]
description: Validate a frozen PR, range or landed-change window using a dynamic recipe set and required runtime smoke proof.
---

# Runtime QA checklist

- TASK.md owns the request, frozen criteria, runtime target and profile inputs.
- `/mms-recipe-qa` freezes scope and criteria; `/mms-recipe-cook/references/qa.md` owns execution.
- Keep this parent checklist and register selected cases as its child.
- For a dispatched task without `artifacts/qa-scope.json`, build the request with `node .agents/skills/mms-recipe-qa/scripts/resolve-scope.mjs --farm-input inputs/qa.json --out inputs/qa-scope-request.json`; never hand-write it.
- Run `node .agents/skills/mms-recipe-qa/scripts/resolve-scope.mjs --input inputs/qa-scope-request.json --out artifacts/qa-scope.json`, then derive criteria through `/mms-recipe-qa` §3 before runtime work.
- The adapter binds `inputs/qa.json` `source` base/head only to `kind: pr`; ranges, windows and refs use their own revisions.
- Every launch carries `--remote-flag <remoteFlagSpec>` when frozen in scope.

## Scope and criteria

- [ ] Bind the task and freeze the selected criteria and cases.
  - Run `.agents/skills/mms-recipe-cook/scripts/init-template --resume-task-dir <TASK_DIR>` and read its locked harness help; preserve TASK.md and this checklist.
  - Apply the caller's author, domain and explicit PR/ticket selection through Recipe QA.
  - Retain included/excluded changes, exclusion reasons and timestamp semantics.
  - Record verbatim authored criteria, labelled derived criteria and prerequisite gaps in TASK.md and `artifacts/recipe-coverage.md`.
  - Before live proof, print the selected PR/ticket list.
  - Freeze and print smoke gates for each fixture/lifecycle phase in `artifacts/recipe-coverage.md` and feature cases in `inputs/qa-cases.md`.
  - Map each case to criteria, assertions, prerequisites and cleanup.
  - Stop on an empty selection; never broaden it. Freeze obligations, not verdicts.

## Live proof

- Limit each frozen case and each planned setup phase's smoke gate to two live attempts across resumes; setup failures consume attempts. A planned fixture change allows two new smoke attempts; recovery reseeding never resets counts.
- Freeze assertions and pass proof preflight before attempt one. Record later assertion/selector changes with reasons and before/after recipe digests; never weaken assertions, rename cases to reset counts or add cases after proof starts.
- Before attempt two, diagnose the retained failure and record its root cause and corrective fix. Keep reproduced product failures FAIL and inconsistent outcomes as flake findings until resolved.
- Never run a third attempt. If the same failure recurs, file its diagnosed product, recipe, harness or environment cause. Keep every failed attempt; a pass does not erase it.
- Continue independent frozen cases within budget, then report partial coverage.

- [ ] Prepare the owned checkout at the frozen head through the locked harness.
  - For an official `proofLane`, acquire and launch the release artifact through `/mms-recipe-qa/references/domain-qa.md`.
  - Before a long native build, record its phase, log path and budget in task progress.
  - Notify the operator so monitoring can be extended.
  - On monitor timeout, check build liveness and progress; do not start another build.
  - Apply the approved ready-wallet fixture through `fixtures set`, or verify an existing matching wallet.
  - Onboarding, migration and first-time criteria use their declared unfinished fixture; never substitute UI wallet import.
  - Extension fixtures reset/relaunch the profile; pass frozen `--remote-flag <remoteFlagSpec>` to fixture commands.
  - Reverify app/build/account/domain-network/flag identity and startup gates before smoke.
  - Read the tested checkout's `package.json` name/version, current branch and full HEAD after setup.
  - Retain that identity with runtime evidence and pass it as `testedBuild` to the shared report renderer.
  - Use `detached HEAD` without a checked-out branch; never infer the tested build from its directory name.
  - Keep setup outside proof windows. A reseed closes the attempt and requires retained setup, identity checks and re-smoke before dependent cases.
  - Fixture authority does not authorize financial actions.
  - Apply Cook's Mainnet rule in `.agents/skills/mms-recipe-cook/SKILL.md`.
- [ ] Compose frozen baseline smoke in `artifacts/recipe.json` using discovered actions/recipes.
  - Pass assertion and proof preflight, execute within the two-attempt budget and inspect retained evidence.
  - With a smoke-only package index, run `node .agents/skills/mms-recipe-qa/scripts/finalize-qa.mjs --task <TASK_DIR> --index <smoke-index.json> --check-only` to validate execution without finalizing a suite.
  - Diagnose failure within budget or report the blocker; preserve every attempt and never broaden the suite.
- [ ] Prepare the frozen feature plan and register its case checklist.
  - After validated smoke, compose the frozen risk-based plan for the requested assurance level.
  - Include essential journeys, risky changes, cross-feature interactions and lower-risk exclusions with prior-evidence/risk rationale; keep every criterion.
  - Map selected targets to user situations, reusable setup/actions, assertions and task-owned cleanup; group compatible setups.
  - Create missing state within caller authority; compose supported primitives when no complete recipe exists.
  - Record library digests, recipe rationale and observed prerequisite/capability failures.
  - Pass assertion and proof preflight before each case's first attempt; preflight alone proves no runtime behavior.
  - Preserve criteria and record later assertion changes as findings.
  - Keep one flat `- [ ]` row per frozen feature case in `inputs/qa-cases.md`, in execution order, with readable case/PR names and criterion IDs.
  - Keep smoke separate and deferred criteria in the plan/report outside this progress count.
  - Register before execution. For an explicitly smoke-only plan, explain why step 5 has no child; never create an empty unit.

  ```bash
  "{{TASK_DIR}}/mark" sub start qa-cases --step 5 --from "{{TASK_DIR}}/inputs/qa-cases.md"
  ```
- [ ] Execute and assess the selected cases through `qa-cases`.
  - Execute attainable independent cases within budget, retaining immutable packages, failed attempts and teardown.
  - Before claiming a blocker, attempt the smallest authorized setup/capability check and retain its failure.
  - Distinguish not run, incomplete proof and observed blockers; record scope, prerequisite and budget limits.
  - Do not stop at a passing subset.
  - Diagnose failures through observed evidence as product, recipe, harness or environment.
  - Preserve unexplained fail-then-pass outcomes as reliability findings.
  - Inspect images for the asserted state; state assertions cannot certify stale screenshots.
  - For smoke-only scope, mark step 5 after confirming the plan.
  - Otherwise mark `{{TASK_DIR}}/mark sub qa-cases <n>` after retaining each case's attempts, evidence, outcome and cleanup.
  - Checked means assessed, not passed; retain case blockers and continue independent cases.
  - If the child cannot continue, retain partial HTML, retrospective and cause, then run `{{TASK_DIR}}/mark sub qa-cases blocked --reason "..."` and `{{TASK_DIR}}/mark blocked --reason "..."`.
  - Never check unexecuted cases.
  - After all cases are assessed, run `{{TASK_DIR}}/mark sub qa-cases complete`, which completes parent step 5.
  - Do not mark the parent while its child owns it, edit `subtasks/`, or treat completion as proof/release approval.

## Report and retrospective

- [ ] Audit each frozen criterion and finalize the declared proven suite.
  - Check executed assertions and reviewed evidence; write shared QA/evidence artifacts with explicit PASS, FAIL and UNTESTABLE boundaries, separating setup and static findings.
  - Finalize with `node .agents/skills/mms-recipe-qa/scripts/finalize-qa.mjs --task <TASK_DIR> --index <index.json>`.
  - The index is `{"packages":{"<case id>":"<package dir relative to artifacts/>"},"smoke":{"caseId":"<case id>","proofTarget":"<proof target id>"}}`.
  - Never hand-author `qa-proof.json`, bound `qa-result.json` or their digests.
  - Passing selected cases do not erase gaps in the requested scope.
- [ ] Render the report and retrospective. Complete through the task's mark wrapper after satisfying its artifact contract.
  - Render `artifacts/report.html` from structured evidence through `/mms-recipe-qa/references/html-report.md`; never duplicate it in Markdown.
  - Headline frozen in-scope PRs/tickets with per-criterion verdicts/evidence; keep other observations supplementary.
  - In `artifacts/retrospective.md`, record reused/new recipes and setup/first-smoke/authoring/execution time.
  - Include failed attempts, assertion/selector changes with reasons, operator interventions and ranked improvements with owning layers.
  - For each flake, retain earliest-failure evidence, diagnosed cause or explicit unknown, owner and fix PR/pending status.
  - A passing retry is not a fix. Use native usage only when available.
  - If the terminal artifact contract is unsatisfied, retain the report and mark failed/partial.
  - Keep shared tools immutable; propose improvements for later runs.
