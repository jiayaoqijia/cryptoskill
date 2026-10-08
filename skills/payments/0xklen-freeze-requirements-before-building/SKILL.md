---
name: freeze-requirements-before-building
description: Use when starting a build whose scope could drift mid-task. Snapshot the accepted requirements to a hash-stamped file and make every later change a visible, numbered delta.
---

# Freeze requirements before building

Moving requirements make "done" unfalsifiable. This skill pins the accepted scope to a content hash so additions show up as measurable deltas instead of being absorbed silently.

## Procedure

1. Enumerate the requirements as numbered acceptance criteria, one testable claim each: `R3: GET /health returns 200 within 50ms at p99`.

2. Write them to `REQUIREMENTS.md`, one criterion per line, no prose paragraphs.

3. Hash the frozen version: `shasum -a 256 REQUIREMENTS.md > REQUIREMENTS.sha256`. Record the first eight characters of the hash in your next message.

4. Confirm the scope with the user before writing any code, stating the criterion count: "12 criteria frozen at a1b2c3d4".

5. When a new request arrives mid-task, append a new numbered row (`R13`) and recompute the hash. Never rewrite an existing criterion in place; supersede it with a new number and a note.

6. Keep a one-line reason beside each appended row so the delta has a provenance.

7. Before declaring done, run `shasum -a 256 REQUIREMENTS.md` and compare to the stored hash. Any drift must map to a numbered append you can name.

8. For each criterion, run its verifying command and paste the output line; a criterion with no command is not closed.

## Pitfalls

- Criteria without a measurable threshold ("fast enough") can never be marked done; rewrite them first.
- A criterion the user never saw is not accepted scope, however reasonable it sounds.
- Re-hashing after every tiny edit makes the hash meaningless; batch and annotate instead.
- Deleting a criterion to reach "done" is the worst failure; it must appear as an announced delta.
- Test flakiness can make a criterion pass once and fail next run; run it twice before closing.

## Verification

    shasum -a 256 REQUIREMENTS.md   # compare to REQUIREMENTS.sha256; drift must map to an appended R-row

Report the criterion count, the hash prefix, and each criterion's verifying command with its output.
