---
name: update
description: "Check for and apply updates to the ChainGPT skill. Use when: update chaingpt, update skill, check for updates, latest version, outdated docs, new api features."
disable-model-invocation: true
---

# ChainGPT Skill Update Manager

When the user invokes this skill, follow these steps in order:

## Step 1: Check the Prepared Local Checkout

Use the prepared local checkout described in the root README. Do not update a marketplace cache or replace files in a running plugin session. Have the user stop that session before applying changes, or prepare a separate checkout for the next session.

From the checkout root, read the installed version and check for local changes:

```
cat VERSION
git status --short
```

Report the current version. If there are local changes, stop the update and let the user preserve them; do not stash, reset, overwrite, or merge them automatically.

## Step 2: Check for Updates

Verify that `origin` is the intended ChainGPT repository. Fetch updates without applying them, then record the full commit SHA from the fetched `origin/main`:

```bash
git -c core.hooksPath=/dev/null fetch origin main
CHAINGPT_REVIEWED_COMMIT="$(git rev-parse --verify origin/main)"
printf '%s\n' "$CHAINGPT_REVIEWED_COMMIT"
git log --oneline "HEAD..$CHAINGPT_REVIEWED_COMMIT"
git diff --stat HEAD "$CHAINGPT_REVIEWED_COMMIT"
```

Retain that exact SHA throughout review and application. If a later command runs in a fresh shell, set `CHAINGPT_REVIEWED_COMMIT` to the recorded literal SHA, never to a freshly resolved remote ref.

- If `HEAD` equals the recorded SHA, report that no update is available.
- If the histories diverge or the local checkout is ahead, stop and report the difference. Do not reset or create a merge commit.
- Otherwise, proceed to review the fetched commit before changing the checkout or installing dependencies.

## Step 3: Review the Exact Update

Inspect the full diff against the recorded SHA. Pay particular attention to dependency manifests and lockfiles, `mcp-server/dist/`, the launcher, hooks, `.mcp.json`, plugin metadata, scripts and skills:

```bash
git diff HEAD "$CHAINGPT_REVIEWED_COMMIT"
```

Check the candidate revision's security and build results. Do not execute downloaded hooks, build scripts or dependency lifecycle scripts during review. Explain material changes and unresolved findings before asking to apply the exact recorded SHA. Categorize changes where useful:

- **New Endpoints** — Any new API routes or SDK methods added
- **SDK Updates** — Version bumps, new packages, breaking changes
- **New Patterns** — Additional smart contract templates or scaffolding
- **Bug Fixes** — Corrections to docs, examples, or the MCP server
- **Other** — Anything that doesn't fit the above

Include the full SHA in the approval request. If the remote advances afterward, apply only the approved SHA; review any newer commit separately.

## Step 4: Apply Update

After the user approves the recorded SHA and the plugin session is stopped, recheck that the checkout has no local changes and fast-forward to that exact commit:

```bash
git status --short
git -c core.hooksPath=/dev/null merge --ff-only "$CHAINGPT_REVIEWED_COMMIT"
git rev-parse HEAD
```

If the status is not clean or fast-forward fails, stop; do not force it. Verify that `HEAD` equals the approved SHA, then read `VERSION` and report the applied revision. Do not use `git pull` to resolve a potentially changed remote after review.

## Step 5: Post-Update

With API keys and wallet secrets unset, prepare the reviewed lockfile's production dependencies from the checkout root:

```bash
npm ci --prefix mcp-server --omit=dev --ignore-scripts
```

Do not reuse dependency caches from an untrusted installation. If lockfile installation fails, stop and report it; do not fall back to `npm install`, remove the lockfile, or enable lifecycle scripts.

The reviewed `mcp-server/dist/` is included, so normal plugin use does not require a build. If the user explicitly needs a local rebuild, install the locked development dependencies with `npm ci --prefix mcp-server --ignore-scripts`, then run the reviewed `npm run build --prefix mcp-server` command.

After preparation succeeds, start a new Claude Code session using `claude --plugin-dir "$PWD"` from this checkout. Runtime startup does not install dependencies.

---

## SDK Version Compatibility

| Product | NPM Package | Minimum Version | Docs Updated For |
|---------|-------------|----------------|-----------------|
| Web3 AI Chatbot | @chaingpt/generalchat | 1.0.0 | Latest |
| AI NFT Generator | @chaingpt/nft | 1.0.0 | Latest |
| Smart Contract Generator | @chaingpt/smartcontractgenerator | 1.0.0 | Latest |
| Smart Contract Auditor | @chaingpt/smartcontractauditor | 1.0.0 | Latest |
| AI Crypto News | @chaingpt/ainews | 1.0.0 | Latest |
| Python SDK | chaingpt | 1.1.3 | Latest |

## API Changelog

When a developer asks about recent API changes or reports an SDK method that does not match the skill's reference files:

1. Check https://docs.chaingpt.org for the latest API documentation.
2. Compare the live docs against the reference files bundled in this skill (under `reference/`).
3. If there is a discrepancy — a new parameter, a renamed method, a deprecated endpoint — inform the user of the difference.
4. Suggest the user run `/chaingpt-update` to pull the latest skill files that may include the fix.
5. If the skill is already up to date but the discrepancy persists, note it as a potential gap and recommend the user open an issue at https://github.com/ChainGPT-org/chaingpt-claude-skill/issues.
