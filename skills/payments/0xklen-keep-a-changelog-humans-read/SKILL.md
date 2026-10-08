---
name: keep-a-changelog-humans-read
description: Use when maintaining a changelog or writing release notes for a project. Writes entries for the person upgrading, grouped by change type, with breaking changes called out first.
---

# Keep a Changelog Humans Read

A changelog is read by someone deciding whether to upgrade. Every entry must answer "does this affect me" and "what do I do about it". Group by kind, never by commit.

## Procedure

1. Keep one file at the repo root, `CHANGELOG.md`, in reverse-chronological order with headings like `## [1.4.0] - 2026-03-11`.
2. Use the standard buckets under each version: Added, Changed, Deprecated, Removed, Fixed, Security as `###` headings. Omit empty buckets.
3. Write each line as a complete sentence addressed to the reader: "Removed the deprecated `--legacy` flag; pass `--mode=v1` instead."
4. Put breaking changes in their own Breaking block at the top of the version, with a one-line migration note and a link to the migration guide.
5. Reference the issue or PR number at the end of the line: `(#412)`.
6. Maintain an `## [Unreleased]` section and move its items down when you cut a tag.
7. Never paste raw `git log`; squash "wip", "typo", and merge commits. Link the compare view between tags.
8. Tag the release so the changelog date is generated, not typed: `git tag -a v1.4.0 -m "1.4.0"`.
9. For a library, follow SemVer strictly: a break in the public API bumps the major only after 1.0.0.
10. Include the upgrade command when non-trivial: `npm i acme@^1.4` or `pip install -U acme==1.4.0`.
11. Write for the reader who skips straight to the latest section; do not make earlier sections required reading to understand it.
12. Keep entries in the past tense and describe the observable behaviour change, not the internal refactor.

## Pitfalls

- Grouping entries by author or by module, which forces the reader to reassemble the impact.
- "Various bug fixes and improvements", which tells the reader nothing actionable.
- A breaking change buried under Changed with no migration note.
- Dating the release to the day you wrote the notes instead of the tag date.
- Deleting old versions; keep history so people on old pins can read forward.
- Listing internal refactors that have no user-visible effect, crowding out the ones that do.
- A Security entry so vague ("fixed an issue") that users cannot judge their exposure.

## Verification

    grep -n '^## \[' CHANGELOG.md | head
    # each line is a version/datestamp; newest is first, Unreleased present during development

Cross-check the changelog against `git log v1.3.2..v1.4.0 --oneline` and confirm every user-visible commit is represented by a sentence.
