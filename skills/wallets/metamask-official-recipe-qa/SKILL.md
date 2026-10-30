---
name: recipe-qa
description: "Validate the runtime effects of a PR, a base/head range (a release is a range), or a window of landed changes: derive the acceptance criteria from that scope, then prove them through the shared Recipe Cook checklist."
disable-model-invocation: true
maturity: experimental
---

# QA from a frozen change scope

Use only when explicitly named by the user or selected workflow. Read the installed `mms-recipe-cook/SKILL.md` as this entry point's declared dependency. Cook proves and the team library owns recipes; this entry point owns the scope and the criteria.

For daily domain checks or release validation, read [Domain QA across changes](references/domain-qa.md). These use this same entry point and `qa/default`: validate the assembled app at one frozen head using domain smoke plus change-specific recipes.

## 1. Scope, optional

- PR: `{ "kind": "pr", "url": "https://github.com/owner/repo/pull/42" }`.
- Range: `{ "kind": "range", "base": "<baseline ref>", "head": "<target ref>" }`. A release is the previous release to the release head.
- Window: `{ "kind": "window", "ref": "<branch/ref>", "hours": 24 }`. Explicit ISO `since`/`until` pin a historical window and override `hours`.
- Ref: `{ "kind": "ref", "ref": "<commit or branch>" }`. Any commit, no diff: a daily or release regression. Criteria come from the domain plan or the caller.
- Any kind may add `"remoteFeatureFlags": { "<flag>": "<variant>" | true | false | { … } }` to pin remote-config overrides for the run, the way an A/B test needs its `treatment` arm. The resolver freezes it as `remoteFlagSpec`, the exact `--remote-flag` value every launch carries. When the diff gates its behaviour on a flag the request does not name, derive the criteria anyway, name the flag and the arm each criterion needs in the report, and let the caller rerun with the field set; never guess a variant.
- Any kind may add `"proofLane": "source-dev" | "official-unmodified" | "official-qa-derived"` (default `source-dev`) and `"mainnetOptIn": true`. Both freeze with the scope; [Domain QA](references/domain-qa.md) says what each changes.

With no scope, take the checkout's current PR from `gh pr view --json url,headRefName,headRefOid` and require exactly one match; with no PR, range the checkout branch against its base. Use a checkout of that repository and refresh moving refs before freezing, fetching missing objects without resetting unrelated work. A fork head stays untrusted for runtime execution until the isolated-checkout and authorization requirements are met.

Then compare the checkout with the scope head. Already on the PR branch (or at the range or ref head): continue without asking. Anywhere else: say which branch and commit the checkout is on and whether it is clean, and ask before switching; on yes, fetch the head and check it out (a PR branch by name, a bare commit detached; fetch the exact object when the branch is gone). Never switch a tree with uncommitted changes: stop instead. Cook never switches checkouts. This is a gate: do not derive criteria or initialize a task until the checkout is at the scope head, so a "no" leaves nothing behind.

## 2. Domain, optional

`--domain <name>` selects the team library whose recipes, checklist and test plan apply. It is not a Git author or path filter. For a domain-only request, record the included changes and the team-owned criteria or supplied selectors that make them relevant; retain excluded changes and selection uncertainty in the report. Shared wallet changes may affect the domain even when another team authored them.

## 3. Derive the acceptance criteria, before any template

Build one numbered list from the scope:

- `pr`: the PR body and its linked tickets. Keep authored criteria verbatim, labelled `authored`; only when none exist, derive candidates from the description and changed files, labelled `derived`. Caller-supplied criteria replace extraction and stay verbatim.
- `range` / `window`: the union over the PRs landed in that scope, each row keeping its PR reference. When the caller explicitly limits validation to a domain or PR set, retain the full change inventory and derive coverage for that recorded selection; never silently drop a selected criterion. Include integration criteria where the selected changes share a user journey, labelled `derived`, without replacing the original criteria.
- With a domain: also that library's test-plan cases, keeping their stable case IDs. A range plus a domain is that domain's plan, run on this release.
- `ref`: the domain's test-plan cases or caller-supplied criteria only; with neither, stop and ask for one.

Pass the list as the task text (`--task-text` or `--task-file`) and as separate, verbatim `--acceptance` flags to Cook's initializer. This records the criteria in `TASK.md` and the handoff. Never reword, split, merge or weaken a criterion to fit a recipe.

## 4. Materialize the task

If TASK/CHECKLIST already exist, run Cook's `scripts/init-template --resume-task-dir <task>` to verify its retained tooling and continue the recorded checklist without changing task files. Otherwise run `scripts/init-template --task-kind qa [--domain <name>]` with that task text, forwarding the supplied project/provider selectors. Use `qa/default`; only a `--template <id>` the caller passed selects another, and a team library may shadow a template by ID. Never ask which template to use. Initialization does not run QA: never pass `--prepare` or create a second task.

## 5. Freeze the scope

Save the scope input as `<task>/inputs/qa-scope-request.json`, or reuse it when supplied, then run from the repository:

```bash
node <installed-skill>/scripts/resolve-scope.mjs --input <task>/inputs/qa-scope-request.json --out <task>/artifacts/qa-scope.json
```

For a dispatched task, run `node <installed-skill>/scripts/resolve-scope.mjs --farm-input <task>/inputs/qa.json --out <task>/inputs/qa-scope-request.json`. The adapter overlays admitted scope on matching-kind preset defaults, maps `proof_lane` to `proofLane`, and binds `source` base/head only to `kind: pr`. Ranges, windows and refs use their own revisions.

`expectedHeadSha`/`expectedBaseSha` bind the request to known commits; the resolver rejects a mismatch, reads Git and provider data without checking out code or launching an app, and never overwrites a frozen scope. On resume, reuse the artifact and its SHA. A request whose scope input differs from a frozen `qa-scope-request.json` for the same target (any key, `remoteFeatureFlags` included) is a new task, never a resume.

## 6. Execute and finalize

Follow the materialized checklist and `/mms-recipe-cook/references/qa.md`. Save an index containing `packages` (case id → retained run package dir) and `smoke` (`caseId`, `proofTarget`), then run `node <installed-skill>/scripts/finalize-qa.mjs --task <task> --index <index.json>`. It validates the retained packages and emits portable `artifacts/qa-proof.json`; missing or failed packages block finalization, so preserve their evidence and report the gap.

For the template's early smoke gate, use the same command with `--check-only` and a smoke-only index. It validates retained packages without creating or replacing the final suite or QA result; do not write a custom validator wrapper.

After a corrective replay, write a new index changing only attempt paths and run `node <installed-skill>/scripts/finalize-qa.mjs --task <task> --index <new-index.json> --reselect` against the existing farm binding; never combine with `--suite` or `--check-only`. Keep original attempts and replay COMPLETE afterward to recapture the result; this grants no review or publication approval.

If a required ref, runtime target, Cook template or declared recipe capability is unavailable, report that missing input or blocked capability. Never substitute a successful static review for runtime QA.

Select a risk-based proof plan for the requested assurance level before feature execution. For `qa/default`, register its selected cases through Cook's existing `qa-cases` child-checklist instructions to track individual case progress; completed cases are assessed outcomes, not automatic passes. Explicit alternative templates keep their own checklist contract unless they declare a child binding. Daily/release smoke does not automatically require replaying every prior PR's full AC suite; retain full inventory and explicit omitted-detail rationale. Do not stop selected coverage at existing recipes. Compose supported actions for the selected checks and attempt prerequisites already within the caller's authority. Distinguish not attempted, incomplete proof, and an observed blocker; an unmet prerequisite or missing recipe is not by itself evidence that a criterion is untestable. Retain the attempted setup/capability check and concrete failure, or the explicit budget/scope reason execution stopped.

## 7. Report

Read [QA report reference](references/report-example.md) for presentation and delivery guidance. Keep Cook's verdict rules and artifact contract. Daily, release, range and ref runs save the report locally with findings, gaps and evidence; publication is a separate authorized action.

Render structured evidence as self-contained `artifacts/report.html`, the sole human report, following the [HTML reference](references/report-example.html) and [rendering instructions](references/html-report.md). Include PR titles/links and full frozen criteria; keep IDs secondary. Contents, collapsible criteria and criterion images must work offline. Preserve machine proof, raw outputs and historical reports.

When Cook completes, return the report and evidence paths. For a `pr` scope with a domain whose static review skill is installed (perps: `/mms-perps-review-pr <PR URL>`), run it too and report its source findings in their own section, never merged with the runtime verdicts. Then ask what to do next; the usual path is posting the report as one PR comment through `/mms-recipe-pretty-pr`'s evidence-comment target, which hosts the manifest-indexed screenshots and refreshes the same comment on a rerun. Cook stays silent; posting and cleanup are separate explicit actions.
