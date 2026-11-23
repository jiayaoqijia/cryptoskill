---
name: github-account-ops
description: "Use when cleaning/publishing a whole GitHub account."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, gh-cli, Security, Secrets, Publishing, Git]
    related_skills: [github-auth, github-repo-management, obsidian-vault-sync, api-key-verification]
---

# GitHub Account Ops (account-wide, not per-repo)

Use this when the ask is about the ACCOUNT, not one repo: "handle my GitHub so I
don't grant access per project", "clean up my repos / project names", "make my
work public for my portfolio", "set up my profile", "audit for leaks".

Bundled `github-auth` / `github-repo-management` cover per-repo basics (clone,
create, releases, secrets). This skill adds what they miss: headless-safe auth,
account inventory, pre-publish leak audit, visibility flips, and authorship rewrite.

Support files:
- `scripts/repo_secret_scan.sh` — two-layer leak scan (gitleaks + custom patterns), masked output.
- `scripts/rewrite_authors.sh` — git-filter-repo authorship rewrite incl. live-clone realignment.
- `references/personal-account-tidyup.md` — full walkthrough, false-positive catalogue, profile/Pages/vault recipes.
- `references/profile-polish-recipe.md` — the content-update loop for the account's public face: profile README / portfolio `index.html` PUT-with-sha, bio PATCH, Pages build status, live-string read-back.
- `references/publishing-artifact-pack.md` — publishing a local pack (skills, templates) as a public repo: include/exclude boundary, identifier scrub, fresh-clone verification, rename-with-redirect.

## 1. Centralize auth (kill the per-project keys)

Diagnosis that explains "I had to grant a key for every project": a **fine-grained**
token only sees the repos it was scoped to. Fix = one OAuth token via `gh`, then
`credential.helper=store` for git.

```bash
gh auth login            # or the device flow in github-auth (headless-safe)
gh auth setup-git        # git credential helper -> no more per-project grants
gh auth status           # scopes should include repo, workflow (+ read:org)
```

Headless boxes (VPS/container, no dbus keyring):

```bash
export GH_TOKEN=$(grep '^GH_TOKEN=' ~/.hermes/.env | cut -d= -f2- | tr -d '\n\r')
timeout 30 gh auth status     # without GH_TOKEN this can hang forever with no output
```

Keep the token in `~/.hermes/.env` as BOTH `GITHUB_TOKEN` and `GH_TOKEN`, plus a
`~/.git-credentials` line so plain `git push` works too. Never print token values
in chat — `[REDACTED]`.

Pitfalls learned the hard way:
- Do NOT set `git config --global credential.https://github.com.helper ""` to
  "suppress prompts" — it removes the store helper and `git ls-remote` then dies
  with `could not read Username`.
- Never extract JSON fields with `sed 's/.*"login": *"\([^"]*\)".*/\1/'`: sed is
  greedy, so a pretty-printed response leaves the variable holding the whole JSON
  body and `hosts.yml` becomes invalid YAML ("failed to load config"). Parse with
  `python3 -c "import sys,json; print(json.load(sys.stdin)['login'])"`.

### Scope escalation later (`gh auth refresh`)

Extra scopes (`user` = edit profile name/bio; `delete_repo` = delete repos) need a
second device authorization. The token is REPLACED — re-sync `.env` +
`~/.git-credentials` from `~/.config/gh/hosts.yml` afterwards, or later calls keep
using the old token.

```bash
# terminal(pty=true, background=true); read the code with process(action='log')
printf '\n' | gh auth refresh -h github.com -s user,delete_repo
```

**A missing scope surfaces as 404, not 403** — `PATCH /user` → `Not Found` means
no `user` scope; gh names the scope it wants in the error text.

## 2. Inventory before touching anything

```bash
gh repo list --limit 50 --json name,visibility,description,isFork,pushedAt,primaryLanguage
gh api user -q '"name: \(.name) | bio: \(.bio) | blog: \(.blog)"'
find ~ -maxdepth 4 -name .git -type d            # local clones, remotes, tokens in URLs
```
Profile README lives in a repo named `<login>/<login>` — missing repo = no profile page.

## 3. Pre-publish leak audit (ALWAYS before making repos public)

Run `scripts/repo_secret_scan.sh` (or by hand): gitleaks over full history + all
branches, plus custom patterns for telegram bot tokens, 64-hex keys, base58 keys,
`+62` phones, and any `.env*`/`*.db` ever tracked.

Scan from INSIDE each repo. Scanning from a parent dir with `grep -r .` re-reads
every sibling repo and reports identical findings under every repo name.

Classify each hit before believing it (print length + first 4 chars, never the value):
placeholder `.env.example` / README templates; `generic-api-key` on 44-char base58
**Solana mint addresses** in tests; 87-88 char base58 = tx signatures; 43-char
program IDs = public on-chain data. These are all benign.

## 4. Publish, rename, Pages

```bash
gh repo edit OWNER/REPO --visibility public --accept-visibility-change-consequences
gh api -X PATCH repos/OWNER/REPO -f name=new-name        # rename: PATCH, there is NO /rename endpoint
gh api -X POST repos/OWNER/REPO/branches/old/rename -f new_name=main
gh api -X PATCH repos/OWNER/REPO -f default_branch=main
echo '{"source":{"branch":"main","path":"/"}}' | gh api -X POST repos/OWNER/REPO/pages --input -
```
Old URLs redirect after a rename. A just-enabled Pages site 404s for ~1 min
while building; a repo containing only a README (no `index.html`) has NO site even
if `homepage` points at one — verify `index.html` before trusting a link.

## 5. Rewriting commit authorship

Run `scripts/rewrite_authors.sh`, or follow this order:

1. Every live clone of that repo (cron engine, vault sync) must be realigned after
   the force-push: `git fetch --all && git reset --hard origin/main`.
2. Unpushed local commits: push them first, or rewrite the live clone in place so
   they get rewritten too. They ARE rewritten by filter-repo and pushed with `--all`.
3. Dirty files: `cp` them aside — filter-repo refuses dirty trees — restore after
   and verify with `cmp` + `git status --porcelain | wc -l`.
4. filter-repo REMOVES the `origin` remote: push by explicit URL (`--all`, `--tags`).
5. mailmap shorthand covers any commit name: `Rivardo <id+login@users.noreply.github.com> <old@email>`.
   Migrating to the noreply address also hides the real email in now-public repos
   while keeping commits attributed.

Always verify after: `git rev-parse HEAD` == `origin/<branch>`,
`git rev-list --left-right --count origin/main...HEAD` == `0  0`, and
`git log -1 --format='%an <%ae>'` shows the new identity.

## 6. Reporting style (this user: Do/Zemiz)

The user explicitly flags verbose output as noise ("jangan banyak noise"). For
account-wide jobs: keep each tool call's output small (`| head`, `| cut -c1-120`,
counts instead of dumps), never paste file contents or repo-context blocks into
chat, do the work silently, then send ONE summary with the list of decisions you
need. Dash-free prose (no `-` bullets). Reply in Indonesian, santai.

Confirm before irreversible steps (visibility flips, deletions) even when the user
says "gas" for the neighbouring work.
