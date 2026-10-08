---
name: onboard-into-an-unfamiliar-codebase
description: Use when dropped into an unfamiliar repo and needing to contribute fast. Finds the entry point, runs the tests, and reads one end-to-end path before touching code, using git history and the build files as the map.
---

# Onboard into an Unfamiliar Codebase

Reading files alphabetically is the slowest way in. The build files say what runs, the tests say what must hold, and one traced request path says how the pieces fit together.

## Procedure

1. Map the shape before opening source with `git ls-files | sed 's#/.*##' | sort | uniq -c | sort -rn | head`.
2. Read the entry points the build names: the `scripts` block in `package.json`, `Makefile` targets, or `pyproject.toml`.
3. Run the test suite and note the time and the pass count; that is your regression baseline, e.g. `make test 2>&1 | tail -5`.
4. Trace one request end to end, from the route or handler to the storage call; grep the handler name to follow it.
5. Ask git who last changed the file you must edit: `git log -1 --format='%an %ad %s' -- path/to/file.py`.
6. Write down three open questions and resolve each against code, not by guessing.
7. Only then open an editor; make the first change the smallest one that ships.
8. Note the slow test and the flaky test now, so you do not later blame them on your change.
9. Find the CI config so you know what a green build actually requires before you push.
10. Write a one-paragraph map of the path you traced and keep it; it is the start of your own onboarding doc.
11. List where the code writes to disk or network; that list usually equals its real responsibilities.
12. Run one existing test in the area you will edit and keep its name for your own change.
13. Capture the commit hash you started from, so you can diff your understanding later.
14. Find the config file that changes behaviour between environments and read it.
15. Locate the logging setup so you can raise verbosity when you debug.
16. Write down the one command that gives you a working dev loop.

## Pitfalls

- Starting to refactor before the suite is green, so you cannot tell your breakage from prior breakage.
- Reading the whole tree instead of one traced path.
- Trusting a README that has drifted from the build files.
- Editing without checking the last author, missing a constraint documented in the commit message.
- Assuming the directory layout matches the runtime flow; it often does not.
- Skipping the CI config and discovering a lint gate only after the push.
- Believing the docs over the build files when the two disagree.
- Chasing a rename across the whole repo instead of the one path you need.
- Assuming the failing tests are yours when they were already red before you arrived.
- Not reading env config and being surprised by a local-only default.
- Debugging without knowing how to raise the log level.
- Discovering the dev loop by accident after a day of guessing.

## Verification

    git ls-files | wc -l ; make test 2>&1 | tail -1
    # passes when you can state the test-count baseline and name the route-to-storage path in one sentence

Report to the user: the entry point, the baseline pass count, and the single traced path.
