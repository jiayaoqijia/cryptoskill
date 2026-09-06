---
name: github-multi-repo-manager
description: Multi-repo GitHub management. Cross-repo issues, Projects v2 boards, team workload analytics, milestone tracking, PR pipelines, and release coordination.
version: 1.0.0
author: hiivmind
tags: [github, multi-repo, enterprise, project-management, team-analytics, projects-v2, graphql, devops]
---

# GitHub Multi-Repo Manager

Manage GitHub operations across multiple repositories from a single workspace. While every other GitHub skill focuses on single-repo operations, this skill orchestrates work across an entire organization or user account -- project boards spanning repos, team workload analysis, milestone tracking, PR review pipelines, and release coordination.

## Quick Start

**Initialize a workspace:**
```
Set up multi-repo management for the "my-org" GitHub organization
```

**Cross-repo search:**
```
Find all open bugs across every repo in my-org
```

**Team workload:**
```
Who on the team is overloaded with issues and pending reviews?
```

**Project board management:**
```
Show the status of all items on project board #2, grouped by repo
```

## Capabilities

| Capability | What It Does | API Used | Reference |
|-----------|-------------|----------|-----------|
| **Workspace Init** | Detect org/user, discover projects, cache config | GraphQL + REST | [patterns/workspace-init.md](patterns/workspace-init.md) |
| **Repo Discovery** | Catalog repos by language, activity, staleness | REST | [references/repo-discovery.md](references/repo-discovery.md) |
| **Cross-Repo Search** | Unified issue/PR search with rich filters | Search API | [references/cross-repo-search.md](references/cross-repo-search.md) |
| **Project Boards** | Projects v2 items, fields, status across repos | GraphQL | [references/project-boards.md](references/project-boards.md) |
| **Team Analytics** | Per-member workload, bottleneck detection | Search + REST | [references/team-analytics.md](references/team-analytics.md) |
| **Milestone Tracking** | Cross-repo milestone progress, overdue detection | REST | [references/milestone-tracking.md](references/milestone-tracking.md) |
| **PR Pipeline** | Review status, stale PRs, merge readiness | REST + CLI | [references/pr-pipeline.md](references/pr-pipeline.md) |
| **Release Coordination** | Unreleased commits, draft releases, cadence | REST | [references/release-coordination.md](references/release-coordination.md) |

## Prerequisites

| Tool | Required | Purpose |
|------|----------|---------|
| `gh` | Yes | GitHub CLI - all API access |
| `jq` | Yes | JSON processing and filtering |
| `yq` | Recommended | YAML config parsing (Python fallback available) |

**Required `gh` auth scopes:** `repo`, `read:org`, `project`, `read:project`

```bash
# Verify tools
gh --version && jq --version && yq --version

# Check auth scopes
gh auth status

# Add missing scopes if needed
gh auth refresh --scopes 'repo,read:org,project,read:project'
```

## Execution Patterns

This skill uses three foundational patterns that all capabilities build on:

| Pattern | Purpose | Key Technique |
|---------|---------|--------------|
| [Workspace Init](patterns/workspace-init.md) | Multi-repo workspace setup | Walk-up config detection, org/user type detection |
| [GraphQL Execution](patterns/graphql-execution.md) | Safe GraphQL queries | Temp file HEREDOC to avoid `$variable` expansion |
| [Config Caching](patterns/config-caching.md) | Cache-first ID resolution | Local YAML cache with staleness tracking |

## Security Model

- **No credentials stored** - all auth via `gh` CLI token
- **Read-only by default** - write operations (project updates) are explicitly marked
- **Rate limit aware** - Search API: 30 req/min, REST: 5,000 req/hr
- **Config is not sensitive** - contains only entity IDs, not tokens
- **Scope verification** - checks required scopes before operations

## Composability

This skill composes well with other skills:
- **Code review skills** can use PR pipeline data to prioritize reviews
- **CI/CD skills** can use release coordination to trigger deployments
- **Documentation skills** can use milestone data for changelog generation
- **Security audit skills** can use repo discovery for org-wide scanning

## Example Prompts

- "Initialize workspace for the my-org organization"
- "List all repos in my-org grouped by language"
- "Find all open issues labeled 'critical' across all repos"
- "Show project board #2 items grouped by status and repo"
- "Add issue #15 from api-server to project board #2"
- "Who has the most pending reviews right now?"
- "Show milestone 'v2.0' progress across all repos"
- "Which PRs have been open for more than 2 weeks without review?"
- "Which repos have unreleased commits since their last release?"
- "Show the release cadence for each repo over the last 6 months"
