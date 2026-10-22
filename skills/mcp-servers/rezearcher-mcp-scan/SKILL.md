---
name: mcp-scan
description: Use when about to add, install, or trust a third-party MCP server — runs a free pre-flight tool-poisoning / prompt-injection scan on its advertised tools and returns clear/review/block. Triggers: install MCP server, add MCP server, mcp.json, tool poisoning, prompt injection in tool descriptions, vet MCP server, claude mcp add.
---

# mcp-scan — vet an MCP server before you connect an agent to it

Static analysis of a server's advertised tool metadata (descriptions, schemas, hidden unicode). It does not call the server's tools. Free preview returns tools scanned, issue counts by severity, risk score and verdict (clear / review / block).

## Remote server (Streamable HTTP)

```bash
B=https://x402-data-api.sigrunner.workers.dev
curl -s "$B/scan/mcp/preview?url=https://HOST/mcp"
```

## Private, OAuth-gated or stdio server

Paste its `tools/list` result; nothing needs to be reachable from outside:

```bash
curl -s -X POST "$B/scan/mcp/preview" -H 'content-type: application/json' \
  -d '{"tools":[ ...the "tools" array from tools/list... ]}'
```

## Acting on the verdict

- `clear` — proceed.
- `review` — read the flagged tool descriptions before enabling the server.
- `block` — do not connect; tell the user which tool and why.

The full itemized report with evidence and OWASP mapping is the paid route `GET /scan/mcp` ($0.05 USDC via x402 on Base). CLI: `npx github:rezearcher/greyridge-x402-tools mcpscan <url>` (exit code 2 = block). Methodology and measured limits: https://github.com/rezearcher/x402-data-api/blob/main/docs/STATUS.md
