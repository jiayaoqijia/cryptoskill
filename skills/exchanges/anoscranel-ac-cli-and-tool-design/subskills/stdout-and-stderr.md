---
name: stdout-and-stderr
domain: software-engineering/stdout-and-stderr
trigger: "Deciding which stream an output belongs on."
anti_trigger: "Not for logging design, and not for API response design."
scope: "Data on one stream, everything else on the other."
status: seedling
---

# Stdout and stderr

## Standard

Standard output is for data and standard error is for everything else: progress, warnings, prompts, and diagnostics. The separation is what makes a tool composable, because a downstream program reads stdout and a human reads stderr, and a tool that writes progress to stdout corrupts the data it was supposed to produce.

The rule survives into every output format. If a tool emits JSON on stdout, the JSON must be the only thing on stdout — not a progress bar, not a summary line, not a colour code. When a human is watching, the progress belongs on stderr where it is still visible and does not enter the pipe.

Primary sources: <https://pubs.opengroup.org/> and <https://clig.dev/>.

## Decision rules

- Record what the tool writes to stdout and confirm it is only data.
- Record what goes to stderr: progress, warnings, prompts, and diagnostics.
- Record whether the data format is stable enough to be parsed, and its schema.
- Record colour behaviour, which must be disabled when the stream is not a terminal.
- Record the behaviour when stdout is closed, as in a pipeline that exits early.
- Record whether a summary is written at all, and to which stream.

## Procedure

1. Classify every output the tool produces as data or diagnostic.
2. Route data to stdout and everything else to stderr.
3. Record the data format and its stability.
4. Disable colour when the stream is not a terminal.
5. Handle a closed stdout without a crash.
6. Verify with a pipe into a parser.

## Anti-patterns

- Writing a progress bar to stdout.
- Emitting colour codes into a pipe.
- Mixing a human summary into the JSON output.
- Crashing when the downstream program exits early.
- Formatting data for humans and calling it machine-readable.

## Done checklist

- [ ] stdout content classified as data only.
- [ ] stderr content recorded.
- [ ] Data format and stability recorded.
- [ ] Colour rule recorded.
- [ ] Closed-stdout behaviour handled.
- [ ] Piped verification performed.

The early-exit case is worth testing explicitly: a downstream command that closes the pipe after a few lines sends the writer a broken-pipe error, and a tool that treats it as a fatal failure will report an error for a completely normal pipeline. Handling it as a normal termination is what makes head work.


## Sources

- POSIX standard streams: <https://pubs.opengroup.org/>
- CLI design guidance: <https://clig.dev/>
- Shell pipeline reference: <https://www.gnu.org/software/bash/>
