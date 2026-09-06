---
name: gh-issue-improvement
description: Generate a structured improvement/enhancement proposal for GitHub issues based on conversation context
disable-model-invocation: true
---

# GitHub Improvement Proposal Generator Skill

This skill generates a well-structured improvement/enhancement proposal for GitHub issues based on the conversation context and saves it to `.ai/gh_issues/YYMMDD-<short-issue-name>.md`. This skill is specifically designed for **improvements and enhancements** - not for bug reports or error fixes.

## Purpose

When invoked, this skill extracts improvement information from the current conversation and creates a standardized GitHub enhancement proposal document.

**Use this skill for:**

- Feature enhancements or improvements
- Code refactoring or restructuring
- Performance optimizations
- Architecture improvements
- Tool migrations (e.g., migrating MCP tools to `direct_api_call`)
- API consolidation or simplification
- Documentation improvements
- Testing improvements

**Do NOT use this skill for:**

- Bugs, errors, or broken functionality
- Incorrect behavior or unexpected results
- System failures or crashes

## Workflow

### 1. Extract Issue Information

Review the conversation to identify:

- The improvement or enhancement being proposed
- Current state and its limitations
- Motivation and benefits of the improvement
- Proposed changes at a conceptual level
- Expected outcomes or impact

### 2. Generate Filename

Create a filename using the pattern:

```text
.ai/gh_issues/YYMMDD-<short-issue-name-with-dashes>.md
```

Where:

- `YYMMDD`: Current date in 2-digit year, month, day format (e.g., `260128` for January 28, 2026)
- `<short-issue-name-with-dashes>`: A brief, descriptive name using lowercase letters and dashes (e.g., `migrate-logs-to-direct-api`, `optimize-pagination-logic`, `consolidate-nft-tools`)

Example: `.ai/gh_issues/260128-migrate-logs-to-direct-api.md`

### 3. Create Issue Document

Write a Markdown document with the following sections:

```markdown
# [Brief Title of the Improvement]

## Description

[Short description of the improvement - 2-3 sentences summarizing what is being proposed]

## Motivation

[Clear explanation of why this improvement is needed - what problems does it solve, what benefits does it provide]

## Current State

[Description of how things work currently, including any limitations or pain points]

## Proposed Changes

[High-level description of what should change conceptually. Focus on WHAT changes, not HOW to implement them. Avoid step-by-step implementation details, specific file paths, or granular action items. Keep it strategic and outcome-focused.]

## Expected Benefits

[List of concrete benefits that will result from this improvement - can include improved performance, better maintainability, reduced complexity, etc.]
```

**Example of well-formed "Proposed Changes" section:**

```markdown
## Proposed Changes

- Transition the standalone tool to a handler-based architecture consistent with similar tools
- Maintain backward compatibility by preserving the REST API endpoint with deprecation notices
- Consolidate response processing logic within the dispatcher pattern
- Update all references in documentation and integration examples to reflect the new approach
```

### 4. Content Guidelines

**MUST INCLUDE:**

- Short description (2-3 sentences)
- Motivation explaining why the improvement is needed
- Current state description showing what exists today
- Proposed changes (clear, organized list describing what should change)
- Expected benefits (concrete outcomes)

**MUST NOT INCLUDE:**

- Detailed code implementation or snippets
- Specific file paths or module names (e.g., `blockscout_mcp_server/tools/direct_api/handlers/x_handler.py`)
- Step-by-step implementation checklists (e.g., "1. Create X, 2. Update Y, 3. Delete Z")
- Granular action items for each file or component
- Function names, decorator names, or code structure details
- Line-by-line diffs or patches
- Test case implementations or test file locations
- Documentation file names or specific sections to update

**STYLE GUIDELINES:**

- Focus on "what" should change and "why" it matters, not "how" to implement it in detail
- Use lists and structured formatting for clarity
- Be specific enough to be actionable but general enough to allow implementation flexibility
- Avoid prescriptive implementation details - leave room for refinement during development
- Keep "Proposed Changes" to 3-6 high-level points maximum
- Each point should describe an outcome or conceptual change, not an implementation task

**PROPOSED CHANGES - GOOD EXAMPLES:**

✓ "Consolidate transaction-related tools under a unified dispatcher pattern"
✓ "Deprecate the dedicated tool in favor of the generic `direct_api_call` interface"
✓ "Preserve existing response processing logic while relocating it to a handler"
✓ "Update documentation to reflect the new tool architecture"

**PROPOSED CHANGES - BAD EXAMPLES:**

✗ "Create handler module at `blockscout_mcp_server/tools/direct_api/handlers/x_handler.py` with `@register_handler` decorator"
✗ "Update REST API in `api/routes.py` to return deprecation response with 410 status code"
✗ "Remove import of `transaction_summary` function from `server.py`"
✗ "Migrate tests: Delete `test_transaction_summary.py` and create new handler tests"

### 5. Output Confirmation

After creating the file, confirm:

- The full path where the file was created
- A brief summary of the improvement documented

## Example Usage

When the user says:

```bash
/gh-issue-improvement
```

You should:

1. Review the conversation for improvement details
2. Generate filename like `.ai/gh_issues/260128-consolidate-transaction-tools.md`
3. Create the issue document with all required sections
4. Confirm creation with: "Created GitHub improvement proposal at [.ai/gh_issues/260128-consolidate-transaction-tools.md](.ai/gh_issues/260128-consolidate-transaction-tools.md)"

## Example Improvements

This skill can document various types of improvements:

- **Tool Migration**: Migrating an MCP tool to use `direct_api_call` handler pattern
- **Refactoring**: Consolidating duplicate code into shared utilities
- **Performance**: Optimizing caching strategies or reducing API calls
- **Architecture**: Restructuring modules for better separation of concerns
- **API Changes**: Simplifying or consolidating API endpoints
- **Testing**: Adding comprehensive test coverage for a module
- **Documentation**: Improving inline documentation or user guides

## Notes

- The skill is designed for improvements discussed during development planning or code reviews
- If insufficient information exists in the conversation, ask the user for clarification before generating the document
- **CRITICAL**: Keep proposed changes conceptual and strategic - avoid prescriptive implementation details
- Before writing "Proposed Changes", review the GOOD vs BAD examples above to ensure appropriate level of abstraction
- Think: "What outcomes do we want?" not "What steps should we take?"
- If you find yourself writing file paths, function names, or numbered checklists, you're being too prescriptive
- Focus on the value proposition - make it clear why this improvement matters
