---
name: instrument-before-reading-the-code
description: Use when you are tempted to infer behaviour from source alone. Adds a probe that prints the actual runtime values, then reads code knowing which path really ran.
---

# Instrument Before Reading the Code

Reading code tells you what *could* happen. A probe tells you what *did*. Add the print or metric first; source comprehension is far cheaper once you know which branch executed.

## Procedure

1. Name the value you actually need to see: the branch taken, the input at a function boundary, the row count, the resolved path. One value at a time.
2. Place a probe at that boundary — a `print` at the top of the suspect function, a `logger.debug` with the arguments, or a breakpoint.
3. Include identity, not just value: add the request id / process pid / thread name so interleaved lines stay attributable.
4. Run the failing case and read the probe output before opening the function body.
5. Follow the value to the next boundary and repeat: instrument, run, read. Walk the data, not the call graph.
6. For compiled or remote code, prefer non-invasive probes: `py-spy dump --pid <pid>`, `bpftrace`, or an OTEL span rather than a rebuild.
7. Once the divergent value is found, read the one function that produced it — not the whole module.
8. Remove or gate every temporary probe behind a debug flag before committing; never ship an unconditional `print`.
9. Record the probe output that proved the path, quoting it in the bug note.

## Pitfalls

- Printing the whole object instead of one scalar, drowning the signal in megabytes of output.
- Adding probes in ten places at once, so you cannot tell which line produced the interesting value.
- Probing inside a hot loop, changing timing enough to hide a race (see `debug-a-heisenbug-under-observation`).
- Leaving debug prints in the commit, leaking internal values into production logs.
- Instrumenting your own new code but not the third-party call you suspect, so the boundary stays invisible.
- Trusting a log line's wording over the value: "cache miss" logged from a branch that also fires on errors.

## Verification

    python3 -m app --debug 2>&1 | grep -n 'PROBE' | head
    # passes when a PROBE line shows the value at the boundary you named, with an id attached

    git diff --stat | grep -E 'print\(|logger\.' && echo "REMOVE PROBES" || echo "clean"
    # before commit: no unconditional debug output remains

Report to the user: the boundary, the observed value, and the single function that produced it.
