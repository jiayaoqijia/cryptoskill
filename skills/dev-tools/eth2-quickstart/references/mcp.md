# MCP

Use the MCP server when an agent runtime supports native tools and you want Claude Code or Codex to call the repo-backed wrapper directly over stdio.

Agents learn the callable surface from MCP `list_tools`. Use `eth2qs_info` when you want a compact in-band catalog with grouped tool names and example argument payloads.

## Scope

This server is intentionally thin. It wraps `./scripts/eth2qs.sh`; it does not reimplement install or operations logic.

Safe read/plan tools:

- `eth2qs_info`
- `eth2qs_help`
- `eth2qs_doctor_json`
- `eth2qs_plan_json`
- `eth2qs_ensure_preview`
- `eth2qs_client_options`
- `eth2qs_stats`
- `eth2qs_stats_json`
- `eth2qs_update_check_json`
- `eth2qs_debug_json`
- `eth2qs_monitor_export_json`
- `eth2qs_monitor_history_json`
- `eth2qs_repair_preview`
- `eth2qs_logs`
- `eth2qs_clean_data_dry_run`
- `eth2qs_cleanup_host_dry_run`

Explicit apply tools:

- `eth2qs_ensure_apply`
- `eth2qs_phase1`
- `eth2qs_phase2`
- `eth2qs_start`
- `eth2qs_stop`
- `eth2qs_restart`
- `eth2qs_repair_apply`
- `eth2qs_monad_install`

Mutating tools require `confirm=true` and `confirmation_token='apply'`.

## Install

The server requires Python 3 and the official MCP Python SDK:

```bash
python3 -m pip install mcp
```

Run it from an `eth2-quickstart` checkout:

```bash
./mcp_server/run_eth2qs_mcp.sh
```

## Claude Code

Example local stdio server registration:

```bash
claude mcp add eth2-quickstart -- ./mcp_server/run_eth2qs_mcp.sh
# or: ./scripts/install_claude_eth2qs_mcp.sh
```

Then run Claude Code from inside the repo checkout so the server can resolve the canonical wrapper.

For Claude plugin packaging, this repo also exposes:

- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.claude/settings.json`

## Codex

Example local stdio registration:

```bash
codex mcp add eth2-quickstart ./mcp_server/run_eth2qs_mcp.sh
```

If your Codex runtime uses config files instead of the CLI, point the server command at the same wrapper script.

## Notes

- Prefer `eth2qs_doctor_json` and `eth2qs_plan_json` before any apply tool.
- Use `eth2qs_phase1` for root/system hardening and `eth2qs_phase2` for explicit Ethereum client install when you do not want planner-driven routing.
- Use `eth2qs_client_options` before `eth2qs_phase2` if the agent needs valid client names or a tested preset.
- Use `eth2qs_stats_json` when you need machine-readable service states, recent error classifications, and bounded repair suggestions.
- Use `eth2qs_update_check_json` when you need repo drift and installed client freshness in the same payload.
- Use `eth2qs_debug_json` when the operator needs structured per-service unit metadata, recent logs, or listen-socket hints.
- Use `eth2qs_monitor_export_json` for compact bot/dashboard output and `eth2qs_monitor_history_json` for recent snapshot deltas.
- Use `eth2qs_repair_preview` before `eth2qs_repair_apply`; the apply path only executes allowlisted safe restart actions and still requires confirmation.
- The MCP `eth2qs_client_options` payload now mirrors `./scripts/eth2qs.sh client-options --json`, so external wrappers can consume the same repo-native source of truth.
- Use the MCP server for native tool use; use `llms.txt` or the skill files for raw-ingest instruction loading.
- `cleanup_host_dry_run` is intentionally preview-only at the MCP layer.
