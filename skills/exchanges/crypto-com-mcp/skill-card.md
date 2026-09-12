## Description:

Use Crypto.com MCP through UXC for exchange market data workflows with help-first discovery and read-only guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and run read-only Crypto.com exchange market data workflows through UXC and the official MCP endpoint. It supports market discovery, ticker, order book, candlestick, and recent trade reads while excluding trading, account, private data, REST, and WebSocket workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or uses a local UXC command link to Crypto.com's market-data MCP endpoint.

Mitigation: Review the fixed endpoint before use and only create the local command link when that connection is acceptable.

Risk: Using the skill outside its intended scope could imply trading, account, private data, or credential workflows.

Mitigation: Keep usage limited to public, read-only market data operations and avoid trading, balance, private account, or credential-bearing requests.

Risk: Automation can become brittle if it parses human-readable command output.

Mitigation: Use the JSON output envelope and parse stable fields such as ok, kind, protocol, data, and error.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Official Crypto.com MCP docs](https://mcp.crypto.com/docs)
- [Crypto.com market-data MCP endpoint](https://mcp.crypto.com/market-data/mcp)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/crypto-com-mcp-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is scoped to JSON-output, read-only market-data MCP operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
