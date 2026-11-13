---
name: commits-history
domain: software-engineering/commits-history
trigger: "\"Write a commit message\", \"squash these commits\", \"rebase or merge\", \"fix my git history\", \"find which commit broke this with bisect\", \"generate the changelog\"."
anti_trigger: "Branch model, protection and CODEOWNERS (subskills/git-workflow.md); PR description; release-note prose for users (out of this tree)."
scope: "Commit messages, Conventional Commits, rebase vs merge, history repair, changelog generation"
status: "seedling"
---

# Commits and History

## Standard

- **Conventional Commits 1.0.0** (https://www.conventionalcommits.org/en/v1.0.0/): `<type>(scope)!: description`. `fix` → PATCH, `feat` → MINOR, `BREAKING CHANGE` footer or `!` → MAJOR.
- **SemVer 2.0.0** (https://semver.org) and **Keep a Changelog 1.1.0** (https://keepachangelog.com/en/1.1.0/).
- **Atomic commit**: builds and passes tests alone; one reason to exist (GitHub Blog, "Write Better Commits").
- **git bisect** binary-searches for the commit that introduced a bug. It needs atomic, small commits (https://git-scm.com/docs/git-bisect).
- Generators: semantic-release, release-please, git-cliff.
- ⚠️ The maintainability benefit of strict conventions is claimed, not measured.

## Decision rules

1. Subject: imperative mood, ≤72 characters, no trailing period. ⚠️ 50/72 is git community convention.
2. Body explains what and why, wrapped at 72. The diff shows how.
3. Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `revert`.
4. One reason per commit. Split with `git add -p`.
5. Rebase your own unpushed or unshared commits freely. Never rewrite history others have pulled.
6. Merge method on main: squash for single-purpose PRs; rebase-merge when each commit is atomic and worth keeping. Keep main linear so bisect stays reliable.
7. Squash agent exploration commits into one clean commit per logical change before merge.
8. Undo on shared branches with `git revert`, not reset.
9. Force-push to a shared branch is **human-gated**. Use `--force-with-lease`, never bare `--force`.
10. Agent-written commits carry a trailer naming the agent, e.g. `Co-authored-by:` or `Assisted-by:`. ⚠️ Trailer name is house convention. The human who merges vouches for the change.

## Procedure

1. Stage one reason: `git add -p`.
2. Write the message:
   ```text
   fix(checkout): reject expired coupons

   Expired coupons were applied because the check used local time.
   Compare in UTC against coupon.expires_at.

   Refs: REQ-014
   ```
3. Before opening a PR, clean local history: `git rebase -i origin/main`. Use `fixup`/`squash` to fold noise; `reword` to fix messages.
4. Check each commit builds: `git rebase -x "make test" origin/main`.
5. To find a regression:
   ```bash
   git bisect start <bad> <good>
   git bisect run ./scripts/repro.sh   # exit 0 good, 1 bad, 125 skip
   git bisect reset
   ```
6. To undo a merged change: `git revert <sha>`; the message states why.
7. To recover lost work: `git reflog`, then `git branch rescue <sha>`.
8. Lint messages in CI with commitlint.
9. Generate the changelog from commits with semantic-release, release-please or git-cliff. Group by type under Keep a Changelog headings.

## Anti-patterns

- "fix", "wip", "updates" as messages.
- One commit mixing refactor, feature and formatting.
- Rewriting pushed shared history.
- Hand-edited changelog that disagrees with commits.
- Squashing a PR whose commits each carried meaning.

## Done checklist

- [ ] Every commit has one reason and a Conventional Commits subject.
- [ ] Every commit builds and passes tests.
- [ ] Main history linear.
- [ ] Agent involvement recorded in a trailer.
- [ ] Changelog generated from commits.

## Sources

- <https://github.blog/developer-skills/github/write-better-commits-build-better-projects/>
- <https://github.com/talkops-ai/ci-copilot>
- https://www.conventionalcommits.org/en/v1.0.0/ · https://git-scm.com/docs/git-bisect · https://keepachangelog.com/en/1.1.0/
