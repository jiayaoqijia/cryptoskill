# Reference: Cross-Repo Search

## Purpose

Search for issues, pull requests, and code across multiple repositories in a single query. Enables unified views of work across an entire organization or set of repos.

## API Methods

| Operation | Method | Rate Limit | Notes |
|-----------|--------|-----------|-------|
| Search issues/PRs | REST: `GET /search/issues` | 30 req/min | Includes both issues and PRs |
| Search issues/PRs | CLI: `gh search issues` | 30 req/min | Same API underneath |
| Search code | REST: `GET /search/code` | 10 req/min | More restrictive |
| Search commits | REST: `GET /search/commits` | 30 req/min | |

---

## Cross-Repo Issue Search

### All Open Issues in an Organization

```bash
OWNER="my-org"

gh api "/search/issues" \
    -f q="org:$OWNER state:open type:issue" \
    -f per_page=100 \
    --jq '.items[] | {
        repo: .repository_url | split("/") | .[-1],
        number: .number,
        title: .title,
        author: .user.login,
        labels: [.labels[].name],
        created_at: .created_at,
        assignees: [.assignees[].login]
    }' | jq -s '.'
```

### Using gh search CLI

```bash
OWNER="my-org"

# Search all open issues
gh search issues --owner "$OWNER" --state open --json repository,number,title,author,labels,createdAt

# With label filter
gh search issues --owner "$OWNER" --state open --label bug --json repository,number,title,author

# With assignee filter
gh search issues --owner "$OWNER" --state open --assignee username --json repository,number,title
```

---

## Targeted Multi-Repo Search

### Search Specific Repos (up to 10 per query)

```bash
OWNER="my-org"

gh api "/search/issues" \
    -f q="repo:$OWNER/repo-a repo:$OWNER/repo-b repo:$OWNER/repo-c state:open type:issue label:bug" \
    -f per_page=100 \
    --jq '.items[] | {repo: .repository_url | split("/") | .[-1], number: .number, title: .title}'
```

**Limit:** The Search API supports up to 10 `repo:` qualifiers per query. For more repos, use `org:` qualifier or make multiple queries.

---

## Search Qualifiers

### Issue/PR Qualifiers

| Qualifier | Example | Notes |
|-----------|---------|-------|
| `org:` | `org:my-org` | All repos in org |
| `repo:` | `repo:owner/repo` | Specific repo (max 10) |
| `state:` | `state:open` | open, closed |
| `type:` | `type:issue` | issue, pr |
| `label:` | `label:bug` | Exact label name |
| `assignee:` | `assignee:username` | Assigned to user |
| `author:` | `author:username` | Created by user |
| `milestone:` | `milestone:"v1.0"` | In milestone |
| `created:` | `created:>2025-01-01` | Date range |
| `updated:` | `updated:>2025-06-01` | Last updated |
| `is:` | `is:open is:issue` | State and type |
| `no:` | `no:assignee` | Missing field |
| `sort:` | `sort:created-desc` | Sort order |
| `involves:` | `involves:username` | Author, assignee, or mentioned |
| `-label:` | `-label:wontfix` | Exclude label |

### Combining Qualifiers

```bash
# Open bugs assigned to nobody, created in last 7 days
gh api "/search/issues" \
    -f q="org:$OWNER state:open type:issue label:bug no:assignee created:>$(date -d '7 days ago' +%Y-%m-%d)" \
    --jq '.items[] | {repo: .repository_url | split("/") | .[-1], number: .number, title: .title}'
```

---

## Grouping Results

### Group by Repository

```bash
OWNER="my-org"

gh api "/search/issues" \
    -f q="org:$OWNER state:open type:issue" \
    -f per_page=100 \
    --jq '.items[] | {repo: .repository_url | split("/") | .[-1], number: .number, title: .title}' \
    | jq -s 'group_by(.repo) | map({repo: .[0].repo, count: length, issues: [.[] | {number, title}]})'
```

### Group by Label

```bash
gh api "/search/issues" \
    -f q="org:$OWNER state:open type:issue" \
    -f per_page=100 \
    --jq '.items[] | {
        labels: [.labels[].name],
        repo: .repository_url | split("/") | .[-1],
        number: .number,
        title: .title
    }' | jq -s '
        [.[] | .labels[] as $label | {label: $label, repo: .repo, number: .number, title: .title}]
        | group_by(.label)
        | map({label: .[0].label, count: length, items: [.[] | {repo, number, title}]})
        | sort_by(.count) | reverse
    '
```

### Group by Assignee

```bash
gh api "/search/issues" \
    -f q="org:$OWNER state:open type:issue" \
    -f per_page=100 \
    --jq '.items[] | {
        assignee: (if .assignees | length > 0 then .assignees[0].login else "unassigned" end),
        repo: .repository_url | split("/") | .[-1],
        number: .number,
        title: .title
    }' | jq -s 'group_by(.assignee) | map({assignee: .[0].assignee, count: length})'
```

---

## PR Search

### All Open PRs Across Org

```bash
OWNER="my-org"

gh api "/search/issues" \
    -f q="org:$OWNER state:open type:pr" \
    -f per_page=100 \
    --jq '.items[] | {
        repo: .repository_url | split("/") | .[-1],
        number: .number,
        title: .title,
        author: .user.login,
        created_at: .created_at,
        draft: .draft
    }' | jq -s 'sort_by(.created_at)'
```

### Stale PRs (no update in 14 days)

```bash
CUTOFF=$(date -d "14 days ago" +%Y-%m-%d)

gh api "/search/issues" \
    -f q="org:$OWNER state:open type:pr updated:<$CUTOFF" \
    -f per_page=100 \
    --jq '.items[] | {
        repo: .repository_url | split("/") | .[-1],
        number: .number,
        title: .title,
        author: .user.login,
        updated_at: .updated_at
    }' | jq -s 'sort_by(.updated_at)'
```

---

## Pagination for Large Result Sets

The Search API returns max 100 items per page and max 1,000 total results.

### Handle Pagination

```bash
PAGE=1
ALL_RESULTS="[]"

while true; do
    RESULTS=$(gh api "/search/issues" \
        -f q="org:$OWNER state:open type:issue" \
        -F per_page=100 \
        -F page=$PAGE \
        --jq '.items[] | {repo: .repository_url | split("/") | .[-1], number: .number, title: .title}' \
        | jq -s '.')

    if [[ $(echo "$RESULTS" | jq 'length') -eq 0 ]]; then
        break
    fi

    ALL_RESULTS=$(echo "$ALL_RESULTS $RESULTS" | jq -s 'add')
    PAGE=$((PAGE + 1))

    # Respect rate limits
    sleep 2
done

echo "$ALL_RESULTS" | jq 'length'
```

### Workaround for 1,000 Result Limit

For orgs with more than 1,000 open issues, split queries by repo or date range:

```bash
# Query per-repo for complete results
REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[].name')

for repo in $REPOS; do
    gh api "/search/issues" \
        -f q="repo:$OWNER/$repo state:open type:issue" \
        -f per_page=100 \
        --jq '.items[] | {repo: "'"$repo"'", number: .number, title: .title}'
    sleep 2  # Rate limit: 30 req/min
done
```

---

## Decision Table

| Need | Method | Notes |
|------|--------|-------|
| All issues in org | Search API with `org:` | Max 1,000 results |
| Issues in 2-10 repos | Search API with `repo:` qualifiers | Max 10 repos per query |
| Issues in 10+ specific repos | Multiple Search API calls | Respect rate limits |
| Complete issue list (>1,000) | Per-repo queries | Slower but complete |
| Issues with complex filters | Search API qualifiers | Rich qualifier syntax |
| Recent issues only | Search API with `created:` | Efficient for recent data |

---

## Rate Limit Awareness

| API | Limit | Reset |
|-----|-------|-------|
| Search API | 30 requests/minute | Per-minute rolling |
| REST API | 5,000 requests/hour | Per-hour rolling |

```bash
# Check current rate limit status
gh api /rate_limit --jq '{
    search: .resources.search,
    core: .resources.core
}'
```

---

## Cross-References

- Uses [repo-discovery.md](repo-discovery.md) to know which repos to search
- Results feed into [team-analytics.md](team-analytics.md) for workload analysis
- Uses [../patterns/config-caching.md](../patterns/config-caching.md) for cached workspace info
