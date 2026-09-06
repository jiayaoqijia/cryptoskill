---
name: gh-issue-publish
description: Publish a GitHub issue from a markdown file in .ai/gh_issues/ created by gh-issue-bug or gh-issue-improvement skills
argument-hint: [path-to-issue-file]
disable-model-invocation: true
---

# GitHub Issue Publisher Skill

This skill publishes a GitHub issue from a markdown file in `.ai/gh_issues/` created by the `gh-issue-bug` or `gh-issue-improvement` skills.

## Workflow

### 1. Determine File Path

- If `$1` is provided and non-empty, use it as the file path.
- Otherwise, extract the file path from the current conversation. Look for the most recent `.ai/gh_issues/*.md` path mentioned — this is typically the output of a preceding `/gh-issue-bug` or `/gh-issue-improvement` invocation.
- If no file path can be determined, ask the user to provide one.

### 2. Run the Publisher Script

Execute:

```bash
.claude/skills/gh-issue-publish/script/gh-issue-publish.sh <file-path>
```

The script handles everything deterministically:

- Validates the file exists
- Checks `gh auth status`
- Parses title from line 1 (strips `#` prefix)
- Detects issue type by section headers (`bug` or `enhancement` label)
- Creates the issue via `gh issue create`

### 3. Relay the Result

**On success** (output starts with `OK`):

Report to the user:

- The issue URL (from the `OK` line)
- The label applied (from the `LABEL` line)

**On failure** (output starts with `ERROR`):

Report the error and suggest remediation:

- **"GitHub CLI not authenticated"**: tell the user to run `gh auth login`
- **"File not found"**: ask the user to verify the path
- **"Cannot detect issue type"**: inform the user the file doesn't match expected bug or improvement templates
- **"Could not extract title"**: the first line of the file is empty or malformed
- **"Failed to create GitHub issue"**: suggest checking network connectivity and repo permissions

## Notes

- The skill relies on section headers defined by `gh-issue-bug` (`## Steps to Reproduce`, `## Root Cause`, etc.) and `gh-issue-improvement` (`## Motivation`, `## Proposed Changes`, etc.) to detect the issue type. If those skills change their templates, the detection patterns in the script must be updated accordingly.
- The `gh` CLI infers the target repository from the current git remote. No `--repo` flag is needed when running from within the repo clone.
- Creating a GitHub issue is an external action — the Bash command will go through normal permission approval.
