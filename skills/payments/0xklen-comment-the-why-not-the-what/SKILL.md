---
name: comment-the-why-not-the-what
description: Use when adding or reviewing code comments that must survive refactors. Keeps comments on intent, constraints, and non-obvious reasons, and deletes ones the code already says.
---

# Comment the Why, Not the What

A comment that restates the code goes stale the moment the code changes. A comment that records a reason outlives refactors because the reason does not change with syntax.

## Procedure

1. Before writing a comment, ask whether it says something the code cannot. If not, do not write it.
2. Delete comments that narrate mechanics, such as `i++ // increment i`. They add noise and rot.
3. Comment the constraint: `// retry capped at 3; the vendor bans a 4th within 60s`.
4. Comment the surprise: `// intentionally no lock here; the caller already holds it`.
5. Record a workaround with its cause and a link: `// freebsd needs the double-read; see issue #88`.
6. Attach a TODO to an owner or issue, never a bare one: `// TODO(#1423): drop when the v1 API is removed`.
7. Prefer a docstring for a public function's contract (params, errors) over scattered inline notes.
8. Keep comments adjacent to the line they explain; a comment three lines away confuses.
9. In review, flag a comment whose subject moved or changed; re-check it, do not trust it.
10. When code changes, update or delete its comment in the same commit; a wrong comment is worse than none.
11. Keep the one non-obvious why per block; several why comments in one function often signal it should be split.
12. Use `#` vs `//` consistently with the language and the file's existing style.

## Pitfalls

- A comment describing what the code used to do, left behind after a refactor.
- Docstring params that no longer match the signature, misinforming every caller.
- Commenting the obvious while leaving the genuinely surprising line uncommented.
- Explaining in prose a rule that should be a named constant or an assertion instead.
- A wall of commented-out code with no date or reason, kept just in case.
- A comment quoting a magic number's value instead of saying where the value comes from.
- A TODO with a name but no issue, which no process ever surfaces.

## Verification

    grep -rnE '//|#|/\*' src/ | wc -l
    grep -rniE '(increment|loop over|assign|set the)' src/

The second command should return few or none. Read each remaining comment and confirm it states a reason, constraint, or contract the code does not already express.
