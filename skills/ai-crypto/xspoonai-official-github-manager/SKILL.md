---
name: github-manager
description: Manage GitHub issues and PRs (list, create, comment).
version: 1.0.0
author: SpoonOS Contributor
tags: [github, productivity, collaboration, issues]
---

# GitHub Manager

A skill to help AI agents manage GitHub repositories by interacting with issues and pull requests.

## Quick Start

```python
# List open issues in a repo
issues = await agent.run_tool("github_tool", action="list_issues", repo="owner/repo")
print(issues)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [github_tool.py](scripts/github_tool.py) | Main tool for GitHub interactions |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | Personal Access Token with repo scope |

## Best Practices

1. Use a granular Personal Access Token (PAT).
2. Always specify the full `owner/repo` name.
