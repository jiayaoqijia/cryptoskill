# Reference: PR Review Pipeline

## Purpose

Build a cross-repo pull request review pipeline. Track PR status, identify stale reviews, detect merge-ready PRs, and surface review bottlenecks across all repositories.

## API Methods

| Data Point | Method | Endpoint |
|-----------|--------|----------|
| List open PRs | CLI | `gh pr list --repo {owner}/{repo}` |
| PR review status | REST | `GET /repos/{owner}/{repo}/pulls/{number}/reviews` |
| PR checks status | REST | `GET /repos/{owner}/{repo}/commits/{sha}/check-runs` |
| Cross-repo PR search | Search API | `/search/issues?q=org:OWNER type:pr` |
| Requested reviewers | REST | `GET /repos/{owner}/{repo}/pulls/{number}/requested_reviewers` |

---

## List Open PRs Across Repos

### Via Search API (Fastest)

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
        updated_at: .updated_at,
        draft: .draft,
        labels: [.labels[].name]
    }' | jq -s 'sort_by(.created_at)'
```

### Via gh CLI (Per Repo, More Detail)

```bash
OWNER="my-org"
REPO="my-repo"

gh pr list --repo "$OWNER/$REPO" \
    --json number,title,author,reviewDecision,createdAt,isDraft,headRefName,additions,deletions,changedFiles \
    | jq '.[] | {
        number,
        title,
        author: .author.login,
        review_decision: .reviewDecision,
        created_at: .createdAt,
        draft: .isDraft,
        branch: .headRefName,
        size: (.additions + .deletions),
        files: .changedFiles
    }'
```

---

## Review Status Analysis

### Get Review Decision Per PR

```bash
OWNER="my-org"
REPO="my-repo"
PR_NUM=42

gh api "/repos/$OWNER/$REPO/pulls/$PR_NUM/reviews" \
    --jq '[.[] | {reviewer: .user.login, state: .state, submitted_at: .submitted_at}]
        | group_by(.reviewer)
        | map({reviewer: .[0].reviewer, latest_state: (sort_by(.submitted_at) | last | .state)})'
```

### Review States

| State | Meaning |
|-------|---------|
| `APPROVED` | Reviewer approved |
| `CHANGES_REQUESTED` | Reviewer requested changes |
| `COMMENTED` | Reviewer left comments only |
| `DISMISSED` | Review was dismissed |
| `PENDING` | Review not yet submitted |

### Review Decision (Aggregated)

| Decision | Meaning |
|----------|---------|
| `APPROVED` | Required reviewers approved |
| `CHANGES_REQUESTED` | At least one reviewer requested changes |
| `REVIEW_REQUIRED` | Awaiting required reviews |
| (empty) | No branch protection requiring reviews |

---

## PR Pipeline Dashboard

### Cross-Repo Review Pipeline

```bash
OWNER="my-org"
REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | select(.archived == false) | .name')

echo "=== PR Review Pipeline: $OWNER ==="
echo ""

TOTAL_OPEN=0
TOTAL_APPROVED=0
TOTAL_CHANGES=0
TOTAL_REVIEW_NEEDED=0
TOTAL_DRAFT=0

for repo in $REPOS; do
    PRS=$(gh pr list --repo "$OWNER/$repo" \
        --json number,title,author,reviewDecision,isDraft,createdAt 2>/dev/null)

    if [[ -z "$PRS" || "$PRS" == "[]" ]]; then
        continue
    fi

    COUNT=$(echo "$PRS" | jq 'length')
    APPROVED=$(echo "$PRS" | jq '[.[] | select(.reviewDecision == "APPROVED")] | length')
    CHANGES=$(echo "$PRS" | jq '[.[] | select(.reviewDecision == "CHANGES_REQUESTED")] | length')
    REVIEW=$(echo "$PRS" | jq '[.[] | select(.reviewDecision == "REVIEW_REQUIRED" or .reviewDecision == "")] | length')
    DRAFT=$(echo "$PRS" | jq '[.[] | select(.isDraft == true)] | length')

    printf "%-25s %d open | %d approved | %d changes | %d needs review | %d draft\n" \
        "$repo" "$COUNT" "$APPROVED" "$CHANGES" "$REVIEW" "$DRAFT"

    TOTAL_OPEN=$((TOTAL_OPEN + COUNT))
    TOTAL_APPROVED=$((TOTAL_APPROVED + APPROVED))
    TOTAL_CHANGES=$((TOTAL_CHANGES + CHANGES))
    TOTAL_REVIEW_NEEDED=$((TOTAL_REVIEW_NEEDED + REVIEW))
    TOTAL_DRAFT=$((TOTAL_DRAFT + DRAFT))

    sleep 0.3
done

echo ""
echo "--- Summary ---"
echo "Total open PRs:       $TOTAL_OPEN"
echo "Approved (merge-ready): $TOTAL_APPROVED"
echo "Changes requested:     $TOTAL_CHANGES"
echo "Needs review:          $TOTAL_REVIEW_NEEDED"
echo "Drafts:                $TOTAL_DRAFT"
```

---

## Stale PR Detection

PRs with no activity for a configurable number of days.

```bash
OWNER="my-org"
STALE_DAYS=14
CUTOFF=$(date -d "$STALE_DAYS days ago" +%Y-%m-%d)

gh api "/search/issues" \
    -f q="org:$OWNER state:open type:pr updated:<$CUTOFF -is:draft" \
    -f per_page=100 \
    --jq '.items[] | {
        repo: .repository_url | split("/") | .[-1],
        number: .number,
        title: .title,
        author: .user.login,
        updated_at: .updated_at,
        stale_days: ((now - (.updated_at | fromdateiso8601)) / 86400 | floor)
    }' | jq -s 'sort_by(.stale_days) | reverse'
```

---

## Merge Readiness Check

A PR is merge-ready when:
1. Review decision is APPROVED
2. CI checks pass
3. No merge conflicts
4. Not a draft

```bash
OWNER="my-org"
REPO="my-repo"

gh pr list --repo "$OWNER/$REPO" \
    --json number,title,author,reviewDecision,isDraft,mergeable,statusCheckRollup \
    | jq '[.[] | select(
        .reviewDecision == "APPROVED"
        and .isDraft == false
        and .mergeable == "MERGEABLE"
    ) | {
        number,
        title,
        author: .author.login,
        checks_passing: ([.statusCheckRollup[]? | select(.conclusion == "SUCCESS")] | length > 0)
    }]'
```

---

## Review Bottleneck Analysis

### Who Has the Most Pending Reviews

```bash
OWNER="my-org"

gh api "/search/issues" \
    -f q="org:$OWNER state:open type:pr review:required" \
    -f per_page=100 \
    --jq '[.items[] | {reviewers: [.requested_reviewers[]?.login]}]
        | [.[] | .reviewers[] as $r | {reviewer: $r}]
        | group_by(.reviewer)
        | map({reviewer: .[0].reviewer, pending_count: length})
        | sort_by(.pending_count) | reverse'
```

### Average Time to First Review

```bash
OWNER="my-org"
REPO="my-repo"

# Get recently merged PRs
MERGED_PRS=$(gh pr list --repo "$OWNER/$REPO" --state merged --limit 20 \
    --json number,createdAt)

for pr_num in $(echo "$MERGED_PRS" | jq -r '.[].number'); do
    CREATED=$(echo "$MERGED_PRS" | jq -r ".[] | select(.number == $pr_num) | .createdAt")
    FIRST_REVIEW=$(gh api "/repos/$OWNER/$REPO/pulls/$pr_num/reviews" \
        --jq '[.[] | .submitted_at] | sort | first' 2>/dev/null)

    if [[ -n "$FIRST_REVIEW" && "$FIRST_REVIEW" != "null" ]]; then
        CREATED_EPOCH=$(date -d "$CREATED" +%s)
        REVIEW_EPOCH=$(date -d "$FIRST_REVIEW" +%s)
        HOURS=$(( (REVIEW_EPOCH - CREATED_EPOCH) / 3600 ))
        echo "PR #$pr_num: ${HOURS}h to first review"
    fi
    sleep 0.5
done
```

---

## PR Size Analysis

Flag large PRs that may be harder to review:

```bash
OWNER="my-org"
REPO="my-repo"

gh pr list --repo "$OWNER/$REPO" \
    --json number,title,additions,deletions,changedFiles \
    | jq '[.[] | {
        number,
        title,
        additions,
        deletions,
        total_changes: (.additions + .deletions),
        files: .changedFiles,
        size_category: (
            if (.additions + .deletions) < 50 then "XS"
            elif (.additions + .deletions) < 200 then "S"
            elif (.additions + .deletions) < 500 then "M"
            elif (.additions + .deletions) < 1000 then "L"
            else "XL"
            end
        )
    }] | sort_by(.total_changes) | reverse'
```

| Size | Lines Changed | Review Difficulty |
|------|-------------|------------------|
| XS | < 50 | Quick review |
| S | 50-199 | Standard review |
| M | 200-499 | Moderate effort |
| L | 500-999 | Significant effort |
| XL | 1000+ | Consider splitting |

---

## Cross-References

- Uses [cross-repo-search.md](cross-repo-search.md) for cross-org PR search
- Complements [team-analytics.md](team-analytics.md) for reviewer workload
- Uses [repo-discovery.md](repo-discovery.md) to iterate over repos
