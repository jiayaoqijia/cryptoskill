---
name: gh-issue-bug
description: Generate a structured bug report for GitHub issues based on conversation context about bugs, errors, or broken functionality
disable-model-invocation: true
---

# GitHub Bug Report Generator Skill

This skill generates a well-structured bug report for GitHub issues based on the conversation context and saves it to `.ai/gh_issues/YYMMDD-<short-issue-name>.md`. This skill is specifically designed for **bug reports** - not for feature requests, enhancements, or improvements.

## Purpose

When invoked, this skill extracts bug information from the current conversation and creates a standardized GitHub bug report document.

**Use this skill for:**

- Bugs, errors, or broken functionality
- Incorrect behavior or unexpected results
- System failures or crashes

**Do NOT use this skill for:**

- Feature requests or enhancements
- Improvements to existing functionality
- Documentation updates
- Refactoring suggestions

## Workflow

### 1. Extract Issue Information

Review the conversation to identify:

- The bug or issue being discussed
- Steps that reproduce the problem
- Expected vs actual behavior
- Root cause analysis (if discussed)
- Potential fixes (if discussed)

### 2. Generate Filename

Create a filename using the pattern:

```text
.ai/gh_issues/YYMMDD-<short-issue-name-with-dashes>.md
```

Where:

- `YYMMDD`: Current date in 2-digit year, month, day format (e.g., `260127` for January 27, 2026)
- `<short-issue-name-with-dashes>`: A brief, descriptive name using lowercase letters and dashes (e.g., `nft-pagination-bug`, `timeout-error-in-ens-lookup`)

Example: `.ai/gh_issues/260127-nft-pagination-bug.md`

### 3. Create Issue Document

Write a Markdown document with the following sections:

```markdown
# [Brief Title of the Issue]

## Description

[Short description of the bug - 2-3 sentences summarizing the problem]

## Steps to Reproduce

1. [First step]
2. [Second step]
3. [Third step]
...

## Expected Behavior

[Clear description of what should happen]

## Actual Behavior

[Clear description of what actually happens, including any error messages]

## Root Cause

[Technical explanation of why the bug occurs - reference specific code, logic, or system behavior]

## Suggested Fix

[Concise description of the proposed solution without code snippets - describe the approach at a high level]
```

### 4. Content Guidelines

**MUST INCLUDE:**

- Short description (2-3 sentences)
- Steps to reproduce (numbered list)
- Expected behavior (clear statement)
- Actual behavior (including errors/symptoms)
- Root cause (technical explanation)
- Suggested fix (concise, high-level approach)

**MUST NOT INCLUDE:**

- Implementation plan or detailed code changes
- Acceptance criteria or testing checklists
- List of affected files
- Code snippets in the suggested fix section

### 5. Output Confirmation

After creating the file, confirm:

- The full path where the file was created
- A brief summary of the issue documented

## Example Usage

When the user says:

```bash
/gh-issue-bug
```

You should:

1. Review the conversation for bug details
2. Generate filename like `.ai/gh_issues/260127-transaction-logs-timeout.md`
3. Create the issue document with all required sections
4. Confirm creation with: "Created GitHub issue description at [.ai/gh_issues/260127-transaction-logs-timeout.md](.ai/gh_issues/260127-transaction-logs-timeout.md)"

## Notes

- The skill is designed for bugs discovered during development or testing
- If insufficient information exists in the conversation, ask the user for clarification before generating the document
- Keep the suggested fix section high-level and solution-oriented, not implementation-detailed
