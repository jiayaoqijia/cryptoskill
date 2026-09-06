---
name: plan-export
description: Export a detailed phased implementation plan for a GitHub issue to a file, reading all applicable rules from .cursor/rules before planning
argument-hint: [issue-number (optional)]
disable-model-invocation: true
---

# Plan Export Skill

This skill composes a detailed, phased implementation plan for a GitHub issue. The issue number can be passed as `$1` or discovered from the conversation context (e.g., after a `/gh-issue-publish` invocation). The plan is designed for a junior developer with minimal knowledge of MCP, Blockscout, and other 3rd-party components but strong Python experience.

## Prerequisites

Before invoking this skill, the agent must already understand the scope of the changes through prior conversation. The skill assumes:

1. The feature/issue has been thoroughly discussed
2. The agent understands what needs to be changed
3. The agent has read the relevant source files that will be modified

## Workflow

### 0. Determine Issue Number

Before proceeding, resolve the GitHub issue number to use throughout the plan:

1. **If `$1` is provided and non-empty**, use it directly as the issue number.
2. **Otherwise**, search the current conversation for:
   - A GitHub issue URL matching `https://github.com/.../issues/<number>` — extract the number from the URL. This is typically present after a preceding `/gh-issue-publish` invocation (which outputs the URL).
   - An explicit issue number reference like `#<number>` or `issue <number>`.
3. **If multiple distinct issue numbers are found** in the conversation, list them and ask the user which one to use.
4. **If no issue number can be determined** from either source, ask the user to provide one before continuing.

Once resolved, use this number as `$1` for all subsequent steps.

### 1. Identify Applicable Guidelines

Read `.cursor/AGENTS.md` to determine which rules from `.cursor/rules/` apply to the discussed changes. That file contains the authoritative mapping of when each rule should be applied.

### 2. Read All Applicable Rules

**MANDATORY:** Read each applicable rule file using the Read tool before composing the plan. Do not skip this step or guess rule contents.

For each rule file:

1. Read the complete file content
2. Note specific requirements, patterns, and constraints
3. Incorporate these into the implementation plan

### 3. Compose the Implementation Plan

**This skill is the complete and only source for the plan's format.** The template below, the slice-marker rules, and the `--inspect` validator in step 6 define every convention you need — section order, marker syntax, the shape of the verification command blocks, all of it. Because the format is fully specified here, you never need to look at another plan to copy its conventions, and you must not: do not open or grep any other file under `.ai/impl_plans/` or `temp/impl_plans/`. Reading a sibling plan does two kinds of harm — it spends context on a document irrelevant to this issue, and, more insidiously, it anchors you to another feature's scope, phasing, and wording, biasing the plan you're writing now. If you're unsure your markers are correct, don't compare against an example — write them per this template and let the step-6 `--inspect` check prove them. (The pattern examples this skill asks you to cite are *source and test files for this feature*, referenced by path — never other plans.)

Create a detailed Markdown document at `.ai/impl_plans/issue-$1.md` with the following structure.

**Slice markers — required.** Wrap every section in paired, namespaced HTML-comment markers so the plan can be sliced deterministically by `scripts/slice_impl_plan.py` (headings alone are unreliable — plans embed code blocks and exact documentation that legitimately contain `#`/`##` as content). Rules:

- Wrap the **preamble** — the title, issue link, Overview, Applicable Guidelines, and Definition of Done — in one region `slug="preamble"`.
- Wrap **each phase** in its own region `slug="phase-<n>"`, where `<n>` is the phase's sequential number (1, 2, 3 … contiguous, matching the `## Phase <n>` heading). Number only the phases you actually emit. Put `title="<short phase name>"` on the begin marker.
- Wrap the **Final Checklist** in `slug="final-checklist"`.
- Markers start at column 0. Every `begin` has a matching `end` with the same slug; never nest them. No real content may live outside a region (blank lines and `---` rules between regions are fine). A `title` must not contain a double-quote.

The structure, with markers in place:

```markdown
<!-- impl-plan:begin slug="preamble" -->
# Implementation Plan for Issue #$1

**GitHub Issue:** https://github.com/blockscout/mcp-server/issues/$1

## Overview

[Brief summary of what needs to be implemented - 2-3 sentences]

## Applicable Guidelines

[List the rule files that were read and applied to this plan, with brief notes on key requirements from each]

---

## Definition of Done — Test Integrity (non-negotiable)

[Mandatory. In your own words — explain the *why*, don't just recite rules — state that the work is done only when its tests genuinely pass for the right reason, for unit and integration tests alike. The wording is yours, but the section must get these points across: each failure is diagnosed (regression vs. legitimately changed expectation) and its root cause fixed, never worked around (no skip/xfail, deletion, loosened assertions, or bypassed hooks); a test is updated only when intended behavior changed; a test that couldn't run, timed out, or hung is a defect to diagnose, not a pass (for integration tests, point at the timeout-protected runner from rule 200); and no phase is "done" while any test is failing, disabled to avoid a failure, or unverified.]
<!-- impl-plan:end slug="preamble" -->

---

<!-- impl-plan:begin slug="phase-1" title="[Phase Name - Functional Changes]" -->
## Phase 1: [Phase Name - Functional Changes]

### Objective

[What this phase accomplishes]

### Files to Modify/Create

- `path/to/file.py`: [Brief description of changes]
- ...

### Implementation Details

[Explain WHAT needs to be changed and WHY. Focus on project-specific context the developer needs to understand:]

- What existing patterns/helpers to reuse and where to find them
- What project conventions apply (naming, structure, error handling approach)
- How this change fits into the existing architecture
- Any non-obvious dependencies or side effects

**Do NOT include code snippets.** The developer knows Python - explain the project-specific aspects they need to understand.

### Unit Tests

- **File:** `tests/tools/category/test_feature.py`
- **Purpose:** [What functionality this test validates]
- **Scenarios to cover:**
  - [List scenarios: success cases, error handling, edge cases]
- **Reference:** [Point to similar existing test file as a pattern example]

### Verification

1. Run unit tests for modified functionality:

   ```bash
   pytest tests/tools/category/test_feature.py -v
   ```

2. Run linting and formatting checks:

   ```bash
   ruff check path/to/modified/files/
   ruff format --check path/to/modified/files/
   ```

3. Fix any linting or formatting issues before proceeding to the next phase.
<!-- impl-plan:end slug="phase-1" -->

---

<!-- impl-plan:begin slug="phase-2" title="[Phase Name - Additional Functional Changes]" -->
## Phase 2: [Phase Name - Additional Functional Changes]

[Same structure as Phase 1, including its own unit tests]
<!-- impl-plan:end slug="phase-2" -->

---

<!-- impl-plan:begin slug="phase-N-1" title="Integration Tests" -->
## Phase N-1: Integration Tests

### Objective

Verify the implementation works correctly with real network calls.

### Files to Create

- `tests/integration/category/test_feature_real.py`

### Test Scenarios

- **Purpose:** [What real-world functionality this validates]
- **Scenarios to cover:** [List scenarios with expected outcomes]
- **Reference:** [Point to similar existing integration test as a pattern example]

### Verification

1. Run integration tests for the new test file:

   ```bash
   pytest -m integration tests/integration/category/test_feature_real.py -v
   ```

2. Run linting and formatting checks:

   ```bash
   ruff check tests/integration/category/test_feature_real.py
   ruff format --check tests/integration/category/test_feature_real.py
   ```

3. Fix any linting or formatting issues before proceeding to the next phase.
<!-- impl-plan:end slug="phase-N-1" -->

---

<!-- impl-plan:begin slug="phase-N" title="Documentation Updates" -->
## Phase N: Documentation Updates (if needed)

**Only include this phase if documentation changes are required.** If no documentation updates are needed, omit this phase entirely.

### Documentation Files

For each documentation file that requires changes, provide **exact text content** to add or modify (documentation requires precise wording):

#### SPEC.md

[Exact section and content to add/modify, if applicable]

#### AGENTS.md

[Exact section and content to add/modify, if applicable]

#### API.md

[Exact section and content to add/modify, if applicable]

#### README.md

[Exact section and content to add/modify, if applicable]

#### TESTING.md

[Exact section and content to add/modify, if applicable]

#### .env.example

[Exact lines to add, if applicable]

### Verification

Review all documentation files for accuracy and completeness.
<!-- impl-plan:end slug="phase-N" -->

---

<!-- impl-plan:begin slug="final-checklist" -->
## Final Checklist

- [ ] All phases completed and verified (including per-phase linting)
- [ ] Every test passed *for the right reason* — none skipped, xfailed, deleted, loosened, or left unrun/timed-out to declare success; any failure was traced to its root cause and fixed
- [ ] All unit tests pass: `pytest tests/tools/`
- [ ] All integration tests pass: `pytest -m integration tests/integration/`
- [ ] Final linting check on entire codebase: `ruff check .`
- [ ] Final formatting check on entire codebase: `ruff format --check .`
- [ ] Documentation updated (if applicable)
- [ ] Version bumped (if applicable)
<!-- impl-plan:end slug="final-checklist" -->

```

### 4. Content Guidelines

**MUST INCLUDE:**

- Reference to the GitHub issue (with full URL)
- List of applicable guidelines that were read and applied
- Phases that allow incremental verification
- Explanations of WHAT to change and WHY (project-specific context)
- References to existing code as pattern examples (file paths, not snippets)
- Complete documentation text (documentation requires precise wording)
- Specific test scenarios with clear descriptions
- Verification steps for each phase (including tests, linting, and formatting checks)
- A mandatory "Definition of Done — Test Integrity" section, placed after "Applicable Guidelines" and before the first phase, covering both unit and integration tests

**MUST NOT INCLUDE:**

- Code snippets for functional changes or tests (developer knows Python)
- Time estimates
- Assumptions about developer's MCP/Blockscout knowledge
- References to "see documentation" without providing the content
- Vague instructions like "update as appropriate"

**PHASE ORGANIZATION:**

1. Only include phases that have actual work to do - omit empty phases
2. **Keep phases small and focused**: Each phase should have a single, clear objective that can be completed, tested, and reviewed as an independent unit. Prefer multiple small phases over fewer large ones.
3. Organize phases so each can be independently verified with its own tests
4. Start with core functionality, then tests, then documentation (if needed)
5. Each phase should build on the previous one

**Phase Size Rationale**: Since each phase's code goes through review, smaller phases are easier to review thoroughly. Catching issues early (e.g., in a model definition phase) prevents building faulty logic on top of flawed foundations.

**Examples of Good Phase Breakdown**:
- ❌ **Too Large**: Phase 1: Create model + handler + all unit tests
- ✅ **Better**: Phase 1: Create model + model unit tests, Phase 2: Create handler + handler unit tests
- ❌ **Too Large**: Phase 1: Refactor 5 modules + add new feature + update tests
- ✅ **Better**: Phase 1: Refactor module A + tests, Phase 2: Refactor module B + tests, Phase 3: Add new feature + tests

**DEPENDENCY ORDERING:**

1. **Between Phases**: Changes in a subsequent phase must build on top of changes from previous phases. Never reference functionality that will be created in a later phase.
2. **Within a Phase**: In the "Implementation Details" section, describe dependencies before things that use them:
   - If a handler uses a data model, describe the model first, then the handler
   - If code imports a helper function, describe the helper first, then the code using it
   - If a test requires a fixture, describe the fixture first, then the test
3. **Files Listing Order**: In "Files to Create/Modify" sections, list files in dependency order (dependencies first)

### 5. Write the Plan File

Save the plan to:

```text
.ai/impl_plans/issue-$1.md
```

### 6. Validate Slice Markers (self-check)

Before handing back, prove the plan you just wrote can actually be sliced. Run the validator in inspect mode (it writes nothing):

- Devcontainer (`/.dockerenv` exists): `python scripts/slice_impl_plan.py .ai/impl_plans/issue-$1.md --inspect`
- Host: `uv run python scripts/slice_impl_plan.py .ai/impl_plans/issue-$1.md --inspect`

Read the exit code:

- **0** — the plan is sliceable. Proceed.
- **non-zero** — the validator prints exactly which marker is unbalanced, duplicated, out of order, or which content escaped a region. **Fix the markers in the plan file and re-run `--inspect` until it exits 0.** Never hand back a plan that fails this check: a plan that cannot be sliced cannot be implemented by `implement-plan`.

### 7. Output and Control Transfer

After writing the plan file:

1. Confirm the file was created with the full path
2. Provide a brief summary of the phases
3. **Stop and wait for user instructions** - do NOT begin implementing the plan

Output format:

```text
Created implementation plan at [.ai/impl_plans/issue-$1.md](.ai/impl_plans/issue-$1.md)

The plan includes {N} phases:
1. [Phase 1 name]
2. [Phase 2 name]
...

Applicable guidelines that were incorporated:
- [List of rule files read]

Awaiting your instructions to proceed.
```

## Important Notes

- **Do NOT implement the plan** - only create the plan document
- **Slice markers are mandatory.** Wrap preamble / each phase / final checklist in paired `<!-- impl-plan:begin slug="…" -->` … `<!-- impl-plan:end slug="…" -->` markers (see step 3) and confirm the plan passes the step-6 `--inspect` self-check before handing back
- The plan must be self-contained and not assume access to conversation history
- **Never read other plans.** This SKILL.md fully defines the format; opening another `.ai/impl_plans/` or `temp/impl_plans/` file only burns context and biases this plan toward another feature (see step 3)
- **Only include phases with actual work** - do not create placeholder phases that say "no changes needed"
- **No code snippets** for functional changes or tests - explain WHAT and WHY instead
- Point to existing files as pattern examples (e.g., "follow the pattern in `tools/address/get_address_info.py`")
- Documentation updates DO require exact text content (prose requires precise wording)
- If the conversation lacks sufficient context, ask clarifying questions before creating the plan
- Each phase must have clear verification criteria so the developer knows when it's complete
- Each phase's verification must include linting and formatting checks for code-quality assurance before proceeding
- **Test integrity is non-negotiable.** Generated plans are executed by a developer or agent who must never declare success on failing, skipped, worked-around, or unrun tests. Ensure the "Definition of Done — Test Integrity" section makes this explicit for both unit and integration tests — diagnose root causes, and treat "couldn't run / timed out" as a defect, not a pass.
