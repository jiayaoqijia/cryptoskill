# Reference: Release Coordination

## Purpose

Track release status across multiple repositories. Identify which repos need releases, compare release cadence, and surface unreleased commits to coordinate org-wide releases.

## API Methods

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Latest release | REST | `GET /repos/{owner}/{repo}/releases/latest` |
| All releases | REST | `GET /repos/{owner}/{repo}/releases` |
| Draft releases | REST | `GET /repos/{owner}/{repo}/releases` (filter draft) |
| Compare (unreleased) | REST | `GET /repos/{owner}/{repo}/compare/{tag}...HEAD` |
| Tags | REST | `GET /repos/{owner}/{repo}/tags` |
| Create release | CLI | `gh release create` |

---

## Latest Release Per Repo

```bash
OWNER="my-org"
REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | select(.archived == false) | .name')

echo "=== Latest Releases: $OWNER ==="
echo ""
printf "%-25s %-15s %-12s %-20s\n" "Repository" "Tag" "Date" "Name"
printf "%-25s %-15s %-12s %-20s\n" "----------" "---" "----" "----"

for repo in $REPOS; do
    RELEASE=$(gh api "/repos/$OWNER/$repo/releases/latest" 2>/dev/null)

    if [[ $? -eq 0 && -n "$RELEASE" ]]; then
        TAG=$(echo "$RELEASE" | jq -r '.tag_name')
        DATE=$(echo "$RELEASE" | jq -r '.published_at[0:10]')
        NAME=$(echo "$RELEASE" | jq -r '.name // .tag_name')
        printf "%-25s %-15s %-12s %-20s\n" "$repo" "$TAG" "$DATE" "$NAME"
    else
        printf "%-25s %-15s %-12s %-20s\n" "$repo" "(none)" "-" "-"
    fi
    sleep 0.3
done
```

---

## Unreleased Commits

Compare the latest release tag with HEAD to find repos with unreleased work.

```bash
OWNER="my-org"
THRESHOLD=5  # Flag repos with more than N unreleased commits

REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | select(.archived == false) | .name')

echo "=== Repos with Unreleased Commits ==="
echo ""
printf "%-25s %-15s %-10s %-10s\n" "Repository" "Latest Tag" "Ahead By" "Status"
printf "%-25s %-15s %-10s %-10s\n" "----------" "----------" "--------" "------"

for repo in $REPOS; do
    # Get latest release tag
    TAG=$(gh api "/repos/$OWNER/$repo/releases/latest" --jq '.tag_name' 2>/dev/null)

    if [[ -z "$TAG" || "$TAG" == "null" ]]; then
        # No releases yet - check if there are any commits
        COMMITS=$(gh api "/repos/$OWNER/$repo/commits" -q 'length' 2>/dev/null)
        if [[ -n "$COMMITS" && "$COMMITS" -gt 0 ]]; then
            printf "%-25s %-15s %-10s %-10s\n" "$repo" "(no release)" "$COMMITS" "NEEDS FIRST"
        fi
        continue
    fi

    # Compare tag with HEAD
    COMPARE=$(gh api "/repos/$OWNER/$repo/compare/$TAG...HEAD" 2>/dev/null)

    if [[ $? -eq 0 ]]; then
        AHEAD=$(echo "$COMPARE" | jq -r '.ahead_by')
        if [[ "$AHEAD" -gt "$THRESHOLD" ]]; then
            printf "%-25s %-15s %-10s %-10s\n" "$repo" "$TAG" "$AHEAD" "NEEDS RELEASE"
        elif [[ "$AHEAD" -gt 0 ]]; then
            printf "%-25s %-15s %-10s %-10s\n" "$repo" "$TAG" "$AHEAD" "minor"
        fi
    fi
    sleep 0.3
done
```

---

## Draft Releases

Find repos with draft releases ready to publish:

```bash
OWNER="my-org"
REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | select(.archived == false) | .name')

echo "=== Draft Releases ==="
for repo in $REPOS; do
    DRAFTS=$(gh api "/repos/$OWNER/$repo/releases" \
        -q '[.[] | select(.draft == true) | {tag: .tag_name, name: .name, created_at: .created_at[0:10]}]' 2>/dev/null)

    if [[ -n "$DRAFTS" && "$DRAFTS" != "[]" ]]; then
        echo ""
        echo "--- $repo ---"
        echo "$DRAFTS" | jq -r '.[] | "  \(.tag) - \(.name) (created: \(.created_at))"'
    fi
    sleep 0.3
done
```

---

## Release Cadence Analysis

Calculate days between releases to understand release frequency:

```bash
OWNER="my-org"
REPO="my-repo"

gh api "/repos/$OWNER/$REPO/releases" -q '
    [.[] | select(.draft == false and .prerelease == false) | {
        tag: .tag_name,
        date: .published_at
    }]
    | sort_by(.date) | reverse
    | . as $releases
    | [range(0; length - 1) | {
        from: $releases[. + 1].tag,
        to: $releases[.].tag,
        days: ((($releases[.].date | fromdateiso8601) - ($releases[. + 1].date | fromdateiso8601)) / 86400 | floor)
    }]
'
```

**Example output:**
```json
[
    {"from": "v1.8.0", "to": "v1.9.0", "days": 14},
    {"from": "v1.7.0", "to": "v1.8.0", "days": 21},
    {"from": "v1.6.0", "to": "v1.7.0", "days": 7}
]
```

### Average Cadence Across Repos

```bash
OWNER="my-org"
REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | select(.archived == false) | .name')

echo "=== Release Cadence ==="
printf "%-25s %-10s %-15s %-15s\n" "Repository" "Releases" "Avg Days" "Last Release"
printf "%-25s %-10s %-15s %-15s\n" "----------" "--------" "--------" "------------"

for repo in $REPOS; do
    RELEASES=$(gh api "/repos/$OWNER/$repo/releases" -q '
        [.[] | select(.draft == false)] | length' 2>/dev/null)

    if [[ -z "$RELEASES" || "$RELEASES" -lt 2 ]]; then
        continue
    fi

    CADENCE=$(gh api "/repos/$OWNER/$repo/releases" -q '
        [.[] | select(.draft == false) | .published_at]
        | sort | reverse
        | . as $dates
        | [range(0; length - 1) | (($dates[.] | fromdateiso8601) - ($dates[. + 1] | fromdateiso8601)) / 86400]
        | (add / length | floor)' 2>/dev/null)

    LAST=$(gh api "/repos/$OWNER/$repo/releases/latest" --jq '.published_at[0:10]' 2>/dev/null)

    printf "%-25s %-10s %-15s %-15s\n" "$repo" "$RELEASES" "${CADENCE} days" "$LAST"
    sleep 0.5
done
```

---

## Coordination Dashboard

Combined view for release planning:

```bash
OWNER="my-org"

echo "========================================"
echo "  Release Coordination: $OWNER"
echo "========================================"
echo ""

# 1. Repos needing release
echo "--- Repos Needing Release ---"
# (Use unreleased commits section above)

echo ""

# 2. Draft releases ready to publish
echo "--- Draft Releases (Ready to Publish) ---"
# (Use draft releases section above)

echo ""

# 3. Recent releases (last 7 days)
echo "--- Recent Releases (Last 7 Days) ---"
WEEK_AGO=$(date -d "7 days ago" -u +"%Y-%m-%dT%H:%M:%SZ")

REPOS=$(gh api "/orgs/$OWNER/repos" --paginate -q '.[] | select(.archived == false) | .name')
for repo in $REPOS; do
    gh api "/repos/$OWNER/$repo/releases" \
        -q ".[] | select(.draft == false and .published_at > \"$WEEK_AGO\") | {
            repo: \"$repo\",
            tag: .tag_name,
            date: .published_at[0:10],
            author: .author.login
        }" 2>/dev/null
    sleep 0.3
done | jq -s 'sort_by(.date) | reverse'
```

---

## Create Release

```bash
OWNER="my-org"
REPO="my-repo"
TAG="v1.0.0"

# Create release with auto-generated notes
gh release create "$TAG" \
    --repo "$OWNER/$REPO" \
    --title "Release $TAG" \
    --generate-notes

# Create draft release
gh release create "$TAG" \
    --repo "$OWNER/$REPO" \
    --title "Release $TAG" \
    --generate-notes \
    --draft
```

---

## Cross-References

- Uses [repo-discovery.md](repo-discovery.md) to enumerate repositories
- Complements [milestone-tracking.md](milestone-tracking.md) for release-milestone alignment
- Uses [../patterns/config-caching.md](../patterns/config-caching.md) for workspace context
