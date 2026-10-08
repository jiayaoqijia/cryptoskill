---
name: generate-a-changelog-from-commits
description: Use when writing release notes from git history. Parses conventional commits between two tags into a grouped, human changelog with breaking changes called out first.
---

# Generate a Changelog from Commits

A changelog written by hand drifts from history. Generate it from the commit range between two tags so it is complete, and edit only the prose.

## Procedure

1. Confirm the range: `git describe --tags --abbrev=0` gives the previous tag; the range is `prev..HEAD`.
2. Enforce conventional commits so the parser has something to read — `feat:`, `fix:`, `perf:`, `docs:`, `chore:`, `refactor:`, with `!` or a `BREAKING CHANGE:` footer for breaks.
3. Generate with a tool that understands the convention:
   `git-cliff --tag v1.5.0 --unreleased -o CHANGELOG.md`
   Or from raw log: `git log v1.4.0..HEAD --pretty=format:'%h %s' --no-merges`.
4. Group by section in this order: Breaking Changes, Features, Bug Fixes, Performance, Documentation, Internal. Drop `chore:` and pure `ci:` noise unless the release is a tooling release.
5. For each entry, prefer the PR title over the raw commit subject, and append the PR number and author: `- Add retry to uploads (#482) @lee`.
6. Call out anything the API diff flagged as breaking even if no commit said so — the changelog is where consumers look first.
7. Commit `CHANGELOG.md` before tagging so the tag contains its own notes.
8. Verify nothing between the tags is missing: `git log --oneline v1.4.0..v1.5.0 --no-merges | wc -l` versus the number of entries you emitted.

## Pitfalls

- Merge commits inflate the list; always pass `--no-merges`.
- A release with no conventional prefixes produces an empty changelog — fix commit hygiene before the release, not after.
- Renaming the tag after generating makes every link in the changelog point at a dead ref.
- Silently dropping `fix:` commits that lacked a PR number hides real user-facing fixes.
- Auto-generated text with empty sections ("## Documentation\n-") reads as noise; omit sections with no entries.

## Verification

    git-cliff --tag v1.5.0 --unreleased | head -40 && \
      test "$(git log v1.4.0..HEAD --oneline --no-merges | wc -l)" -ge "$(grep -c '^- ' CHANGELOG.md)"

Every non-`chore` commit is represented exactly once, breaking changes appear at the top, and the tag `v1.5.0` exists on the same commit as the committed changelog.

Report: "Generated CHANGELOG for v1.5.0 covering <N> commits across <M> PRs; <K> breaking changes listed first."
