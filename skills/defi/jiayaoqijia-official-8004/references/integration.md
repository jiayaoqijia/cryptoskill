# Integration Patterns

## MCP (Model Context Protocol)

Agents can expose an MCP endpoint for structured tool/resource access:

```json
{
  "services": {
    "mcp": { "url": "https://agent.example.com/mcp" }
  }
}
```

MCP provides:
- **Tools**: Executable functions the agent can perform
- **Prompts**: Pre-built prompt templates
- **Resources**: Data the agent can access

When inspecting an agent with MCP, show the endpoint URL, available tools, and a config snippet for integration.

## A2A (Agent-to-Agent Protocol)

Agents can expose an A2A endpoint for direct agent communication:

```json
{
  "services": {
    "a2a": { "url": "https://agent.example.com/a2a" }
  }
}
```

A2A provides:
- **Agent Card**: Discovery metadata at the A2A URL
- **Skills**: Agent capabilities
- **Context/Task IDs**: Conversation threading

## ENS Integration

Agents can register an ENS name for human-readable discovery:

```json
{
  "services": {
    "ens": { "name": "myagent.eth" }
  }
}
```

The 8004scan backend collects ENS names and ETH balances via a periodic worker (every 6 hours).

## OASF (Open Agent Skill Framework)

Agents declare skills and domains from the OASF taxonomy:

```json
{
  "skills": ["code-review", "testing", "deployment"],
  "domains": ["software-engineering", "devops"]
}
```

Taxonomy source: [agntcy/oasf](https://github.com/agntcy/oasf)

Use `--validate-oasf true` during registration to validate against the official taxonomy.

## x402 Payment Protocol

Agents can declare x402 payment readiness for monetized endpoints:

```json
{
  "x402": true
}
```

Requirements for x402 readiness:
1. `x402: true` in registration file
2. Agent wallet set via `setMetadata("agentWallet", ...)` with EIP-712 signature
3. `active: true` status
4. At least one reachable endpoint

The x402 protocol enables HTTP 402-based payment flows where clients pay per-request for agent services.

## Webhook Integration (8004scan)

8004scan provides webhook subscriptions for real-time event notifications:

- Register webhooks: `POST /api/v1/webhooks`
- Events: agent registration, feedback submission, validation response
- Security: HMAC-SHA256 signatures on payloads
- Retry logic: Exponential backoff on delivery failure

## WalletConnect v2

For write operations (register, feedback, transfer, wallet set/unset), ERC-8004 tools use WalletConnect v2 for signing:

- Agent never holds private keys
- All signing happens in the user's wallet app
- Session file at `~/.8004skill/wc-storage.json` (relay metadata only)
- EIP-712 typed data for wallet management (300s deadline, replay-protected)

## Agent Registration Best Practices

From the official best practices (v2.0):

1. **Clear name + detailed description** — Be specific about capabilities
2. **At least one endpoint** — MCP, A2A, or web URL
3. **OASF skills/domains** — Use standard taxonomy for discoverability
4. **ERC-8004 registration details** — Complete metadata for trust
5. **Domain verification** — Set up `/.well-known/agent-registration.json`
6. **Active monitoring** — Keep endpoints reachable and `active: true`
