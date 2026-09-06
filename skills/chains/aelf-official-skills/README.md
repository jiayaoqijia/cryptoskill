[中文](README.zh-CN.md) | English

# aelf Skills

A single discovery and bootstrap entry for the aelf skill ecosystem.

[![npm](https://img.shields.io/npm/v/@blockchain-forever/aelf-skills)](https://www.npmjs.com/package/@blockchain-forever/aelf-skills)

This repository provides:
1. Bilingual entry docs for humans and AI agents.
2. A machine-readable catalog: `skills-catalog.json`.
3. One-click bootstrap: `bootstrap.sh`.

## AI Quick Prompt (OpenClaw / Codex / Cursor / Claude Code)

```text
Repository: https://github.com/AElfProject/aelf-skills
This is a client-agnostic prompt for OpenClaw, Codex, Cursor, and Claude Code.
Read first: skills-catalog.json, docs/SKILL_ROUTING_MATRIX.md, docs/AI_E2E_SCENARIOS.md.
Then run:
1) ./bootstrap.sh --source github --dest ./downloaded-skills
2) bun run health:check -- --skills-root ./downloaded-skills
3) read `clientInstall.openclaw` / `clientInstall.ironclaw` from `skills-catalog.json`; if `installCommand` exists, execute it locally instead of treating a GitHub tree URL as the final install input
Routing rule: follow SKILL_ROUTING_MATRIX; if ambiguous, output Recommended/Alternative/Reason.
Failure rule: use Common Recovery Template in docs/AI_E2E_SCENARIOS.md.
```

## Scope

This hub focuses on **discovery, download, install, and capability indexing**.

It does **not** replace each skill repository's own client integration logic.
Client-specific setup (`OpenClaw`, `Cursor`, `Claude Desktop`, `IronClaw`, `Codex`, `Claude Code`) remains inside each skill repo.
AI agents: jump to [AI Navigation](#ai-navigation) for routing and execution guides.

## Discovery vs Activation

Treat skill distribution in two stages:
1. `discovery`: GitHub repo URL / npm package / ClawHub slug help the host find the skill.
2. `activation`: the host or agent executes the machine-readable install contract from `skills-catalog.json`.

Rules:
1. GitHub tree/repo URLs are discovery sources only. Do not treat them as the final IronClaw install artifact.
2. For IronClaw, prefer `clientInstall.ironclaw.installCommand` and expect a trusted local install step.
3. For OpenClaw, prefer `ClawHub` / managed install when `distributionSources.clawhubId` exists; otherwise use `clientInstall.openclaw.installCommand`.

## Prerequisites

- `bun >= 1.1.0` (hard requirement)
- `npm >= 10`
- `git >= 2.39`
- `tar` (GNU tar / bsdtar)

## Local Environment Setup

`workspace.json` paths use `${SKILLS_BASE}` placeholders for portability.
`workspace.json` is Codex-local workspace config; external consumers should use `skills-catalog.json` as the data source.

```bash
export SKILLS_BASE=/path/to/your/workspace
```

Example:
- `${SKILLS_BASE}/AElf/aelf-node-skill`
- `${SKILLS_BASE}/awaken/awaken-agent-skills`

## Install

```bash
npm install @blockchain-forever/aelf-skills
# or
bun add @blockchain-forever/aelf-skills
```

## Quick Start

```bash
# 1) Generate public catalog and sync README tables
bun run catalog:generate

# 2) Generate local catalog with sourcePath (for local bootstrap/health)
bun run catalog:generate:local

# 3) Run baseline gates
bun run health:check
bun run readme:check
bun run security:audit

# 4) Bootstrap selected skills
./bootstrap.sh --only aelf-node-skill --skip-install

# 5) Check hub/catalog update drift (non-blocking)
bun run update:check
```

## Bootstrap CLI

```bash
./bootstrap.sh [--catalog <path>] [--dest <dir>] [--source auto|npm|github|local] [--skip-install] [--skip-health] [--only <csv>]
```

Defaults:
1. `--source auto` (npm first, fallback to github)
2. install enabled
3. health check enabled
4. `skills-catalog.json` as catalog source

## Update Self-Check

`aelf-skills` includes built-in update reminders for `bootstrap`, `health:check`, and `catalog:generate`.
Checks are non-blocking and cache-backed (default TTL 24h).
Reminder output is throttled to once per TTL window by `lastNotifiedAt`.

Commands:
1. `bun run update:check`
2. `bun run update:check -- --force`
3. `bun run update:check:json`

Environment variables:
1. `AELF_SKILLS_UPDATE_CHECK=0|1` (default `1`)
2. `AELF_SKILLS_UPDATE_TTL_HOURS=24` (default `24`)
3. `AELF_SKILLS_UPDATE_CACHE_PATH=<path>` (default `~/.aelf-skills/update-check-cache.json`)

## Generated Catalog

`skills-catalog.json` is the stable machine interface.

Main fields per skill:
1. `id`, `displayName`
2. `npm` (`name`, `version`)
3. `repository.https`
4. `distributionSources` (`githubRepo`, `npmPackage`, optional `clawhubId`)
5. `description`, `capabilities`
6. `artifacts` (`skillMd`, `mcpServer`, `openclaw`)
7. `setupCommands` (compatibility display commands such as `claudeDesktop`, `cursor`, `openclaw`, `ironclaw`)
8. `clientSupport` (support matrix such as `claude_desktop`, `cursor`, `ironclaw`, `codex`)
9. `clientInstall` (machine-executable activation contract for `openclaw` / `ironclaw`)
10. `dependsOn` (optional, schema `1.3.0`)

Schema references:
1. `docs/schemas/workspace.schema.json`
2. `docs/schemas/skill-frontmatter.schema.json`
3. `docs/schemas/openclaw.schema.json`
4. `docs/schemas/skills-catalog.schema.json`

Schema evolution policy:
1. `patch` (`1.3.x`): wording/docs fixes, no field semantics change.
2. `minor` (`1.x.0`): backward-compatible field additions.
3. `major` (`x.0.0`): breaking changes only.

## AI Navigation

1. Catalog field semantics: [docs/CATALOG_SCHEMA.md](docs/CATALOG_SCHEMA.md) | [docs/CATALOG_SCHEMA.zh-CN.md](docs/CATALOG_SCHEMA.zh-CN.md)
2. Intent routing matrix: [docs/SKILL_ROUTING_MATRIX.md](docs/SKILL_ROUTING_MATRIX.md) | [docs/SKILL_ROUTING_MATRIX.zh-CN.md](docs/SKILL_ROUTING_MATRIX.zh-CN.md)
3. End-to-end execution scenarios (with recovery): [docs/AI_E2E_SCENARIOS.md](docs/AI_E2E_SCENARIOS.md) | [docs/AI_E2E_SCENARIOS.zh-CN.md](docs/AI_E2E_SCENARIOS.zh-CN.md)
4. Type safety baseline and rollout status: [docs/TYPE_SAFETY_MATRIX.md](docs/TYPE_SAFETY_MATRIX.md) | [docs/TYPE_SAFETY_MATRIX.zh-CN.md](docs/TYPE_SAFETY_MATRIX.zh-CN.md)

## Current Skill Snapshot

This section is auto-synced by `bun run catalog:generate`.

<!-- SKILL_TABLE_START -->
| ID | npm Package | Version | OpenClaw Tools | Description |
|---|---|---:|---:|---|
| aelf-node-skill | @blockchain-forever/aelf-node-skill | 0.1.3 | 11 | AElf node querying and contract execution skill for agents. |
| aelfscan-skill | @aelfscan/agent-skills | 0.2.2 | 61 | AelfScan explorer data retrieval and analytics skill for agents. |
| awaken-agent-skills | @awaken-finance/agent-kit | 1.2.4 | 11 | Awaken DEX trading and market data operations for agents. |
| eforest-agent-skills | @eforest-finance/agent-skills | 0.4.3 | 48 | eForest symbol and forest NFT operations for agent workflows. |
| portkey-ca-agent-skills | @portkey/ca-agent-skills | 2.3.0 | 32 | Portkey CA wallet registration/auth/guardian/transfer operations for agents. |
| portkey-eoa-agent-skills | @portkey/eoa-agent-skills | 1.2.6 | 21 | Portkey EOA wallet and asset operations for aelf agents. |
| tomorrowdao-agent-skills | @tomorrowdao/agent-skills | 0.2.0 | 44 | TomorrowDAO governance, BP, and resource operations for agents. |
<!-- SKILL_TABLE_END -->

## Health Check

If a check fails, use the [Common Recovery Template](docs/AI_E2E_SCENARIOS.md#common-recovery-template).

```bash
# Check local source repositories from workspace.json
bun run health:check

# Check downloaded skills under specific root
bun run health:check -- --skills-root ./downloaded-skills
```

## Security Boundary

1. `bootstrap` does not execute setup commands.
2. `bootstrap` only downloads, optionally installs dependencies, and runs health checks.
3. Use `bun run security:audit` to detect risky setup command patterns.

## CI Gates

CI workflow: `.github/workflows/gates.yml`

Fixture-based gate set:
1. `catalog:generate` with `testdata/workspace.ci.json`
2. `health:check` against fixture catalog
3. `readme:check`
4. `security:audit`
5. `bootstrap --only fixture-node-skill --source local --skip-install`

## Contributing

1. Contribution guide: [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md) | [CONTRIBUTING.md](CONTRIBUTING.md)
2. AI execution contract: [docs/AI_SKILL_CONTRACT.zh-CN.md](docs/AI_SKILL_CONTRACT.zh-CN.md) | [docs/AI_SKILL_CONTRACT.md](docs/AI_SKILL_CONTRACT.md)
3. AI prompt template: [docs/templates/AI_NEW_SKILL_PROMPT.zh-CN.md](docs/templates/AI_NEW_SKILL_PROMPT.zh-CN.md) | [docs/templates/AI_NEW_SKILL_PROMPT.md](docs/templates/AI_NEW_SKILL_PROMPT.md)
4. PR checklist: [docs/templates/NEW_SKILL_CHECKLIST.zh-CN.md](docs/templates/NEW_SKILL_CHECKLIST.zh-CN.md) | [docs/templates/NEW_SKILL_CHECKLIST.md](docs/templates/NEW_SKILL_CHECKLIST.md)
5. Skill markdown template: [docs/templates/SKILL_TEMPLATE.zh-CN.md](docs/templates/SKILL_TEMPLATE.zh-CN.md) | [docs/templates/SKILL_TEMPLATE.md](docs/templates/SKILL_TEMPLATE.md)
6. Golden path example: [docs/examples/EXAMPLE_NEW_SKILL_DIFF.zh-CN.md](docs/examples/EXAMPLE_NEW_SKILL_DIFF.zh-CN.md) | [docs/examples/EXAMPLE_NEW_SKILL_DIFF.md](docs/examples/EXAMPLE_NEW_SKILL_DIFF.md)
