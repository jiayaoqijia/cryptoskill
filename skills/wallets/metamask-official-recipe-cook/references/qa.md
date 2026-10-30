# Runtime QA flow

This is Recipe Cook's `qa` execution contract. Keep product code unchanged. Use `gh` for PR facts and `mm-harness` as the only runtime front door. Runtime setup and task-owned test state may be created within the caller's existing authority; QA is not inherently limited to read-only app interactions. Never post to the PR or invent a runner action.

Run phases in order. A failed shared prerequisite blocks dependent cases; preserve its evidence and report the exact recovery command or operator decision. A case failure does not block independent cases with verified prerequisites and safe teardown. Keep the failed criterion in the report, classify it through the locked harness's drift guidance, and continue independent coverage without routing around its assertion.

Serialize harness runtime commands: launch, fixtures, call, run and doctor. On `SANDBOX_BUSY`, wait for this task's lock-owning PID to exit before retrying; report a foreign or hung owner as a blocker with its PID. List the frozen scope's commits with `git log` once to map changed behavior to criteria. Mark steps after all their subprocesses exit. Inspect only secret-free fixture metadata: labels, addresses and networks.

## Artifact contract

State this contract before runtime work:

```text
<task>/artifacts/
  qa-scope.json                   frozen change scope from recipe-qa
  qa-suite/                      standard Recipe v1 suite scope/result and recipe packages
  qa-proof.json                  portable scope/suite digests, package paths and smoke target
  qa-result.json                 the same proof bound to the task (written only when inputs/qa.json exists); never hand-authored
  recipe.json                     review AC proof graph, when generated
  recipe-plan.json                mm-harness plan output
  recipe-run/                     report, summary, trace, diagnostics, executed
                                  recipe, artifact manifest, and evidence
  recipe-coverage.md              AC -> mode -> planned proof -> nodes -> evidence -> verdict
  evidence-manifest.json          strict reviewer-facing evidence selection
  recipe-quality.json             Recipe Cook quality verdict
  report.html                     single human QA report
  report-data.json                 renderer input from the same retained evidence
  pr-verdicts.json                per-PR rollup from the shared HTML renderer
  review-reply.md                 checklist-formatted proposed PR reply
  review.md                       portable copy of review-reply.md
  line-comments.json              validated changed-line findings; never posted
  learnings.md                    reusable, secret-free workflow learnings
```

For visual ACs, require AC-named PNGs and request the full recipe video. For state/log ACs, require trace entries plus the exact state, command output, or watched log evidence. Do not claim an artifact that the run package does not contain.

For Extension, record the driven view and viewport: `home.html`, side panel or popup. Establish the requested display mode during setup through the locked harness, and check for unintended duplicate views before proof. Use the declared `ui.capture_surface` for report evidence of the driven document; a native `ui.screenshot` may include both the tab and an unrelated side panel. Inspect the actual PNG and label its target and observation limits. Full-document capture does not prove viewport clipping, and resizing `home.html` does not prove popup or side-panel behavior. Preserve ambiguous or stale captures as gaps; obtain fresh evidence in a new retained run rather than cropping or replacing the original to imply a clean run.

Every relative review artifact named below lives under `<task>/artifacts/`.

Cook locks and records the harness during materialization. Use its task-local front door for every harness command so PATH cannot bypass that provenance:

```bash
HARNESS="<task>/mm-harness"
test -x "$HARNESS"
```

## Observable case execution

For `qa/default`, use the task runtime's existing child checklist for selected feature cases. Other explicit templates retain their own checklist unless they declare a child binding. After freezing the plan, write `inputs/qa-cases.md`: one flat checkbox per selected case, in execution order, with a readable case/PR name and criterion references. Register one `qa-cases` child on the parent feature-execution step (step 5 in `qa/default`) with `<task>/mark sub start qa-cases --step <n> --from <task>/inputs/qa-cases.md`. Keep the parent numbering unchanged; do not register one child per case or a child of another child. An explicitly smoke-only plan with no selected feature cases uses the normal parent mark and no empty child.

Update each row through `<task>/mark sub qa-cases <n>` only after its attempts, outcome, evidence and required cleanup are recorded. A case-level failure or observed blocker can be assessed while other cases continue; preserve its verdict in the QA artifacts. When the child cannot continue as a whole, save the partial HTML report, retrospective and observed cause first, then run `<task>/mark sub qa-cases blocked --reason "..."` and finish the parent with `<task>/mark blocked --reason "..."`. Do not tick unexecuted cases or force completion. Finish with `<task>/mark sub qa-cases complete`, which ticks the owning parent step. The child signal's success/fixed fields describe assessment completion, not product correctness. The QA proof/result artifacts own validation verdicts; progress completion never substitutes for proof finalization or passing coverage.

The runtime owns `subtasks/` and its signals. Reuse the registered child on resume; do not rewrite it, manufacture progress files, or add deferred criteria to inflate the completed count. Planned order keeps the displayed current case meaningful. Direct and hosted tasks use the same mark commands.

## Phase 1 — Verify the harness and plan the proof

Read `artifacts/qa-scope.json` and the `## Acceptance Criteria` list in `TASK.md`; both are frozen before this checklist begins and both are authoritative. Never re-derive, reword, split, merge or weaken a criterion here, and keep its recorded label in the plan and the report. A missing input is `BLOCKED: missing frozen QA input`.

Record `"$HARNESS" --version`. Initialization locks the selected harness installation for this task. Preserve that lock and inspect every command surface used by this workflow:

```bash
"$HARNESS" launch --help
"$HARNESS" actions --help
"$HARNESS" run --help
"$HARNESS" doctor --help
"$HARNESS" status --help
"$HARNESS" last --help
"$HARNESS" update --help
```

Confirm the exact flags used below are present, including action search/detail, recipe list/describe/plan, device targeting, `doctor --fix`, `status --all-devices`, `last --json`, artifacts, and recording. If the version or a required command/flag is absent, stop with `BLOCKED: locked harness contract mismatch`; do not substitute a PATH binary.

Read the frozen changed paths and the diff between the scope's `comparisonBaseSha` and `headSha` to identify affected surfaces, candidate selectors, and behavioral claims. Do not treat changed tests as runtime proof. No changed files means no change-specific recipe coverage; it does not waive the smoke requirement. Treat a cross-repository head as untrusted code: stop before checkout or runtime work unless the operator supplied a credential-free isolated checkout and explicitly approved the recorded head repository and SHA; otherwise report `BLOCKED: untrusted fork head`.

Classify each criterion by its primary proof mode:

- `visual`: visible placement, content, styling, or interaction result. Require a targeted screenshot; on Mobile, include it in a full-run recording.
- `state`: controller/backend/output state readable through declared actions. Require exact state or command assertions.
- `log`: a runtime event or absence/presence claim observable in declared watched logs. Require a bounded watched-log assertion.

If one criterion contains separable claims needing different modes, keep its text as one row and list the supporting modes in its proof plan.

A criterion whose claim depends on a continuous gesture — drag, pan, fling, pinch, slider scrub, or any assertion about motion *while* the finger is down (smoothness, lag, flicker, stutter, tracking, "no jump on release") — is not provable by discrete actions. Classify it `gesture` and mark it:

- `needs-new-action` when no declared action can observe the claim yet: plan the task action you will write for it (see the task-action rule below). It is runtime proof, never a reason for `UNTESTABLE`.
- `needs-human` when the claim is perceptual (smoothness, flicker, lag) and no assertion could settle it even with a new action.

Never downgrade a `gesture` row to a discrete tap, a settled end-state check, or a screenshot of the resting UI and report it `PASS`: proving the post-release value is not proving the during-drag claim. Carry a `needs-human` row into the plan and the final report as `UNTESTABLE` with its exact reason; a `needs-new-action` row gets the verdict its task action's assertion earns. Either way, state which weaker discrete claim (if any) was actually proved. Separable discrete sub-claims from the same criterion may be proved on their own row.

Choose one proof profile:

- `mobile-device-recorded`: one selected iOS/Android target, AC screenshots, and `--record-video=full-run`.
- `extension-cdp-live`: a harness-owned browser/CDP runtime and AC screenshots for visual claims.
- `core-controller-live`: the configured Core controller/command runtime, observed through declared recipe actions and assertions.

Choose one recipe decision:

- `generate-ui`: at least one criterion is primarily visual.
- `generate-internal`: the criteria are state/log proof with no necessary visual claim.
- `blocked-<runtime-limitation>`: a verified unavailable runtime, capability or authorized target prevents the smoke path. A docs-only, test-only or empty change set does not waive explicitly requested QA smoke.

Backend-only is never by itself a skip reason. Use `generate-internal` when `command`, `assert_exit_code`, `assert_output`, `assert_json`, `watch_logs`, or a product action can prove it.

This decision is provisional until post-checkout action discovery. Do not claim a missing action before querying the active manifest.

Write the plan as the first version of `recipe-coverage.md`, one row per criterion:

| # | Acceptance criterion | Source | Proof mode | Planned proof | Preconditions |
|---|---|---|---|---|---|

Also record adapter, proof profile, recipe decision, changed surfaces, target device/environment, and every known limitation. The audit phase completes the same table with nodes, evidence and verdicts.

Full-run recording is not available for every platform. `"$HARNESS" run --help` proves only that the flag exists; support is proven by the actual target run producing its video artifact. For Android visual criteria, request `--record-video=full-run` on the recipe run and disclose the result. Continue when the artifact is produced. If the adapter returns a structured unsupported or provider-unavailable result, mark the visual criterion `UNTESTABLE`/`BLOCKED` with that exact reason; do not substitute `adb`, another recorder, or unrecorded visual proof. Never pre-block an Android-specific visual criterion solely because it targets Android. Android-only state/log criteria may run without video when their declared evidence fully observes the claim.

Write the plan before checkout or runtime work, then continue in the same run. If the decision is `blocked-<runtime-limitation>`, do not check out or launch: write one `UNTESTABLE` coverage row per criterion with that exact limitation, emit a `BLOCKED` report, and recommend the named static/check workflow instead.

## Phase 2 — Prepare the exact frozen head

For range, window or ref scope, the entry point has already put the clean, owned checkout at `qa-scope.json.headSha` with the operator's consent; verify HEAD equals that SHA and stop if it does not. Do not resolve the original moving ref again. Continue with steps 4 onward below. For Core, use the harness's declared controller/command runtime and omit mobile/browser launch commands. The following PR refresh/checkout steps apply only to PR scope.

1. Require a clean tree in this checkout. If `git status --short` is non-empty, stop and ask the operator to commit or stash; never stash or discard for them, and never move to another checkout, worktree or clone.
2. For PR scope, re-fetch the head metadata immediately before checkout. If `headRefOid` differs from the frozen SHA, retain the contract and report `BLOCKED: PR head changed during validation`. A new task may validate the new head; never retarget this task or overwrite its frozen scope.
3. Verify `git rev-parse HEAD` equals the frozen SHA from `qa-scope.json`; the entry point performed the checkout with the operator's consent. If it differs, stop and report; never substitute a moving branch, base branch or merge commit for the frozen head.
4. Read changed production files at the frozen head before deciding how to exercise them. For deletions, inspect the file at its recorded before revision and validate the intended removal.
5. For Mobile, run `"$HARNESS" status --all-devices --json`. Use the selected target. If it is unavailable or ambiguous, stop and ask for one iOS/Android target.
6. Launch the checked-out PR through the published harness:

   ```bash
   # Run exactly one Mobile command for the selected target
   "$HARNESS" launch ios --device "<selected device>" --verify --json
   "$HARNESS" launch android --device "<selected device>" --verify --json

   # Extension; add --sidepanel only when the review contract requires it
   "$HARNESS" launch --verify --json
   ```

   When `qa-scope.json` carries `remoteFlagSpec`, append `--remote-flag "<remoteFlagSpec>"` to every launch above, including any `--build` rerun. The harness pins the variant and fails the launch if the runtime does not hold it (`REMOTE_FLAG_NOT_APPLIED`), so the launch's own `remoteFeatureFlags` output is the proof; record it in the report.

   Let launch decide whether the current app build can be reused. If its next action says the build is missing or stale, run those exact launch arguments through `"$HARNESS"` with `--build`, and no product build command of your own devising.

   Dependency preparation is the exception, because the harness cannot do it: launch refuses a checkout whose `node_modules` tree is incomplete and names the checkout's own setup command (for Mobile, `yarn setup:expo --no-build-ios --no-build-android`). Run the command launch names, verbatim, then re-run the same launch arguments. Do not substitute a different install or build command, and do not treat this as licence to build the product yourself.

   If launch returns any other recovery action, follow it once through `"$HARNESS"` or stop with the exact blocker. Never request or expose a recovery phrase, private key, or password.

7. Establish the test plan's starting state before proof. For domain QA that requires an existing wallet, apply the approved fixture through `"$HARNESS" fixtures set --json` on this owned isolated profile, or verify an already matching wallet with declared wallet/account, feature-flag and domain-network reads. Extension `fixtures set` resets the profile and relaunches from prelaunch E2E state, so the earlier launch receipt is no longer current. When the frozen scope has `remoteFlagSpec`, append `--remote-flag "<remoteFlagSpec>"` to `fixtures set` or `reset` too. Retain the fixture result and post-setup runtime/account/network/flag observations before smoke; use `metamask.feature_flags.read` for flag readback. UI `wallet.import` tests a different onboarding journey and may leave consent/tutorial gates; do not substitute it for ordinary fixture setup. Onboarding, migration, account creation and first-time feature criteria instead keep their declared unfinished state. Fixture setup does not authorize financial mutations. After proof starts, do not reseed the active attempt: preserve its packages, record any necessary reseed as a new explicit setup/lifecycle phase, re-establish runtime identity and rerun smoke before dependent cases.

## Phase 3 — Discover the capability boundary

Run discovery from the PR checkout:

```bash
"$HARNESS" actions --json
"$HARNESS" run --list --json
```

For each proposed action or reusable recipe, narrow to the exact current contract:

```bash
"$HARNESS" actions "<AC search term>" --json
"$HARNESS" actions --action "<exact action name>" --json
"$HARNESS" run "<closest recipe>" --describe --json
```

The discovered list is law, including team/custom actions. Never recall names, fields, selectors, recipe refs, assertion operators, or platform support from memory. When no declared action can observe an AC, write a task action under a new name, modeled on a library action (`"$HARNESS" actions --action <name> --json` shows its `sourceManifest`) but self-contained (node built-ins, plus any helper copied next to it): keep its manifest in `<task>/artifacts/task-actions/manifests/` and its script in the sibling `<task>/artifacts/task-actions/actions/`, pass `--action-manifest <manifest>` to every `"$HARNESS"` `actions`, `run --plan`, `run` and `call`, and flag it in the report as a library candidate. A missing declared action is never a reason for `UNTESTABLE`.

Launch and the supported fixture setup above are the runtime bring-up steps. Do not call Cook's sandbox preparation path. The recipe itself must use discovered actions to establish and assert every required start-state prerequisite before a mutation or user-flow node. If the active manifest cannot deterministically establish a safe wallet, account, network, permission, or page state required by the review, mark the affected AC `UNTESTABLE` or stop `BLOCKED: non-deterministic runtime prerequisite`; never mutate arbitrary pre-existing state. Feature-flag state is not such a prerequisite: a variant the review needs is pinned at launch from the scope's `remoteFlagSpec`, read back with `metamask.feature_flags.read`, and changed on Mobile mid-run with `metamask.feature_flags.set` / `.clear` (the Extension needs a relaunch). A flag the scope does not name is a report finding naming the flag and the arm, never a hunt for undeclared overrides.

Re-evaluate the recipe decision against discovered capabilities. If it changes, update `recipe-coverage.md`, name the capability-driven change, and continue.

## Phase 4 — Author and plan the recipe

Use the frozen changed paths and criteria to select a dynamic set of discovered library recipes. Record each selected recipe's reason, covered criteria and source digest from the harness plan. Prefer composition or parameterization; author a missing path only when no existing recipe covers it. Preserve coverage gaps explicitly.

Keep the full frozen change/criterion inventory, then choose a risk-based execution plan for the requested assurance level. PR bug verification may require each acceptance criterion; daily/release integration validation normally combines essential domain smoke with focused checks for risky changes and cross-feature interactions. Do not recreate every prior PR recipe by default. For each selected proof target record its user situation, reusable setup/action recipes, assertion and task-owned cleanup. Record deliberate exclusions with risk/prior-evidence rationale before execution, without deleting or weakening authored criteria. Group compatible cases to reuse setup, but isolate conflicting or destructive states. An authorized prerequisite belongs in setup, not the blocker list. Compose existing primitives when no complete recipe exists.

Preserve the criterion's actual difficulty too. Do not add a stronger timing, platform or fixture requirement and then cite that invented requirement as a blocker. “Double-tap” requires two rapid user inputs and evidence of their effect; it does not automatically require two handler calls in the same JavaScript tick. Record the implemented input timing and check it against the authored claim. Likewise, a UI warning or slider interaction should not require submitting an order unless the claim depends on submission.

After smoke, execute the selected independent cases whose prerequisites can be established. If a case is not executable, attempt the smallest supported setup or capability check that determines why. Retain the result, not just “needs a fixture.” Use bounded retries for observed failures and continue other cases. A genuine unavailable capability, incompatible build, missing authority or failed prerequisite may block proof. An unfinished recipe, unattempted setup or exhausted run budget is nonexecution, not an inherent app limitation. Preserve the existing machine verdict vocabulary and add this precise coverage reason to the report; never improve a coverage number by weakening a criterion.

Every successful QA execution includes a real smoke path on the selected app, or live controller/command assertions for Core. Launch/health checks alone are insufficient. Plan, execute and validate the reusable smoke package before spending time on change-specific helpers or exploratory probes. Then compose independent cases around the recorded criteria so an early failure cannot hide unrelated coverage. Include smoke even when the change set is empty; change-specific checks cannot replace it.

Declare root `proofTargets` and bind each to portable `assert_output`, retained-state `assert_json`, or live `ui.wait_for` proof. Domain assertions return structured results. Use `assert_output` with its `source` and `assert` object to check them, for example `{"source":"assert-positions","assert":{"path":"$.matchingCount","operator":"eq","value":0}}`. Its `contains` and `match` options inspect stdout/stderr strings; do not use them for a structured action result. Keep composed actions within the same recipe run rather than nesting another harness invocation for the same checkout.

Compose the selected recipes into the task's Recipe v1 proof graph using the installed harness's documented composition mechanism. Preserve its resolved recipe/source digests and verify the execution used those same inputs. Keep the selected recipe list in the frozen task evidence.

Write `recipe.json` as Recipe Protocol v1 with `$schema`, `description`, root `paramsSchema`, and `workflow.{entry,nodes}`. Enforce:

- Every AC node ID starts `ac<N>-`; plumbing starts `setup-`, `gate-`, or `teardown-`.
- Every non-terminal node has a concise human-facing `intent`. The validator rejects an intent that restates the action, the node ID, a selector, or a generic verb (`workflow.invalid_intent`). Write the user-visible goal — "The trade screen is ready for the trader to choose an amount", not "Wait for the slider to mount".
- Every selected proof target has a planned assertion and start-state composition, or an evidence-backed unavailable prerequisite. Full-scope ACs not selected for a smart smoke run retain their explicit exclusion rationale; they are not labelled runtime blockers or certified by related smoke. Planned but unattempted cases remain execution gaps, not deliberate exclusions added after the fact.
- Visual evidence paths use `evidence-ac<N>-<claim>.png`.
- Use only exact discovered action names and fields.
- Use `eq`/exact equality rather than `contains`; use meaningful thresholds rather than existence checks. If a current watched-log action exposes only substring matching, require the full stable log line and disclose that weaker operator in the report.
- Use `workflow.teardown` for cleanup that must run after success or failure.
- Identify every node that mutates wallet, network, order, transaction, or persistent app state. Record its reset/teardown path before execution; absence of a proven reset makes any post-mutation replay ineligible.
- Never use a default branch to route around an AC assertion, a manual step, or a delay as a substitute for a declared wait action.
- For visual ordering/placement claims, combine a state/geometry assertion with a screenshot.
- Ask: “Would this assertion fail if the PR change were reverted?” If not, strengthen it.

Plan without touching the runtime. Run exactly one command matching the frozen adapter and selected Mobile target:

```bash
# Mobile
"$HARNESS" run <task>/artifacts/recipe.json --plan --adapter mobile --platform ios --device "<selected device>" --json
"$HARNESS" run <task>/artifacts/recipe.json --plan --adapter mobile --platform android --device "<selected device>" --json

# Extension
"$HARNESS" run <task>/artifacts/recipe.json --plan --adapter extension --json

# Core
"$HARNESS" run <task>/artifacts/recipe.json --plan --adapter core --json
```

Save machine stdout as `recipe-plan.json`, diagnostic stderr separately, and the harness process's own exit code; do not pipe the command through `tail` or mix logs into JSON. Use the installed harness's proof-preflight option when its help advertises one. This checks structural proof bindings only; it does not verify executed branches, runtime outcomes, or artifact indexing. Exit 5 or any schema/action error means the recipe is invalid: fix only against current discovery output, then plan again. If the CLI lacks a needed capability, stop and report the gap; never fake a plan.

## Phase 5 — Execute on the prepared runtime

Validate the first executed smoke package with the installed QA finalizer's `--check-only` mode and a smoke-only index before expanding the suite. This performs the same package, containment and runtime-proof checks without writing the final suite or QA result. Run this only after the smoke package exists; a runtime-proof failure is distinct from a recipe-plan schema error.

Phase 2 already launched and verified the checked-out PR app. Do not relaunch a healthy matching runtime. If liveness fails, run `"$HARNESS" last --json`, preserve its evidence paths, and stop with the returned next action. Do not loop or borrow another checkout's runtime.

Execute:

```bash
# Mobile
"$HARNESS" run <task>/artifacts/recipe.json --adapter mobile --platform ios --device "<selected device>" --artifacts-dir <task>/artifacts/recipe-run --record-video=full-run --json
"$HARNESS" run <task>/artifacts/recipe.json --adapter mobile --platform android --device "<selected device>" --artifacts-dir <task>/artifacts/recipe-run --record-video=full-run --json

# Extension
"$HARNESS" run <task>/artifacts/recipe.json --adapter extension --artifacts-dir <task>/artifacts/recipe-run --json

# Core
"$HARNESS" run <task>/artifacts/recipe.json --adapter core --artifacts-dir <task>/artifacts/recipe-run --json
```

Run exactly one command matching the selected platform.

Do not retry a deterministic state mutation with different values. Before any rerun after a partial execution, read `trace.json`. If a mutation node succeeded, first execute and prove its declared reset/teardown. If no reset exists or reset evidence fails, preserve the first run and stop with `BLOCKED: unsafe mutation replay`; never replay the whole recipe merely with the same values.

Bound exploratory diagnosis to a concrete causal question. Once a focused reproduction cannot distinguish product behavior from observation or environment, retain the uncertain finding and move to independent cases. Do not retry until green or claim a live-price discrepancy from unsynchronized captures as a reproduced regression.

Preserve the first failure and classify it:

- Product assertion failure -> continue to the evidence audit and report `FAIL`.
- Recipe/schema failure -> correct only from `actions --action` output, rerun `--plan`, then execute once.
- Fixture/runtime failure -> run `"$HARNESS" doctor --fix --json` and follow its exact next action.
- Harness failure -> run `"$HARNESS" last --json`, report the gap, and stop.

Every reproduction, retry or narrowing of a failure is a recipe run: extend `recipe.json` (or a variant beside it) and execute it with `"$HARNESS" run` into its own `--artifacts-dir` under `<task>/artifacts/`, so it is retained. Bare `"$HARNESS" call` invocations are for discovering and validating a node while authoring; they are never evidence. The one exception is a capture the report will cite (`ui.screenshot`, a state read): run it with `--artifacts-dir <task>/artifacts/calls/<label>` so it lands as a manifest-indexed package. A PNG copied loose under `artifacts/` has no manifest and is never published.

## Phase 6 — Audit evidence

Require and read `report.md`, `summary.json`, `trace.json`, `diagnostics.json`, the executed `recipe.json`, `artifact-manifest.json`, and every AC-bound PNG directly. When the recipe composes other recipes, also require the recorded resolution graph and resolved dependency documents. For a Mobile visual review, require the manifest-indexed video with `record: "full_run"`, verify its recorder target and inspect the recording. Use its recorded path; the harness may name it after the run directory. A warning that recording continued without video is a gap, not a pass.

For each AC:

1. Confirm every drafted `ac<N>-` node has a trace entry.
2. Derive executed/passed/failed counts from `trace.json`; never report drafted counts.
3. Match evidence to the claim, not its filename. A mounted element outside the visible frame does not prove a visual AC.
4. Reject blank, black, irrelevant, mislabeled, duplicate, synthetic, or DOM-raster screenshots. Check manifest capture provenance and require a real harness-owned device/browser capture for visual proof. A settled endpoint or matching DOM identity does not prove a temporal claim such as no flash, no intermediate reload, or continuous updates. Use time-spanning evidence or keep that part UNTESTABLE. Do not add DOM marker properties to manufacture continuity evidence.
For Extension evidence that must isolate the driven document, use the advertised `ui.capture_surface` action. It excludes browser chrome and adjacent panels; it may include content below the viewport, so keep viewport-visibility assertions separate.

5. Mark exactly one verdict:
   - `PASS`: the assertion executed and the evidence proves the whole review AC.
   - `FAIL`: an AC assertion failed or evidence contradicts the AC.
   - `UNTESTABLE`: the environment cannot produce the required state (a named environment or fixture limitation). A missing declared action is not one.

Never convert `UNTESTABLE` to `PASS`. If evidence is weak or missing, improve and rerun the recipe or mark the AC `UNTESTABLE` with a concrete reason.

Treat `diagnostics.json` warnings as adjacent, non-blocking leads. Report one as PR-specific only when the trace window and changed code establish the connection.

Complete `recipe-coverage.md`:

| # | Review AC | Mode | Recipe nodes | Evidence path | Verdict | Rationale |
|---|---|---|---|---|---|---|

Write `evidence-manifest.json` with only the strongest AC-bound evidence. If `recipe-quality.json` is absent, follow Cook's [Finish instructions](../skill.md#finish); never hand-author the final artifact.

Perform a bounded first code-review pass over the complete patch and changed production files. Report only correctness, regression, security, or missing-test findings that survive direct code/runtime validation. Give each finding a priority and concrete file/line reference; omit speculative concerns and style-only noise. Keep code findings separate from AC verdicts.

## Phase 7 — Emit the QA report

Use `/mms-recipe-qa/references/html-report.md` to render the single human QA report, and `report-example.md` for scope-specific presentation and delivery guidance. It does not replace the verdict rules or proof contract below.

Retain the declared dynamic cases in a standard Recipe v1 `qa-suite/suite-scope.json` and their actual outcomes in `qa-suite/suite-result.json`. Reference each executed package's summary path and digest. Include the smoke case even when no changed behavior requires another case. Record missing execution as nonexecution, never remove a case to make the suite pass. A composed graph may be one case when its proof targets account for the selected criteria.

Save an index with `packages` mapping case IDs to retained recipe package directories, and `smoke: { caseId, proofTarget }`. Run the QA skill's `scripts/finalize-qa.mjs --task <task> --index <index.json>` to validate packages, finalize the suite and write `qa-proof.json`. The result binds the frozen source, suite and package evidence without caller-specific identities or profile data.

For a corrected attempt on a finalized task, follow Recipe QA's Execute and finalize `--reselect` procedure. Preserve case IDs, smoke, source and inputs; retain prior registrations/packages and advance only the existing farm result binding. Never overwrite the old proof/index or hand-author a result. Replay COMPLETE to recapture review.

For range/window scope, title the report with that scope and include the frozen commits/window, selected recipe digests, smoke result, coverage and gaps. Omit PR-specific recommendation text; no PR publication is implied. Write `artifacts/report.html` for the human report. For PR scope, retain the proposed-review format as a delivery artifact only.

For PR scope only, re-fetch `gh pr view "$PR_URL" --json headRefOid` before writing the report and compare it with the frozen, locally validated SHA. If it moved, report `BLOCKED: PR head changed during validation`. Retain the evidence under its original SHA and request a new QA task for the new head. Never overwrite the scope or attach old evidence to the new SHA.

Render `artifacts/report.html` from `artifacts/report-data.json` using Recipe QA's renderer. Include the tested head/build, platform, scope, selected plan, recorded verdict, smoke proof, full criterion inventory, findings and evidence. For PR scope include the reviewer recommendation below. Do not author duplicate `qa-report.md` or `report.md` copies. Raw `recipe-run/report.md` remains an automatically generated execution artifact, not a second QA report.

Every `FAIL` verdict and every finding cites a retained run (its artifacts directory and node id). A claim with no retained run is `UNTESTABLE`, never `FAIL`.

Overall verdict rules:

- `PASS`: the runtime smoke assertions passed, every review AC is `PASS`, and Recipe Quality is `pass`.
- `FAIL`: a runtime smoke assertion or any review AC is `FAIL`, or Recipe Quality is `fail`.
- `PASS WITH GAPS`: runtime smoke assertions passed and there are no failures, but at least one AC is `UNTESTABLE` or Recipe Quality is `warn`.
- `BLOCKED`: smoke proof did not execute, or a frozen skip limitation or checkout/tool/runtime failure prevented meaningful execution. Launch or health checks alone cannot satisfy this gate, even when there are no changed files.

Recommendation rules:

- `READY FOR HUMAN REVIEW`: verdict `PASS`, Recipe Quality is `pass`, and there are no validated correctness findings.
- `CHANGES RECOMMENDED`: verdict `FAIL`, Recipe Quality is `fail`, or there is any validated correctness/security/regression finding.
- `MANUAL VALIDATION NEEDED`: verdict `PASS WITH GAPS` and no change-request finding.
- `BLOCKED`: overall verdict `BLOCKED`.

For PR scope, map the proposed reply recommendation without changing its meaning:

- `READY FOR HUMAN REVIEW` → `APPROVE`
- `CHANGES RECOMMENDED` → `REQUEST_CHANGES`
- `MANUAL VALIDATION NEEDED` or `BLOCKED` → `COMMENT`

For range/window scope, write `artifacts/learnings.md` and return `artifacts/report.html` and the evidence directory. Do not invent a PR number, review recommendation or PR reply. The remaining reply and line-comment steps apply only to PR scope.

For PR scope, prepare `artifacts/review-reply.md` using the selected checklist's `## Proposed Reply Format` exactly: preserve its heading order and team language, fill every section from validated evidence, and omit no required section. If the selected checklist has no reply format, use `Summary`, `Acceptance Criteria`, `Validation`, `Findings`, `Evidence`, `Limitations`, and `Recommended Action` in that order.

Copy the proposed reply to `artifacts/review.md` as the portable review artifact. Keep `## Summary` and `## Recommended Action` in hosted reply formats; the latter must contain the mapped review recommendation. Write `artifacts/learnings.md` without secrets. Return the detailed report, proposed reply, and evidence directory. Do not post or approve the PR.

Write `artifacts/line-comments.json` as:

```json
{
  "pr_number": 123,
  "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT",
  "summary": "Concise evidence-backed summary",
  "comments": [
    {
      "path": "changed/file.ts",
      "line": 42,
      "body": "Validated finding and required action",
      "severity": "must_fix|suggestion|nitpick"
    }
  ]
}
```

Retain every finding in the report. Inline comments must resolve to RIGHT-side added or context lines in the diff at the frozen head; keep out-of-diff notes in the body, `comments` empty when none qualify, and never post the artifact automatically.

## When not to use

Use static review for inspection requests with no runtime validation goal. Explicit daily/release QA may have no changed runtime behavior; its successful outcome still requires the selected runtime smoke proof. This workflow uses the MetaMask harness and its declared adapters.

## Worked example

Read `qa-example.md` when an example would help classify ACs, render the contract freeze, map nodes, or format the final report. Do not copy its selectors or action names without rediscovering them in the active checkout.

The portable result also binds the retained `qa-scope.json` and suite-scope document through
`scope: { path, digest, suiteDigest }`. The finalizer computes canonical JSON digests using
`digestRecipeDocument`; consumers can verify these plus the scope's reported base/head.
Do not substitute a scope or suite from another validation.
