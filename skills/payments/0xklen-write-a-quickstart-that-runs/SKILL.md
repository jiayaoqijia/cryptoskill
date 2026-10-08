---
name: write-a-quickstart-that-runs
description: Use when a product needs a five-minute first-run experience a newcomer can finish. Times the path end to end and removes every step that is not on it.
---

# Write a Quickstart That Runs

The quickstart is the product's first impression; it succeeds only if a newcomer reaches a visible result in under ten minutes. Cut every step that is not on that path.

## Procedure

1. State the outcome and the time budget up front: "In five minutes you will have a running instance serving http://localhost:8080."
2. Start from the most common starting point (a fresh shell, an empty dir), not an assumed preconfigured machine.
3. Number the steps and make each a single fenced command with no prose in between beyond one line of what it does.
4. Pin versions in every install command so the quickstart does not drift: `docker run acme/server:1.4.2`.
5. Provide the credentials or seed data the step needs inline; a quickstart that says "ask an admin" is not a quickstart.
6. Show the success signal explicitly: a URL to open, a log line, or a curl with its expected output.
7. End with a "what next" with two links: the reference and one task the reader likely wants.
8. Time it: run the whole thing on a clean machine and clock it; if it exceeds ten minutes, cut steps until it fits.
9. Test on the slowest supported path (fresh Docker pull, no cached layers) to catch time hidden by local caches.
10. Keep it under one screen where possible; collapse prerequisites into a note.
11. Add a one-line troubleshoot for the single most common failure (port already in use).

## Pitfalls

- Requiring a build from source with a 15-minute toolchain compile as step one.
- "Then configure your environment" with no command, stranding the reader at step three.
- A quickstart that works only on the author's macOS, not on the CI's Linux.
- Dependencies pulled from `latest`, so the quickstart breaks on someone else's release day.
- No visible success state, so the reader cannot tell whether it worked.
- Hiding a required signup or API key several steps in, breaking the promise of five minutes.
- A port that collides with the reader's existing services, with no note to change it.

## Verification

    time bash -c 'set -e; docker pull acme/server:1.4.2; head -n 40 docs/quickstart.md'

The end-to-end walk on a clean host finishes within the stated budget and shows the success signal. Report the measured wall-clock time from a clean machine and the exact command that produced the visible result.
