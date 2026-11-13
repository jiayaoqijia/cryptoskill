---
name: ac-monorepo-and-build-systems
description: "Making a large repository build correctly and quickly: the dependency graph and why build correctness depends on declaring it, affected-target selection and its false-negative risk, remote caching and the inputs that must be part of the key, hermetic builds and undeclared dependencies, generated code in the graph, CI incrementalism, and the written build record. Use when asking \"monorepo\", \"build cache\", \"affected targets\", \"remote cache\", \"hermetic build\", \"bazel\", \"build graph\", \"why does it build locally but not in CI\", \"incremental CI\", \"codegen in the build\". Not for branching models and commit conventions (ac-git-workflow), for CI pipeline wiring and deployment (ac-ci-and-release), or for dependency upgrade policy (ac-codebase-maintenance)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Monorepo and build systems

## Overview

A build system is a correctness tool that happens to be a speed tool. Its job is to know, for each output, which inputs produced it, so that a rebuild happens exactly when those inputs change and not otherwise. When that knowledge is wrong in one direction the build is slow; when it is wrong in the other direction the build is wrong, and a stale artifact ships.

Most of this skill follows from that single property. Declaring dependencies precisely is what makes incremental builds safe; caching is only sound if the cache key covers every input; hermeticity is the discipline that keeps undeclared inputs from sneaking in; and affected-target selection is a bet that the graph is complete. Branching and pipeline wiring belong to other skills.

Primary sources: <https://bazel.build/> and <https://www.cncf.io/>.

## When to use

- When a repository's build time has become a constraint.
- When builds succeed locally and fail in CI, or the reverse.
- When introducing or auditing a remote cache.
- When affected-target selection is deciding what CI runs.

## When NOT to use

- For branching models and commit conventions (use ac-git-workflow).
- For pipeline wiring, deployment, and release cuts (use ac-ci-and-release).
- For dependency upgrade and licence policy (use ac-codebase-maintenance).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/dependency-graph.md` | `software-engineering/dependency-graph` | Declared inputs, and why an undeclared one breaks correctness. |
| `subskills/affected-target-selection.md` | `software-engineering/affected-target-selection` | Running only what changed, and the false negatives it risks. |
| `subskills/remote-cache-keys.md` | `software-engineering/remote-cache-keys` | What must be in the key for a cache hit to be safe. |
| `subskills/hermetic-builds.md` | `software-engineering/hermetic-builds` | Undeclared dependencies, environment leakage, and reproducibility. |
| `subskills/generated-code-in-graph.md` | `software-engineering/generated-code-in-graph` | Codegen as a graph node, and the stale-output traps. |
| `subskills/incremental-ci.md` | `software-engineering/incremental-ci` | Making CI consume the graph rather than run everything. |
| `subskills/build-record.md` | `software-engineering/build-record` | The written record: graph health, cache hit rate, and known gaps. |

## Status and honest limits

Build systems differ enormously in how much they enforce: some require declared dependencies, others permit implicit ones and diagnose them weakly. A technique that is safe in an enforcing system is unsafe in a permissive one, and the record should say which regime applies. Nothing here promises a fast build, and a cache miss rate that is high for legitimate reasons is not a problem to be fixed by loosening the key.
