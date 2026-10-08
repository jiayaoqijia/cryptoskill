---
name: detect-doc-drift-against-code
description: Use when docs may have fallen behind the code, through renamed flags, changed defaults, or moved paths. Extracts every claim and tests it against the current source.
---

# Detect Doc Drift Against Code

Docs rot silently: the flag is renamed, the default changes, the path moves, and the doc keeps describing an old reality. Compare claims to source on a schedule.

## Procedure

1. Extract every command, flag, path, and code identifier from the target docs:
   `grep -noE '(--[a-z][a-z-]+|/[a-z0-9/_.-]+)' docs/*.md | sort -u`
2. For each CLI flag, confirm it still exists: `your-tool --help | grep -w -- '--flag'`.
3. For every config key in the docs, check it against the schema or default table in the source, not against another doc.
4. For each documented default, read the code default and diff it, e.g. `grep -rn 'default' src/config.py`.
5. For each path such as `docs/foo.md` or `scripts/bar.sh`, assert the file exists: `test -e "$path" || echo "DRIFT: $path"`.
6. For each code snippet, run it if cheap, otherwise check that the called symbols still exist.
7. Record drift findings with the doc line number and the source line that contradicts it.
8. Wire the cheap checks into CI so drift fails a build rather than accumulating.
9. Re-run after every rename or default change; treat a rename as a doc-touching change.
10. Fix by editing the doc to match source, or, if the doc encoded intent, fix the code and add a test.
11. Check version-pinned claims: if the doc says "requires 3.2+", confirm the code enforces that bound.
12. Prefer generating the claim from source (help text, schema) so it cannot drift again.

## Pitfalls

- Grepping another doc as the source of truth, so drift is copied forward instead of caught.
- Checking only flag names and missing changed default values, which are just as breaking.
- A doc that describes an aspirational design never implemented, mistaken for drift.
- Versioned docs for old releases flagged as drifting when they correctly describe that old release.
- Extracting flags from comments and examples that were illustrative, not real usage.
- A generated file checked in and never regenerated, so the "source" is itself stale.
- Fixing the doc when the code was the bug, cementing the wrong behaviour.

## Verification

    grep -c 'DRIFT:' drift-report.txt
    # zero lines means every extracted flag, path, and default matched the source

Report the count of claims checked and the specific drifted lines, not a general "docs look fine".
