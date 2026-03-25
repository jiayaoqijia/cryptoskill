---
name: eth2-quickstart
description: Bootstrap, operate, diagnose, and safely clean production Ethereum validator nodes through a tested command surface with strict safety guardrails.
version: 1.0.0
author: chimera-defi
tags:
  - ethereum
  - validator
  - staking
  - node
  - beacon
  - consensus
  - execution
  - mev
  - devops
homepage: https://github.com/chimera-defi/eth2-quickstart
triggers:
  - "set up an ethereum node"
  - "install ethereum validator"
  - "bootstrap beacon node"
  - "run geth and prysm"
  - "install consensus client"
  - "ethereum node setup"
  - "configure mev-boost"
  - "clean ethereum node data"
  - "check ethereum node health"
config:
  FEE_RECIPIENT:
  LOGIN_UNAME:
---

# Eth2 Quickstart

Automates production-ready Ethereum node setup on Linux servers — execution client, consensus client, MEV integration, OS hardening, and optional RPC exposure. Supports 7 execution clients (Geth, Besu, Nethermind, Erigon, Reth, Nimbus-eth1, Ethrex) and 6 consensus clients (Prysm, Lighthouse, Teku, Nimbus, Lodestar, Grandine).

This skill is **repo-aware**: it runs inside an `eth2-quickstart` checkout and routes all actions through `./scripts/eth2qs.sh`. It never invents new lifecycle commands.

## Install

```bash
# Recommended
clawhub install eth2-quickstart

# Or clone directly
git clone --depth 1 https://github.com/chimera-defi/eth2-quickstart.git
cd eth2-quickstart
```

## What agents can do with this skill

- **Bootstrap a fresh host**: detect the next safe install step and execute it
- **Check node health**: machine-readable JSON output from `doctor --json`
- **Operate services**: start, stop, restart, view logs
- **Update clients**: `update-all` covers all installed components
- **Safe cleanup**: `clean-data --dry-run` shows what would be removed before any deletion; secrets and validator keystores are always preserved

## Commands

```bash
# Detect the next safe install step (machine-readable)
./scripts/eth2qs.sh plan --json

# Preview next step without executing
./scripts/eth2qs.sh ensure

# Execute next step (requires explicit confirmation)
./scripts/eth2qs.sh ensure --apply --confirm

# Install Ethereum node (execution + consensus + MEV)
sudo ./scripts/eth2qs.sh phase1
./scripts/eth2qs.sh phase2 --execution=geth --consensus=prysm --mev=mev-boost

# Health check
./scripts/eth2qs.sh doctor --json

# Operate
./scripts/eth2qs.sh start
./scripts/eth2qs.sh stop
./scripts/eth2qs.sh logs --run2 -n 200
./scripts/eth2qs.sh stats

# Cleanup (always dry-run first)
./scripts/eth2qs.sh clean-data --dry-run
./scripts/eth2qs.sh clean-data --confirm
sudo ./scripts/eth2qs.sh cleanup-host --dry-run
```

## Safety guardrails

- `ensure --apply` requires explicit `--confirm` — no silent destructive execution
- `clean-data` preserves `~/secrets`, validator keystores, and wallet directories by design
- `doctor --json` detects service-unit drift (running binary doesn't match unit file)
- Agents must require human confirmation before phase1 (root/reboot), destructive cleanup, or host-wide changes
- Agents must never generate validator keys or remove secrets

## `doctor --json` output shape

```json
{
  "summary": { "passed": 12, "warnings": 2, "failed": 0, "status": "warn" },
  "checks": [
    { "status": "pass", "name": "RAM: 32GB (recommended: 16GB+)", "details": "" },
    { "status": "warn", "name": "Execution client (eth1): Not installed", "details": "" }
  ]
}
```

Use `doctor --json` as the canonical agent-readable health surface. Use `status` / `stats` / `logs` for human-readable RCA.

## Minimum host requirements

| Spec | Minimum | Recommended |
|------|---------|-------------|
| Disk | 2 TB SSD | 4 TB NVMe |
| RAM | 16 GB | 32 GB |
| CPU | 4 cores | 8 cores |
| OS | Ubuntu 20.04+ | Ubuntu 22.04+ |
