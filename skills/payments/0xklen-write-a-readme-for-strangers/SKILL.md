---
name: write-a-readme-for-strangers
description: Use when writing documentation, a runbook, or a handoff for someone with no context. Assume zero shared memory and make every step runnable from a clean checkout.
---

# Write a README for strangers

Documentation is read by people who were not there. Any step that depends on memory the reader lacks is a step they cannot take.

## Procedure

1. Open with two sentences: what the thing is, and what it is for.

2. Give the exact setup path from nothing: `git clone <url> && cd <dir> && make setup`, tested on a clean machine.

3. List prerequisites with versions: `python3 --version`, `node -v`, `docker --version`.

4. For every command, show the expected output or exit code, so a reader can tell success from failure.

5. Define each internal term on first use; assume no jargon and no acronyms.

6. Add a short "common failures" section: the three errors a new person hits and their fixes.

7. Close with where to go next and who owns the document.

## Pitfalls

- "As described earlier" assumes memory the stranger does not have.
- Untested commands rot; run every line in the doc before publishing.
- Requiring undocumented env vars or secrets blocks the reader at step one.
- Screenshots with no alt text fail for readers who search or use a screen reader.
- A doc that explains how it works but not how to run it fails its main job.

## Verification

    grep -nE "^\s*(git|make|npm|python|docker)" README.md | wc -l   # every step copy-pasteable

Hand the doc to someone with no context; if they cannot reach a running state, it is not done.
