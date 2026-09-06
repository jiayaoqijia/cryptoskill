---
name: gate-mcp-openclaw-installer-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "Execution specification for installing Gate MCP servers with OpenClaw/mcporter."
---

# Gate OpenClaw Installer MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Install Gate MCP servers via mcporter (all or selective)
- Guide post-install auth for remote exchange and DEX

Out of scope:
- Executing exchange business actions

## 2. MCP Detection and Fallback

Detection:
1. Verify `mcporter` availability.
2. Validate target mode (all vs selective) and connectivity.

Fallback:
- If automated install fails, provide explicit manual `mcporter add`/auth sequence.

## 3. Authentication

- Installer workflow itself can run without exchange API keys.
- Post-install auth may be required:
  - local `gate` with API keys
  - `gate-cex-ex` OAuth2 via `mcporter auth`
  - `gate-dex` wallet + OAuth flow

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

No Gate MCP business tool call is required.
Installer entrypoint:
- `skills/gate-mcp-openclaw-installer/scripts/install.sh`

Mode options:
- default all install
- `--select` / `-s` selective install

## 6. Execution SOP (Non-Skippable)

1. Confirm install mode (all or selective).
2. Check `mcporter` runtime and prerequisites.
3. Run installer script.
4. Verify installed server list with `mcporter list`.
5. Provide required auth follow-up instructions by server type.

## 7. Output Templates

```markdown
## Installer Result (OpenClaw)
- Mode: {all_or_selective}
- Servers Installed: {list}
- Verification: {mcporter_list_or_status_summary}
- Next Steps: {auth_and_usage_notes}
```

## 8. Safety and Degradation Rules

1. Never claim installed/authenticated state without verification.
2. Keep credentials and tokens out of plain output.
3. On partial failures, report exact failed server(s) and recovery steps.
4. Do not execute non-installer business operations in this skill.
