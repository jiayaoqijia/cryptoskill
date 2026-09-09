---
name: dashboard
description: "Open the ChainGPT marketplace dashboard — a localhost web UI with six read-only panels (Overview, Wallet, Skills, Activity, Health, About). Bind 127.0.0.1 only, admin-token auth, same-origin CSRF defense. Triggers: dashboard, open the dashboard, ChainGPT dashboard, marketplace dashboard, show me the dashboard, web UI, control panel, skills overview, agent wallet panel, env check, plugin health."
---

# ChainGPT Dashboard

A single localhost web UI that gives a glance-at-it view of the marketplace: which plugin/MCP/marketplace version is installed, what skills are available, recent agent-wallet activity, environment-variable health, and pointers to docs + changelog.

**Read-only.** No signing flows are proxied through the browser. The dashboard intentionally cannot move funds — that stays in MCP tool calls with explicit user confirmation.

## How to open

The fastest path is the slash command:

```
/chaingpt:dashboard
```

That calls the underlying MCP tool, prints a URL and a one-time admin token, and asks if you want to open the URL in your browser.

You can also call the tool directly:

```
> Use chaingpt_dashboard_serve to start the dashboard on port 8788
```

## Panels

| Panel | What it shows | Source |
|---|---|---|
| Overview | Plugin / MCP / marketplace versions; skill count; agent-wallet init state; docs link | `.claude-plugin/*.json`, `mcp-server/package.json`, `~/.chaingpt-mcp/agent-wallet/keystore.json` |
| Wallet | Agent EOA address (copy button); policy summary (kill switch, unrestricted mode, allowed chains, allowed/blocked address counts, max tx value, max gas, memo requirement, policy digest); tracked-token + custom-chain counts; signed-tx count; CTA to launch the full Wallet Admin UI (port 8787) for editing. Read-only — reads the public address from the keystore, never decrypts. | `~/.chaingpt-mcp/agent-wallet/{keystore,policy,tracked-tokens,custom-chains}.json` |
| Skills | One card per skill in `skills/` with name + description from its SKILL.md frontmatter | `skills/*/SKILL.md` |
| Activity | Most recent signed transactions (newest first) | `~/.chaingpt-mcp/agent-wallet/activity.jsonl` (empty if you haven't signed yet) |
| Health | Presence (not value) of CHAINGPT_API_KEY, agent-wallet passphrase, Etherscan/Moralis/GoPlus keys; Node runtime; key paths | `process.env`, filesystem |
| About | Plugin info + top of `CHANGELOG.md` | `.claude-plugin/plugin.json`, `CHANGELOG.md` |

## Security model

- **Bind:** `127.0.0.1` only — never `0.0.0.0`. Cross-host access requires an SSH tunnel.
- **Admin token:** 48 hex chars / 192 bits, written to `~/.chaingpt-mcp/dashboard/.admin-token` with `0600` perms. Rotated on every `chaingpt_dashboard_serve` call.
- **Sessions:** HttpOnly cookie `cg_dash_sid`, 1-hour sliding TTL, in-memory only (no persistence across restarts).
- **CSRF:** All state-changing requests checked against `Origin` (or `Referer`) — must equal `http://127.0.0.1:<port>` / `http://localhost:<port>`.
- **No secrets in the browser.** API keys never leave the Node process; the dashboard reports presence flags only.

## Coexistence with the agent-wallet UI

The dashboard and `chaingpt_agent_wallet_serve_ui` run as separate servers on separate ports (8788 vs. 8787) with independent admin tokens. They share no auth state. Both can run simultaneously.

## Environment variables (optional)

| Var | What |
|---|---|
| `CHAINGPT_DASHBOARD_DIR` | Override the dashboard state dir. Default: `~/.chaingpt-mcp/dashboard/` |

## Troubleshooting

- **Login screen rejects the token:** the token rotates each invocation. Re-run `/chaingpt:dashboard` and use the freshly printed token.
- **Port in use:** pass a different port: `chaingpt_dashboard_serve({ port: 9999 })`.
- **403 Origin check failed:** you're hitting the URL from somewhere other than `127.0.0.1:<port>` / `localhost:<port>`. Open the URL exactly as printed.
