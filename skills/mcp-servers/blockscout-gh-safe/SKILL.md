---
name: gh-safe
description: >
  Use this skill whenever you are about to run any write `gh` CLI command —
  `gh pr edit`, `gh pr create`, `gh issue edit`, `gh issue create`,
  `gh pr comment`, `gh issue comment`, `gh pr close`, `gh pr merge`,
  `gh release create`, or similar. High-level `gh` commands sometimes fail
  with "missing required scopes" auth errors even though the underlying
  GitHub REST API works fine with the same token. This skill makes you
  automatically fall back to `gh api` instead of stopping to ask the user
  to re-authenticate. Always invoke before running any mutating `gh` command.
---

# gh-safe: try `gh` first, fall back to `gh api`

## Why this exists

`gh pr edit --body "..."` (and similar write commands) can fail with:

```
error: your authentication token is missing required scopes [read:project]
To request it, run:  gh auth refresh -s read:project
```

The suggested `gh auth refresh` requires interactive browser confirmation, which
blocks automation. The `gh api` REST equivalent works with the **existing token**
and does not need the extra scope. So the right response is to fall back
immediately — not to ask the user to re-auth.

## The pattern

1. Run the high-level `gh` command and capture stderr.
2. If exit code is non-zero **and** stderr contains `"missing required scopes"` or
   `"authentication token"`, retry using the `gh api` equivalent below.
3. Do **not** prompt the user to re-authenticate or run `gh auth refresh`.

```bash
# Example: update a PR body
if ! gh pr edit 123 --repo owner/repo --body "text" 2>/dev/null; then
  # Fallback
  gh api repos/owner/repo/pulls/123 --method PATCH --field body='text'
fi
```

## Resolve owner/repo

When the repo is not already known, resolve it once:

```bash
REPO=$(gh repo view --json owner,name -q '"\(.owner.login)/\(.name)"')
# e.g. blockscout/mcp-server
```

## Command → API fallback table

### Pull requests

| High-level command | `gh api` fallback |
|---|---|
| `gh pr edit <n> --body "..."` | `gh api repos/{R}/pulls/<n> --method PATCH --field body='...'` |
| `gh pr edit <n> --title "..."` | `gh api repos/{R}/pulls/<n> --method PATCH --field title='...'` |
| `gh pr edit <n> --add-label "..."` | `gh api repos/{R}/issues/<n>/labels --method POST --field 'labels[]=...'` |
| `gh pr create --title T --body B` | `gh api repos/{R}/pulls --method POST --field title='T' --field body='B' --field head='<branch>' --field base='main'` |
| `gh pr comment <n> --body "..."` | `gh api repos/{R}/issues/<n>/comments --method POST --field body='...'` |
| `gh pr close <n>` | `gh api repos/{R}/pulls/<n> --method PATCH --field state='closed'` |
| `gh pr merge <n> --squash` | `gh api repos/{R}/pulls/<n>/merge --method PUT --field merge_method='squash'` |

### Issues

| High-level command | `gh api` fallback |
|---|---|
| `gh issue edit <n> --body "..."` | `gh api repos/{R}/issues/<n> --method PATCH --field body='...'` |
| `gh issue edit <n> --title "..."` | `gh api repos/{R}/issues/<n> --method PATCH --field title='...'` |
| `gh issue create --title T --body B` | `gh api repos/{R}/issues --method POST --field title='T' --field body='B'` |
| `gh issue comment <n> --body "..."` | `gh api repos/{R}/issues/<n>/comments --method POST --field body='...'` |
| `gh issue close <n>` | `gh api repos/{R}/issues/<n> --method PATCH --field state='closed'` |

### Releases

| High-level command | `gh api` fallback |
|---|---|
| `gh release create <tag> --title T --notes N` | `gh api repos/{R}/releases --method POST --field tag_name='<tag>' --field name='T' --field body='N'` |
| `gh release edit <tag> --notes N` | First `gh api repos/{R}/releases/tags/<tag> -q .id` to get the numeric ID, then `gh api repos/{R}/releases/<id> --method PATCH --field body='N'` |

`{R}` = `owner/repo` resolved above.

## Tips

- `--field` URL-encodes the value; use `--raw-field` when the value must be
  passed byte-for-byte (rare).
- Multi-line bodies work cleanly with a HEREDOC:
  ```bash
  gh api repos/{R}/pulls/123 --method PATCH --field body="$(cat <<'EOF'
  ## Summary
  ...
  EOF
  )"
  ```
- `gh api` returns JSON. Append `-q .html_url` (or any jq path) to extract
  just what you need.
- The `--repo` flag on high-level commands is equivalent to resolving `{R}`
  manually for `gh api`; either approach is fine.
