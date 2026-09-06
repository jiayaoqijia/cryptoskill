# GitHub Multi-Repo Manager

Enterprise multi-repository GitHub management for AI agents. The only skill in the SpoonOS ecosystem that manages GitHub across multiple repositories -- project boards spanning repos, team workload analysis, cross-repo milestone tracking, PR review pipelines, and coordinated releases.

## Why This Skill?

Every existing GitHub skill operates on a single repository. Real engineering teams manage **dozens of repos** under an organization, with:
- Issues scattered across repos that need unified tracking
- Project boards aggregating work from multiple repos
- Milestones with the same name in different repos
- Pull requests that need cross-repo review coordination
- Releases that should be coordinated across services

This skill fills that gap with production-grade patterns adapted from [hiivmind-pulse-gh](https://github.com/hiivmind/hiivmind-pulse-gh), a battle-tested GitHub automation plugin.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      SKILL.md                           │
│              (Gateway + Capability Matrix)               │
└──────────────────────┬──────────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐
   │ Patterns │ │ Patterns │ │ Patterns │     Foundation Layer
   │workspace │ │ graphql  │ │  config  │     (HOW to execute)
   │  init    │ │execution │ │ caching  │
   └──────────┘ └──────────┘ └──────────┘
          │            │            │
          └────────────┼────────────┘
                       │
    ┌──────┬───────┬───┴───┬───────┬──────┬───────┐
    ▼      ▼       ▼       ▼       ▼      ▼       ▼
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│ repo ││cross-││proj- ││ team ││mile- ││  PR  ││rel-  │  Operation
│disco-││ repo ││ect  ││analy-││stone ││pipe- ││ease  │  Layer
│ very ││search││boards││tics ││track ││ line ││coord │  (WHAT to do)
└──────┘└──────┘└──────┘└──────┘└──────┘└──────┘└──────┘
```

**Pattern documents** teach the agent *how* to execute safely (temp file GraphQL, config caching, workspace detection).

**Reference documents** teach the agent *what* to do for each domain (exact commands, jq patterns, decision tables).

## Capabilities

### 1. Workspace Initialization
Set up a multi-repo workspace with automatic org/user detection, project discovery, and config caching.

### 2. Repository Discovery
Catalog all repos by language, activity, staleness. Filter by topic, visibility, or date range.

### 3. Cross-Repo Search
Unified search for issues and PRs across all repos using GitHub Search API. Rich filtering by label, assignee, milestone, date range. Group results by repo, label, or assignee.

### 4. Projects v2 Board Management
Full GraphQL-based Projects v2 support: list projects, query items with status, add items from any repo, update field values (status, priority, dates), build cross-repo board dashboards.

### 5. Team Workload Analytics
Per-member workload analysis: assigned issues, authored PRs, pending reviews. Bottleneck detection, workload scoring, and threshold-based alerts.

### 6. Cross-Repo Milestone Tracking
Track identically-named milestones across repos. Progress calculation, due date monitoring, overdue detection, and blocker identification.

### 7. PR Review Pipeline
Cross-repo PR dashboard: review status, stale PR detection, merge readiness checks, reviewer bottleneck analysis, and PR size categorization.

### 8. Release Coordination
Track releases across repos: latest release per repo, unreleased commits detection, draft releases, release cadence analysis, and coordination dashboards.

## Prerequisites

| Tool | Required | Installation |
|------|----------|-------------|
| `gh` (GitHub CLI) | Yes | `brew install gh` / `apt install gh` |
| `jq` (JSON processor) | Yes | `brew install jq` / `apt install jq` |
| `yq` (YAML processor) | Recommended | `brew install yq` / `pip install yq` |

### Authentication

```bash
# Login to GitHub CLI
gh auth login

# Required scopes
gh auth refresh --scopes 'repo,read:org,project,read:project'

# Verify
gh auth status
```

| Scope | Purpose |
|-------|---------|
| `repo` | Access issues, PRs, commits across repos |
| `read:org` | List org members, teams, repos |
| `project` | Read/write Projects v2 boards |
| `read:project` | Read-only project access |

## Quick Start

### 1. Initialize Workspace

```
Set up GitHub multi-repo management for the "my-org" organization
```

The agent will:
- Detect workspace type (org vs user)
- Discover all repositories
- Discover Projects v2 boards and fields
- Cache configuration to `.hiivmind/github/config.yaml`

### 2. Explore Your Org

```
List all active repos in my-org, grouped by language
```

### 3. Find Cross-Repo Issues

```
Find all open issues labeled "bug" across all repos in my-org
```

### 4. Check Team Workload

```
Show me the workload for each team member - issues, PRs, and pending reviews
```

### 5. Track Milestones

```
Show progress for the "v2.0" milestone across all repos
```

## File Structure

```
github-multi-repo-manager/
├── SKILL.md                          # Skill definition + capability matrix
├── README.md                         # This documentation
├── patterns/                         # Execution patterns (HOW)
│   ├── workspace-init.md             # Multi-repo workspace setup
│   ├── graphql-execution.md          # Safe GraphQL via temp file
│   └── config-caching.md             # Cache-first ID resolution
└── references/                       # Domain operations (WHAT)
    ├── repo-discovery.md             # Org repo cataloging
    ├── cross-repo-search.md          # Unified issue/PR search
    ├── project-boards.md             # Projects v2 GraphQL operations
    ├── team-analytics.md             # Team workload analysis
    ├── milestone-tracking.md         # Cross-repo milestone tracking
    ├── pr-pipeline.md                # PR review pipeline
    └── release-coordination.md       # Release tracking & coordination
```

## Security

- **No credentials stored** - all authentication via `gh` CLI
- **No API keys required** - uses GitHub CLI's OAuth token
- **Config contains only IDs** - project IDs, field IDs, repo names (not sensitive)
- **Rate limit aware** - documents limits per API type
- **Read-only by default** - write operations clearly marked in references
- **Scope verification** - checks auth scopes before operations

## Design Decisions

### Why Not Python Scripts?

This skill uses **pure documentation patterns** instead of Python scripts because:

1. **No dependencies** - works with `gh` + `jq` already installed on most dev machines
2. **Transparent** - every command is visible, auditable, and modifiable
3. **Composable** - patterns combine freely; scripts impose rigid interfaces
4. **Agent-native** - AI agents excel at following documented patterns and adapting them to context
5. **Production-proven** - these patterns come from hiivmind-pulse-gh, used daily across multiple orgs

### Why Patterns + References?

The two-layer architecture separates concerns:

- **Patterns** (3 files) teach *mechanics* - how to execute GraphQL safely, how to find config, how to resolve IDs
- **References** (7 files) teach *operations* - what to query for each domain, what jq filters to apply, what the results mean

This means the agent can combine any reference with any pattern. Adding a new domain (e.g., Actions workflow management) only requires a new reference file -- the execution patterns are already in place.

## Provenance

Core patterns adapted from [hiivmind-pulse-gh](https://github.com/hiivmind/hiivmind-pulse-gh), a production GitHub automation plugin used to manage the hiivmind organization (7+ repositories, multiple projects, team coordination). The workspace initialization, GraphQL temp file execution, and config caching patterns have been refined through months of daily use.

## License

MIT
