---
name: recipe-cook
description: "Run MetaMask recipe-backed development, bug fixing, or runtime PR QA through one live checklist and mm-harness proof. Present compatible template IDs and stop for a new human reply unless the caller supplies an exact ID or a SELECT default is available. Resume an existing materialized task instead of creating another one."
disable-model-invocation: true
maturity: experimental
---

# Recipe Cook

Use only when explicitly named by the user or a selected workflow. Descriptions, labels and changed paths never activate this skill or another skill. A selected template may declare dependencies by name; read their installed files explicitly as part of that workflow.

Cook selects or resumes one execution template and works its checklist. Team skills own domain criteria. QA uses recipes for runtime proof; static review needs no app, device, recipe or harness. Template metadata filters candidates only after invocation.

The portable task runtime behind `mm-harness` owns TASK.md, CHECKLIST.md, provenance and the task's mark command. No control-plane installation or configuration is required. Scripts live under `.agents/skills/mms-recipe-cook/`.

## Versioned recipe method

For dev/fix-bug/QA, task initialization records and locks the harness it resolves: an explicit `MM_HARNESS_BIN`, else the `mm-harness` found on PATH, else an explicit task-local install. Execution and checklist markers verify that recorded installation; only explicit initialization or resume may resolve a replacement.

The lock covers implementation files and validator dependencies, excluding external runner state directories `.omc` and `.omx`. For unattended runs, the caller should supply a run-owned harness installation and recipe-library snapshots; a version receipt does not isolate a shared installation from concurrent updates.

This skill routes and governs the task; it does not teach recipe syntax from memory. The first recipe-authoring action after the task's harness is locked is:

```bash
mm-harness help --json
```

Run it through the task's recorded harness and follow that version's discovery, composition, branching, quality, and drift-repair guidance. Recipe, recipe-library or action-contract mismatches never block: copy the closest recipe into the task, adapt to current actions and continue. For an explicitly supplied existing task, read its recorded harness and run this before resuming recipe work.

At the recipe-authoring step for dev/fix-bug/QA, after the task's acceptance criteria are recorded, check whether that harness's `recipe-quality --help` advertises `advisor-status`. If supported, follow [optional recipe advice](references/advisor.md), reusing prior assessments on resume. Older harnesses continue without advice. Static review does not use this step. Forward explicit `--advisor`, `--advisor-model` and `--advisor-stages` task options; never turn key availability into opt-in or change engineer settings on the task's behalf.

## Start

For a static `review-pr` request with no explicit `--template`, apply [review verdicts](references/team-libraries.md#review-verdicts), then invoke the selected team review skill directly and skip the numbered materialization steps below and Cook's Finish procedure. Use that skill's output and completion contract. If a parent task has frozen the source bundle, execute its shared skill and selected `repos/<repository>.md` as the parent's consecutive child checklists; the parent owns completion. If the requested skill is missing, report that gap instead of substituting runtime QA. An explicit `--template` keeps the catalog procedure below.

Work directly in this checkout. Before materialization, limit work to reading the source task and its evidence, routing, and template selection. Do not inspect product code or launch subagents; generic batching or parallelism guidance does not override this order. Never delegate file, component, symbol, route, fixture, or recipe discovery; use bounded subagents only for genuinely cross-cutting synthesis described below.

1. Capture task (natural language or local prompt file); `init-template` records it in the task's `TASK.md` (`--task-text` or `--task-file`). If the invocation explicitly provides an existing materialized task directory, run `init-template --resume-task-dir <path>`, resume its recorded checklist, and skip steps 2–6. Never create a second task/checklist. Otherwise treat the invocation as new; never list or read prior `temp/tasks/recipe-cook/*`.
2. Route exactly one flow:
   - `qa`: PR, range or time-window runtime validation through `/mms-recipe-qa`. Use `qa/default` and [the QA execution contract](references/qa.md). Resume an existing task rather than creating a second checklist.
   - `review-pr`: static inspection of a PR or branch. Invoke the installed team review skill directly, or select its explicit static template if one is provided; no app launch, runtime preparation, or harness installation. Missing criteria or reference repositories remain reported gaps.
   - `fix-bug`: broken behavior or a reproduction/fix request.
   - `dev`: a new/change request, a diagnose-only investigation, or a smoke test of the current checkout with no PR, range, window or bug.

   Runtime PR validation is `qa`, through `/mms-recipe-qa` with `qa/default` (`qa/pr.<platform>` only by explicit `--template`). Performance work remains `dev`/`fix-bug` and may use an explicitly requested `/mms-recipe-performance`.
3. List: `.agents/skills/mms-recipe-cook/scripts/list-templates [--task-kind <task-kind>] [--domain <domain>]`. It delegates discovery to the shared catalog, through the portable task tooling.
   - If the invocation contains `--template <ID>`, require that exact ID in `.templates[]` from `list-templates --json`; skip steps 4–5. If absent, print valid IDs and stop. Never fuzzy-match or substitute.
   - When no `--template` is specified, use the `SELECT:` id printed by `list-templates` and skip steps 4–5; other listed ids are opt-in through `--template`. This does not select a later wallet fixture; the fixture must already exist or be named by the caller.

4. When no `SELECT:` line was printed (for example `review-pr` or a missing default), show compatible IDs as a numbered list with **recommended** pick + one-line why. A one-character reply selects that item; also accept its exact ID. Decide from catalog metadata, not template bodies.
5. **Wait for template selection.** A new human message containing a number or exact ID confirms; a step 3 selection is the only exception. While waiting: no tools, reads, initialization, sandbox, or product work.
6. After selection, run `.agents/skills/mms-recipe-cook/scripts/init-template --task-kind <task-kind> --template <selected-ID> --slug <slug> --title "<source task title>" --task-text "<the request, verbatim>" [--task-file <path>] [--acceptance "<criterion>"]... [--ticket <source ticket>] [--source-ref <PR URL>] [--domain <domain>]`, adding `--prepare` only for `dev` and `fix-bug`. Pass known criteria verbatim and in order as separate `--acceptance` flags; never treat a ticket ID or task prose as extracted criteria. When both `--task-file` and `--task-text` are given, the file is the description and the text is only the conversational form. Use the source title/ticket/PR URL exactly. The shared producer writes TASK.md and one CHECKLIST.md with template provenance. Runtime flows lock one harness first; tracked static review uses the same task tooling without preparing or launching an app. For runtime initialization, follow the existing harness-resolution choice when required; `sandbox.json` is authoritative after dev/fix-bug preparation. If preparation fails, follow the printed recovery lines.
7. Print the task document and checklist paths (`TASK.md` + `CHECKLIST.md` for a new task, or the recorded checklist for a resumed task); from the repo root invoke that task directory's `mark` by path (`temp/tasks/recipe-cook/<task>/mark start`, then `…/mark N`). `mark` self-resolves; do not `cd` into the task directory.

## Hard rules

| When | What |
|------|------|
| Acceptance criteria | Before edits or proof, record observable task criteria under `## Acceptance Criteria` in the task's `TASK.md` (never as checkboxes; `CHECKLIST.md` is the only step list). A resumed task without `TASK.md` gets one created beside its checklist with the same sections. Preserve supplied wording; label derived criteria and assumptions. Resolve material ambiguity through the selected template's existing gates; QA criteria arrive frozen. Never weaken criteria to fit a recipe. Report evidence and a verdict for each criterion, including unresolved gaps. |
| Before dev/fix-bug implement / recipe run | Checklist **Sandbox ready** gate (details in harness skill): `doctor --fix`, resolve any numbered fixture choice, then status/launch-or-reuse/verify for **this checkout only** |
| review-pr | Execute the selected review skill or explicit static checklist against its frozen diff. Record criteria outcomes, findings and gaps; no product edits or runtime actions. |
| qa | Read `references/qa.md`; prove the frozen criteria with runtime smoke plus change-specific recipes. |
| Gate order | Mark each prerequisite before continuing. Never begin product edits until the recipe plan or baseline gate is marked PASS; never batch-mark it after editing. |
| Progress | For dev/fix-bug/QA, send a brief update at checklist phase changes and before a long setup or proof step. If it runs quietly for several minutes, report the active step and elapsed time from `mm-harness status --task <task-dir>`; name any known blocker. Avoid narrating every command or guessing why a step is slow. |
| Before product edits | Local **task branch** (`<ticket>-<flow>-<slug>-hhmm`); preserve explicit task markers such as `do-not-merge` in its name; follow the task host's commit policy; direct invocation keeps the diff uncommitted unless the engineer requested a commit. No PR |
| Skill baseline | Installed skills are immutable after task start: never run `yarn skills` or another skill install/update/sync command. If ancillary guidance is missing, use existing repo conventions and record the gap; do not replace the task's skill baseline. |
| fix-bug | No product edits before baseline proof |
| Checkout | Work only in the checkout you were started in: its ports, device, browser profile and wallet fixture belong to it. Never create a worktree or clone, never borrow another checkout. |
| Investigation | Never inspect git stashes or other task branches. Start with direct `rg`/read inside this checkout or explicitly named skill/harness roots; never search `/` or unrelated host paths. Never assume a domain value's shape: before comparing, normalizing, or transforming it, search the current domain for an existing helper and reuse it. For a bounded external dependency API lookup, use `.agents/skills/mms-recipe-cook/scripts/find-package-symbol <package> <symbol>`. If a linked example is not local, use the documented local pattern instead of hunting for it. No subagent for a single path/symbol lookup. Delegate only cross-cutting synthesis, capped at 10 tool calls and 10 result bullets. One investigation per question; consume its result before retrying, never duplicate. |
| Recipe method | When the selected template requires runtime proof, after task materialization, run `mm-harness help --json` through the task's provenance-locked harness. Follow its version-matched discovery, parameterization, composition, branching, node-by-node authoring, quality, and drift-repair guidance. It also owns failure diagnosis and runtime-blocker evidence. Cook adds workflow policy but does not restate or override the installed harness contract. |
| Final recipe run | Keep the authored document at `<task>/artifacts/recipe.json`; run it with `--artifacts-dir <task>/artifacts/recipe-run`. The nested directory is the immutable run package; top-level `artifacts/` also holds reports and `check diff` output. |
| Proof | Runtime claims require a real-app recipe assertion: live action or run-scoped marker/log. Tests corroborate only. Temporary markers use a logging path proven active in the target build, observe only, and are removed. An unobservable marker is evidence setup: fix its channel and rerun. `state` = logs/action; positive `visual`/`mixed` = wait for the claimed target selector (not a page root), then **read PNG**; negative UI claims = `ui.wait_for` with `expected: absent` on that selector, plus capture + **read PNG** when the AC is visual. On the first deterministic-state mutation failure, stop: do not tune parameters, retry, or switch mutation actions; capture the exact action/error and record the target BLOCKED/N/A. Never force product state or rendering to manufacture evidence. |
| Mainnet | Apply the [Mainnet rule](#mainnet-rule) for network selection, gaps and cleanup. |
| Coverage | Product code: focused test + project analyzer **>=80% new lines**. Never commit to make an analyzer see working-tree changes; if it cannot, keep focused-test evidence and record the analyzer limitation as an explicit coverage gap. |
| Mid-run | Local artifacts only — **no** `gh pr create` / PR push |
| Learning capture | Never put secrets in reports or learnings; reference them by name only. Successful terminal marks stage locally through mm-harness. Central sharing is opt-in: set `METAMASK_AGENTIC_LEARNINGS_DIR`, then separately approve `mm-harness checklist closeout <task> --share`. |

For dev/fix-bug, read `references/dev-fix-bug.md` after materialization. Read `references/team-libraries.md` for library setup/customization or its domain-review section when the checklist requires it.

For `qa`, read `references/qa.md` after materialization; read `references/qa-example.md` only when an example is useful. Do not load either for dev/fix-bug.

## Mainnet rule

- Testnet is the default; use mainnet only when the dispatch requests it. Mainnet proof requires the dedicated fixture account, explicit platform opt-in and the harness's mainnet policy. QA also requires frozen `mainnetOptIn: true`.
- For Perps, use `dev1` only, 1x isolated market orders, at most $15 notional at worst-case fill and `close_immediately: true`. Every order node sets `network: mainnet`.
- For Perps Mobile, select `metamask.perps.start_state account=dev1 network=mainnet`; reads follow the app's network. Restore with `metamask.perps.start_state network=testnet`.
- For Perps Extension, select `metamask.wallet.select_account name=dev1`, switch the app to mainnet in its UI and set explicit `provider` on order nodes. The fixture-policy lane forbids `--funding-*` files. Confirming positions/orders reads set `network: mainnet`.
- For Perps Core, opt in with `CORE_PERPS_ALLOW_MAINNET_WRITES=1`; confirming positions/orders reads set `network: mainnet`, since reads otherwise default to testnet.
- Close or cancel task-created orders/positions, confirm with a read and retain every order ID and confirming read. Restore testnet before the next case, except on an Extension build without that toggle. Switch networks between cases, never mid-proof.
- If mainnet is unavailable, unfunded, not opted in or refused by the harness, prove what is possible on testnet. The AC verdict covers only the observed testnet proof; the mainnet claim stays UNTESTABLE with `mainnet gap: <reason>`, never PROVEN/PASS. A mainnet gap alone does not block completion on the testnet proof.
- For Perps Extension without `perps-testnet-toggle`/`METAMASK_DEBUG`, source-dev runs try `mm-harness launch --verify`, then `mm-harness launch --build --verify` with `METAMASK_DEBUG=true`. Never rebuild an official artifact. If testnet stays unreachable, mark affected claims UNTESTABLE with `testnet gap: <reason>`, not `mark blocked` for network selection.

## Finish

If a required runtime claim remains unproved, keep repairing it. Use `./mark blocked` only for missing credentials, a product decision the ticket does not settle, or a farm/device failure outside the checkout. A checklist's "or BLOCKED" branch does not authorize `complete` or a `fixed` disposition. Apply the Mainnet rule for network-gap exceptions. When the harness records `awaiting-review` for captured visual proof, prepare any explicitly requested local PR draft below and return that pending status. Never approve the criterion, weaken its proof kind, or complete the task to bypass review.

1. `artifacts/pr-description.md` (or `artifacts/no-change-report.md`) + `artifacts/learnings.md`. The PR description follows the repository PR template headings and carries the proof summary (what changed, root cause, validation, evidence paths). `qa` writes the single human `artifacts/report.html`; static `review-pr` writes its declared review outputs. The frozen `inputs/worker-terminal-contract.json` is authoritative for required artifacts. When the request explicitly asks for PR evidence or a PR description, also write `artifacts/pr-description.md` on a no-change outcome, stating that the product is unchanged and preserving proof gaps. When a recipe exists, also write:
   - `artifacts/recipe-coverage.md`: proof target -> node -> evidence.
   - `artifacts/evidence-manifest.json`: strict visual selection only. Example: `{"version":1,"preferred_mode":"screenshots","standalone":[{"label":"AC1","covers":["AC1"],"file":"after-ac1.png"}]}`. For state-only proof: `{"version":1,"summary":"No visual evidence required."}`.
   - If `artifacts/recipe-quality.json` is absent, apply the quality section from the task harness's `help --json`, write `artifacts/recipe-quality-input.json`, then run `mm-harness recipe-quality build`. Never hand-author the final artifact.
2. An explicit request for PR evidence or a PR description selects `/mms-recipe-pretty-pr` for local packaging. Once the retained run and quality report are ready, read that installed skill, apply its evidence gate, and run its package script before the terminal mark, including no-change and `awaiting-review` outcomes. Keep pending human review explicit in the draft; packaging does not approve claims or authorize publication.
3. `./mark complete --mark-last` (or `./mark no-change --reason "..."`) only when the task checks permit it. Otherwise return the pending review status and local draft paths without completing the task.

## After task completion

Return the report, requested local draft and artifact paths, then stop. Do not inspect caller identity, publish, ask publication/cleanup questions or release resources. The caller controls any subsequent action. Pretty PR remains a separate explicit invocation when the original request did not ask for PR evidence or a PR description.
