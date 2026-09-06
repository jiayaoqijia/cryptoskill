# Pattern: Multi-Repo Workspace Initialization

## Purpose

Initialize a workspace that spans multiple GitHub repositories under a single organization or user account. Detects workspace context, discovers projects, and caches configuration for efficient multi-repo operations.

## When to Use

- First-time setup for multi-repo GitHub management
- Workspace config is missing or stale
- Switching to a different organization or user account

## Prerequisites

- `gh` CLI installed and authenticated
- `jq` installed for JSON processing
- `yq` installed for YAML processing (recommended) or Python with PyYAML

---

## Phase 1: Context Detection

### Detect Workspace Root

The workspace root is the parent directory containing multiple repositories. Config is stored here.

```bash
# Strategy: Walk up directory tree to find config or workspace root
find_workspace_root() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        # Check for existing config
        if [[ -f "$dir/.hiivmind/github/config.yaml" ]]; then
            echo "$dir"
            return 0
        fi
        # Check if this looks like a workspace (contains multiple git repos)
        local repo_count=$(find "$dir" -maxdepth 2 -name ".git" -type d 2>/dev/null | wc -l)
        if [[ "$repo_count" -gt 1 ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    # Default to current directory
    echo "$PWD"
    return 0
}

WORKSPACE_ROOT=$(find_workspace_root)
```

### Quick Check (2 levels)

```bash
CONFIG_PATH=""
if [[ -f ".hiivmind/github/config.yaml" ]]; then
    CONFIG_PATH=".hiivmind/github/config.yaml"
elif [[ -f "../.hiivmind/github/config.yaml" ]]; then
    CONFIG_PATH="../.hiivmind/github/config.yaml"
fi
```

---

## Phase 2: Owner Detection

### From Git Remote

If inside a git repository, extract the owner from the remote URL.

```bash
detect_owner_from_git() {
    if ! git rev-parse --is-inside-work-tree &>/dev/null; then
        return 1
    fi

    local url=$(git remote get-url origin 2>/dev/null)
    if [[ -z "$url" ]]; then
        return 1
    fi

    # Handle both SSH and HTTPS formats
    if [[ "$url" == git@* ]]; then
        echo "$url" | sed -E 's#git@github\.com:([^/]+)/.*#\1#'
    elif [[ "$url" == https://* ]]; then
        echo "$url" | sed -E 's#https://github\.com/([^/]+)/.*#\1#'
    fi
}

OWNER=$(detect_owner_from_git)
```

### From User Input

When detection fails or user is in a non-git directory:

```
You're in a directory without a git remote. This might be a multi-repo workspace.

Please specify the GitHub organization or username to initialize:

Examples:
- Organization: "my-org"
- Personal account: "my-username"
```

---

## Phase 3: Workspace Type Detection

Determine if the owner is an organization or user account. This affects which GraphQL query root to use.

```bash
detect_workspace_type() {
    local owner="$1"

    # Try organization first
    local type=$(gh api "orgs/$owner" --jq '.type' 2>/dev/null)
    if [[ "$type" == "Organization" ]]; then
        echo "organization"
        return 0
    fi

    # Fall back to user
    type=$(gh api "users/$owner" --jq '.type' 2>/dev/null)
    if [[ "$type" == "User" ]]; then
        echo "user"
        return 0
    fi

    echo "not_found"
    return 1
}

WORKSPACE_TYPE=$(detect_workspace_type "$OWNER")
```

### Impact on Queries

| Feature | Organization | User |
|---------|-------------|------|
| GraphQL root | `organization(login:)` | `user(login:)` |
| Repo listing | `/orgs/{owner}/repos` | `/users/{owner}/repos` |
| Teams | Available | Not available |
| Projects v2 | `organization.projectsV2` | `user.projectsV2` |
| Members | `/orgs/{owner}/members` | Not available |

---

## Phase 4: Repository Discovery

List all repositories in the workspace for multi-repo operations.

```bash
discover_repos() {
    local owner="$1"
    local type="$2"

    local endpoint
    if [[ "$type" == "organization" ]]; then
        endpoint="/orgs/$owner/repos"
    else
        endpoint="/users/$owner/repos"
    fi

    gh api "$endpoint" --paginate \
        -q '.[] | select(.archived == false) | {name: .name, full_name: .full_name, language: .language, open_issues: .open_issues_count, pushed_at: .pushed_at}' \
        | jq -s 'sort_by(.pushed_at) | reverse'
}

REPOS=$(discover_repos "$OWNER" "$WORKSPACE_TYPE")
```

---

## Phase 5: Project Discovery

Discover GitHub Projects v2 boards for cross-repo project management.

```bash
discover_projects() {
    local owner="$1"
    local type="$2"

    local query_root
    if [[ "$type" == "organization" ]]; then
        query_root="organization"
    else
        query_root="user"
    fi

    cat > /tmp/query.graphql << 'QUERY'
query($login: String!) {
  __TYPE_ROOT__(login: $login) {
    projectsV2(first: 20) {
      nodes {
        number
        title
        closed
        id
        url
        fields(first: 30) {
          nodes {
            ... on ProjectV2SingleSelectField {
              name
              id
              options {
                name
                id
              }
            }
            ... on ProjectV2Field {
              name
              id
            }
          }
        }
      }
    }
  }
}
QUERY

    # Replace type root placeholder
    sed -i "s/__TYPE_ROOT__/$query_root/" /tmp/query.graphql

    gh api graphql \
        -f query="$(cat /tmp/query.graphql)" \
        -f login="$owner" \
        | jq ".data.$query_root.projectsV2.nodes"

    rm -f /tmp/query.graphql
}

PROJECTS=$(discover_projects "$OWNER" "$WORKSPACE_TYPE")
```

---

## Phase 6: Write Config

Cache discovered data to `.hiivmind/github/config.yaml`.

```bash
write_config() {
    local workspace_root="$1"
    local owner="$2"
    local type="$3"
    local repos="$4"
    local projects="$5"

    local config_dir="$workspace_root/.hiivmind/github"
    mkdir -p "$config_dir"

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    cat > "$config_dir/config.yaml" << EOF
# GitHub Multi-Repo Workspace Configuration
# Generated: $timestamp

workspace:
  type: $type
  login: $owner

projects:
  default: null
  catalog: []

repositories: []

cache:
  initialized_at: "$timestamp"
  last_synced_at: null
EOF

    # Populate repositories from discovered data
    echo "$repos" | jq -r '.[] | "  - name: " + .name + "\n    full_name: " + .full_name' \
        >> "$config_dir/config.yaml"

    echo "Config written to $config_dir/config.yaml"
}
```

---

## Verification

After initialization, verify the workspace is functional:

```bash
verify_workspace() {
    local config="$1"

    echo "=== Workspace Verification ==="

    # Check workspace
    local login=$(yq '.workspace.login' "$config")
    local type=$(yq '.workspace.type' "$config")
    echo "Owner: $login ($type)"

    # Check repos
    local repo_count=$(yq '.repositories | length' "$config")
    echo "Repositories: $repo_count"

    # Check projects
    local project_count=$(yq '.projects.catalog | length' "$config")
    echo "Projects: $project_count"

    # Check auth scopes
    local scopes=$(gh auth status 2>&1 | grep "scopes" || echo "unknown")
    echo "Auth: $scopes"

    echo "=== Initialization Complete ==="
}
```

---

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `gh: command not found` | gh CLI not installed | Install: `brew install gh` or `apt install gh` |
| `Not logged into any GitHub hosts` | Not authenticated | Run: `gh auth login` |
| `Could not resolve to an Organization` | Wrong owner name | Verify spelling, check access |
| `Resource not accessible` | Missing scopes | Run: `gh auth refresh --scopes 'repo,read:org,project'` |
| Config already exists | Re-initialization | Prompt to overwrite or update |

---

## Related Patterns

- [graphql-execution.md](graphql-execution.md) - Safe GraphQL query execution via temp file
- [config-caching.md](config-caching.md) - Reading and updating cached configuration
