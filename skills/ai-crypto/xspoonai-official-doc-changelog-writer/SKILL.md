---
name: doc-changelog-writer
track: enterprise-skills
version: 0.1.0
summary: Generate CHANGELOG.md entries from git commits
---

## Description

Generate CHANGELOG.md entries from git commits. Automatically categorizes commits into features, fixes, and breaking changes for release documentation.

## Inputs

```json
{
  "commits": ["list of commit messages"],
  "version": "1.0.0",
  "date": "2026-02-06"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "changelog": "Changelog markdown content"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Generate Changelog
```bash
echo '{"commits": ["feat: add new endpoint", "fix: memory leak"], "version": "1.0.0"}' | python3 scripts/main.py
```

## Examples

### Example 1: Create Release Notes
```bash
$ echo '{"commits": ["feat: add new feature", "fix: bug fix"], "version": "1.0.0", "date": "2026-02-06"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "changelog": "## [1.0.0] - 2026-02-06\n\n### Features\n- add new feature\n\n### Fixes\n- bug fix"
  }
}
```

## Error Handling

When an error occurs, the skill returns:

```json
{
  "ok": false,
  "error": "Error description",
  "details": {
    "commits": "Invalid commit list"
  }
}
```
