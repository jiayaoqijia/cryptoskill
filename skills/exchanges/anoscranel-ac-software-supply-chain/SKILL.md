---
name: ac-software-supply-chain
description: "Trusting the code you did not write: lockfiles and the integrity they give, dependency risk and update discipline, vendoring versus fetching, artifact signing and provenance verification, lockfile maintenance across a fleet, and the written supply-chain record. It explains how to make third-party code a managed input; it never recommends a registry and never promises safety. Use when asking \"lockfile\", \"supply chain attack\", \"dependency confusion\", \"provenance\", \"artifact signing\", \"should I vendor\", \"pinned dependency\", \"typosquatting\", \"lockfile drift\", \"dependency update discipline\", \"security release across a fleet\", \"lockfile merge review\", \"exception log with expiry\", \"dormant repository updates\", \"where did this package come from\". Not for vulnerability management of shipped code (ac-security-engineer), not for upgrade planning within one codebase (ac-codebase-maintenance), not for secure coding practices (ac-code-construction)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Software supply chain

## Overview

Almost every application is mostly code nobody in the organisation read. That code arrives through a channel — a registry, a mirror, a vendored copy — and the channel's properties decide what the organisation actually runs: whether a version pinned today is the same bytes tomorrow, whether a package name maps to the publisher it claims, and whether an artifact can be traced back to a source tree that produced it.

This skill covers that channel as an engineering problem: lockfiles as the tool that makes dependencies reproducible, update discipline as the tool that keeps them from rotting or from surprising, vendoring as thesometimes-right alternative, integrity and provenance verification, and managing a lockfile across a fleet of repositories. The security-review of a shipped application belongs elsewhere; this is about the trustworthiness of what enters the build.

Primary source: <https://slsa.dev/>.

## When to use

- When designing or auditing how dependencies enter the build.
- When lockfile drift, stale pins, or unexplained versions need resolving.
- When deciding whether to vendor a dependency.
- When adding integrity or provenance verification to artifact handling.

## When NOT to use

- For vulnerability assessment of shipped code (use ac-security-engineer).
- For upgrade large-scale planning within the codebase (use ac-codebase-maintenance).
- For secure coding of what you write yourself (use ac-code-construction).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/lockfiles-and-integrity.md` | `software-engineering/lockfiles-and-integrity` | What a lockfile pins and what it does not. |
| `subskills/dependency-risk-and-updates.md` | `software-engineering/dependency-risk-and-updates` | Keeping dependencies current without ambush. |
| `subskills/vendoring-versus-fetching.md` | `software-engineering/vendoring-versus-fetching` | When to copy a dependency into the repository. |
| `subskills/provenance-and-signing.md` | `software-engineering/provenance-and-signing` | Verifying where an artifact came from. |
| `subskills/registry-hygiene.md` | `software-engineering/registry-hygiene` | Scopes, mirrors, and the namespace attacks. |
| `subskills/fleet-lockfile-management.md` | `software-engineering/fleet-lockfile-management` | Coordinating pins across many repositories. |
| `subskills/supply-chain-record.md` | `software-engineering/supply-chain-record` | The written record of sources and verifications. |

## Status and honest limits

Ecosystem tooling changes fast and differs by language; the mechanisms here — pin, verify, update deliberately — are stable, but the command that implements one is not, and a lockfile format today may be replaced tomorrow. Nothing here recommends a registry or a tool. Verification proves an artifact matches a claim; it does not prove the claim is good. A signed malicious dependency is signed, and the last line of defence remains not depending on things nobody examined.
