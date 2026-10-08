---
name: report-absence-of-evidence
description: Use when a search, test, or query returns nothing. State what was searched, how sensitively, and that the null result is not proof the thing does not exist.
---

# Report absence of evidence

"I found nothing" hides the gap between "it is not there" and "I did not look properly". This skill makes the scope and the sensitivity of a null result explicit so no one mistakes it for proof.

## Procedure

1. Record the exact command that found nothing: `grep -rn "api_key" src/ --include=*.py`.

2. Record the scope implied: which directories, file types, hosts, branches, and time range were actually covered.

3. Capture the negative result verbatim, including the exit code. `grep` and `rg` return 1 on no match, `find` exits 0 with empty output — the code is part of the evidence.

4. Test the search's sensitivity. Would it have matched if the thing were present? A case-sensitive `grep` misses `API_KEY`, so re-run with variants: `grep -rin "api[_-]\?key" src/`.

5. Run a positive control where possible: search for a string you know exists, to prove the tool and path work.

6. Report as "no match in <scope> using <command>", never as "there is no X".

7. Name the parts of the space you did not search — other branches, the database, the vendor's closed source — so the limit of the null is explicit.

## Pitfalls

- Searching the wrong branch or a stale checkout is the most common false negative; confirm with `git rev-parse --abbrev-ref HEAD`.
- A tool's include filter silently narrows scope; `--include=*.py` skips config files, so say so.
- Absence in logs may mean logging is off, not that the event never happened.
- Reporting a null as a clean success skips the case where the check itself is broken.
- A regex typo produces a confident empty result; the positive control is what catches it.

## Verification

    grep -rn "api_key" src/ --include=*.py; echo "exit=$?"   # exit=1 is the no-match signal

Report scope, command, and exit code; say "not found in X", never "does not exist".
