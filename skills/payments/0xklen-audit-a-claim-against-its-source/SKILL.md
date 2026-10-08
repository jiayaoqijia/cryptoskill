---
name: audit-a-claim-against-its-source
description: Use when you are about to repeat, cite, or act on a claim someone else made. Trace it to the primary artefact, compare wording field by field, and record exactly what survived.
---

# Audit a claim against its source

A claim you cannot trace back to a file, log line, or record is a rumour wearing a lab coat. This skill forces every borrowed assertion back to the artefact it came from before you pass it on, and records the parts that did not survive the trip.

## Procedure

1. Write the claim as one falsifiable sentence in a scratch file, for example `claim: "the API rejects tokens older than 3600s"`.

2. Identify the earliest source you actually possess: ticket, chat message, README, commit, or command output. Run `git log -S "3600" --oneline -- src/auth/token.py` to find the commit that introduced the number.

3. Open the primary artefact itself, never a summary of it. For a code claim read the file with `read_file`; for a spec claim fetch it directly with `curl -s https://host/path | head -40`.

4. Quote the supporting lines verbatim into the scratch file under an `evidence:` heading, including file path and line numbers.

5. Diff the claim against the quote, field by field: same numeric value, same scope (all users versus admins), same units (seconds versus milliseconds), same version or date.

6. Record a verdict on one line: `VERIFIED`, `PARTIAL`, or `UNSUPPORTED`, plus the path and lines. `PARTIAL` means part of the claim holds and part does not — name both halves explicitly.

7. Check freshness before trusting an old source: `git log -1 --format=%ci src/auth/token.py`. A quote from three years ago may describe code that has since changed.

8. Only once the verdict is written do you restate the claim to the user, carrying the source path and verdict with it.

## Pitfalls

- A second summary that repeats the claim is not evidence; two copies of one error still fail the audit.
- Numbers drift through retelling: 3,600 seconds becomes "an hour" becomes "about a day" by the third hop.
- Scope narrows silently — a result measured on the test tenant is not the production rule.
- A live URL can rot; record the retrieval date so a later 404 reads as drift rather than error.
- The most authoritative-looking source is often a presentation of the real one; keep walking up the chain.

## Verification

    grep -c "evidence:" claim.txt   # must be >= 1, and every quote must name a path

Report the verdict with the source: "claim verified/partial/unsupported against <path>:<lines>", never the bare claim.
