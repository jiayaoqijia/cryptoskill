# Personal account tidy-up — walkthrough and field notes

Case: Do/Zemiz account `rivardoad9-source` (Oct 2026). 9 repos, several private
work repos, no profile README, a dead portfolio link, and a fine-grained token that
forced per-project grants. Everything below is the order that actually worked.

## Order of operations

1. **Explain the diagnosis before acting.** The "key per project" pain = fine-grained
   token scoped to N repos. One OAuth token via `gh` (device flow) removes it.
2. **Auth**: install `gh`, device flow, write the token to `~/.hermes/.env`
   (`GITHUB_TOKEN` + `GH_TOKEN`) and the `~/.git-credentials` line. Verify with
   `gh auth status` + a real `git ls-remote` on a private repo.
3. **Inventory**: `gh repo list --json`, plus `find ~ -maxdepth 4 -name .git -type d`
   to catch local clones, stale remotes, and tokens embedded in remote URLs.
4. **Clone every repo** into a scratch dir, then scan (this doubles as a local
   backup and lets you read READMEs to write honest descriptions).
5. **Fix metadata**: description + topics per repo (`gh api PATCH .../topics`).
6. **Portfolio/profile**: profile README repo `<login>/<login>`, portfolio site
   `index.html`, Pages enabled, verify HTTP 200.
7. **Publish** the work repos only after the leak audit.
8. **Authorship rewrite** last, after every repo is in its final state.

## Findings worth remembering

- **A "dead" portfolio link is usually a repo with only a README.** The `homepage`
  field pointed at `OWNER.github.io/<project>/` while the repo had no
  `index.html` and Pages was never enabled (`gh api repos/.../pages` → 404). Fix:
  push the site, enable Pages, verify 200 + `pages.status == "built"`.
- **Backups can silently no-op.** The Obsidian vault had a remote repo that was
  EMPTY (0 commits) and the local clone had no `origin` at all, so the sync script
  exited 0 every run doing nothing (it no-ops when the remote is missing). Lesson:
  verify the REMOTE has commits (`git ls-remote` / `gh api .../commits`), never just
  "the script ran fine". Same check applies to any git-based backup cron.
- **Empty duplicate repos** (`Obsidian` vs `obsidian-vault`) and repos whose name
  doesn't match their content (`Zemiz` = a Claude-skills dump; `test` = an industry
  report) are the common junk: rename the ones with content, propose deletion for
  empty/duplicate ones.
- **Repo pinning has no documented REST/GraphQL mutation** — ask the user to pin in
  the UI (2 clicks) instead of burning calls hunting an endpoint.

## False-positive catalogue from the deep scan

| Hit | Verdict |
|---|---|
| `GOOGLE_PRIVATE_KEY="<private key block>"` in `dashboard/.env.example` (public repo, scary) | benign template — key body was 7 chars of placeholder |
| gitleaks `generic-api-key` x2 in `src/tests/failedAttemptCost.test.ts` | 44-char base58 **Solana mint** (`8RVB...`), public on-chain data |
| 87-88 char base58 in docs/prompts | transaction signatures |
| `LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo` | Meteora DLMM program ID, public |
| `sync-needpaw-9jv.vercel.app` in a Supabase URL | public app host, not a secret |

gitleaks install on this box (no pip):
`URL=$(gh api repos/gitleaks/gitleaks/releases/latest -q '.assets[]|select(.name|test("linux_x64.tar.gz$"))|.browser_download_url')`

## Profile README + profile fields

- Profile page = repo named exactly `<login>/<login>` (public) containing `README.md`.
- Profile fields need the `user` scope: `PATCH /user` with `name`, `bio`, `blog`,
  `location`, `company` — a missing scope returns **404**, not 403.
- Keep the README honest: what they build, stack, links. No invented metrics.

## Authorship rewrite specifics used here

- Identities to normalise on this account: `ubuntu@localhost.localdomain`,
  `hermes@local`, `hermes@zemiz.local`, `noreply@anthropic.com`,
  `your-email@example.com` (any name) → `Rivardo <306490977+rivardoad9-source@users.noreply.github.com>`.
  The noreply form also hides the real address in now-public repos.
- The engine repo had **9 unpushed commits and 4 dirty files**. Handling that:
  `cp` the 4 files aside → `git checkout -- .` → rewrite in place → `push --all`
  (the 9 commits ride along, rewritten) → restore the 4 files → verify with `cmp`
  and `git status --porcelain | wc -l` → `git fetch` + compare
  `git rev-list --left-right --count origin/main...HEAD` (must be `0  0`).
- Live clones needing realignment afterwards: `~/flowmetrix-ai-agent` (engine),
  `~/NewsAgent`, `~/obsidian-vault`.

## Decisions to hand back to the user (never decide alone)

Which private repos to publish, which repos to delete, and whether to rewrite
history on a live engine repo. Deliver them as a short numbered list in one message.
