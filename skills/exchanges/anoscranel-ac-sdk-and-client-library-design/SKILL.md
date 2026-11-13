---
name: ac-sdk-and-client-library-design
description: "Designing a client library other people will depend on: surface area and what to hide, error types that callers can act on, retry and timeout defaults that are safe to inherit, configuration precedence and credential handling, semantic versioning and the deprecation of a published method, language idiom and packaging, and the written SDK record. It explains how a client earns trust; it never recommends a language ecosystem and never promises stability. Use when asking \"SDK design\", \"client library\", \"public API surface\", \"error types\", \"default retry in SDK\", \"semantic versioning for libraries\", \"deprecating a method\", \"credential handling in SDK\", \"why do people hate our SDK\". Not for public HTTP API contracts (ac-api-design), not for package publishing logistics (ac-ci-and-release), not for client-side application architecture (ac-architecture)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# SDK and client library design

## Overview

A client library is a promise that other people's code will keep compiling and behave predictably. That promise is harder than an API contract because the library runs inside the caller's process: it consumes their threads, inherits their configuration, throws into their error handling, and upgrades on their schedule. The design decisions are therefore about what the caller is allowed to depend on.

This skill covers those decisions: how much surface to expose and what to keep private, what an error type must carry for a caller to act, which retry and timeout defaults are safe to inherit, how configuration precedence and credentials should work, and what semantic versioning commits a published library to. HTTP contract design and release logistics belong to other skills.

Primary sources: <https://semver.org/> and <https://www.rfc-editor.org/rfc/rfc9110>.

## When to use

- When publishing a client library for an API.
- When a library's changes keep breaking its users.
- When deciding what to expose publicly and what to hide.
- When handling credentials and configuration in a shared library.

## When NOT to use

- For the HTTP API contract itself (use ac-api-design).
- For publishing pipelines and release automation (use ac-ci-and-release).
- For internal application module structure (use ac-architecture).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/public-surface.md` | `software-engineering/public-surface` | What to expose, what to hide, and the cost of every public name. |
| `subskills/error-types.md` | `software-engineering/error-types` | Errors a caller can act on, and the information they must carry. |
| `subskills/defaults-and-timeouts.md` | `software-engineering/defaults-and-timeouts` | Retry and timeout defaults, and the danger of inheriting them silently. |
| `subskills/configuration-and-credentials.md` | `software-engineering/configuration-and-credentials` | Precedence, environment, and never logging a secret. |
| `subskills/versioning-and-deprecation.md` | `software-engineering/versioning-and-deprecation` | Semantic versioning, and retiring a published method. |
| `subskills/idiom-and-packaging.md` | `software-engineering/idiom-and-packaging` | Following the language's conventions rather than importing another's. |
| `subskills/sdk-record.md` | `software-engineering/sdk-record` | The written record: surface, defaults, versioning, and deprecation policy. |

## Status and honest limits

Library ecosystems differ in their tolerance for change: some treat every release as potentially breaking, others expect strict compatibility over years. A semantic version number communicates intent rather than guaranteeing behaviour, and a major version bump does not make a break acceptable if the migration is undocumented. Nothing here promises that a design will not need to change, and a library that has never deprecated anything has either no users or no discipline.
