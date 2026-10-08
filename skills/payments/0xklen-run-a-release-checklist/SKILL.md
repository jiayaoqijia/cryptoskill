---
name: run-a-release-checklist
description: Use when cutting a tagged release to production. Runs a fixed gate of tests, version, changelog, migrations, rollback and rollout steps before the tag is pushed.
---

# Run a Release Checklist

Releases fail on the step someone assumed was done. A fixed, ordered checklist makes "we forgot to bump the version" impossible to reach production.

## Procedure

1. Freeze: confirm `git status` is clean on the release branch and every PR for this version is merged. `git log --oneline origin/main..HEAD` should be empty.
2. Green builds: the full CI suite passes on the exact commit, not a two-day-old run. Check the SHA of the last green pipeline equals `git rev-parse HEAD`.
3. Version bump: apply the semver decision (see the semver skill) in the one canonical file — `package.json`, `Cargo.toml`, `pyproject.toml` — and nowhere else.
4. Changelog: regenerate from commits and commit it *before* tagging, so the tag contains its own changelog:
   `git-cliff --tag v1.4.0 -o CHANGELOG.md`
5. Migrations: list any schema or data migration, confirm they are backward-compatible with the still-running previous version, and that a backfill is idempotent.
6. Docs and SDKs: update the install snippet, the `--version` output test, and any generated client. A stale README install command is a support ticket.
7. Rollback plan: state the exact revert — previous image digest, `git revert <tag>` commit, or feature-flag kill switch — and who can trigger it.
8. Tag and push signed: `git tag -s v1.4.0 -m "v1.4.0" && git push origin v1.4.0`.
9. Roll out staged: canary 1%, then 10%, then 100%, watching error rate and latency at each hold. Publish release notes after the canary is clean.

## Pitfalls

- Tagging before the changelog commit means the tag's own CHANGELOG is stale.
- "CI was green on main" is not the same commit you are tagging; verify the SHA.
- A rollback that needs a new build is not a rollback — have the previous artifact still deployable.
- Forgetting to push tags (`git push --tags`) leaves the release invisible to consumers.
- Recording the checklist only in someone's head; keep it in the repo as `RELEASING.md`.

## Verification

    git rev-parse HEAD && git rev-parse v1.4.0^{commit} && \
      test -z "$(git log --oneline origin/main..HEAD)" && echo READY

The two SHAs are identical, the range is empty, and the pipeline status for that SHA is passing.

Report: "Tagged v1.4.0 at <sha> with matching green pipeline; changelog committed, canary at 1% for 30 min clean, rollback digest <prev> ready."
