# Domain QA across changes

The question is whether the selected changes work together in the assembled app. A daily Perps run and a release run use the same `recipe-qa` entry point, Cook checklist and recipe library. The scope and target change; the execution method does not.

## Inputs

| Request | Scope | Runtime target |
|---|---|---|
| Previous rolling day | `{"kind":"window","ref":"origin/main","hours":24}` | Head frozen at the window cutoff |
| Previous calendar day | `window` with explicit ISO `since` and `until` | Head frozen at that cutoff |
| Release | `{"kind":"range","base":"v13.49.0","head":"origin/release/13.50.0"}` | Frozen release head |
| Domain regression on one build | `{"kind":"ref","ref":"<SHA>"}` | That commit, with domain-plan or caller criteria |

Pass `--domain perps` to select the registered team library. These are skill inputs, not `mm-harness run` options. The resolver selects window commits by first-parent committer timestamps, not GitHub PR merge timestamps. State that selection in the report. A scheduled caller should freeze explicit boundaries and reuse the task on retry, so a delayed run does not shift its coverage window.

A domain is a library and test-plan selection, not an automatic author filter. Inventory the range, map relevant changes to the team's criteria, and explain exclusions. Include shared wallet changes that affect Perps. Missing ownership or test-plan information is a coverage uncertainty, not permission to call an empty selection complete.

## One combined proof

- Daily Perps validation uses the approved ready-wallet fixture, like dev/fix-bug work. Before proof, apply the locked harness's `fixtures set` on the owned isolated profile, then verify account, network, flags and readiness against each case and earlier baselines.
- On Extension this seeds standard E2E state and approved accounts, unlike UI `wallet.import`, which can leave Terms and first-time gates visible. The seed requests Perps testnet and completes tutorial/first-order state. Verify the Perps provider network separately from the EVM chain with a supported read such as `metamask.perps.read_positions network=<expected>`.
- Apply Cook's Mainnet rule in `.agents/skills/mms-recipe-cook/SKILL.md`.
- The seed also defaults to the side panel, so select and record the intended display mode during setup.
- Verify wallet/account identity with `metamask.wallet.read_state` and flags with `metamask.feature_flags.read`; fixture setup is not authority for financial actions.

- Onboarding is setup unless a criterion tests it. Onboarding, account-setup, Perps tutorial and first-order profiles need their declared fresh or migration fixture and must exercise those gates as product behavior. Never seed away required unfinished onboarding.
- Scope kind alone does not choose the fixture. Reuse a verified ready wallet that matches the contract; a new browser profile does not require UI onboarding.

Start with the domain's reusable smoke and regression journeys, then compose recipes covering the included PR criteria and their interactions. For example, category filtering and account-data recovery may each pass alone but interfere when navigating back to Perps home. Preserve both original criteria and label the combined check `derived`.

- Use catalog metadata and targeted recipe descriptions before authoring. Compose references and parameters; reuse setup, navigation, reads and assertions, adding task-local nodes only for uncovered behavior. A prior pass does not guarantee compatibility or prove a new feature.
- Consume structured results first; inspect detailed traces and media where the proof contract or a failure requires them.

- Choose risk-based proof targets from the full change inventory. Plan each target's start state, reusable setup, missing task-owned records, assertion and cleanup; share safe setup across cases to spend time on uncovered behavior.
- Missing a complete recipe is not a blocker when declared primitives can compose it. Attempt authorized prerequisite creation, then record the failed setup/action or unavailable capability. "Needs an order/position/history record" alone is not a blocker.

- Measure coverage against all frozen criteria. Distinguish proved, failed, not run, incomplete evidence and blocked-by-observed-prerequisite; explain legacy `UNTESTABLE` rows with coverage reasons without changing machine verdicts.
- Report setup reuse, time to first proof and composition gaps. Continue attainable independent selected checks without expanding smoke into every historical AC. An exhausted budget means unfinished work, not proof that remaining cases cannot be tested.

- Run on the frozen assembled head and keep the release unchanged; being behind `main` is expected. Follow the locked harness's drift guidance to distinguish version differences from regressions, adapt the smallest stale recipe node without weakening criteria and retain fresh evidence. Check supported versions or declare a compatibility boundary before promoting a reusable repair.

Record runtime identity separately from source scope: proof lane, client, build/artifact identity, flags, fixture and relevant network state. The frozen scope's `proofLane` decides what runs; absent means `source-dev`.

- `source-dev`: the frozen head built from source. Label its evidence `source-dev`; it never validates the official release build.
- `official-unmodified`: the official release build of the frozen head, unchanged.
  - Before setup, run `node <installed-skill>/scripts/acquire-official-artifact.mjs --scope <task>/artifacts/qa-scope.json --platform <android|extension> --out <task>/../scratch-<id>/official --record <task>/artifacts/runtime-artifact.json`.
  - It takes the release branch CI build of that exact head (Mobile `android-apk-main-rc`, Extension `build-dist-webpack`), checks it against GitHub's artifact digest and records the file SHA-256, version and build.
  - Launch with the locked harness's `runtime-launch` and the recorded `launch` arguments plus `--target` and the task's `--device` or `--cdp-port`; the harness verifies that identity again on install.
  - No CI build for the frozen head, iOS, a failed verification, or setup the harness refuses for an artifact is `BLOCKED` with that reason.
  - Never fall back to a source build on this lane.
- `official-qa-derived`: the official build with approved QA changes. It needs a harness-declared derivation that records each change; until the installed harness declares one, report `BLOCKED: no supported QA derivation`.

## Select the assurance level

PR validation and integration smoke answer different questions. Preserve all authored criteria for traceability, but do not automatically replay every PR's original suite for daily/release integration checks.

Before feature proof, record a compact plan containing:

- Essential domain smoke and the recent changes each journey crosses.
- Targeted checks for financial mutations, shared state, changed validation/error paths, novel provider behavior, integration collisions and weak/missing prior evidence.
- Lower-risk detail deliberately omitted, with the prior evidence or risk rationale and what would trigger a deeper check.

Use a few composed user situations to cover multiple changes where the assertions really observe each claim. Prefer a representative integration check over many duplicate isolated checks. Escalate depth when smoke fails or reveals ambiguity; keep the original selected plan so escalation and deferred work are visible. Prior PR evidence informs selection but does not certify the current release build.

- A selected check must not be abandoned merely because setup requires composing a recipe.
- Conversely, an AC deliberately outside the selected assurance level is not “untestable.” Report selected-plan results separately from full-AC coverage: “smoke passed, 6/6 planned checks; 12/28 full criteria re-proved” is different from “release fully validated.” Only use full validation when the required full scope actually has proof.

## Report

Produce one QA report for the run, containing:

- Frozen base/head or window, runtime identity, domain/library revisions and included/excluded PRs.
- Smoke, change-specific and integration criteria mapped to recipe nodes, verdicts and retained evidence.
- Product failures separated from recipe drift, harness/runtime failures and untested criteria.
- Reproduction steps and the remaining human checks; no claim beyond the executed assertions.

An empty change window still runs the selected smoke. Missing proof cannot become a pass. Follow Cook's existing verdict rules and the finalizer's package validation; a partial report does not satisfy an all-passing completion gate.

## Direct use and orchestration

An engineer can request:

> Use mms-recipe-qa with domain perps and scope {"kind":"window","ref":"origin/main","since":"2026-09-23T00:00:00Z","until":"2026-09-24T00:00:00Z"}. Validate Perps-relevant changes together, run domain smoke, reuse the team library, and produce one report with exclusions and gaps.

For release QA, replace the scope with the release range above. Resolve its refs before freezing. Both calls use `qa/default` and the same materialized task contract.

A farm QA profile supplies these inputs and the shared template. The orchestration layer owns slot allocation, runner launch, admission, task retention and result validation. A schedule may submit the same request; selecting a `daily` profile alone does not create a timer. Publication is a separate authorized action.

Keep one workflow source. The skill owns scope, criteria and report policy; Cook owns the checklist; the library owns reusable journeys; the harness owns execution and version-specific recovery. Farm configuration must not duplicate that workflow.

## Improvement-loop acceptance

In the retrospective, separate a missing reusable capability from one that existed but was not discovered or composed. Route verified reusable fixes to the library, execution/observability failures to the harness, and planning or unsupported blocker claims to this workflow. Preserve original failed attempts and add observer corrections separately.

- A local edit is not an installed improvement.
- Before a fresh autonomous comparison run, verify the installed skill/template/library/harness revisions and use the same frozen scope and comparable runtime/fixture conditions.
- Do not coach the agent during execution.
- Compare selected-plan completion and full-scope coverage separately, along with observed blockers, setup reuse and native inference usage/cost.
- Record model and cache differences; duration is not a proxy for token cost.
- Unknown usage remains unknown.
- Close the learning only after the new run demonstrates the intended benefit without weaker assertions; keep unverified proposals open.
