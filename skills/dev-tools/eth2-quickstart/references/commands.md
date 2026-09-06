# Commands

Canonical command surface:

- Bootstrap repo install: `./scripts/eth2qs.sh bootstrap --non-interactive`
- Configure scripts: `./scripts/eth2qs.sh configure --non-interactive`
- Detect the next safe install step: `./scripts/eth2qs.sh plan --json`
- List supported clients and tested presets: `./scripts/eth2qs.sh client-options --json`
- Preview/apply the next safe step: `./scripts/eth2qs.sh ensure` or `./scripts/eth2qs.sh ensure --apply --confirm`
- Run Phase 1 hardening: `sudo ./scripts/eth2qs.sh phase1`
- Run Phase 2 install: `./scripts/eth2qs.sh phase2 --execution=geth --consensus=prysm --mev=mev-boost`
- Run explicit Monad install: `./scripts/eth2qs.sh monad-install`
- List active validators on the current node: `./scripts/eth2qs.sh validators --json`
- Filter validators by balance / withdrawal type / status: `./scripts/eth2qs.sh validators --json --min-balance 32 --withdrawal-type 0x01 --status active_ongoing` (withdrawal-type: 0x00 BLS / 0x01 execution / 0x02 compounding)
- Read-only validator listing for agents (MCP): tool `eth2qs_validators(min_balance, max_balance, withdrawal_type, status)`
- Deploy validators + generate keys/deposit data (0x01 or 0x02): `./scripts/eth2qs.sh validator-deploy --num-validators 1 --withdrawal-type 0x02 --amount 64 --withdrawal-address 0xYourAddr` (set keystore password via `ETHQS_KEYSTORE_PASSWORD`; `--amount` 32-2048 ETH for 0x02 only; prints the client import command and the deposit command, no auto-submit)
- Focused exit checklist / client-specific voluntary exit flow: `./scripts/eth2qs.sh validator-exit`
- Preview, generate, or submit BLS-to-execution changes for 0x00 validators: `./scripts/eth2qs.sh validator-withdrawal-changes --dry-run --generate --submit --yes`
- Focused 0x02 compounding validator creation flow: `./scripts/eth2qs.sh validator-create-0x02`
- Combined validator menu (exit / consolidate / EIP-7002 exit / withdrawal-credential change): `./scripts/eth2qs.sh validator-manage [--exit|--consolidate|--eip7002-exit|--withdraw-change]`
- Agent preview of a funds-affecting validator op (MCP, returns the CLI command, never executes): tool `eth2qs_validator_op_preview(operation)` where operation is exit|withdrawal-change|consolidate|eip7002-exit|create-0x02|deploy
- Health/status: `./scripts/eth2qs.sh doctor --json`
- Monitoring/triage: `./scripts/eth2qs.sh stats --json`
- Structured service debug: `./scripts/eth2qs.sh debug --json --service cl`
- Update freshness / repo drift: `./scripts/eth2qs.sh update-check --json`
- Compact monitor summary: `./scripts/eth2qs.sh monitor export --json`
- Save a monitor snapshot: `./scripts/eth2qs.sh monitor snapshot --json`
- Review recent monitor history: `./scripts/eth2qs.sh monitor history --json --limit 5`
- Smart repair preview/apply: `./scripts/eth2qs.sh repair` or `./scripts/eth2qs.sh repair --apply --confirm`
- Human-readable status: `./scripts/eth2qs.sh status`
- Start services: `./scripts/eth2qs.sh start`
- Stop services: `./scripts/eth2qs.sh stop`
- Restart services: `./scripts/eth2qs.sh restart` or `./scripts/eth2qs.sh restart --smart`
- Service/system stats: `./scripts/eth2qs.sh stats`
- View logs: `./scripts/eth2qs.sh logs --run2 -n 200`
- Clean default data dirs only: `./scripts/eth2qs.sh clean-data --dry-run`
- Confirm cleanup after review: `./scripts/eth2qs.sh clean-data --confirm`
- Host cleanup for stale root-managed installs: `sudo ./scripts/eth2qs.sh cleanup-host --dry-run`
- Confirm host cleanup after review: `sudo ./scripts/eth2qs.sh cleanup-host --confirm`
- Update installed components: `./scripts/eth2qs.sh update-all`

Prefer these commands over direct utility-script paths unless a task specifically needs the lower-level script.

## cli-anything-eth2-quickstart (Python Harness)

An alternative agent-native entrypoint for runtimes that prefer a structured Python CLI over raw shell. Install from `eth2-quickstart/agent-harness/`:

```bash
pip install -e eth2-quickstart/agent-harness/
```

Key commands (always pass `--json` for agent parsing):

```bash
# Machine-readable health
cli-anything-eth2-quickstart --json health-check

# Phase 2 install with explicit client choices
cli-anything-eth2-quickstart --json install-clients \
  --network mainnet \
  --execution-client geth \
  --consensus-client lighthouse \
  --mev mev-boost \
  --confirm

# Guided node setup (auto-detects phase)
cli-anything-eth2-quickstart --json setup-node \
  --phase auto \
  --execution-client geth \
  --consensus-client prysm \
  --mev commit-boost \
  --confirm

# Validator metadata (no key import)
cli-anything-eth2-quickstart --json configure-validator \
  --consensus-client prysm \
  --fee-recipient 0x1111111111111111111111111111111111111111 \
  --graffiti "my-node"

# RPC exposure
cli-anything-eth2-quickstart --json start-rpc \
  --web-stack nginx \
  --server-name rpc.example.org \
  --confirm
```

Discovers repo root from `--repo-root` flag → `ETH2QS_REPO_ROOT` env var → current directory. Prefer the `./scripts/eth2qs.sh` surface for direct shell use; use the Python harness when your agent runtime needs structured argument parsing or a REPL-style interface.
