---
name: ac-code-generation-and-apis
description: "Generating code as a managed part of the system: codegen as a build step and its ownership, type generation from schemas and the drift it prevents, API client generation and what the generated surface promises, database query and model generation, configuration and bindings generation, reviewing generated code without rewriting it, and the written codegen record. It explains how generation is wired and kept honest; it never recommends a generator and never promises correctness from generation alone. Use when asking \"code generation\", \"codegen\", \"generated client\", \"openapi to typescript\", \"type generation\", \"scaffold\", \"protobuf types\", \"generated code drift\", \"should I edit generated files\", \"golden file\". Not for writing the code by hand (ac-code-construction), not for build graph and caching mechanics (ac-monorepo-and-build-systems), not for API contract design itself (ac-api-design)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Code generation and APIs

## Overview

Generated code is written by a program from a source of truth — a schema, a contract, a database, a configuration — and its defining property is that a human did not write it and should not edit it. The craft is not in the generation itself but in the wiring around it: what the generator reads, when it runs, what it owns, how its output is checked, and how drift between the source of truth and the artifacts is prevented or at least detected.

This skill covers that wiring. It treats codegen as a build dependency with an owner and a failure mode, covers type and client generation from API contracts, database-driven generation, and configuration bindings, and addresses the recurring question of how generated code is reviewed without being rewritten. The design of the API contract itself belongs elsewhere; this is about what the contract mechanically produces.

Primary source: <https://www.openapis.org/>.

## When to use

- When adding or changing a code generation step in a build.
- When generated types or clients drift from their source of truth.
- When deciding whether to edit, wrap, or regenerate output.
- When reviewing a change that includes generated artifacts.

## When NOT to use

- For hand-written code craft (use ac-code-construction).
- For build graph and caching mechanics (use ac-monorepo-and-build-systems).
- For the design of the API contract (use ac-api-design).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/codegen-as-build-step.md` | `software-engineering/codegen-as-build-step` | Inputs, outputs, freshness, and who owns the step. |
| `subskills/type-generation.md` | `software-engineering/type-generation` | Deriving types from schemas and detecting drift. |
| `subskills/client-generation.md` | `software-engineering/client-generation` | Generated API clients and what their surface promises. |
| `subskills/database-model-generation.md` | `software-engineering/database-model-generation` | Generating query and model layers from the database. |
| `subskills/config-bindings-generation.md` | `software-engineering/config-bindings-generation` | Typed configuration from schema to binding. |
| `subskills/reviewing-generated-code.md` | `software-engineering/reviewing-generated-code` | Reviewing output without owning it by hand. |
| `subskills/codegen-record.md` | `software-engineering/codegen-record` | The written record of generators and their contracts. |

## Status and honest limits

Generators move faster than the systems around them, and a generated artifact that was correct when generated is only as correct as its input was current. This skill holds the wiring stable, not the tools; flag names and plugin ecosystems change. Nothing here recommends a generator, and generation guarantees shape, never behaviour — a type generated from a schema says the field exists, not that the value is right.
