# Operator Workflows

Use this reference when the agent's goal is to get a node running or keep one running, not just to answer repo questions.

## Primary Goals

- Bootstrap a new Ubuntu/Debian host for node use
- Resume an interrupted install after the reboot boundary
- Start, stop, restart, inspect, update, or safely clean an installed node
- Explain what is blocking readiness in machine-readable terms

## Choose The Workflow

### 1. Fresh Host Bootstrap

Use this for a blank host that has not run `run_1.sh` yet.

1. Confirm the host is intended for repo-managed node setup.
2. Confirm the human accepts root access, SSH hardening, and the reboot boundary.
3. Start with `./scripts/eth2qs.sh plan --json` so the agent can explain the next safe action before changing the host.
4. Run `./scripts/eth2qs.sh bootstrap --non-interactive` for the one-line installer if the host is starting from scratch.
5. Or use `./scripts/eth2qs.sh ensure --apply --confirm` if the planner reports `phase1`.
6. If working from an existing checkout, use:
   - `sudo ./scripts/eth2qs.sh phase1`
   - reboot
   - `./scripts/eth2qs.sh phase2 --execution=<client> --consensus=<client> --mev=<stack>`
7. After install, run `./scripts/eth2qs.sh doctor --json`.

### 2. Resume After Reboot

Use this when Phase 1 has already run and the host rebooted.

1. Confirm the agent is logged in as the non-root repo user.
2. Start with `./scripts/eth2qs.sh plan --json`.
3. Run `./scripts/eth2qs.sh ensure --apply --confirm`, `./scripts/eth2qs.sh phase2 ...` for Ethereum, or `./scripts/eth2qs.sh monad-install` for Monad when reproducibility matters.
4. Validate with `./scripts/eth2qs.sh doctor --json`.
5. If service status is unclear, run `./scripts/eth2qs.sh stats` and `./scripts/eth2qs.sh logs --run2 -n 200`.

### 3. Operate A Running Node

Use these commands for routine operations:

- Start services: `./scripts/eth2qs.sh start`
- Stop services: `./scripts/eth2qs.sh stop`
- Restart services: `./scripts/eth2qs.sh restart`
- Preview bounded smart repairs: `./scripts/eth2qs.sh repair`
- Apply bounded smart repairs: `./scripts/eth2qs.sh repair --apply --confirm`
- Show current status: `./scripts/eth2qs.sh stats`
- Machine-readable health: `./scripts/eth2qs.sh doctor --json`
- Structured per-service debug: `./scripts/eth2qs.sh debug --json --service cl`
- Repo/component freshness: `./scripts/eth2qs.sh update-check --json`
- Compact monitor summary: `./scripts/eth2qs.sh monitor export --json`
- Next-step planner: `./scripts/eth2qs.sh plan --json`
- Update software: `./scripts/eth2qs.sh update-all`

### 4. Recover Disk Space Safely

1. Inspect current health first: `./scripts/eth2qs.sh doctor --json`
2. Dry-run cleanup: `./scripts/eth2qs.sh clean-data --dry-run`
3. Require human confirmation before `--confirm`
4. Explain that default cleanup preserves secrets, validator keystores, wallets, and `~/secrets`
5. If the host has stale root-managed clients or datadirs outside the operator home, use `sudo ./scripts/eth2qs.sh cleanup-host --dry-run` before confirming host cleanup.

## Decision Guidance

- Prefer explicit `phase2` client flags when another agent or CI needs reproducibility.
- Prefer `monad-install` over implicit chain guessing when the target stack is Monad.
- Prefer `plan --json` before calling `ensure --apply --confirm`.
- Prefer `doctor --json` before and after any install, update, or cleanup step.
- Prefer `update-check --json` before a manual upgrade so the operator knows whether the repo or installed clients are actually stale.
- Prefer `repair` over `restart --smart` when you want to see exactly which allowlisted actions are eligible before changing the host.
- Prefer `debug --json` when a machine or wrapper needs recent logs, unit metadata, or socket hints for a specific service.
- Prefer `monitor export --json` when you need a compact summary for bots, dashboards, or periodic checks.
- Prefer `stats` and `logs` when a human needs a readable RCA. `stats` must stay read-only and must not trigger client downloads.
- If the requested action falls outside repo-supported workflows, say so instead of improvising.

## Not Covered

- Validator key generation
- Secret management outside the repo's existing flows
- Arbitrary non-repo node deployments
