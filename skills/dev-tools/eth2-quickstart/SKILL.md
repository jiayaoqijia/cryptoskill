---
name: eth2-quickstart
description: Use this skill whenever the task involves an Ethereum validator node — setting up a node, installing Geth/Besu/Nethermind/Reth or Prysm/Lighthouse/Teku/other clients, configuring MEV-Boost or Commit-Boost, checking node health, listing active validators, managing validator exits, BLS-to-execution withdrawal changes, or 0x02 compounding creation, operating services, cleaning node data, or updating clients. Routes all actions through `./scripts/eth2qs.sh` with strict safety guardrails. If in doubt about an Ethereum node task, trigger this skill.
metadata:
  openclaw:
    skillKey: eth2-quickstart
---

# Eth2 Quickstart

Use this skill for Ethereum node workflows inside an `eth2-quickstart` checkout. Publish/install it through ClawHub or `npx clawhub`, then run it from the repo so it can use the canonical wrapper commands.

## Routing

- For end-to-end node operator goals, read [operator.md](references/operator.md).
- Install/bootstrap: use `./scripts/eth2qs.sh bootstrap ...`. Read [workflow.md](references/workflow.md).
- Configure or rerun phases: use `./scripts/eth2qs.sh configure`, `phase1`, `phase2`, or `monad-install`. Read [workflow.md](references/workflow.md).
- Diagnose or inspect status: use `./scripts/eth2qs.sh doctor --json` for health gates, `./scripts/eth2qs.sh stats --json` for machine-readable triage, `./scripts/eth2qs.sh debug --json --service <name>` for structured RCA, `./scripts/eth2qs.sh update-check --json` for freshness/drift, and `./scripts/eth2qs.sh repair` for bounded repair preview/apply. Read [outputs.md](references/outputs.md).
- For validator lifecycle operations, use `./scripts/eth2qs.sh validators --json` to list active validators and `./scripts/eth2qs.sh validator-exit`, `./scripts/eth2qs.sh validator-withdrawal-changes`, `./scripts/eth2qs.sh validator-create-0x02`, or `./scripts/eth2qs.sh validator-manage` for focused exit / withdrawal-change / compounding / consolidation flows. Rehearse withdrawal changes with `./scripts/eth2qs.sh validator-withdrawal-changes --dry-run --generate --submit --yes` before touching live keys. Read [commands.md](references/commands.md) and [operator.md](references/operator.md).
- Operate services, logs, cleanup, or updates: use the mapped commands in [commands.md](references/commands.md).
- Before destructive or privilege-sensitive actions, load [safety.md](references/safety.md).
- For server recommendation or host-fit questions, read [sizing.md](references/sizing.md).
- For concrete user-task phrasing, read [examples.md](references/examples.md).
- For Claude Code / Codex native tool use, read [mcp.md](references/mcp.md).
- For durable repo-scoped improvement loops, read [improvement.md](references/improvement.md).

## Rules

- Do not invent new command entrypoints when an existing wrapper command fits.
- Prefer `./scripts/eth2qs.sh` over calling utility scripts directly.
- Do not generate validator keys.
- Do not remove secrets.
- Require human confirmation before destructive cleanup, host-wide changes, or steps that require reboot/root.
- Treat `doctor --json` as the canonical health gate, `stats --json` as the canonical machine-readable triage surface, and `monitor export --json` as the canonical compact alert/dashboard surface.
- Treat `validators --json` as the canonical read-only validator inventory surface; use it to inspect local validator index/status/balance before taking exit, withdrawal-change, or compounding actions. The JSON output also carries inventory freshness metadata and beacon query status.

## References

- [workflow.md](references/workflow.md): choose bootstrap vs configure vs phase workflows
- [operator.md](references/operator.md): operator-focused install, resume, run, update, and cleanup flows
- [commands.md](references/commands.md): canonical command mapping
- [safety.md](references/safety.md): destructive boundaries and secrets policy
- [sizing.md](references/sizing.md): server sizing and host-fit guidance
- [outputs.md](references/outputs.md): expected outputs and checks for agents
- [examples.md](references/examples.md): concrete prompt/task examples for common operator goals
- [mcp.md](references/mcp.md): Claude Code / Codex MCP server usage and safety contract
- [improvement.md](references/improvement.md): how to turn failures and test output into durable repo learnings
