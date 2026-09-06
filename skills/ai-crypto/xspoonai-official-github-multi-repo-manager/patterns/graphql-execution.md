# Pattern: Safe GraphQL Execution

## Purpose

Execute GraphQL queries and mutations via `gh api graphql` without shell variable expansion conflicts. This is the foundational execution pattern used by all reference operations that require GraphQL.

## When to Use

- Any GraphQL query or mutation with `$variable` parameters
- Projects v2 operations (most require GraphQL)
- Cross-repo queries that need the Search API's GraphQL interface

## The Problem

GraphQL uses `$variable` syntax that conflicts with bash `$expansion`:

```bash
# FAILS - shell tries to expand $login as a bash variable
gh api graphql -f query='query($login: String!) { organization(login: $login) { id } }'
# Error: Expected VAR_SIGN, actual: UNKNOWN_CHAR
```

---

## Solution: Temp File Method

Write the query to a temp file using a single-quoted HEREDOC delimiter, then read it back.

### Step 1: Write Query

```bash
cat > /tmp/query.graphql << 'QUERY'
query($login: String!) {
  organization(login: $login) {
    id
    projectsV2(first: 20) {
      nodes {
        number
        title
        id
      }
    }
  }
}
QUERY
```

**Key:** The `'QUERY'` delimiter (single-quoted) prevents shell expansion inside the HEREDOC.

### Step 2: Execute

```bash
gh api graphql \
  -f query="$(cat /tmp/query.graphql)" \
  -f login="hiivmind"
```

### Step 3: Cleanup

```bash
rm -f /tmp/query.graphql
```

### Full Pattern

```bash
cat > /tmp/query.graphql << 'QUERY'
query($login: String!) {
  organization(login: $login) {
    projectsV2(first: 20) {
      nodes { number title id }
    }
  }
}
QUERY

RESULT=$(gh api graphql \
  -f query="$(cat /tmp/query.graphql)" \
  -f login="$OWNER" 2>&1)

rm -f /tmp/query.graphql

# Check for errors
if echo "$RESULT" | jq -e '.errors' >/dev/null 2>&1; then
    echo "GraphQL Error:"
    echo "$RESULT" | jq -r '.errors[].message'
    exit 1
fi

echo "$RESULT" | jq '.data'
```

---

## Variable Passing

### Flag Types

| GraphQL Type | gh Flag | Example |
|--------------|---------|---------|
| `String!` | `-f` | `-f login="hiivmind"` |
| `Int!` | `-F` | `-F number=2` |
| `Boolean` | `-F` | `-F includeArchived=true` |
| `ID!` | `-f` | `-f projectId="PVT_xxx"` |

**Rule:** Use `-f` for strings/IDs, `-F` for numbers and booleans.

### Multiple Variables

```bash
gh api graphql \
  -f query="$(cat /tmp/query.graphql)" \
  -f login="hiivmind" \
  -F number=2 \
  -F includeArchived=false
```

---

## Direct Queries (No Variables)

Queries without `$variable` parameters can be passed directly:

```bash
# Works - no $ variables in query body
gh api graphql -f query='{ viewer { login id } }' --jq '.data.viewer'
```

Use this for:
- Viewer queries (authenticated user info)
- Queries with hardcoded values
- Simple introspection

---

## Organization vs User Queries

The GraphQL root differs based on workspace type:

### Organization

```graphql
query($login: String!) {
  organization(login: $login) {
    projectsV2(first: 20) { nodes { number title id } }
  }
}
```

### User

```graphql
query($login: String!) {
  user(login: $login) {
    projectsV2(first: 20) { nodes { number title id } }
  }
}
```

### Dynamic Root Selection

```bash
QUERY_ROOT="organization"  # or "user" based on workspace type

cat > /tmp/query.graphql << QUERY
query(\$login: String!) {
  $QUERY_ROOT(login: \$login) {
    projectsV2(first: 20) {
      nodes { number title id }
    }
  }
}
QUERY
```

Note: When using unquoted HEREDOC (for variable substitution in root), escape GraphQL `$` with `\$`.

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Expected VAR_SIGN, actual: UNKNOWN_CHAR` | Shell expanded `$` in query | Use temp file method |
| `Could not resolve to an Organization` | Wrong login or no access | Check spelling, verify membership |
| `Resource not accessible by integration` | Missing scopes | `gh auth refresh --scopes 'repo,read:org,project'` |
| `Could not resolve to a ProjectV2` | Wrong project number | Verify project exists |
| `type mismatch` on variable | Wrong flag type | Use `-F` for Int, `-f` for String |

### Error Detection Pattern

```bash
RESPONSE=$(gh api graphql -f query="$(cat /tmp/query.graphql)" -f login="$OWNER" 2>&1)

if echo "$RESPONSE" | jq -e '.errors' >/dev/null 2>&1; then
    echo "GraphQL Error:"
    echo "$RESPONSE" | jq -r '.errors[].message'
else
    echo "$RESPONSE" | jq '.data'
fi
```

---

## Examples

### Example 1: List Projects

```bash
cat > /tmp/query.graphql << 'QUERY'
query($login: String!) {
  organization(login: $login) {
    projectsV2(first: 20) {
      nodes { number title closed id url }
    }
  }
}
QUERY

gh api graphql \
  -f query="$(cat /tmp/query.graphql)" \
  -f login="hiivmind" \
  | jq '.data.organization.projectsV2.nodes[] | select(.closed == false)'

rm -f /tmp/query.graphql
```

### Example 2: Add Item to Project

```bash
cat > /tmp/query.graphql << 'QUERY'
mutation($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {
    projectId: $projectId
    contentId: $contentId
  }) {
    item { id }
  }
}
QUERY

gh api graphql \
  -f query="$(cat /tmp/query.graphql)" \
  -f projectId="PVT_kwDOxx" \
  -f contentId="I_kwDOxx"

rm -f /tmp/query.graphql
```

### Example 3: Update Item Field Value

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
  -f projectId="PVT_kwDOxx" \
  -f itemId="PVTI_xx" \
  -f fieldId="PVTSSF_xx" \
  -f optionId="47fc9ee4"

rm -f /tmp/query.graphql
```

---

## Related Patterns

- [workspace-init.md](workspace-init.md) - Uses GraphQL execution for project discovery
- [config-caching.md](config-caching.md) - Provides cached IDs for GraphQL variables
