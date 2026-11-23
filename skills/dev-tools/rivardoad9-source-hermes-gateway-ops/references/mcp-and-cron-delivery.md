# MCP registration + cron delivery (gateway-adjacent, verified 2026-08)

## MCP servers load at gateway start

Adding/removing `mcp_servers` in config.yaml requires the detached gateway restart (see SKILL.md "THE pitfall") — MCP tools are discovered at gateway startup, no hot-reload.

Registration commands (write config.yaml — never hand-edit it):

```bash
hermes mcp add <name> --command <cmd> --args ...     # stdio server
hermes mcp add <name> --url <http-url>               # HTTP/SSE server
hermes mcp configure <name>                          # per-server TOOL SELECTION
hermes mcp test <name>                               # connection + discovery test
hermes mcp list
```

- `hermes mcp configure` is the way to restrict a server's allowed_tools to a subset (the "Toggle tool selection" command).
- Stdio subprocess env is FILTERED — only safe baseline vars + explicit `--env KEY=VALUE` entries are passed to the server. Put API keys there, not in the shell env.
- Tool names are registered as `mcp_<server>_<tool>` (hyphens/dots → underscores).
- If the `mcp` Python package is missing, discovery silently skips: install with `pip install mcp`.
- `hermes mcp add --help` lists all flags.

## Cron delivery semantics (CLI sessions)

- Cron jobs scheduled from a CLI session are LOCAL-ONLY: output saved (viewable via `cronjob action='list'`), NOT delivered live into the terminal. Do not promise the user live results from a CLI-scheduled job.
- To notify, the job's `deliver` must target a gateway-connected platform (`deliver='telegram'` or `'all'`) — set at create/update time (CLI-session jobs default to local).
- `enabled_toolsets` on a cron job restricts which toolsets load (e.g. `["terminal","web"]`) — leaner jobs and fewer stray capabilities; MCP-injected tools live in the platform toolsets.
- Cron prompts must be self-contained (fresh session, no chat context); hard rules belong in the prompt AND enforced by scripts (see the buffer-api skill's gate pattern).
