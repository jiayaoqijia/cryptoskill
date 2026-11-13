---
name: ac-ci-and-release
description: "CI pipelines, deployment, release: pipeline-as-code and required checks, canary and blue-green deploys, feature flags, SemVer release cuts and launch checklists, IaC and environment parity. Use when asking \"set up CI\", \"add a GitHub Actions workflow\", \"which checks should be required\", \"speed up the pipeline\", \"deploy safely\", \"set up a canary\", \"roll back the release\", \"put it behind a flag\", \"cut a release\", \"launch checklist\", \"containerize this\", \"write the Terraform\". Not for choosing which tests to run, triaging a red pipeline, branch policy, or incident response; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# CI and Release

## Overview

Five leaves run from merge to production: the pipeline's gates and caching, live-environment wiring (IaC, containers, config), progressive deployment, feature flags, and the version cut with its launch checklist. Pipeline builds the artifact; environments-config runs it; deployment, flags and release-launch govern how it reaches users.

## When to use

- Setting up or speeding up CI; choosing required checks; pinning actions.
- Writing IaC or containers; moving config out of code; environment parity.
- Deploy safely: canary, blue-green, rollback drills.
- Adding a flag, a kill switch, or a staged rollout by percentage.
- Cutting a SemVer release; a launch checklist; mobile-store rollout.

## When not to use

- Choosing the test portfolio or fixing test design — outside this skill.
- Triaging why the pipeline is red — outside this skill.
- Branching models, merge queues, branch protection — outside this skill.
- Running an outage — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/ci-pipeline.md` | Pipeline gates and caching | "set up CI" |
| `subskills/environments-config.md` | IaC, containers, config parity | "containerize this" |
| `subskills/deployment.md` | Canary, blue-green, rollback | "deploy safely" |
| `subskills/feature-flags.md` | Decouple deploy from release | "put it behind a flag" |
| `subskills/release-launch.md` | Version cut, launch checklist | "cut a release" |

## See also

- `subskills/ci-pipeline.md` — the gates a commit must pass.
- `subskills/environments-config.md` — the host it lands on.
- `subskills/deployment.md` — the rollout mechanics.
- `subskills/feature-flags.md` — the exposure switch.
- `subskills/release-launch.md` — the version line itself.
