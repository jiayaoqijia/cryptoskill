---
name: implementation-plan-review
description: Expert review of an implementation plan against a GitHub issue/enhancement description (provided as a local file or a GitHub issue URL) and the current repository codebase. Use when asked to critique a plan for correctness, completeness, codebase alignment, risks, and test/rollout readiness (do not implement).
disable-model-invocation: true
---

# Implementation Plan Review (Expert)

Review an implementation plan for coverage, correctness, and fit with the current codebase. Do not implement.

## Inputs

- Implementation plan: a local file path.
- Issue/requirements: either (a) a local file path, or (b) a GitHub issue number (run from the target repo so `gh` resolves it).

If the user provides a GitHub issue number, prefer fetching it into a local file using the bundled script:

```bash
bash scripts/fetch_github_issue.sh <issue-number> --out /tmp/issue.md
```

Run this command from the skill directory when that directory is inside the target repository. If it is not, keep the
command agent-agnostic by resolving the script path relative to this skill directory while running `gh` from the target
repo so the issue number resolves against the correct repository.

Fetching is a network operation. When command execution is sandboxed, request
network escalation (`require_escalated`) for this exact fetch command rather
than granting a reusable broad `bash` permission. On failure, follow the
script's self-contained `ACTION` line. It distinguishes unavailable network
(exit `6`), credentials unavailable to the process (exit `3`), other GitHub
fetch failures (exit `4`), and local output failures (exit `5`).

## Workflow

1) Prepare a clean review run:
   - Before reading or listing any scratchpad files, run from this skill directory:

```bash
bash scripts/new_scratchpads_dir.sh <plan-file>
```

   - Use exactly the absolute path the script printed on stdout as this review's run directory; never glob or guess a path under `scratchpads/` yourself.
   - Each run creates a fresh timestamped directory (`scratchpads/<YYMMDD-HHMM>/`); nothing is deleted. Directories from earlier reviews belong to a different run — never read or reuse them for this review. (If the printed path is ever lost from context, the lexicographically-last timestamp subdirectory is the most recent, since the format sorts chronologically — but prefer the printed path.)
   - If the script fails (non-zero exit; `error: <message>` on stderr), stop and report the failure.

2) Read the two inputs in full:
   - Plan file
   - Issue description file (or the fetched `/tmp/issue.md`)

3) Apply versioning neutrality policy:
   - Do **not** request a missing version bump (package version, `server.json`, manifests, etc.) unless a repo rule, user instruction, release plan, or issue text explicitly requires one.
   - Do **not** suggest removing version bump steps merely because the issue does not mention versioning. Issues usually describe the problem, motivation, or code-level improvement; they are not expected to spell out release mechanics.
   - If the plan already includes version bump steps, review them only for correctness and consistency with applicable repo rules: required files, matching version strings, valid version format, and no unrelated version/manifests changed.
   - Raise a versioning finding only when the plan's versioning steps are internally inconsistent, contradict explicit requirements, or are objectively attached to the wrong files/surfaces.

4) Apply review-noise policy:
   - Do not raise findings only because an implementation plan omits developer execution mechanics such as checking `/.dockerenv`, choosing host vs devcontainer command prefixes, or spelling out both command variants.
   - Do not teach command invocation mechanics in recommendations.
   - Review verification semantically: required test/lint/integration categories, targets, and coverage, not how a developer invokes commands in their environment.
   - Still flag objectively wrong verification scope, such as requiring only a narrow test subset when repo rules require the full default suite.

5) Validate codebase reality (start targeted, expand as needed):
   - Start by finding referenced modules/configs/env vars/tests with `rg` (fast and low-noise).
   - Prefer opening the minimal set of files *first* to confirm patterns and naming, but broaden freely if you suspect hidden coupling or cross-cutting behavior (e.g., shared helpers, config loading, response models, pagination, truncation).
   - If the plan touches MCP tools, REST API, docs, or tests, cross-check relevant `.cursor/rules/*.mdc` guidance.
   - If it improves confidence, use any other repo investigation strategy (e.g., inspect docs like `SPEC.md`/`API.md`, check tests, use `git blame`, or run unit tests/lint locally).

Suggested commands (adapt as needed):

```bash
rg -n "name_in_plan|function_in_plan|ENV_VAR_IN_PLAN" -S .
rg -n "ToolResponse\\[|@mcp\\.tool\\(|log_tool_invocation" blockscout_mcp_server -S
rg -n "ServerConfig\\(|BaseSettings\\(|BLOCKSCOUT_" blockscout_mcp_server/config.py -S
rg -n "pytest\\.mark\\.integration|tests/integration|tests/tools" tests -S
```

6) Independently adjudicate candidate findings:

   Read these two skill resources completely before creating candidate inputs or
   launching adjudicators:

   - `references/finding-adjudication-protocol.md`
   - `assets/finding-adjudication-report.md`

   Treat every initially suspected problem as a **candidate**, not a final
   finding. Do not create candidates for pure summary text or obvious nits.

   For each candidate, create a directory in the clean run:

```text
finding-01-short-slug/
├── input.md
├── full-report.md  # written by the adjudicator
└── brief.md        # generated by the finalizer
```

   Create `input.md` with:

   - candidate ID;
   - absolute plan, issue snapshot, template, protocol, and output paths;
   - one neutral, falsifiable candidate hypothesis;
   - focused research questions;
   - candidate-specific scope or edge cases;
   - an explicit statement that `Confirmed`, `Downgraded`, `Question`, and
     `Closed` are all successful outcomes.

   Do not include prior scratchpad conclusions, a preferred solution, expected
   disposition, or another adjudicator's work.

   Launch one independent subagent per candidate, batching when concurrency is
   limited. Use `fork_turns="none"` so the adjudicator receives only the
   candidate input and stable protocol. Prefer a strong reasoning model
   (`gpt-5.6-sol` with `xhigh` reasoning when available) unless the user
   requests otherwise. The launcher prompt should contain only:

   - the absolute protocol path and instruction to read it completely;
   - the absolute `input.md` path;
   - the exact writable candidate directory;
   - the absolute template path;
   - the requirement to run the protocol's finalization loop before returning.

   Each adjudicator must write `full-report.md`, run
   `scripts/finalize_adjudication.py`, fix every validation error, and return
   only the protocol's short completion record. The script deterministically
   generates `brief.md`; the adjudicator must not edit the brief.

   After all adjudicators finish, independently verify the complete run:

```bash
python3 scripts/verify_adjudication_run.py \
  --run <absolute-run-directory> \
  --expected-count <candidate-count>
```

   If verification fails, send the exact errors back to the responsible
   adjudicator and require it to correct and re-finalize its report. Do not use
   an invalid or stale brief.

   Read all valid `brief.md` files first. Open the full report or extract a
   tagged section only when progressive disclosure is warranted, for example:

   - unexpected `Closed` or `Downgraded` disposition;
   - low confidence or a close variant result;
   - a decision that depends on an unresolved product assumption;
   - overlap or conflict between candidates;
   - a recommendation that materially expands plan scope;
   - a challenged finding.

   Extract one validated section without loading the full report:

```bash
python3 scripts/finalize_adjudication.py \
  --report <candidate-directory>/full-report.md \
  --extract <section-slug>
```

   The main agent owns cross-finding work: deduplicate overlapping candidates,
   resolve conflicts, apply one common severity scale, and assess cumulative
   scope. Case-specific rubric totals are not comparable across candidates.

   Only `Confirmed`, actionable `Downgraded`, and unresolved `Question`
   candidates may reach final §4. Omit `Closed` candidates. Point the final
   comment's `Scratchpad` field to the candidate's generated `brief.md`, never
   directly to `full-report.md`. The brief's generated `Source` link is the
   progressive-disclosure path to the full report.

7) Produce the review in the required format (next section).

## Required output format

Produce a review with these sections:

### 1) Understanding

- Issue summary
- Acceptance criteria (bulleted)

### 2) Plan ↔ Requirements coverage

- What is covered well
- What is missing / ambiguous

### 3) Codebase alignment

- Key files/modules you inspected (with paths)
- Assumptions in the plan that match the codebase
- Assumptions that don’t match (explain and suggest correction)

### 4) Review comments (actionable)

Provide comments as a list. Each comment must include:

- Severity: `Blocker | Major | Minor | Question | Nit`
- Location: plan section/step + (when relevant) repo file/function/class
- Problem: what’s wrong / missing
- Recommendation: concrete change to the plan
- Rationale: why it matters (bug risk / security / perf / maintainability)
- Scratchpad: path to the candidate's generated `brief.md`, when the comment is actionable and not a pure `Question`; never link `full-report.md` directly from the final review

**Testing gaps rule:**

- List every specific missing/incorrect test as an actionable comment in **§4**.
- In **§6**, provide a consolidated checklist that references those items **without repeating full explanations**.

### 5) Junior-dev readiness check

- Missing task-specific prerequisites, step ordering, and verification coverage
- Do not flag omitted environment-specific command invocation details
- Where the plan needs more explicit detail

### 6) Test & rollout strategy

- Consolidated test checklist (Unit / Integration / E2E / Negative & security / Performance & regression), referencing §4 test comments
- Migration/rollback plan if applicable
- Feature flags / safe rollout suggestions if applicable

## Review focus checklist (use as prompts, not new requirements)

- Coverage: every acceptance criterion mapped to plan steps.
- Codebase alignment: paths, module structure, naming, existing helpers and patterns.
- Edge cases & compatibility: pagination, timeouts, empty results, truncation limits, backward compatibility.
- Security: input validation, SSRF/DNS rebinding boundaries, secrets handling, logging redaction, auth assumptions.
- Performance/scale: API call counts, caching, pagination strategy, long-running tasks/progress updates.
- Ops/observability: error handling, logs, metrics/telemetry/analytics implications, rollout/rollback.
- Versioning: only comment if explicitly required by the issue description; otherwise assume omission is intentional.
