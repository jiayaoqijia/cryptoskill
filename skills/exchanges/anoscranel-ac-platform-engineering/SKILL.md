---
name: ac-platform-engineering
description: "Running an internal platform as a product: the golden path and what it must shorten, service catalogue and ownership metadata, self-service provisioning and its guardrails, toil measurement and the case for automating it, on-call rotation design and escalation, developer experience metrics and their limits, and the written platform record. It explains how an internal platform earns adoption; it never prescribes a toolchain and never promises a velocity gain. Use when asking \"platform engineering\", \"golden path\", \"service catalogue\", \"developer portal\", \"self-service infrastructure\", \"toil\", \"on-call rotation\", \"developer experience metrics\", \"DORA metrics\", \"why does nobody use our platform\". Not for CI pipeline wiring (ac-ci-and-release), not for deployment strategy and rollback (ac-ci-and-release), not for SLO definition and incident response (ac-reliability)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Platform engineering

## Overview

An internal platform is a product whose users are engineers, and it succeeds or fails on adoption rather than on capability. A platform that offers ten ways to deploy and no recommended one is a toolkit; a platform that offers one path that is genuinely shorter than the alternative is a product. The distinction is the whole discipline, and it is why the golden path matters more than the catalogue around it.

This skill covers that: how a golden path is defined and measured, what a service catalogue holds beyond a list of names, how self-service provisioning gives autonomy without giving away control, how toil is measured so that automating it can be justified, how on-call is designed so that it does not destroy the team, and which developer metrics mean something and which flatter. CI mechanics and incident response belong to other skills.

Primary sources: <https://sre.google/> and <https://dora.dev/>.

## When to use

- When introducing or reviewing an internal platform.
- When adoption is low and the cause is unclear.
- When deciding what to automate next.
- When designing on-call and escalation for a team.

## When NOT to use

- For pipeline wiring, deployment strategy, and rollback (use ac-ci-and-release).
- For SLO definition and incident command (use ac-reliability).
- For cloud cost optimisation (use ac-cost-aware-engineering).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/golden-path.md` | `software-engineering/golden-path` | The recommended path, what it shortens, and how adoption is measured. |
| `subskills/service-catalogue.md` | `software-engineering/service-catalogue` | Ownership metadata, dependencies, and what the catalogue must contain to be used. |
| `subskills/self-service-and-guardrails.md` | `software-engineering/self-service-and-guardrails` | Provisioning without tickets, and the guardrails that make it safe. |
| `subskills/toil-measurement.md` | `software-engineering/toil-measurement` | Measuring repetitive work and the case for automating it. |
| `subskills/on-call-design.md` | `software-engineering/on-call-design` | Rotation, escalation, load, and the sustainability of being paged. |
| `subskills/developer-experience-metrics.md` | `software-engineering/developer-experience-metrics` | What the metrics measure, and where they mislead. |
| `subskills/platform-record.md` | `software-engineering/platform-record` | The written record: path, catalogue, guardrails, and adoption evidence. |

## Status and honest limits

Platform adoption is a social outcome, and a platform can be technically excellent and unused because the alternative was easier. Metrics such as lead time and deployment frequency describe a pipeline's behaviour, not necessarily a team's experience, and they are easy to improve without improving anything that matters. Nothing here prescribes a toolchain, and a golden path that has not been walked by someone outside the platform team has not been tested.
