---
name: ac-skill-adoption
description: "Third-party skill adoption and consumer governance for agent packs: discovering registries, judging trust signals, security vetting against prompt injection, verifying provenance and open-source licenses, staged install gating, build-versus-adopt trade-offs, and managing post-install lifecycles. Use when asking 'find skills for this task', 'should I install this skill', 'vet a third-party skill', 'is this skill safe', 'explore skill registries', 'adopt vs build skill', 'check skill license', 'audit adopted skill'. Not for: authoring your own skills from scratch (use ac-subskills-author), publishing your own releases (use ac-release-publish), or auditing internal system security (use ac-security-engineer)."
license: MIT
metadata:
  domain: skill-authoring
---

# Skill Adoption and Consumer Governance

## Overview

Adopting third-party agent skills is a supply-chain operation, not a casual download. While authoring skills focuses on creating new prompt instructions, skill adoption governs the consumer side: discovering registries, evaluating maintainer trust signals, inspecting raw instruction text for prompt-injection payloads, verifying copyright and license terms, gating installations through sandboxed verification checks, deciding whether adoption beats building from scratch, and maintaining adopted dependencies across updates.

The consumer of third-party skills faces unique risks: markdown instructions can carry hidden instruction-injection directives, popular listings often conflate download volume with safety, and unvetted repositories can introduce unmonitored network egress or private data access into agent workflows. This skill establishes rigorous operational gates to ensure every adopted component is discoverable, secure, legally compliant, and actively maintained.

## When to use

Use this skill when searching public or curated agent skill registries, evaluating whether a third-party skill is safe to adopt, inspecting downloaded skill instructions for security flaws, verifying software licenses and provenance, configuring staged installation gates, deciding between building bespoke prompts or integrating external packages, or managing the post-install maintenance lifecycle of adopted dependencies.

## When NOT to use

Do not use this skill when authoring new agent skills from scratch (use ac-subskills-author), publishing or syncing public releases of your own packages (use ac-release-publish), writing production application code, or conducting security vulnerability penetration testing against infrastructure systems (use ac-security-engineer).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/landscape-and-registries.md` | skill-authoring/landscape-and-registries | Mapping third-party skill registries, curated audits versus open listings, and search discipline |
| `subskills/trust-signals.md` | skill-authoring/trust-signals | Judging skill trustworthiness via maintenance recency, issue hygiene, and security scan verdicts |
| `subskills/security-vetting.md` | skill-authoring/security-vetting | Pre-install source inspection for prompt injection, dangerous tool bindings, and egress risks |
| `subskills/provenance-and-license.md` | skill-authoring/provenance-and-license | Authenticating author lineage, fork status, SPDX license compatibility, and copyright terms |
| `subskills/install-gating.md` | skill-authoring/install-gating | Staged sandboxed installation, fail-closed gate checks, cryptographic hash verification, and rollback |
| `subskills/build-vs-adopt.md` | skill-authoring/build-vs-adopt | Total cost of adoption versus custom authoring, fork decisions, and dependency minimization |
| `subskills/post-install-lifecycle.md` | skill-authoring/post-install-lifecycle | Upstream drift detection, scheduled security audits, package pruning, and workspace hygiene |

## Status and Honest Limits

Status: seedling. 

Limitations: Automated security scanners and static instruction analysis cannot detect zero-day prompt injection payloads disguised as subtle natural language instructions. Legal provenance checks rely on declared SPDX metadata and cannot independently verify maintainer identity falsification without external cryptographic attestation. Regular manual audits remain mandatory for all adopted third-party agent packages.
