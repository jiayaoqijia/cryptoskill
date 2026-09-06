---
name: describe-changes
description: Describe very high level changes required to implement discussed functionality (functionality, test, docs)
disable-model-invocation: true
---

# Describe Changes Skill

This skill composes a concise description of changes required to implement the feature or fix the issue discussed in the conversation. The purpose is to confirm the agent's understanding of the scope and what files will be modified.

## Purpose

When invoked, this skill generates a structured description of all changes needed to address the discussed issue/feature. This description serves as a confirmation that the agent:

1. **Understands the scope** of the changes
2. **Has actually read** all files that will be modified (not just guessed based on names)
3. **Can articulate** specific modifications at a high level

## CRITICAL REQUIREMENT: File Reading Before Inclusion

**MANDATORY:** Before listing ANY file in the changes description, you MUST read that file first using the Read tool.

**Why this matters:**

- File names and project structure descriptions can be misleading
- Actual file contents reveal the true implementation details
- Reading ensures accurate understanding of what needs to change
- Guessing based on file names leads to incorrect or incomplete descriptions

**Verification checklist before including a file:**

- [ ] Did I read this file in the current conversation?
- [ ] Do I understand its current implementation?
- [ ] Can I describe the specific change needed?

**If you have NOT read a file, you MUST read it before including it in the description.**

## Workflow

### 1. Review Conversation Context

Identify from the conversation:

- The feature or issue being discussed
- Technical requirements and constraints
- Any implementation decisions already made

### 2. Read All Relevant Files

Before proceeding, use the Read tool to examine:

- All source files that will need modification
- Related test files
- Documentation files that may need updates
- Configuration files if applicable

**DO NOT SKIP THIS STEP.** Reading files is not optional - it's the core purpose of this skill to ensure accurate understanding.

### 3. Generate Changes Description

Create a Markdown document with the following sections:

```markdown
## Changes Description

### Functional Changes

[List each file with a brief description of what will change]

- `path/to/file.py`: [What will be modified and why]
- `path/to/another_file.py`: [What will be modified and why]

### Test Changes

[List unit test files that need to be created or modified]

- `tests/tools/category/test_feature.py`: [New tests or modifications needed]

### Integration Test Changes

[List integration test files if applicable, or state "No integration test changes required"]

- `tests/integration/category/test_feature_real.py`: [New tests or modifications needed]

### Documentation Changes

[List documentation files including AI-coding agent artifacts]

- `SPEC.md`: [What sections need updating]
- `AGENTS.md`: [Project structure updates if applicable]
- `.cursor/rules/xxx.mdc`: [Rule file changes if applicable]
- `API.md`: [API documentation updates if applicable]

### Project Artifacts

[List non-functional project files like configuration]

- `pyproject.toml`: [Dependency or metadata changes if needed]
- Other configuration files as applicable
```

## Content Guidelines

### MUST INCLUDE

- **Functional Changes**: All source code files with specific modification descriptions
- **Test Changes**: Unit test files that need creation or modification
- **Integration Test Changes**: Integration test files if the feature requires real network testing (or explicit statement that none are needed)
- **Documentation Changes**: Including AI-coding agent artifacts (AGENTS.md, .cursor/rules/, etc.)
- **Project Artifacts**: Configuration files, pyproject.toml, etc.

### MUST NOT INCLUDE

- **Problem Summary**: The conversation already contains this context
- **Verification Steps**: This is a pre-implementation description, not a test plan
- **Risk Assessment**: Not part of the scope confirmation

### Format Guidelines

- Use relative paths from project root
- Keep descriptions concise (1 sentence per file)
- Group related files logically within each section
- If a section has no changes, explicitly state "No changes required" rather than omitting

## Example Output

```markdown
## Changes Description

### Functional Changes

- `blockscout_mcp_server/tools/transaction/get_pending_txs.py`: New tool implementation for fetching pending transactions with pagination support
- `blockscout_mcp_server/tools/common.py`: Add helper function for pending transaction status normalization
- `blockscout_mcp_server/server.py`: Register the new `get_pending_txs` tool

### Test Changes

- `tests/tools/transaction/test_get_pending_txs.py`: Unit tests covering success scenarios, error handling, pagination, and edge cases

### Integration Test Changes

- `tests/integration/transaction/test_get_pending_txs_real.py`: Integration tests with real network calls to verify pending transaction retrieval

### Documentation Changes

- `AGENTS.md`: Add new tool module to project structure
- `SPEC.md`: Document the new tool's behavior and API contract
- `.cursor/rules/110-new-mcp-tool.mdc`: No changes needed (existing rule covers new tools)

### Project Artifacts

- No changes required
```

## Example Usage

When the user says:

```bash
/describe-changes
```

You should:

1. Review the conversation for the discussed feature/issue
2. **Read all files** that will be mentioned in the description
3. Generate the structured changes description
4. Output it directly in the conversation (no file creation needed)

## Notes

- This skill is for **pre-implementation confirmation**, not post-implementation documentation
- If you haven't read a file, read it before including it - do not guess
- If the conversation lacks sufficient context about what needs to change, ask clarifying questions first
- Focus on accuracy over completeness - it's better to read fewer files thoroughly than to guess about many
