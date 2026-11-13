---
name: ac-cli-and-tool-design
description: "Designing command-line tools that compose: exit codes and their meaning, stdout as data and stderr as progress, argument and flag conventions, idempotency and safe re-runs, interactive versus non-interactive modes, signal handling and interruption, help output that answers the question, and the written interface record. Use when asking \"CLI design\", \"exit code\", \"stderr or stdout\", \"flag conventions\", \"make it scriptable\", \"idempotent command\", \"Ctrl-C handling\", \"--json flag\", \"CLI help text\", \"tool takes a pipe\". Not for shell scripting and process supervision (ac-code-construction), not for public HTTP API contracts (ac-api-design), not for terminal UI layout and accessibility (ac-frontend-ui)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# CLI and tool design

## Overview

A command-line tool is an interface with unusually strict conventions, and the conventions exist because tools are composed by shell scripts rather than read by humans. Exit codes tell a script whether to continue; stdout carries data and stderr carries everything else; flags are parsed by a library that has already decided what a short option means. Violating those conventions produces a tool that works when typed and fails when scripted.

This skill covers the design decisions that make a tool composable: what each exit code means, how to separate data from diagnostics, how to design flags that are unsurprising, how to make a re-run safe, how to behave when there is no terminal, and how to handle interruption without leaving half-written state. Shell scripting technique and API design belong to other skills.

Primary sources: <https://pubs.opengroup.org/> and <https://www.gnu.org/software/bash/>.

## When to use

- When designing a new command-line tool or a major flag change.
- When a tool must work in a pipeline or in CI.
- When a command's re-run safety matters.
- When interruption could leave inconsistent state.

## When NOT to use

- For shell scripting idiom and process supervision (use ac-code-construction).
- For external API contract design (use ac-api-design).
- For interactive terminal layout (use ac-frontend-ui).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/exit-codes.md` | `software-engineering/exit-codes` | What each code means, and the script that consumes it. |
| `subskills/stdout-and-stderr.md` | `software-engineering/stdout-and-stderr` | Data on one stream, everything else on the other. |
| `subskills/flag-conventions.md` | `software-engineering/flag-conventions` | Long and short options, defaults, and the least surprising parse. |
| `subskills/idempotency-and-reruns.md` | `software-engineering/idempotency-and-reruns` | Making a command safe to run twice. |
| `subskills/interactive-and-noninteractive.md` | `software-engineering/interactive-and-noninteractive` | Detecting a terminal, and behaving without one. |
| `subskills/signals-and-interruption.md` | `software-engineering/signals-and-interruption` | Ctrl-C, cleanup, and not leaving half a write. |
| `subskills/cli-record.md` | `software-engineering/cli-record` | The written record: the interface contract a tool promises. |

## Status and honest limits

The conventions described here are widespread rather than universal, and platform differences are real: a tool that behaves correctly on one operating system can violate a convention on another. Nothing here overrides the specific expectations of the environment a tool ships into. A tool's interface is also a compatibility obligation, and every flag added is one that will need to keep working.
