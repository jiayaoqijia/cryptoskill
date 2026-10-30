# Team libraries

Keep ownership separated:

- `recipe-cook` owns template routing, sandbox preparation, checklist execution, and proof closeout.
- `mm-harness` owns generic runtime, action/recipe discovery, execution, and artifacts.
- The team library owns domain checklists, parameterized recipes, assertions, defaults, and safe preconditions.
- Product code and controllers own business rules, state transitions, validation, and transactions. Actions only translate stable UI/CDP/controller operations; recipes compose them.

## Register

```bash
export RECIPE_LIBRARY_PATH="<team>=$HOME/shared-library/<team>"
```

`recipe-cook` discovers optional checklists from `<library>/checklists`; the
harness discovers actions and recipes from the same root. When `checklists/`
is absent, canonical templates remain available and no other library directory
is scanned as a checklist. Named roots provide the stable domain/source identity
used by `--domain`; unnamed roots are general-only. Do not encode a personal
checkout path in shared files.

## Customize

1. Copy the nearest `<task-kind>/<variant>.md` checklist (`dev`, `fix-bug`, `qa`, or static `review-pr`). Its catalog ID is that relative path without `.md`; add frontmatter only when it cannot be inferred.
   - A runtime PR QA customization can use the platform ID `qa/pr.mobile` or `qa/pr.extension`. It shadows Cook's bundled template only when that team domain is selected.
   - Keep exact-head checkout, harness provenance/launch, evidence integrity, recommendation rules, and terminal artifacts in Cook's `references/qa.md`. The team checklist adds domain recipes, review heuristics, report sections, and its shared `## Proposed Reply Format`; it must not replace those safety contracts.
   - The selected checklist owns the proposed reply's headings, order, and team language. Keep `## Summary` and `## Recommended Action` for the review report format, write the preview to `artifacts/review-reply.md`, and never post it automatically.
2. Put safe, deterministic defaults and exact invocations in the checklist. Ask only for product intent, unsafe mutation, credentials, or real ambiguity.
   - Custom templates must retain Cook's acceptance-criteria and per-criterion reporting requirements.
3. Reuse runtime capabilities in this order:
   - `mm-harness run --list --json` then `run <recipe> --describe --json`;
   - existing team recipes;
   - existing actions;
   - direct CDP/controller access for task-specific inspection;
   - a new shared recipe only after discovery proves repeated inference, reuse, or a safety invariant;
   - a new action only when UI actions, controller access, and composition cannot express a repeated operation with a stable contract.
4. Validate the recipe with `mm-harness run <recipe> --plan` before live execution.

Use the task's provenance-locked `mm-harness help --json` for catalog
size, parameterization, composition, drift repair, compatibility, and promotion
rules. Team libraries add stable domain vocabulary and checklist policy; they do
not redefine the versioned recipe method. Keep one-off acceptance proof in the
task directory.

## Invoke

Default template:

```text
/mms-recipe-cook <task>
```

Known team checklist, no menu:

```text
/mms-recipe-cook --template <exact-template-id> <task>
```

An unavailable preselection must stop and print valid exact IDs; it must never fall back silently.

PR QA with one named team library:

```text
Codex: Use $mms-recipe-qa for <PR URL> using domain <domain>
Claude: /mms-recipe-qa
Cursor: @mms-recipe-qa <PR URL> using domain <domain>
```

Cook passes `--domain <domain>`, resolves the effective
`qa/default` template (or an explicitly selected `qa/pr.<platform>`), records its source/digest, and
continues without a template confirmation gate.

## Static review

Invoke the team's installed static review skill directly. For Perps, `mms-perps-review-pr/SKILL.md` already contains the shared checklist and the repository overlay composed by the skills installer. When a parent task freezes the source bundle instead of installing it, register the shared skill and selected `repos/<repository>.md` as consecutive child checklists using `mark sub start <name> --step <n> --from <file>`. The parent owns completion and publication. No harness installation or application launch is needed.

The Perps library remains the rules source. Its maintainer regenerates the skill and references with `node scripts/materialize-review.mjs --library <canonical-perps-library>`; `--check` verifies outputs and source digests. For a shell-less analyzer, `--analyzer-out <file> --client <client>` emits the same checks with their rule text inline. No analyzer is enabled by installation.

Other teams may provide a static execution-template catalog when needed. Register it with `RECIPE_COOK_TEMPLATES_DIRS` and select its explicit template ID. Do not create a duplicate catalog merely to invoke an installed checklist-shaped skill.

## Review verdicts

Apply to static review and code self-review; runtime QA keeps its verdict mapping in `qa.md`. Use a declared approval policy when supplied. Otherwise APPROVE requires zero blocker, major or minor findings and at most three nits; a minor or four nits means COMMENT with concrete asks; a blocker or major means REQUEST_CHANGES. Preserve a team's blocking domain checks.

A minor is a real defect or gap, such as a wrong value, changed behavior without a test, a false PR-description claim or a duplicated helper. A nit affects only style or wording. Size alone is not a finding; unrelated concerns mixed into one PR are a minor asking to split.

Retain every finding in the report, including body-only notes. Inline comments must resolve to RIGHT-side added or context lines in the diff at the reviewed head; out-of-diff findings stay in the body. Recompute the recommendation when findings or severities change.

For a PR follow-up, retain previous findings and review only the new committed delta at the requested head. Uncommitted fixes do not resolve a finding at that head. Direct self-review still includes working-tree changes. Do not re-review an unchanged PR head.

## Dev and fix-bug domain review

Read domain `D` from `<task>/inputs/handoff.json`; never infer it from paths. In `artifacts/review.md`, record `N/A: no domain` if absent, or `N/A: no review skill for domain <D> (.agents/skills/mms-<D>-review-pr/SKILL.md absent)` if the skill is missing. Either completes the domain step.

Otherwise read the installed skill and applicable references. Review the implementation and test diff, including committed, staged, unstaged and untracked changes. Record base, head, working-tree status and reference revisions in `artifacts/review.md`; mark missing references `NOT_CHECKED`. Do not install or refresh skills mid-task.

With `n` set to the parent's domain step, reuse its existing child on resume or register it once:

```bash
<task>/mark sub start <D>-review --step <n> --from .agents/skills/mms-<D>-review-pr/SKILL.md
<task>/mark sub <D>-review <criterion-number>
<task>/mark sub <D>-review complete --report artifacts/review.md
```

Execute the child checklist and repository overlay read-only, without harness commands, app launch, product edits or publication. Fix findings in the parent, rerun affected validation and review the updated content before completing the child. Keep it open until the final verdict and criterion outcomes are recorded. Never overwrite the parent checklist. Child completion does not replace runtime proof or independent review gates.
