# Reference: Projects v2 Board Management

## Purpose

Manage GitHub Projects v2 boards that span multiple repositories. Projects v2 is GitHub's modern project management system using GraphQL. This is the **innovation core** of the multi-repo manager -- no other skill in the ecosystem provides this depth of Projects v2 coverage.

## API Support Matrix

| Operation | gh CLI | REST | GraphQL | Notes |
|-----------|--------|------|---------|-------|
| List projects | `gh project list` | Read-only | Full | REST only for org/user listing |
| View project | `gh project view` | Read-only | Full | |
| Create project | `gh project create` | No | `createProjectV2` | |
| Edit project | `gh project edit` | No | `updateProjectV2` | |
| Add item (issue/PR) | `gh project item-add` | No | `addProjectV2ItemById` | From any repo |
| Update field value | `gh project item-edit` | No | `updateProjectV2ItemFieldValue` | |
| List items | `gh project item-list` | No | Query | |
| List fields | `gh project field-list` | No | Query | |
| Archive item | `gh project item-archive` | No | `archiveProjectV2Item` | |
| Delete item | `gh project item-delete` | No | `deleteProjectV2Item` | |
| Link repository | `gh project link` | No | `linkProjectV2ToRepository` | |
| Clear field value | No | No | `clearProjectV2ItemFieldValue` | GraphQL only |
| Move item position | No | No | `updateProjectV2ItemPosition` | GraphQL only |

---

## Querying Projects

### List All Projects (Organization)

```bash
cat > /tmp/query.graphql << 'QUERY'
query($login: String!) {
  organization(login: $login) {
    projectsV2(first: 20) {
      nodes {
        number
        title
        closed
        id
        url
        shortDescription
        items {
          totalCount
        }
      }
    }
  }
}
QUERY

gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f login="$OWNER" \
    | jq '.data.organization.projectsV2.nodes[] | select(.closed == false)'

rm -f /tmp/query.graphql
```

### List All Projects (User)

Replace `organization` with `user` in the query:

```bash
cat > /tmp/query.graphql << 'QUERY'
query($login: String!) {
  user(login: $login) {
    projectsV2(first: 20) {
      nodes {
        number
        title
        closed
        id
        url
      }
    }
  }
}
QUERY

gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f login="$OWNER" \
    | jq '.data.user.projectsV2.nodes[] | select(.closed == false)'

rm -f /tmp/query.graphql
```

### CLI Alternative

```bash
gh project list --owner "$OWNER" --format json | jq '.projects[] | select(.closed == false)'
```

---

## Project Fields

### List Fields with Options

```bash
cat > /tmp/query.graphql << 'QUERY'
query($login: String!, $number: Int!) {
  organization(login: $login) {
    projectV2(number: $number) {
      fields(first: 30) {
        nodes {
          ... on ProjectV2SingleSelectField {
            name
            id
            dataType
            options {
              name
              id
              description
              color
            }
          }
          ... on ProjectV2Field {
            name
            id
            dataType
          }
          ... on ProjectV2IterationField {
            name
            id
            dataType
            configuration {
              iterations {
                id
                title
                startDate
                duration
              }
            }
          }
        }
      }
    }
  }
}
QUERY

gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f login="$OWNER" \
    -F number=$PROJECT_NUM \
    | jq '.data.organization.projectV2.fields.nodes'

rm -f /tmp/query.graphql
```

### Field Types

| Type | GraphQL Type | Value Format | Update Method |
|------|-------------|-------------|---------------|
| Text | `ProjectV2Field` | String | `value: {text: "..."}` |
| Number | `ProjectV2Field` | Float | `value: {number: 42.0}` |
| Date | `ProjectV2Field` | ISO 8601 | `value: {date: "2025-01-15"}` |
| Single Select | `ProjectV2SingleSelectField` | Option ID | `value: {singleSelectOptionId: "..."}` |
| Iteration | `ProjectV2IterationField` | Iteration ID | `value: {iterationId: "..."}` |

---

## Project Items

### List Items with Status

```bash
cat > /tmp/query.graphql << 'QUERY'
query($login: String!, $number: Int!) {
  organization(login: $login) {
    projectV2(number: $number) {
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue {
              number
              title
              state
              repository { name }
              url
            }
            ... on PullRequest {
              number
              title
              state
              repository { name }
              url
            }
            ... on DraftIssue {
              title
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2SingleSelectField { name } }
              }
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2Field { name } }
              }
              ... on ProjectV2ItemFieldDateValue {
                date
                field { ... on ProjectV2Field { name } }
              }
            }
          }
        }
      }
    }
  }
}
QUERY

gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f login="$OWNER" \
    -F number=$PROJECT_NUM \
    | jq '.data.organization.projectV2.items.nodes'

rm -f /tmp/query.graphql
```

### Items Grouped by Status

```bash
# After fetching items (as above), group by status field
echo "$ITEMS" | jq '
    [.[] | {
        status: (.fieldValues.nodes[] | select(.field.name == "Status") | .name) // "No Status",
        repo: .content.repository.name,
        number: .content.number,
        title: .content.title,
        type: (if .content.state then (if .content.url | test("/pull/") then "PR" else "Issue" end) else "Draft" end)
    }]
    | group_by(.status)
    | map({status: .[0].status, count: length, items: .})
'
```

### Items from a Specific Repository

```bash
echo "$ITEMS" | jq '[.[] | select(.content.repository.name == "target-repo")]'
```

---

## Adding Items from Any Repository

This is the key multi-repo capability -- add issues/PRs from any repo in the org to a project board.

### Step 1: Get Item Node ID

```bash
cat > /tmp/query.graphql << 'QUERY'
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $number) {
      id
      title
    }
  }
}
QUERY

ISSUE_ID=$(gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f owner="$OWNER" \
    -f repo="$REPO" \
    -F number=$ISSUE_NUM \
    --jq '.data.repository.issue.id')

rm -f /tmp/query.graphql
```

### Step 2: Add to Project

```bash
cat > /tmp/query.graphql << 'QUERY'
mutation($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {
    projectId: $projectId
    contentId: $contentId
  }) {
    item {
      id
    }
  }
}
QUERY

ITEM_ID=$(gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f projectId="$PROJECT_ID" \
    -f contentId="$ISSUE_ID" \
    --jq '.data.addProjectV2ItemById.item.id')

rm -f /tmp/query.graphql
echo "Added as project item: $ITEM_ID"
```

### CLI Alternative

```bash
gh project item-add $PROJECT_NUM --owner "$OWNER" --url "https://github.com/$OWNER/$REPO/issues/$ISSUE_NUM"
```

---

## Updating Field Values

### Set Status (Single Select)

Requires: Project ID, Item ID, Field ID, Option ID.

```bash
cat > /tmp/query.graphql << 'QUERY'
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
    value: { singleSelectOptionId: $optionId }
  }) {
    projectV2Item { id }
  }
}
QUERY

gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f projectId="$PROJECT_ID" \
    -f itemId="$ITEM_ID" \
    -f fieldId="$FIELD_ID" \
    -f optionId="$OPTION_ID"

rm -f /tmp/query.graphql
```

### Set Text Field

```bash
cat > /tmp/query.graphql << 'QUERY'
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $text: String!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
    value: { text: $text }
  }) {
    projectV2Item { id }
  }
}
QUERY

gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f projectId="$PROJECT_ID" \
    -f itemId="$ITEM_ID" \
    -f fieldId="$FIELD_ID" \
    -f text="My custom value"

rm -f /tmp/query.graphql
```

### Set Date Field

```bash
cat > /tmp/query.graphql << 'QUERY'
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $date: Date!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
    value: { date: $date }
  }) {
    projectV2Item { id }
  }
}
QUERY

gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f projectId="$PROJECT_ID" \
    -f itemId="$ITEM_ID" \
    -f fieldId="$FIELD_ID" \
    -f date="2025-06-15"

rm -f /tmp/query.graphql
```

### Clear Field Value

```bash
cat > /tmp/query.graphql << 'QUERY'
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!) {
  clearProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
  }) {
    projectV2Item { id }
  }
}
QUERY

gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f projectId="$PROJECT_ID" \
    -f itemId="$ITEM_ID" \
    -f fieldId="$FIELD_ID"

rm -f /tmp/query.graphql
```

---

## Project Board Dashboard

### Cross-Repo Status Overview

Build a dashboard showing items across all repos grouped by status:

```bash
# Fetch all items
ITEMS=$(gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f login="$OWNER" \
    -F number=$PROJECT_NUM \
    | jq '.data.organization.projectV2.items.nodes')

# Dashboard
echo "=== Project Board: $PROJECT_NUM ==="
echo ""

for status in "Todo" "In Progress" "In Review" "Done"; do
    COUNT=$(echo "$ITEMS" | jq "[.[] | select(.fieldValues.nodes[] | select(.field.name == \"Status\" and .name == \"$status\"))] | length")
    echo "--- $status ($COUNT) ---"
    echo "$ITEMS" | jq -r "
        [.[] | select(.fieldValues.nodes[] | select(.field.name == \"Status\" and .name == \"$status\"))]
        | .[] | \"  [\(.content.repository.name // \"draft\")] #\(.content.number // \"-\") \(.content.title)\"
    "
    echo ""
done
```

---

## Linking Repositories to Projects

```bash
cat > /tmp/query.graphql << 'QUERY'
mutation($projectId: ID!, $repositoryId: ID!) {
  linkProjectV2ToRepository(input: {
    projectId: $projectId
    repositoryId: $repositoryId
  }) {
    repository { name }
  }
}
QUERY

# Get repo ID first
REPO_ID=$(gh api "/repos/$OWNER/$REPO" --jq '.node_id')

gh api graphql \
    -f query="$(cat /tmp/query.graphql)" \
    -f projectId="$PROJECT_ID" \
    -f repositoryId="$REPO_ID"

rm -f /tmp/query.graphql
```

---

## ID Resolution for Projects

All project operations need IDs. Use the cache-first strategy:

```bash
# From config cache (fast)
PROJECT_ID=$(yq ".projects.catalog[] | select(.number == $PROJECT_NUM) | .id" "$CONFIG_PATH")
FIELD_ID=$(yq ".projects.catalog[] | select(.number == $PROJECT_NUM) | .fields[\"Status\"].id" "$CONFIG_PATH")
OPTION_ID=$(yq ".projects.catalog[] | select(.number == $PROJECT_NUM) | .fields[\"Status\"].options[\"In Progress\"]" "$CONFIG_PATH")

# Fallback to API (slow but always works)
# See patterns/config-caching.md for full resolution flow
```

---

## Required Scopes

| Scope | Purpose |
|-------|---------|
| `project` | Read/write access to projects |
| `read:project` | Read-only access to projects |
| `repo` | Access to issues/PRs (needed to add items) |
| `read:org` | Access to org-level projects |

```bash
# Verify scopes
gh auth status

# Add missing scopes
gh auth refresh --scopes 'repo,read:org,project'
```

---

## Limitations

- **Views:** UI-only, no API for creating/managing views
- **Workflows:** Can only delete, not create/update via API
- **Field options:** `updateProjectV2Field` replaces ALL options at once
- **Status updates:** Require project admin permissions
- **Item limit:** Pagination needed for projects with 100+ items
- **Cross-org:** Cannot add items from repos outside the project's org/user

---

## Cross-References

- Uses [../patterns/graphql-execution.md](../patterns/graphql-execution.md) for all GraphQL queries
- Uses [../patterns/config-caching.md](../patterns/config-caching.md) for ID resolution
- Fed by [cross-repo-search.md](cross-repo-search.md) to find issues to add to boards
- Complements [team-analytics.md](team-analytics.md) with project-based workload views
