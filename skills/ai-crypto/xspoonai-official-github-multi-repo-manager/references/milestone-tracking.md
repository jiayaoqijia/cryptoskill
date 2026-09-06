# Reference: Cross-Repo Milestone Tracking

## Purpose

Track milestone progress across multiple repositories. Milestones are repo-scoped in GitHub, so cross-repo tracking requires aggregating data from each repo individually.

## API Methods

> **IMPORTANT:** There is NO `gh milestone` CLI command. All milestone operations use REST API.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List milestones | REST | `GET /repos/{owner}/{repo}/milestones` |
| Get milestone | REST | `GET /repos/{owner}/{repo}/milestones/{number}` |
| Create milestone | REST | `POST /repos/{owner}/{repo}/milestones` |
| Update milestone | REST | `PATCH /repos/{owner}/{repo}/milestones/{number}` |
| Close milestone | REST | `PATCH /repos/{owner}/{repo}/milestones/{number}` (state: closed) |
| Set on issue | CLI | `gh issue edit {num} --milestone {name}` |

---

## List Milestones Per Repo

```bash
OWNER="my-org"
REPO="my-repo"

gh api "/repos/$OWNER/$REPO/milestones" \
    -q '.[] | {
        number: .number,
        title: .title,
        state: .state,
        open_issues: .open_issues,
        closed_issues: .closed_issues,
        due_on: .due_on,
        description: .description
    }'
```

---

## Cross-Repo Milestone Dashboard

### Find Same Milestone Across Repos

Many organizations use the same milestone title (e.g., "v2.0", "Q1 2026") across multiple repos.

```bash
OWNER="my-org"
MILESTONE_TITLE="v2.0"

# Get all repos
REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | select(.archived == false) | .name')

echo "=== Milestone: $MILESTONE_TITLE ==="
echo ""
printf "%-25s %-8s %-8s %-8s %-12s %-10s\n" "Repository" "Open" "Closed" "Progress" "Due" "State"
printf "%-25s %-8s %-8s %-8s %-12s %-10s\n" "----------" "----" "------" "--------" "---" "-----"

TOTAL_OPEN=0
TOTAL_CLOSED=0

for repo in $REPOS; do
    MILESTONE=$(gh api "/repos/$OWNER/$repo/milestones" \
        -q ".[] | select(.title == \"$MILESTONE_TITLE\")" 2>/dev/null)

    if [[ -n "$MILESTONE" ]]; then
        OPEN=$(echo "$MILESTONE" | jq -r '.open_issues')
        CLOSED=$(echo "$MILESTONE" | jq -r '.closed_issues')
        TOTAL=$((OPEN + CLOSED))
        DUE=$(echo "$MILESTONE" | jq -r '.due_on // "none" | if . != "none" then .[0:10] else "none" end')
        STATE=$(echo "$MILESTONE" | jq -r '.state')

        if [[ $TOTAL -gt 0 ]]; then
            PCT=$(( (CLOSED * 100) / TOTAL ))
        else
            PCT=0
        fi

        printf "%-25s %-8s %-8s %-7s%% %-12s %-10s\n" "$repo" "$OPEN" "$CLOSED" "$PCT" "$DUE" "$STATE"

        TOTAL_OPEN=$((TOTAL_OPEN + OPEN))
        TOTAL_CLOSED=$((TOTAL_CLOSED + CLOSED))
    fi
    sleep 0.3  # Rate limit courtesy
done

echo ""
GRAND_TOTAL=$((TOTAL_OPEN + TOTAL_CLOSED))
if [[ $GRAND_TOTAL -gt 0 ]]; then
    GRAND_PCT=$(( (TOTAL_CLOSED * 100) / GRAND_TOTAL ))
else
    GRAND_PCT=0
fi
printf "%-25s %-8s %-8s %-7s%%\n" "TOTAL" "$TOTAL_OPEN" "$TOTAL_CLOSED" "$GRAND_PCT"
```

**Example output:**
```
=== Milestone: v2.0 ===

Repository                Open     Closed   Progress Due          State
----------                ----     ------   -------- ---          -----
api-server                3        12       80%      2025-03-01   open
web-frontend              5        8        62%      2025-03-01   open
shared-libs               0        4        100%     2025-02-15   closed
mobile-app                7        3        30%      2025-03-15   open

TOTAL                     15       27       64%
```

---

## Progress Calculation

```bash
calculate_progress() {
    local open=$1
    local closed=$2
    local total=$((open + closed))

    if [[ $total -eq 0 ]]; then
        echo "0"
    else
        echo $(( (closed * 100) / total ))
    fi
}
```

---

## Due Date Tracking

### Overdue Milestones

```bash
OWNER="my-org"
TODAY=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | select(.archived == false) | .name')

echo "=== Overdue Milestones ==="
for repo in $REPOS; do
    gh api "/repos/$OWNER/$repo/milestones" \
        -q ".[] | select(.state == \"open\" and .due_on != null and .due_on < \"$TODAY\") | {
            repo: \"$repo\",
            title: .title,
            due_on: .due_on[0:10],
            open_issues: .open_issues,
            closed_issues: .closed_issues
        }" 2>/dev/null
    sleep 0.3
done | jq -s '.'
```

### Milestones Due This Week

```bash
WEEK_START=$(date -u +"%Y-%m-%dT00:00:00Z")
WEEK_END=$(date -d "+7 days" -u +"%Y-%m-%dT23:59:59Z")

for repo in $REPOS; do
    gh api "/repos/$OWNER/$repo/milestones" \
        -q ".[] | select(.state == \"open\" and .due_on != null and .due_on >= \"$WEEK_START\" and .due_on <= \"$WEEK_END\") | {
            repo: \"$repo\",
            title: .title,
            due_on: .due_on[0:10],
            open_issues: .open_issues
        }" 2>/dev/null
    sleep 0.3
done | jq -s '.'
```

---

## Blocker Detection

Find open issues blocking milestone completion:

```bash
OWNER="my-org"
REPO="my-repo"
MILESTONE_TITLE="v2.0"

gh api "/search/issues" \
    -f q="repo:$OWNER/$REPO milestone:\"$MILESTONE_TITLE\" state:open type:issue" \
    --jq '.items[] | {
        number: .number,
        title: .title,
        assignee: (.assignees[0].login // "unassigned"),
        labels: [.labels[].name],
        created_at: .created_at,
        age_days: ((now - (.created_at | fromdateiso8601)) / 86400 | floor)
    }' | jq -s 'sort_by(.age_days) | reverse'
```

---

## Create Milestone Across Repos

Create the same milestone in multiple repositories:

```bash
OWNER="my-org"
TITLE="v3.0"
DESCRIPTION="Version 3.0 release"
DUE_DATE="2025-06-01T00:00:00Z"

REPOS="api-server web-frontend shared-libs mobile-app"

for repo in $REPOS; do
    echo "Creating milestone '$TITLE' in $repo..."
    gh api "/repos/$OWNER/$repo/milestones" \
        --method POST \
        -f title="$TITLE" \
        -f description="$DESCRIPTION" \
        -f due_on="$DUE_DATE" \
        --jq '{number: .number, title: .title, url: .html_url}'
    sleep 0.3
done
```

---

## Update Milestone Cache

After querying milestones, cache them for fast resolution:

```bash
OWNER=$(yq '.workspace.login' "$CONFIG_PATH")
REPO="my-repo"

MILESTONES=$(gh api "/repos/$OWNER/$REPO/milestones" \
    --jq '[.[] | {number: .number, title: .title, id: .node_id, state: .state}]')

yq -i ".milestones[\"$REPO\"] = $MILESTONES" "$CONFIG_PATH"
```

---

## Milestone Health Summary

```bash
health_check() {
    local open=$1
    local closed=$2
    local due_date=$3
    local total=$((open + closed))

    if [[ $total -eq 0 ]]; then
        echo "EMPTY"
        return
    fi

    local pct=$(( (closed * 100) / total ))

    if [[ -n "$due_date" && "$due_date" != "null" ]]; then
        local due_epoch=$(date -d "$due_date" +%s 2>/dev/null)
        local now_epoch=$(date +%s)
        local days_left=$(( (due_epoch - now_epoch) / 86400 ))

        if [[ $days_left -lt 0 ]]; then
            echo "OVERDUE (${pct}% done, $((days_left * -1)) days past due)"
        elif [[ $days_left -lt 7 && $pct -lt 80 ]]; then
            echo "AT RISK (${pct}% done, ${days_left} days left)"
        elif [[ $pct -ge 100 ]]; then
            echo "COMPLETE"
        else
            echo "ON TRACK (${pct}% done, ${days_left} days left)"
        fi
    else
        echo "NO DUE DATE (${pct}% done)"
    fi
}
```

---

## Cross-References

- Uses [repo-discovery.md](repo-discovery.md) to iterate over repositories
- Uses [../patterns/config-caching.md](../patterns/config-caching.md) for milestone ID caching
- Complements [cross-repo-search.md](cross-repo-search.md) for finding milestone blockers
