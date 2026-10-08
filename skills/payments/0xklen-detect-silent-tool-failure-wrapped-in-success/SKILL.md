---
name: detect-silent-tool-failure-wrapped-in-success
description: Use when a tool reports success but the work may not have happened. Verify the effect independently instead of trusting a zero exit code or a "done" message.
---

# Detect silent tool failure wrapped in success

A tool that exits 0 has told you it ran, not that it worked. Empty results, partial writes, and swallowed errors all wear a success mask; only an independent check removes it.

## Procedure

1. Distinguish the three signals: exit code (did it run), stdout (what it claims), effect (what changed). Only the third is success.
2. After every write tool, verify by reading back: `SELECT COUNT(*)` after an insert, `ls -l` after a write, the message id after a send.
3. Treat an empty result as suspect, not as success. `grep` with no match exits 1; a tool that returns "" and 0 is hiding the difference.
4. Check for a nonzero exit hidden behind a pipe: `${PIPESTATUS[0]}`, or avoid the pipe entirely.
5. Watch stderr even on success — warnings and partial-failure notices often land there while stdout looks clean.
6. Validate the shape of the output, not just its presence: a JSON response that parses to `{"error": "..."}` is a failure wearing a 200.
7. For batch operations, confirm the count matches the input size; "completed" over 9 of 10 items is a silent loss.
8. Log the verification result next to the call so a false success is caught at the step, not days later.

```bash
set -o pipefail
psql -c "INSERT INTO t VALUES (1)" | tail -1
psql -tAc "SELECT count(*) FROM t WHERE id=1"   # must print 1, or the insert silently failed
```

## Pitfalls

- Trusting `&& echo DONE` as proof the operation changed anything.
- Reading only the last line of piped output and missing the real error above it.
- Accepting an HTTP 200 without parsing the body, where many APIs report failure in-band.
- Assuming a deleted file is gone without checking existence, when the tool silently skipped a permission error.
- Counting "processed" records from the tool's own log instead of the destination store.
- Treating a timeout-and-retry as success because the retry returned 0, while the first attempt also landed.

## Verification

    psql -tAc "SELECT count(*) FROM t WHERE id=1"   # prints the expected row count, not 0

Report the write performed, the independent read-back command, and the value it returned.
