# Reference: Repository Discovery

## Purpose

Catalog all repositories in a GitHub organization or user account. Provides filtering, grouping, and activity analysis across the entire repo portfolio.

## API Methods

| Operation | Method | Rate Limit |
|-----------|--------|-----------|
| List org repos | REST: `GET /orgs/{owner}/repos` | 5,000/hr |
| List user repos | REST: `GET /users/{owner}/repos` | 5,000/hr |
| Get repo details | REST: `GET /repos/{owner}/{repo}` | 5,000/hr |
| Search repos | REST: `GET /search/repositories` | 30/min |

---

## List All Repositories

### Organization Repos

```bash
OWNER="my-org"

gh api "/orgs/$OWNER/repos" --paginate \
    -q '.[] | {
        name: .name,
        language: .language,
        stars: .stargazers_count,
        open_issues: .open_issues_count,
        pushed_at: .pushed_at,
        archived: .archived,
        visibility: .visibility,
        default_branch: .default_branch,
        topics: .topics
    }'
```

### User Repos

```bash
OWNER="my-username"

gh api "/users/$OWNER/repos" --paginate \
    -q '.[] | {
        name: .name,
        language: .language,
        stars: .stargazers_count,
        open_issues: .open_issues_count,
        pushed_at: .pushed_at,
        archived: .archived,
        fork: .fork
    }'
```

### Key Differences

| Aspect | Organization | User |
|--------|-------------|------|
| Endpoint | `/orgs/{owner}/repos` | `/users/{owner}/repos` |
| Includes forks | By default | By default |
| Visibility field | Yes (public/private/internal) | Yes (public/private) |
| Internal repos | Possible | Not applicable |
| Max per page | 100 | 100 |

---

## Filtering

### Active Repos Only (Not Archived)

```bash
gh api "/orgs/$OWNER/repos" --paginate \
    -q '.[] | select(.archived == false) | .name'
```

### By Language

```bash
gh api "/orgs/$OWNER/repos" --paginate \
    -q '.[] | select(.language == "Python") | {name: .name, stars: .stargazers_count}'
```

### By Topic

```bash
gh api "/orgs/$OWNER/repos" --paginate \
    -q '.[] | select(.topics | index("backend")) | .name'
```

### Recently Active (pushed in last 30 days)

```bash
CUTOFF=$(date -d "30 days ago" -u +"%Y-%m-%dT%H:%M:%SZ")

gh api "/orgs/$OWNER/repos" --paginate \
    -q ".[] | select(.pushed_at > \"$CUTOFF\") | {name: .name, pushed_at: .pushed_at}" \
    | jq -s 'sort_by(.pushed_at) | reverse'
```

### Stale Repos (no push in 90 days)

```bash
CUTOFF=$(date -d "90 days ago" -u +"%Y-%m-%dT%H:%M:%SZ")

gh api "/orgs/$OWNER/repos" --paginate \
    -q ".[] | select(.archived == false and .pushed_at < \"$CUTOFF\") | {name: .name, pushed_at: .pushed_at}" \
    | jq -s 'sort_by(.pushed_at)'
```

---

## Grouping & Analysis

### Group by Language

```bash
gh api "/orgs/$OWNER/repos" --paginate \
    -q '.[] | select(.archived == false) | {name: .name, language: (.language // "None")}' \
    | jq -s 'group_by(.language) | map({language: .[0].language, count: length, repos: [.[].name]})'
```

**Example output:**
```json
[
    {"language": "Python", "count": 5, "repos": ["api", "worker", "tools", "scripts", "ml"]},
    {"language": "TypeScript", "count": 3, "repos": ["frontend", "dashboard", "mobile"]},
    {"language": "Shell", "count": 2, "repos": ["infra", "deploy"]}
]
```

### Summary Dashboard

```bash
OWNER="my-org"

echo "=== Repository Summary: $OWNER ==="

# Total counts
REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | .name')
TOTAL=$(echo "$REPOS" | wc -l)
ARCHIVED=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | select(.archived == true) | .name' | wc -l)
ACTIVE=$((TOTAL - ARCHIVED))

echo "Total: $TOTAL | Active: $ACTIVE | Archived: $ARCHIVED"

# Top repos by open issues
echo ""
echo "--- Top 5 by Open Issues ---"
gh api "/orgs/$OWNER/repos" --paginate \
    -q '.[] | select(.archived == false) | {name: .name, issues: .open_issues_count}' \
    | jq -s 'sort_by(.issues) | reverse | .[:5] | .[] | "\(.name): \(.issues) open issues"' -r

# Language distribution
echo ""
echo "--- Language Distribution ---"
gh api "/orgs/$OWNER/repos" --paginate \
    -q '.[] | select(.archived == false) | (.language // "None")' \
    | sort | uniq -c | sort -rn
```

---

## Pagination

GitHub returns max 100 items per page. Use `--paginate` to auto-fetch all pages.

```bash
# Automatically paginates through all results
gh api "/orgs/$OWNER/repos" --paginate -q '.[] | .name'
```

For very large orgs (1000+ repos), be aware this makes multiple API calls:
- 100 repos/page = 10 API calls for 1000 repos
- Each call counts against the 5,000/hr rate limit
- `--paginate` handles the `Link` header automatically

---

## Decision Table

| Need | Use This |
|------|----------|
| All repos in org | `GET /orgs/{owner}/repos --paginate` |
| All repos for user | `GET /users/{owner}/repos --paginate` |
| Search by name/topic | `GET /search/repositories?q=org:{owner}+topic:...` |
| Single repo details | `GET /repos/{owner}/{repo}` |
| Repos with specific language | REST list + jq filter |
| Recently active repos | REST list + jq date filter |

---

## Cross-References

- Used by [../references/cross-repo-search.md](cross-repo-search.md) to know which repos to search
- Used by [../references/team-analytics.md](team-analytics.md) to scope workload queries
- Uses [../patterns/config-caching.md](../patterns/config-caching.md) to cache repo list
