# Configure x402

Configure x402 micropayments for agent-to-agent commerce (pay per MCP request in USDC on Base with ~200ms settlement).

→ **[SKILL.md](SKILL.md)** — Full skill specification and workflow.

## Installation

Install into Claude Code or Cursor with:

```bash
npx skills add https://github.com/wpank/Agentic-Uniswap/tree/main/.ai/skills/configure-x402
```

Or via Clawhub:

```bash
npx clawhub@latest install configure-x402
```

## When to use

Use this skill when:

- You want your agent to **pay other agents per MCP request** using x402.
- You want to **accept x402 payments** for services your agent provides.
- You need to understand and configure **x402 limits, pricing, and settlement behavior**.

## Example prompts

- "Configure x402 so my agent pays USDC per MCP request to a specific service on Base."
- "Set up my agent to accept x402 micropayments for portfolio reports."
- "Show me a safe default x402 configuration for development and then one for production."
