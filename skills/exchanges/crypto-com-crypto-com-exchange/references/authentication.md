# Authentication

The `cdcx` CLI handles all authentication automatically — signing, nonce generation, and credential persistence.

## Login

```bash
cdcx auth login --oauth
```

Opens a browser for OAuth authentication. Credentials are persisted automatically across sessions.

If authentication fails or credentials are missing, you MUST immediately execute `cdcx auth login --oauth` via Bash tool. The command requires ~120s timeout as it waits for browser callback. Print the callback url to users

## Verify

```bash
cdcx account summary -o json
```

If this returns "No credentials found" or HTTP 401, re-run `cdcx auth login --oauth`.

## Environments

```bash
cdcx --env production account summary    # Production (default)
cdcx --env uat account summary           # UAT sandbox
```

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.crypto.com/exchange/v1/` |
| UAT Sandbox | `https://uat-api.3ona.co/exchange/v1/` |

## Multiple Profiles

```bash
cdcx --profile uat account summary
```

## MCP Server

When running as an MCP server, credentials from `cdcx auth login --oauth` are used automatically:

```json
{
  "mcpServers": {
    "cdcx": {
      "command": "npx",
      "args": ["-y", "@cryptocom/cdcx-cli@latest", "mcp"]
    }
  }
}
```

To enable dangerous-tier operations (cancel-all, withdrawals) via MCP, add `"--allow-dangerous"` to the args array. Only do this if you understand the risks.
