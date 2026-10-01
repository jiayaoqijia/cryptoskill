# Providers

The minimum checkout contract is a local repository, `git`, Node.js, a shell, and local file reads. Detect `gh`, a GitHub MCP, and specialist skills at runtime.

## Provider order

1. **`gh` for a peer pull request.** Authenticated `gh` is the default when the user gives a pull request URL or number.
2. **GitHub MCP as an equivalent adapter.** Use it when `gh` cannot authenticate and one installed GitHub MCP tool returns every required peer field: repository, number, URL, title, body, base SHA, head SHA, diff, checks, and existing review comments. Record the tool name. A partial MCP response does not replace `gh`.
3. **`local-git`.** Use the checkout diff for self-review. For a peer review, use it only when the exact pull request diff is already in the checkout and GitHub data could not be read. That run is `DEGRADED`.

A `github.com` or `raw.githubusercontent.com` page is outside this order, including blob, pull, commit, and files views. Read peer data through the collector or the GitHub MCP adapter above. Read a cited file through `read-frozen-file.mjs`, `read-frozen-json.mjs`, or `search-frozen-tree.mjs`. A failed read stays `failed` or `BLOCKED`.

## Freeze the target

Resolve the SHAs, capture this block, and store it once as the report's first section. Freeze it before opening a specialist skill or writing a finding. The default display shows this block when the user asks for the frozen state. A review started with `non-interactive` prints this block first:

```text
review-pr target
repository: <owner>/<name>
provider: gh | github-mcp | local-git
base: <40-char SHA>
head: <40-char SHA>
workingTree: included | excluded
```

Copy the SHAs from command output. A symbolic ref such as `HEAD` or `main` is not a frozen SHA.

## Self-review operation

Resolve the script relative to this skill's root and choose whether the requested scope includes the working tree:

```bash
node <skill-root>/scripts/collect-self-review-context.mjs <included-or-excluded>
```

`workingTree: included` when the user asks to review the current changes. The reviewed diff is the branch diff plus staged and unstaged diffs. `workingTree: excluded` when the user asks to review the branch commits only.

The script resolves `origin/main` first and `main` second, then emits the resolved base ref and frozen SHA. A failed resolution classifies the local diff source as `failed`.

## Peer-review commands

Resolve `scripts/collect-pr-context.mjs` relative to this skill's root, then run the checked-in collector:

```bash
node <skill-root>/scripts/collect-pr-context.mjs <number-or-url>
```

The collector runs fixed, read-only `gh pr view`, `gh pr diff`, and paginated `gh api` requests. It emits one JSON document with repository identity, pull request metadata, frozen SHAs, normalized check names and states, reviews, issue references, conversation comments, inline comments, and the exact diff. Use `baseRefOid` and `headRefOid` as the frozen SHAs. `workingTree` is `excluded` unless the user also asks to include the local working tree.

Run the named collector directly. Its checked-in implementation replaces generated `python -c`, `node -e`, shell pipelines, and temporary parser commands.

The reviewed diff is `gh pr diff` between those two SHAs: the exact diff of the pull request branch. Do not replace it with `git diff` of the current checkout, the working tree, or another local branch.

Read every cited repository file at the frozen head SHA:

```bash
node <skill-root>/scripts/read-frozen-file.mjs <head-sha> <repository-path>
```

When that SHA is not in the local object store, run the registered `ensure-pr-head` operation, then repeat the file-read operation. Keep the working tree unchanged. When the file-read operation cannot read the path at that SHA, classify that repository file as `unavailable`.

Linked issue context is `available` when either a GitHub issue or a Jira issue was read. One of them is enough. Read a GitHub issue from `closingIssuesReferences`. When that list is empty, read a Jira key cited in the pull request title or body with the installed Atlassian tool. When both lookups return nothing, classify the source as `unavailable`. When a lookup errors, classify it as `failed` and keep the fields that returned.

## Source classification

| Source | `available` | `unavailable` | `failed` |
| --- | --- | --- | --- |
| Local diff | Peer review: non-empty `gh pr diff` between the frozen pull request SHAs. Self-review: non-empty `git diff` for the requested scope | No diff for that scope | `git` or `gh pr diff` exited non-zero, or the base SHA did not resolve |
| Repository files | Cited file was read with `git show <head-sha>:<path>` | File cannot be read at the frozen head SHA | Read exited non-zero |
| Pull request title and body | `gh` or the equivalent MCP returned both | Self-review has no pull request | Command or tool error |
| Linked issue context | A GitHub issue body or a Jira issue body was read | Neither a GitHub issue nor a Jira issue was returned | Lookup error |
| Checks | `statusCheckRollup` or the MCP equivalent was returned | Self-review, or the payload listed no checks | Command or tool error |
| Existing review comments | Review and inline comment payloads were returned | Payloads were empty | Command or tool error |

A peer review with an exact diff and any optional source `unavailable` or `failed` is `DEGRADED`. A missing repository identity, missing SHA, or empty diff is `BLOCKED`.
