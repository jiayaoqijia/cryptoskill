---
name: write-a-migration-guide
description: Use when users must move from one major version, API, or platform to another. Structures the guide as before/after diffs with a runnable codemod, a checklist, and a rollback.
---

# Write a Migration Guide

A migration guide is read by someone with a broken build and a deadline. Lead with the mechanical changes and the tool that automates them, then the manual cases.

## Procedure

1. State the source and target versions and the time it should take: "Migrating from 2.x to 3.0 takes about 30 minutes."
2. Provide the one command that runs the automated migration first: `npx @acme/upgrade@3 --from=2`. Codemods beat prose for mechanical edits.
3. Give a before/after for each breaking change as a two-column diff inside one fenced block, so the reader sees the shape change.
4. Order changes by blast radius: things that fail the build first, then behaviour changes that fail silently, then renames.
5. For each silent behaviour change, give a manual grep to find affected call sites: `grep -rn 'old_fn(' src/`.
6. List removed APIs in a table with the replacement, or "no replacement" and the reason.
7. Add a "things that now behave differently" section, same signature and new semantics, because tests pass while production breaks.
8. Include the rollback: `npm i acme@^2.9` and the data-compat note if a schema changed.
9. Provide a checklist the reader ticks: dependencies bumped, codemod run, greps clean, tests green, canary deployed.
10. Cover the common skip-a-major path: readers going from 1.x to 3.0 need both guides, so link the intermediate one.
11. Date the guide and pin it to the target's exact version; migration guides drift fast.
12. Test the codemod on a fixture project and paste its actual output into the guide.

## Pitfalls

- Prose describing changes with no before/after, so the reader reverse-engineers the diff.
- A codemod that covers 80% and no guidance for the 20%, leaving the hard cases undocumented.
- Missing the semantic-only changes, which pass CI and fail in production.
- Telling readers to "update as needed" without the exact greps that find the need.
- A guide for 1.x to 3.0 that skips 2.x, ignoring readers two majors behind.
- Commands that assume a global CLI the reader has not installed, failing at step one.
- A rollback path that is stated but never tested against a migrated database.

## Verification

    npx @acme/upgrade@3 --from=2 --dry-run 2>&1 | tail -5
    # the codemod reports the files it would change on a fixture repo, matching the guide's examples

Run the guide end to end on a copy of a real 2.x project; report every step that needed an undocumented fix.
