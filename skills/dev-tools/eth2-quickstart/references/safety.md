# Safety

## Boundaries

- Require human confirmation before:
  - root-required actions
  - reboot-causing workflow steps
  - destructive cleanup
  - host-wide config changes
- Do not manage validator keys or secrets outside the repo's existing documented flows.
- Always preserve secrets during cleanup. The data purge flow is for default data/state directories, not keys.

## Cleanup

- Prefer `./scripts/eth2qs.sh clean-data --dry-run` first.
- Prefer `sudo ./scripts/eth2qs.sh cleanup-host --dry-run` for stale root-managed installs.
- Only move to `--confirm` after the human confirms scope.
- The purge flow is designed to preserve secrets, validator keystores, wallets, and `~/secrets`.
- Preserve `/root/secrets` and `/root/.eth2/network-keys` during host cleanup.
- Custom datadirs are not covered by the default cleanup command.

## Command Discipline

- Prefer `./scripts/eth2qs.sh` before direct script paths.
- Use `./scripts/eth2qs.sh doctor --json` for agent-readable health checks.
- If a requested action falls outside the repo's supported commands, say so instead of improvising a new lifecycle path.
