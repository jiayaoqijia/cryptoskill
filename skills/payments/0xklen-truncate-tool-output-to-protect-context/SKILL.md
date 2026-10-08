---
name: truncate-tool-output-to-protect-context
description: Use when a tool can return more than you can afford to read. Bound its output to a head/tail window plus a count before it enters context, and fetch the rest on demand.
---

# Truncate tool output to protect context

One unbounded tool result can evict the working set you spent the run building. Cap every result at the boundary, keep the useful head and tail, and pull the middle only if you actually need it.

## Procedure

1. Decide a per-tool cap before calling: search results ~50 lines, file reads ~2000, command output ~200 lines.
2. Wrap the call so the cap is structural, not hopeful: `cmd 2>&1 | head -200`, `search_files(limit=50)`, `read_file(limit=2000)`.
3. Preserve both ends. Errors surface at the tail and signatures at the head — keep `head -100` and `tail -50`, not just one.
4. Always print the true total so you know what was hidden: append `... 8,241 of 30,000 lines; full output at /tmp/out.txt`.
5. Spill the full result to a file and hand back only the path plus the window, so the middle stays retrievable without re-running the tool.
6. For JSON, reduce before reading: `jq '.[0:20] | length, .[]'`, and carry counts alongside samples.
7. When you must read the middle, fetch it by line range in a second call rather than uncapping the first.
8. Track cumulative context: if three results each hit their cap, summarise to the essentials before the next call.
9. For log-like output, cap by matches rather than lines: `grep -m 50 pattern`, so the cap follows the useful signal.
10. Record the cap and the true size in the log next to the call, so a truncated result is never mistaken for the whole.

## Pitfalls

- Running `ls -laR` or `find /` uncapped and flooding the window with names you will never use.
- Truncating with `head` only and losing the error that was printed last.
- Dropping the total count, so "showing all results" hides that 95% were cut.
- Re-running the expensive tool to see the hidden middle instead of reading the spilled file.
- Capping so low that the result becomes ambiguous — a head of 3 lines that could be a success or a failure.
- Letting a subagent's full output pass through uncapped because "it is only one call".
- Capping a diff to its first lines so the hunk that matters, later in the file, is invisible.
- Truncating inside a JSON string, producing output that no parser can read.

## Verification

    mystat() { wc -lc "$1"; }; run_cmd | head -100 > /tmp/w.txt; wc -l /tmp/w.txt   # window lines bounded, total recorded

Report the cap applied, the true total returned, and the path holding the full output.
