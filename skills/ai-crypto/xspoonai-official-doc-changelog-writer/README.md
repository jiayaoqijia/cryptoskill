# doc-changelog-writer (Track: enterprise-skills)

Automatic changelog generation from conventional commit messages

## Overview

This skill parses conventional commits and generates formatted changelog files. It automatically organizes commits by type (features, fixes, documentation) and creates release notes suitable for public distribution.

## Features

- **Conventional Commits Support**: Parse standard commit message format
- **Auto-Organization**: Group commits by type (feat, fix, docs, style, etc.)
- **Markdown Output**: Generate readable changelog in Markdown format
- **Version Tracking**: Associate changelogs with release versions
- **Template Customization**: Customize changelog format and sections

## Use Cases

- Generate changelogs automatically from git history
- Create release notes for public distribution
- Track breaking changes between versions
- Document feature additions and bug fixes
- Maintain project history for users

## Quickstart
```bash
python3 scripts/main.py --help
```

## Example
```bash
python3 scripts/main.py --demo
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| commits | array | Yes | Array of commit messages |
| version | string | No | Version number for release |
| date | string | No | Release date (ISO format) |

## Example Output

```json
{
  "ok": true,
  "data": {
    "changelog": "# Changelog\n\n## Features\n- Add user authentication\n- Implement password reset\n\n## Fixes\n- Resolve database connection issue\n\n## Documentation\n- Update API documentation\n",
    "commit_count": 4,
    "format": "markdown"
  }
}
```
