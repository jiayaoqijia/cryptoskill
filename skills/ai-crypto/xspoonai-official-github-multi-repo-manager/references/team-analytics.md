# Reference: Team Workload Analytics

## Purpose

Analyze team workload distribution across multiple repositories. Identifies bottlenecks, overloaded contributors, and unassigned work to support resource planning.

## API Methods

| Data Point | Method | Endpoint |
|-----------|--------|----------|
| Assigned issues | Search API | `/search/issues?q=assignee:USER org:OWNER` |
| Authored PRs | Search API | `/search/issues?q=author:USER type:pr org:OWNER` |
| Pending reviews | REST | `/repos/{owner}/{repo}/pulls` + requested_reviewers |
| Team members | REST | `/orgs/{owner}/teams/{team}/members` |
| Contributor stats | REST | `/repos/{owner}/{repo}/stats/contributors` |

---

## Per-Member Workload

### Issues Assigned Across All Repos

```bash
OWNER="my-org"
USERNAME="developer1"

gh api "/search/issues" \
    -f q="org:$OWNER assignee:$USERNAME state:open type:issue" \
    --jq '{
        total_count: .total_count,
        items: [.items[] | {
            repo: .repository_url | split("/") | .[-1],
            number: .number,
            title: .title,
            labels: [.labels[].name],
            created_at: .created_at
        }]
    }'
```

### Open PRs Authored

```bash
gh api "/search/issues" \
    -f q="org:$OWNER author:$USERNAME state:open type:pr" \
    --jq '{
        total_count: .total_count,
        items: [.items[] | {
            repo: .repository_url | split("/") | .[-1],
            number: .number,
            title: .title,
            created_at: .created_at,
            draft: .draft
        }]
    }'
```

### Pending Review Requests

```bash
OWNER="my-org"
USERNAME="developer1"

# Check each repo for pending review requests
REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | select(.archived == false) | .name')

PENDING_REVIEWS="[]"
for repo in $REPOS; do
    REVIEWS=$(gh api "/repos/$OWNER/$repo/pulls" \
        -q "[.[] | select(.requested_reviewers[].login == \"$USERNAME\") | {repo: \"$repo\", number: .number, title: .title, author: .user.login}]" 2>/dev/null)
    if [[ -n "$REVIEWS" && "$REVIEWS" != "[]" ]]; then
        PENDING_REVIEWS=$(echo "$PENDING_REVIEWS $REVIEWS" | jq -s 'add')
    fi
    sleep 0.5  # Rate limit courtesy
done

echo "$PENDING_REVIEWS"
```

---

## Team Workload Dashboard

### Full Team Overview

```bash
OWNER="my-org"

# Get all org members (or team members)
MEMBERS=$(gh api "/orgs/$OWNER/members" --paginate -q '.[].login')

echo "=== Team Workload: $OWNER ==="
echo ""
printf "%-20s %-10s %-10s %-10s\n" "Member" "Issues" "PRs" "Reviews"
printf "%-20s %-10s %-10s %-10s\n" "------" "------" "---" "-------"

for member in $MEMBERS; do
    # Count open issues assigned
    ISSUES=$(gh api "/search/issues" \
        -f q="org:$OWNER assignee:$member state:open type:issue" \
        --jq '.total_count' 2>/dev/null || echo "0")

    # Count open PRs authored
    PRS=$(gh api "/search/issues" \
        -f q="org:$OWNER author:$member state:open type:pr" \
        --jq '.total_count' 2>/dev/null || echo "0")

    # Count pending review requests (approximate via search)
    REVIEWS=$(gh api "/search/issues" \
        -f q="org:$OWNER review-requested:$member state:open type:pr" \
        --jq '.total_count' 2>/dev/null || echo "0")

    printf "%-20s %-10s %-10s %-10s\n" "$member" "$ISSUES" "$PRS" "$REVIEWS"
    sleep 2  # Rate limit: 30 search req/min
done
```

---

## Bottleneck Detection

### Review Bottlenecks

Identify who has the most pending review requests:

```bash
OWNER="my-org"

# Get all open PRs with review requests
gh api "/search/issues" \
    -f q="org:$OWNER state:open type:pr review:required" \
    -f per_page=100 \
    --jq '.items[] | {
        repo: .repository_url | split("/") | .[-1],
        number: .number,
        title: .title,
        author: .user.login,
        reviewers: [.requested_reviewers[].login],
        created_at: .created_at
    }' | jq -s '
        [.[] | .reviewers[] as $reviewer | {reviewer: $reviewer}]
        | group_by(.reviewer)
        | map({reviewer: .[0].reviewer, pending_reviews: length})
        | sort_by(.pending_reviews) | reverse
    '
```

### Workload Thresholds

| Level | Issues | PRs | Pending Reviews | Action |
|-------|--------|-----|-----------------|--------|
| Low | 0-3 | 0-1 | 0-2 | Available for new work |
| Medium | 4-7 | 2-3 | 3-4 | Normal load |
| High | 8-12 | 4-5 | 5+ | Consider rebalancing |
| Overloaded | 13+ | 6+ | 7+ | Redistribute immediately |

```bash
classify_workload() {
    local issues=$1
    local prs=$2
    local reviews=$3

    local total=$((issues + prs + reviews))

    if [[ $total -le 6 ]]; then
        echo "LOW"
    elif [[ $total -le 14 ]]; then
        echo "MEDIUM"
    elif [[ $total -le 22 ]]; then
        echo "HIGH"
    else
        echo "OVERLOADED"
    fi
}
```

---

## Team Members

### Organization Members

```bash
gh api "/orgs/$OWNER/members" --paginate \
    -q '.[] | {login: .login, id: .id, type: .type}'
```

### Team Members (Organization Teams)

```bash
TEAM_SLUG="engineering"

gh api "/orgs/$OWNER/teams/$TEAM_SLUG/members" --paginate \
    -q '.[] | {login: .login, role: .role_name}'
```

### List All Teams

```bash
gh api "/orgs/$OWNER/teams" --paginate \
    -q '.[] | {name: .name, slug: .slug, members_count: .members_count}'
```

**Note:** Team endpoints are organization-only. User accounts don't have teams.

---

## Unassigned Work

### Issues Without Assignees

```bash
gh api "/search/issues" \
    -f q="org:$OWNER state:open type:issue no:assignee" \
    -f per_page=100 \
    --jq '{
        total: .total_count,
        by_repo: [.items[] | .repository_url | split("/") | .[-1]] | group_by(.) | map({repo: .[0], count: length}) | sort_by(.count) | reverse
    }'
```

### PRs Awaiting Review

```bash
gh api "/search/issues" \
    -f q="org:$OWNER state:open type:pr review:required" \
    -f per_page=100 \
    --jq '{
        total: .total_count,
        items: [.items[] | {
            repo: .repository_url | split("/") | .[-1],
            number: .number,
            title: .title,
            author: .user.login,
            age_days: ((now - (.created_at | fromdateiso8601)) / 86400 | floor)
        }]
    }'
```

---

## Activity Scoring

Simple formula to rank contributor activity:

```bash
# Score = (issues_closed * 2) + (prs_merged * 3) + (reviews_given * 1)
# Over the last 30 days

OWNER="my-org"
USERNAME="developer1"
SINCE=$(date -d "30 days ago" +%Y-%m-%d)

ISSUES_CLOSED=$(gh api "/search/issues" \
    -f q="org:$OWNER assignee:$USERNAME type:issue closed:>$SINCE" \
    --jq '.total_count')

PRS_MERGED=$(gh api "/search/issues" \
    -f q="org:$OWNER author:$USERNAME type:pr merged:>$SINCE" \
    --jq '.total_count')

# Note: Review count is harder to get via search
# Approximate from PR review comments
SCORE=$(( (ISSUES_CLOSED * 2) + (PRS_MERGED * 3) ))
echo "$USERNAME: $SCORE points (${ISSUES_CLOSED} issues closed, ${PRS_MERGED} PRs merged)"
```

---

## Rate Limit Considerations

Team analytics is search-heavy. Plan your queries:

| Query Type | Cost | Per-Team-Member |
|-----------|------|-----------------|
| Open issues assigned | 1 search req | Yes |
| Open PRs authored | 1 search req | Yes |
| Pending reviews | 1 search req | Yes |
| **Total per member** | **3 search reqs** | |
| 10-person team | 30 search reqs | ~1 minute |
| 20-person team | 60 search reqs | ~2 minutes |

**Tip:** For large teams, cache results and refresh periodically rather than querying on every request.

---

## Cross-References

- Uses [cross-repo-search.md](cross-repo-search.md) for issue/PR queries
- Uses [repo-discovery.md](repo-discovery.md) to scope repo list
- Complements [project-boards.md](project-boards.md) with project-based workload views
- Complements [pr-pipeline.md](pr-pipeline.md) for review bottleneck analysis
