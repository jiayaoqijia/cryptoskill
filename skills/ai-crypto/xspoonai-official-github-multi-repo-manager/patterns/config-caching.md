# Pattern: Config Caching & ID Resolution

## Purpose

Cache GitHub entity IDs (projects, fields, options, repositories, milestones) locally for fast resolution without repeated API calls. Implements a cache-first strategy with API fallback and staleness tracking.

## When to Use

- Before any operation requiring GitHub entity IDs
- When resolving user-friendly names/numbers to GraphQL IDs
- After workspace initialization to store discovered data
- When checking if cached data needs refreshing

---

## Config Location

Config is stored at `.hiivmind/github/config.yaml` relative to the workspace root.

### Find Config Path

```bash
find_config() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/.hiivmind/github/config.yaml" ]]; then
            echo "$dir/.hiivmind/github/config.yaml"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

CONFIG_PATH=$(find_config) || echo "Config not found - run workspace init"
```

---

## Config Schema

```yaml
workspace:
  type: organization|user
  login: string
  id: string|null

projects:
  default: number|null
  catalog:
    - number: 1
      title: "Project Name"
      id: "PVT_xxx"
      fields:
        Status:
          id: "PVTSSF_xxx"
          type: single_select
          options:
            Todo: "option_id_1"
            "In Progress": "option_id_2"
            Done: "option_id_3"
        Priority:
          id: "PVTF_xxx"
          type: single_select
          options:
            High: "option_id_4"
            Medium: "option_id_5"
            Low: "option_id_6"

repositories:
  - name: "repo-name"
    full_name: "owner/repo-name"

milestones:
  repo-name:
    - number: 1
      title: "v1.0"
      id: "MI_xxx"

cache:
  initialized_at: "2025-01-15T10:00:00Z"
  last_synced_at: "2025-01-15T10:00:00Z"
  staleness_threshold_hours: 24
```

---

## Cache-First Resolution Strategy

```
User Input (name/number)
        |
   [Check Cache]  <-- yq/Python extraction
        |
   +----+----+
   |         |
  Found    Miss
   |         |
  Return   [Query GitHub API]
  ID         |
         [Optionally cache result]
             |
         Return ID
```

---

## Resolution Patterns

### Project ID by Number

```bash
PROJECT_NUM=2
PROJECT_ID=$(yq ".projects.catalog[] | select(.number == $PROJECT_NUM) | .id" "$CONFIG_PATH")

if [[ -n "$PROJECT_ID" && "$PROJECT_ID" != "null" ]]; then
    echo "Resolved from cache: $PROJECT_ID"
else
    echo "Cache miss - querying GitHub..."
    # Fallback: query projects via GraphQL (see references/project-boards.md)
fi
```

### Field ID by Name

```bash
PROJECT_NUM=2
FIELD_NAME="Status"

FIELD_ID=$(yq ".projects.catalog[] | select(.number == $PROJECT_NUM) | .fields[\"$FIELD_NAME\"].id" "$CONFIG_PATH")

if [[ -n "$FIELD_ID" && "$FIELD_ID" != "null" ]]; then
    echo "Resolved: $FIELD_ID"
fi
```

### Option ID by Name

```bash
PROJECT_NUM=2
FIELD_NAME="Status"
OPTION_NAME="In Progress"

OPTION_ID=$(yq ".projects.catalog[] | select(.number == $PROJECT_NUM) | .fields[\"$FIELD_NAME\"].options[\"$OPTION_NAME\"]" "$CONFIG_PATH")
```

### Milestone ID by Title

```bash
REPO="my-repo"
MILESTONE_TITLE="v1.0"

# Try cache first
MILESTONE_ID=$(yq ".milestones[\"$REPO\"][] | select(.title == \"$MILESTONE_TITLE\") | .id" "$CONFIG_PATH" 2>/dev/null)

if [[ -z "$MILESTONE_ID" || "$MILESTONE_ID" == "null" ]]; then
    # REST fallback (milestones have no gh CLI command)
    OWNER=$(yq '.workspace.login' "$CONFIG_PATH")
    MILESTONE_ID=$(gh api "/repos/$OWNER/$REPO/milestones" \
        --jq ".[] | select(.title == \"$MILESTONE_TITLE\") | .node_id")
fi
```

---

## Entity Resolution Matrix

| Entity | Lookup Key | Cached? | Cache Path | Fallback API |
|--------|-----------|---------|------------|-------------|
| Project | Number | Yes | `.projects.catalog[].number` -> `.id` | GraphQL: `projectsV2` |
| Field | Name + Project | Yes | `.fields[name].id` | GraphQL: `projectV2.fields` |
| Option | Name + Field | Yes | `.fields[name].options[name]` | GraphQL: field options |
| Repository | Name | Yes | `.repositories[].name` | REST: `/repos` |
| Milestone | Title + Repo | Partial | `.milestones[repo][]` | REST: `/milestones` |
| Issue | Number | No | -- | GraphQL: `repository.issue` |
| Pull Request | Number | No | -- | GraphQL: `repository.pullRequest` |

---

## Staleness Detection

Track when cached data was last refreshed to know when re-querying is needed.

```bash
check_staleness() {
    local config="$1"
    local threshold_hours=${2:-24}

    local last_sync=$(yq '.cache.last_synced_at // .cache.initialized_at' "$config")
    if [[ -z "$last_sync" || "$last_sync" == "null" ]]; then
        echo "stale"
        return 1
    fi

    local last_epoch=$(date -d "$last_sync" +%s 2>/dev/null)
    local now_epoch=$(date +%s)
    local diff_hours=$(( (now_epoch - last_epoch) / 3600 ))

    if [[ "$diff_hours" -gt "$threshold_hours" ]]; then
        echo "stale ($diff_hours hours old, threshold: ${threshold_hours}h)"
        return 1
    else
        echo "fresh ($diff_hours hours old)"
        return 0
    fi
}
```

---

## Config Update Patterns

### Update Sync Timestamp

```bash
yq -i ".cache.last_synced_at = \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"" "$CONFIG_PATH"
```

### Add Repository to Cache

```bash
yq -i '.repositories += [{"name": "new-repo", "full_name": "owner/new-repo"}]' "$CONFIG_PATH"
```

### Update Milestone Cache for a Repo

```bash
OWNER=$(yq '.workspace.login' "$CONFIG_PATH")
REPO="my-repo"

# Fetch current milestones
MILESTONES=$(gh api "/repos/$OWNER/$REPO/milestones" \
    --jq '[.[] | {number: .number, title: .title, id: .node_id, state: .state, open_issues: .open_issues, closed_issues: .closed_issues}]')

# Update config (requires yq 4.x)
yq -i ".milestones[\"$REPO\"] = $MILESTONES" "$CONFIG_PATH"
```

---

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| Config not found | Not initialized | Run workspace init |
| `null` from yq | Key exists but empty | Use API fallback |
| Parse error | Malformed YAML | Validate: `yq '.' "$CONFIG_PATH"` |
| `yq: command not found` | yq not installed | Fall back to Python PyYAML |
| Stale cache | Data changed on GitHub | Run refresh |

### Python Fallback

When yq is not available:

```bash
python3 -c "
import yaml
config = yaml.safe_load(open('$CONFIG_PATH'))
projects = config.get('projects', {}).get('catalog', [])
project = next((p for p in projects if p.get('number') == 2), None)
print(project.get('id', '') if project else '')
"
```

---

## Security Notes

- **No credentials in config** - uses `gh` CLI auth exclusively
- **Config may contain project/field IDs** - not sensitive, but gitignore `.hiivmind/` to avoid noise
- **Rate limit awareness** - cache-first strategy reduces API calls significantly
- **Read-only by default** - only init/refresh write to config

---

## Related Patterns

- [workspace-init.md](workspace-init.md) - Creates initial config during setup
- [graphql-execution.md](graphql-execution.md) - Executes API fallback queries
