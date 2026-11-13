---
name: interactive-and-noninteractive
domain: software-engineering/interactive-and-noninteractive
trigger: "Making a tool behave correctly when there is no terminal."
anti_trigger: "Not for terminal UI design, and not for accessibility."
scope: "Detecting a terminal, and behaving without one."
status: seedling
---

# Interactive and non-interactive

## Standard

A tool that prompts for confirmation is unusable in a script, and a tool that assumes a terminal is present hangs or produces corrupted output when there is none. Detecting whether each stream is a terminal is the mechanism, and the design decision is what to do when the answer is no: fail, proceed with a non-interactive default, or require an explicit flag.

The safe design makes the non-interactive path explicit. A destructive operation should refuse to proceed without a confirming flag when stdin is not a terminal, rather than assuming consent. A prompt that is skipped in non-interactive mode has silently answered the question, and the answer it chose is usually the one the operator would have given only after reading it.

Primary sources: <https://pubs.opengroup.org/> and <https://clig.dev/>.

## Decision rules

- Record which operations require confirmation and what happens without a terminal.
- Record the flag that provides confirmation explicitly, and require it in scripts.
- Record the terminal detection per stream, since stdin, stdout, and stderr can differ.
- Record the behaviour when stdin is a pipe carrying data rather than answers.
- Record the timeouts on any prompt, if prompts exist at all.
- Record the environment variable that forces a mode, for testing.

## Procedure

1. Enumerate the operations that prompt.
2. For each, define the non-interactive behaviour.
3. Require an explicit flag for destructive actions without a terminal.
4. Detect terminal status per stream rather than once.
5. Handle piped stdin distinctly from interactive stdin.
6. Test with every stream redirected.

## Anti-patterns

- Prompting for confirmation in a script and accepting the default.
- Detecting the terminal once and applying the answer to all streams.
- Reading answers from stdin that was meant to carry data.
- A destructive default in non-interactive mode.
- Hanging on a prompt that nobody can answer.

## Done checklist

- [ ] Prompting operations enumerated.
- [ ] Non-interactive behaviour defined per operation.
- [ ] Explicit confirmation flag required.
- [ ] Per-stream detection recorded.
- [ ] Piped stdin handled.
- [ ] Tested with streams redirected.

The confirmation flag is worth requiring rather than defaulting: a destructive operation that proceeds when no terminal is present has silently answered the question in the affirmative, and the operator who intended to confirm has instead confirmed by omission. Requiring the flag makes consent explicit and greppable in a script.


## Sources

- POSIX terminal conventions: <https://pubs.opengroup.org/>
- CLI design guidance: <https://clig.dev/>
- Shell behaviour reference: <https://www.gnu.org/software/bash/>
